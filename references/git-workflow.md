# 本地 Git 存档规范

为求职简历项目建立本地 Git 版本管理（不上传任何远端），用于防止误删、回溯历史版本。

## 初始化

```bash
cd <项目目录>
git init
git config user.name "<姓名>"
git config user.email "<本地占位邮箱>"   # 纯本地存档可用占位，如 name@local
git config core.quotepath false          # 中文路径正常显示
```

- 身份用**仓库级 local 配置**，不污染全局。
- 若项目已在父目录某个 Git 仓库内，先 `git rev-parse --show-toplevel` 检查，避免嵌套仓库。

## .gitignore（排除清单）

| 排除项 | 理由 |
|---|---|
| `.DS_Store` | macOS 系统缓存 |
| `.workbuddy/` | 本地工作记忆，含薪资/离职原因等**私密信息** |
| `html/历史简历/` | 「保存历史」运行时快照，含 base64 字体 + 缩略图缓存，每次导出产生大量无意义 diff |
| `文件/*.png` | 简历截图预览产物，可由 HTML 重新生成 |

## 纳入清单

- 简历 HTML 源文件（`.html`，含嵌入字体）
- 投递 PDF（`.pdf`，作为核心交付物纳入，防丢失、可回溯）
- JD 分析与打招呼话术（`.md`）
- `.gitignore` 本身

## 提交

```bash
git add -A
git status --short          # 核对纳入/忽略是否与预期一致
git status --ignored --short # 验证被忽略文件
git commit -m "存档说明"
```

- commit message 用中文，写清楚本次改动（如「<岗位名>简历 v1/v2 初始存档」「新增 <公司> 岗位定制简历」）。
- 提交后确认 `git remote -v` 为空（纯本地，无远端）。

## 后续维护

- 每次生成新岗位简历 / 修改简历后，提示用户可 `git add -A && git commit` 存档。
- 新岗位的 HTML/PDF 若放进纳入目录（如 `文件/`），会自动进入版本管理；历史快照目录（`html/历史简历/`）保持被忽略。
