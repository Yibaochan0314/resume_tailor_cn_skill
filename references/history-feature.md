# 历史页面功能实现细节

在简历 HTML 内实现「历史页面」侧边栏，用于自动留档不同岗位版本的简历，支持查看与回填编辑。

## 功能需求

- 左侧固定「📋 历史页面」竖排按钮，点击展开抽屉侧边栏
- 每次「导出 PDF / 导出 Word / 手动保存」时自动留档
- 同岗位名称的简历共用一个历史条目，内容以最新保存/导出为准（覆盖旧内容）
- 最多保留 30 条，超出删除最旧
- 列表项显示：缩略图 + 岗位名 + 保存日期时间 + 月份
- hover 缩略图显示首行预览文字浮窗
- 每项 3 个按钮：**「打开」**（新标签页打开自包含快照 HTML，当前编辑区 100% 不动）、**「加载」**（先自动保存当前编辑区为新历史，再载入选中项到主编辑器）、**「删除」**
- 历史按钮/侧边栏不出现在「预览」和「导出 PDF/Word」中

## 存储方案（纯 IndexedDB，零权限依赖）

历史快照**不写本地磁盘目录**（弃用 File System Access API）。根因：Chrome 重启后目录授权失效、`requestPermission`/`showDirectoryPicker` 必须由用户手势同步触发（async await 链中手势已失效导致弹窗不出现、Promise 挂起）、`file://` 下 IndexedDB 按文件路径隔离导致文件改名/移动后授权句柄读不到——三者叠加造成「打开/加载」按钮点击后**完全无响应**。改为直接存浏览器 IndexedDB（`indexedDB.open('resume_history',1)` → objectStore 'kv'）：

| key | 内容 | 大小 |
|---|---|---|
| `historyIndex` | 索引数组 `[{jobTitle,savedAt,savedAtTs,thumbnail,preview,reason}]` | 每条约 10-30KB（含缩略图 jpeg） |
| `snapshot:<岗位名>` | 该岗位最新 `#resume` 的 outerHTML（纯内容，不含字体） | 每条约 5-10KB |
| `snapshotTemplate` | 共享快照骨架（完整 `<style>` 含内嵌 Noto 双字重 base64 + 3 个占位符） | 约 3MB，**只存一份** |

关键设计：约 3MB 的字体 base64 只存一次（`snapshotTemplate`），每条历史只存几 KB 的轻量内容，30 条历史总占用约 3.5MB，IndexedDB 轻松容纳；「打开」时用模板 + 内容拼出完整快照 HTML。全程 async IndexedDB 读写，毫秒级响应，无需任何目录授权/弹窗/手势。

### 保存快照

1. 提取岗位名（优先读「求职意向」行，兜底读工具栏副标题）
2. 生成缩略图（见下）、首行预览文本
3. `buildSnapshotContent()`：clone `#resume` 的 outerHTML（去 photo-tip）
4. 首次保存时 `buildSnapshotTemplate()` 生成共享模板并写入（占位符 `__SNAPSHOT_TITLE__` / `__SNAPSHOT_TIME__` / `__SNAPSHOT_CONTENT__`）
5. `histIDB.set('snapshot:<岗位名>', 内容)`；更新 `historyIndex`（同岗位覆盖：filter 掉同名再 unshift）；超 30 条删最旧（连带删 `snapshot:<岗位名>`）

### 加载快照（「加载」按钮）

1. `histIDB.get('snapshot:<岗位名>')` 直接读内容（毫秒级）
2. `DOMParser` 解析 outerHTML，取 `#resume` 的 innerHTML
3. 先 `saveHistorySnapshot('auto-before-load')` 保存当前编辑区（**不丢失当前内容**）
4. 将快照 innerHTML 写回主编辑器 `#resume`，刷新 JD 标注
5. 成功后 `showToast('✓ 已载入编辑区：<岗位名>')`（底部黑色 toast，2.6s 自动消失，比 alert 醒目）
6. 内容缺失（旧版本数据未迁移到 IndexedDB）→ alert 提示「重新保存历史生成一份」

### 打开快照（「打开」按钮，新标签页，不动当前编辑区）

1. `histIDB.get('snapshot:<岗位名>')` + `histIDB.get('snapshotTemplate')`
2. 用 `split/join` 把 3 个占位符替换为 `escapeHtml()` 后的岗位名/时间/内容（`split/join` 保证全局替换，`replace` 字符串模式只替换首个）
3. `new Blob([html])` → `URL.createObjectURL` → `window.open(url,'_blank')` 打开自包含快照（含全部 `<style>` + 内容，可查看/打印/继续编辑）
4. 若 `window.open` 返回 null（浏览器拦截弹窗）→ alert 提示允许本站弹窗
5. 成功后 `showToast('✓ 已在新标签页打开：<岗位名>')`；`setTimeout` 120s 后 `revokeObjectURL` 释放 blob
6. **用途**：日常「查看/对照」历史版本时用「打开」（当前编辑区零风险）；要把某历史版本「拿回来继续改」时用「加载」（自动先存当前，也不丢）

### 数据迁移说明

