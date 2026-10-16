#!/usr/bin/env python3
"""
Convert an HTML resume to A4 PDF using headless Chrome via CDP (Page.printToPDF).

Why CDP instead of `--print-to-pdf` CLI:
1. `--print-to-pdf` + `@page { margin: X }` (X != 0) triggers font fallback in
   headless Chrome (data-URI @font-face lost -> Times-Roman/STSongti, kills ATS).
2. `@page { margin: 0 }` + `#resume { padding }` loses the padding on page 2+
   (padding is not repeated across fragmentation), so page 2 text touches the
   top edge.
Solution (verified): keep `@page { size: A4; margin: 13mm 12mm; }` in the HTML
and drive Page.printToPDF via CDP with preferCSSPageSize=true. CDP's print path
keeps embedded fonts AND applies the @page margin on EVERY page.

Requires: pip install websocket-client  (into the same venv as this script)
"""
import base64
import json
import os
import platform
import subprocess
import sys
import time
import urllib.request

import websocket


def find_chrome() -> str:
    system = platform.system()
    candidates = []
    if system == "Darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        ]
    elif system == "Linux":
        candidates = ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]
    elif system == "Windows":
        for p in [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]:
            candidates.append(p)

    for c in candidates:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("Google Chrome not found. Please install Chrome or pass the binary path.")


def html_to_pdf(html_path: str, pdf_path: str, chrome_path: str = None, port: int = 0) -> None:
    chrome = chrome_path or find_chrome()
    if not port:
        # pick a random free-ish port
        import socket
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]

    html_abs = os.path.abspath(html_path)
    pdf_abs = os.path.abspath(pdf_path)

    proc = subprocess.Popen(
        [
            chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
            f"--remote-debugging-port={port}",
            "--remote-allow-origins=*",
            "--user-data-dir=/tmp/chrome_cdp_" + str(os.getpid()),
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # wait for CDP endpoint
        ws_url = None
        for _ in range(50):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2) as r:
                    for t in json.loads(r.read().decode()):
                        if t.get("type") == "page":
                            ws_url = t["webSocketDebuggerUrl"]
                            break
                if ws_url:
                    break
            except Exception:
                time.sleep(0.2)
        if not ws_url:
            raise RuntimeError("CDP endpoint not available")

        ws = websocket.create_connection(ws_url, timeout=60)
        msg_id = 0

        def send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == msg_id:
                    return r

        send("Page.enable")
        send("Runtime.enable")
        send("Page.navigate", {"url": "file://" + html_abs})
        # wait for document readyState == complete
        for _ in range(100):
            r = send("Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True})
            if r.get("result", {}).get("result", {}).get("value") == "complete":
                break
            time.sleep(0.2)
        time.sleep(3)  # extra settle for embedded fonts (data-URI webfont)

        result = send("Page.printToPDF", {
            "printBackground": True,
            "paperWidth": 8.27,
            "paperHeight": 11.69,
            "marginTop": 0.63,
            "marginBottom": 0.63,
            "marginLeft": 0.49,
            "marginRight": 0.49,
            "preferCSSPageSize": True,   # CSS @page size + margins win (13mm/12mm per page)
            "printHeaderFooter": False,
            "displayHeaderFooter": False,
        })
        data = result.get("result", {}).get("data")
        if not data:
            raise RuntimeError("printToPDF failed: " + json.dumps(result, ensure_ascii=False)[:300])
        with open(pdf_abs, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"PDF saved to: {pdf_abs}")
        ws.close()
    finally:
        proc.kill()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 html_to_pdf.py <input.html> <output.pdf> [chrome_path]")
        sys.exit(1)
    html_to_pdf(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