- 旧版（File System Access）历史存在用户手动选择的磁盘目录里，无法自动迁移（权限正是旧 bug 根源）
- 升级后首次使用：旧历史不显示，点一次「保存历史」即可重建当前版本快照；此后所有历史走 IndexedDB 新存储
- 清浏览器站点数据会同时清掉 IndexedDB 历史（与旧版磁盘目录互不影响的取舍）；如需长期留存，仍用「导出 PDF/Word」落盘

## 方案 A：1 份通用 HTML 管理多岗位

**背景**：用户工作流是「一份简历编辑器里管理多份不同岗位的简历（A/B/C），点「加载」在当前页面切换编辑，自动先存前一份，同岗位覆盖最新，互不影响」。IndexedDB 在 `file://` 下按文件路径隔离，导致每份独立 HTML 各自一套历史——这不是 bug，是浏览器机制。与其「3 份 HTML 跨共享」，不如**合并为 1 份通用 HTML**（单文件 = 单存储分区，隔离问题自然消失）。

**实现要点**：

1. **生成**：以最新版独立 HTML（含全部历史功能 + 新版 @page margin）为模板，title/tb-sub 通用化；resume 默认放其中一份岗位内容。
2. **初始历史数据内嵌**：`<script id="__history_init_data__" type="application/json">` 存 `[{jobTitle, content}]`，content 是各岗位 `#resume` 的 outerHTML（去 photo-tip，几 KB/份，字体 3MB 不重复存——仍走 `snapshotTemplate` 共享模板）。
3. **首次打开自动导入**：`initHistoryImport()` 在 IIFE 初始化时调用，把内嵌数据写入 IndexedDB（`snapshot:<jobTitle>` + `historyIndex`），`historyInitialized` 标记保证幂等（删光历史也不会重新导入）。
4. **jobTitle 对齐（关键坑）**：初始历史的 jobTitle 必须 = `getCurrentJobTitle()` 从简历正文提取的求职意向文本（如「<岗位名>（<公司>）」）。若用「<公司><岗位名>」这类自定义名，auto-before-load 时 filter 按正文提取的 jobTitle 匹配不上 → 同岗位覆盖失效 → 历史重复（曾实测历史数从 3 变 4）。
5. **getCurrentJobTitle 选择器修复（关键坑）**：求职意向元素实际 class 是 `target-role`，原选择器 `.intention-line, [class*="intention"]` 匹配不到 → 退回 `.tb-sub` 兜底。若 tb-sub 已不是岗位名（是工作台名），兜底会提取出无意义岗位名 → 每次自动保存都产生垃圾历史。修复：选择器改为 `.intention-line, .target-role, [class*="intention"]`。
6. **加载后动态更新 tb-sub**：`loadHistoryItem` 成功后 `tb-sub.textContent = entry.jobTitle`，编辑器标题跟随当前岗位。
7. **导出 PDF/Word 不受影响**：文件名/标题从 resume 内求职意向提取，与 tb-sub 无关。

**验证**（无头 Chrome CDP 冒烟测试，可复用 `scripts/html_to_pdf.py` 的 CDP 通道）：初始导入 N 份 → 面板 N 条 → 依次加载各岗位往返切换 → 每次切换 auto-before-load 保存前一份 → 历史数始终 N（同岗位覆盖生效）→ 加载 B 时 C 的历史时间戳不变（互不影响）。测试脚本注意：面板每次打开会重新渲染列表，第二次操作必须重新 `querySelectorAll` 取按钮（旧引用失效）。

### showToast（全局轻提示）

- 底部居中黑色圆角 toast，`position:fixed; bottom:40px`，`opacity` 过渡，2.6s 自动隐藏，`pointer-events:none` 不挡点击
- 用于「已载入编辑区 / 已在新标签页打开」等操作反馈，替代容易忽略的 `alert`（alert 不聚焦时用户看不到）

### 缩略图生成（SVG foreignObject → canvas，失败回退占位符）

```
clone #resume（去 contenteditable）→ 收集 document.styleSheets 全部 cssText →
拼 SVG: <svg><foreignObject><div style="width:源宽;height:源高;transform:scale(thumbW/源宽)">
<style>全部样式</style> + clone.outerHTML</div></foreignObject></svg>
→ new Image() + data:image/svg+xml;charset=utf-8,encodeURIComponent(svg)
→ drawImage 到 canvas（200px 宽，按 A4 比例限高 400）→ toDataURL('image/jpeg',0.55)
```

注意：base64 字体 + foreignObject 可能导致 canvas 污染（tainted），`toDataURL` 抛错时回退空字符串 → 列表显示 📄 占位符。

### 触发点与隐藏

- `exportPdf` / `exportWord` 调用前 `await saveHistorySnapshot(reason)`（**但 `window.print()` 必须留在同步栈内，详见 SKILL.md 踩坑清单第 7 条**）
- 新增「💾 保存历史」按钮手动保存
- 隐藏：`@media print` 加 `#history-btn,#history-panel,#history-backdrop,#history-tooltip{display:none!important}`；`openPreview()` 与 `getResumeHtml()` 的 clone 中移除这些元素
