---
name: 简历定制-skill（中国内资企业）
description: 中国大陆内资企业求职简历定制工作流。当用户提供内资企业岗位 JD 和个人工作经历文档或最新简历，或需要分析岗位与个人经验的匹配度，或为不同岗位 JD 定制求职简历时使用。覆盖 JD 解码与匹配度评估、中文简历深度定制（A4 两页，可编辑 HTML + PDF）、打招呼话术生成，并沉淀了一套经实战验证的硬性写作规范（重复度/总分分/句式多样化/bullet 行数/数据溯源闸门）、问题处理流程（先测试确认→找根因→给方案→等确认再改）、经历档案动态更新机制（同步即记录、累积只增不改、定制时全量选材）、版块排版规范、Noto Sans SC 双字重字体嵌入（ATS 异体字根治）、导出 PDF 六项样式（照片去编辑元素/姓名居中/底部填充/标题线细淡/浮层全隐/未传照片隐藏照片位）、历史永不丢失三层保障、跨文件 IndexedDB 草稿污染防护等工程能力。触发词：岗位 JD、改简历、定制简历、匹配度、打招呼话术、投这个岗位、内资企业、新工作经历、同步经历。
agent_created: true
---

# 中国内资企业简历定制工作流

针对一个中国大陆内资企业岗位（JD），基于候选人已有简历和经历档案，完成 JD 解码、匹配度分析、中文简历深度定制、打招呼话术生成，最终输出可直接投递的 A4 两页 PDF 简历 + 可编辑 HTML 源文件。

> **首次使用**：直接把「岗位 JD（截图或文本）」+「你的简历或工作经历文档」发给 AI 即可，本工作流会按下面 6 个步骤自动跑完。首次定制前建议先按 `references/experience-archive.md` 建一份自己的经历档案，后续每个岗位都从它选材，越用越准。
>
> **文中的「规范」条款**：均为经实战验证的默认约定，目的是让产出稳定达标。你可以在自己的副本里按需调整，但改之前建议先跑几个岗位感受一下差异。

## 问题处理流程（所有问题必须遵守）

**任何问题出现时，必须按此流程执行，禁止跳过确认直接改：**

1. **先测试确认问题存在**：用 CDP/实测复现，不凭印象、不臆断。
2. **找根因（第一性原理）**：定位到具体代码/机制层，说明为什么会出现。
3. **给解决方案**：含取舍说明（改什么、影响什么）。
4. **等用户确认后再修改**：未经用户确认不得动代码。

已踩坑案例（后续如再遇同类问题直接按根因定位）：
- JD 侧栏错位 = cp 模板时漏改 JS 里的 `JD` 数组 + `data-jd` 标注
- bullet 超行 = 违反总分分结构，把项目级细节下沉到工作经历
- 成果段不可编辑 = `<p>` 成果段漏 `contenteditable`（不在 `<ul>` 内）
- 打开 A 文件显示 B 文件内容 = 同一端口所有 HTML 共享 IndexedDB，草稿跨文件污染
- 历史备份「导入后恢复不了编辑内容」= importHistory 严格相等匹配（短名当新增）+ 种子占位时间戳误用 now（刷新后编辑版被当旧数据删）→ 修复见踩坑清单第 9 条
- JD 侧栏取消过滤后其余条目仍变灰 = `toggleJdFilter` 取消分支只清了被点那条的 `.filtered`，未清整列（本模板已修复；若你的 HTML 是早期副本，按此改法清理整列即可）

## 适用场景

- 用户提供内资企业岗位 JD（截图/文本/链接）+ 个人工作经历文档或最新简历
- 用户想评估「该岗位是否值得投」、计算与个人经验的匹配度
- 用户想为不同岗位 JD 分别定制一份贴合的中文简历
- 用户需要一段用于 Boss 直聘 / 脉脉 / 内推的打招呼话术

## 不适用场景

- 国央企 / 事业单位需要政治面貌、籍贯、照片等特殊字段的简历（需额外定制，本流程未覆盖）
- 用户没有任何简历或经历素材（本工作流依赖真实经历，绝不杜撰）
- 英文简历 / 外企双语简历（本流程为中文简历；英文版需另行翻译）

## 输入要求

必须获取以下三类素材中的前两类：

1. **JD**：截图或文本；需确认公司名、岗位名、工作地点、薪资范围、岗位职责、任职要求。
   - 注意：Boss 直聘分享链接（`m.zhipin.com/.../weijd-job/<jobId>?sid=...`）是 Vue SPA + API 异步加载 + 风控（code 37），**无法脚本/无头抓取**。若用户只给链接，第一步就直接请用户提供 JD 截图或复制文本，不要浪费时间抓取。
2. **简历**：PDF 最佳（保留原格式逻辑），也可接受 Word / 文本 / Markdown。
3. **经历档案**（强烈推荐）：Markdown 文件，含完整工作经历、项目、数据、荣誉，用于补全简历遗漏细节。**经历档案是简历定制的唯一权威数据源（持续累积制）**——用户每次同步的新工作经历/内容都要追加记录，禁止丢弃历史内容；每次定制简历必须从「完整档案」全量选材（见「经历档案动态更新机制」）。

### 经历档案动态更新机制

**规则：用户每次同步新工作经历/内容 → 立即记录并累积到经历档案 → 后续每次新岗位 JD 从「完整档案」按匹配度选材制作简历。** 归档来源包括两类：① 用户主动同步的新经历；② **JD 定制过程中向用户发起的提问（如匹配度 <50% 的深挖问答）→ 用户回答的真实经历/动作/数据 → 一并归档**。

1. **同步即记录（两类来源）**：
   - **主动同步**：用户发来任何新工作经历/项目/数据/荣誉/技能（聊天、文档、Markdown 均可），当场追加到经历档案，并标注来源与日期；**只增不改**——历史经历内容保留不动，新内容追加在对应板块。
   - **JD 深挖问答归档**：每次定制简历时，凡因 JD 匹配需要向用户发起的提问（尤其是匹配度 <50% 的 5 轮问答式深挖，也含任何补充问答），**用户回答的内容当场结构化归档**（按「岗位 / 问题 / 用户回答要点 / 可引用数据 / 日期」记录），并同步进经历档案对应板块——这些答案可能是后续岗位的稀缺素材，不能随单次任务丢失。
2. **全量选材**：每次定制简历（新岗位 JD）时，从**完整经历档案**（含历史全部经历 + 最近新增 + 历史问答归档）中，按 JD 匹配度挑选最匹配的案例与数据，而非只取最近一段经历。匹配度算法照常：0.6 经历重合 + 0.2 关键能力 + 0.2 行业业务匹配。
3. **累积的价值**：经历与问答归档越多、覆盖能力越广，后续岗位的选材池越大；同一能力可能有多个候选案例时，优先选数据强、与 JD 关键词口径一致的案例。
4. **数据溯源闸门同样适用**：新增经历/问答归档中的数字进入档案时即建立「数据 → 出处」映射；简历引用时仍须可溯源，不因"档案里写过"而免除核对。
5. **维护动作**：经历档案建议常驻项目目录（如 `经历档案-<你的名字>.md`），问答归档单独一节或并入对应岗位板块；档案空模板见 `references/experience-archive.md`；新增内容写入后同步 Git 存档。

## 执行流程

### Step 1 · 读取与解析素材

1. 用 Read 读 Markdown 经历档案全文。
2. 用 `scripts/pdf_extract.py` 提取 PDF 简历文本。
3. JD 为图片则直接看图；为文本则读取。

### Step 2 · JD 解码与匹配度评估

1. **5 层解码**：招聘经理真实需求 / Must Have / Nice to Have / Hidden Signals（团队阶段、P 级、风格）/ Level 判断。
2. **匹配度打分**：0.6 经历重合 + 0.2 关键能力 + 0.2 行业业务匹配。
3. **Gap 三档**：强 / 中 / 弱，标出缺失能力。
4. **Tailor 策略**：简历强化什么、弱化什么、关键词如何对齐 JD。

**关键决策：匹配度 < 50% 时，先对缺失的关键能力做 5 轮问答式深挖**（挖真实经历、动作、数据），再动笔；深挖不到则只呈现已有匹配案例，不强求、不杜撰。

### Step 3 · 定制简历内容（按硬性写作规范）

先按 JD 关键能力拆解，再从经历中挑选最匹配的经验与数据对应展示。写作规范见下方「硬性写作规范」，必须逐条遵守。

### Step 4 · 生成可编辑 HTML 简历

创建单文件 HTML，内联 CSS，A4 打印优化（可参考 `assets/resume-template-cn.html`，该模板已内置 JD 标注侧栏 + 历史留档 + 全部工程修复）。功能与排版要求见下方「HTML 简历工程规范」与「版块内排版规范」。

### Step 5 · 转 PDF 并验证

1. 用 `scripts/html_to_pdf.py` 转 A4 PDF。**该脚本必须走 CDP（Page.printToPDF）而非 CLI `--print-to-pdf`**（已踩坑，原因见下）：
   - CLI `--print-to-pdf` + `@page { margin: X }`（X≠0）→ **字体回退**（data-URI Noto 失效，回退 Times-Roman/STSongti，产生异体字、ATS 全挂）；
   - CLI `--print-to-pdf` + `@page { margin: 0 }` + `#resume { padding }` → 分页后 **padding 不跨页重复**，页 2 文字贴顶；
   - **已验证解法**：HTML 里 `@page { size: A4; margin: 13mm 12mm; }`（2026-09 由 16mm 12.5mm 收窄定稿）+ `#resume { padding: 0 !important; width: auto }`，用 CDP printToPDF（`preferCSSPageSize: true`）→ 每页都有边距且内嵌字体正常。
2. 验证：页数 ≤ 2 且无溢出（pdfplumber 检查 words 坐标 x1/bottom 不超页面边界）；**每页上/下/左/右边距 ≈ 16/16/12.5/12.5mm**（重点看第 2 页顶部，防止 padding 丢失导致的贴顶）；`pdfplumber` 提取中文零异体字、字体出现 `NotoSansSC-Regular` + `NotoSansSC-Bold` 两个字重且**无 Times-Roman/STSongti 回退**。
3. 字体嵌入流程见「中文 PDF 异体字根治」。

### Step 6 · 生成打招呼话术

结构（尽量 250 字以内）：

```
[开头：具备x年xxx经验，擅长xxx，主导过N个匹配案例，总体取得xxx数据成果]
[3-4 个匹配关键能力分点，每点=能力名+数据案例，1 句以内]
[结尾：对该岗位的价值展望]
```

数据必须与简历一致。

## 硬性写作规范（必须遵守）

### 整体逻辑
- 制作前先按 JD 关键能力拆解，结合个人经历整理匹配经验与数据成果，再展示到简历对应能力中。
- 关键能力描述口径与 JD 一致。
- **重复度硬性规则（违反会被打回）**：
  - 同一能力关键词、同一案例内容、同一数据结果，在全简历出现次数均 **≤ 2 次**。
  - 若出现 2 次，**分布只能是「自我评价」1 次 + 「项目经历」或「工作经历」1 次**；禁止「自评 + 工作 + 项目」三处同现同一内容/数据。
  - 起草完成后必须自查：列一份「案例/数据 → 出现位置」检查表，逐项核对 ≤2 次且分布合规。
- **总分分结构**：自我评价 = 对工作经历 + 项目经历的**总结汇总**（概括性、带核心亮点数据）；工作经历 = 相对项目经历**更概括**（方法/能力 + 结果，不展开项目级细节）；项目经历 = **具体展开**（背景/动作/复杂度/创新解法/数据，允许比工作经历细 2-3 倍）。禁止三者写同样详细的内容。

### bullet 撰写底层逻辑（全简历通用）

- **行数限制**：每个 bullet = 能力关键词标题 + **1-2 行**具体描述；超 2 行即精简（冗余信息点下沉到项目经历或删除，不得挤压行数上限）。
  - **超行根因（已踩坑）**：信息密度压过行数约束——违反「总分分结构」把项目级细节（功能列举/部门罗列）下沉到工作经历 bullet，或项目经历塞满冗余列举。
  - **精简方法**：按总分分结构归位——工作经历删项目级细节（只留「能力 + 问题 + 方法 + 数据」三要素），项目经历删冗余列举（功能名清单/渠道罗列），保留「复杂度/协作/创新 + 数据」。**精简 ≠ 删数据，是把细节放回正确层级**。
  - **行数验证法（CDP 硬性验证，Range 行框法）**：对每个 `<li>` 用 `range.selectNodeContents(li)` 后取 `getClientRects()` 过滤 `height>5` 的行框、按 `Math.round(top/4)` 去重计数——旧的 `height ÷ lineHeight` 法会把 padding/取整误差算进去（2 行实测报 2.2 造成大批误判超行），已弃用。全部 ≤2 才通过（实测案例：19 个 bullet 从 12 个超标精简到 19/19 达标）。
- **底层逻辑（固定）**：每个 bullet 必须含三要素——「解决什么问题 → 用什么方法/技能 → 达成什么数据成果/价值/影响」，缺任一要素即补。
- **编写形式（灵活）**：三要素的呈现方式可灵活，开头在「问题现象 / 动作前置 / 场景切入 / 数据切入 / 目标切入」等类型间交替；结构逻辑统一 ≠ 句式统一。
- **句式多样化硬性规则**：全简历所有 bullet 正文开头句式必须多样化，禁止 ≥2 个 bullet 使用相同开头模板。**起草后必须逐条列出每个 bullet 的开头短语并核对，确认无 ≥2 个同构**——这是硬性自查环节，不可省略。已踩坑雷区（必须规避）：「为此…」衔接（曾同现 3 次）、「搭建…」动词前置（曾同现 2 次）、「为解决/为了…」等固定模板。
- **协同类 bullet 证明方向**：涉及「多角色协同 / 跨部门协同」的 bullet，证明方向 = **为了达成统一利益、协同不同部门共同解决问题**（正向框架，非"利益冲突"负面框架），必须点明四要素——① 统一目标/利益是什么；② 具体解决什么问题；③ 什么方式协同了哪些部门（列出部门）；④ 带来什么数据成果/价值/影响。禁止只写「利益冲突 + 一个结果」的单薄表述。

### 自我评价
- 第一句一句话总结（x 年经验 + 擅长能力/技能 + 主导过 N 个匹配案例 + 总体数据成果），**不要加「综合概述」等前缀标签**。
- 后接 3-4 个能力分点，每点是**汇总整份简历匹配该能力的案例与亮点数据**（不是单独展开一个案例），带具体数据 + 案例证明。
- 禁忌：不写爱好/生活/性格等无法用数据证明的内容。

### 工作经历
- 每家公司 = 公司背景 + 2-3 个匹配 JD 的关键能力。
- 每个能力：能力关键词为标题 + 1-2 行具体描述（为了什么 → 用什么方法/工具/技能 → 做了什么动作 → 拿到什么数据结果/价值/影响）。
- 因果顺序要正确：监测指标 → 搭建数据/定位问题 → 分析根因 → 提策略方案 → 拿成效。
- 句式多样化、行数限制、底层逻辑（问题→方法→成果）见上方「bullet 撰写底层逻辑」通用小节，全简历统一遵守。
- 禁忌：禁用「负责」「配合」等宽泛词，用执行类动词（主导/设计/搭建/推动/落地/验证/复制等）。
- 工作经历的描述要比项目经历更概括，不重复项目经历的细节；与能力词匹配度不高的经验内容要换别的案例。

### 项目经历
- 只选最匹配 JD 的 2 个项目，按时间**新→旧**排序，用 STAR 法则：
  - 背景：一句话。
  - 项目职责与策略：分点，每点对应 JD 关键能力，1-2 行，含方法/技能/渠道 + 解决的问题难点 + 数据成果。
  - 成果：一句话/一行总结项目成果与影响。
- **项目经历必须比工作经历更细化（细节 ≈ 工作 2-3 倍），并强制融合展示以下三维**（缺一则被打回）：
  1. **项目复杂度高**：每条 bullet 至少点出一种——① 业务逻辑复杂（业务链条长 / 协作角色多 / 规则互斥）；② 协作复杂度（多部门利益或需求不一致，需拉齐各方诉求）；③ 无明确规则、需做重要业务决策（没有现成机制可循，要自己定义标准/模型/权重）。
  2. **创新思路解法**：方法更巧妙 / 更高效 / 更低成本 / 效果更好（如 0-1 设计、以量换价、RFM/CVP 建模、A/B 验证替代拍脑袋）。
  3. **有结果的动作与经验**：一句话提动作 + 结合具体案例 + 带数据成果，**不长篇大论**。
  - 写法示范（含协作复杂 + 复杂度 + 无规则决策 + 创新）：「市场调研与机会识别：在短短一周时间内组织客服、市场、产品等多方部门开展 200+ 品类市场价格调研，并独立结合 RFM 用户分层识别"价格不透明"核心痛点，从 0 到 1 创新设计交易一口价业务方案和产品原型。」
- **不同项目之间的 bullet 关键词不重复**（如两个项目都用「创新解法」要改掉）。
- **起草后自查（项目维度）**：逐条标注该 bullet 体现了「复杂度/协作/无规则决策/创新」中哪几项 + 数据来源，缺维度则补。

### 个人技能
- 每个 bullet 后的技能点用「｜」分隔。
- 出现「项目管理能力」时，PMP 放该 bullet 首个技能点；否则放「行业认证」首个技能点。
- JD 提到 AI 经验时，可单独列「AI能力」项（AI 知识 + 工具 + 成果）。

### 格式细节
- 最多 A4 两页；不写性别、居住地；bullet 标题用「能力关键词：」而非「【能力关键词】」。
- 数字统一：表达增长用文字（「增长/提升/降低」），仅范围用「+」，避免「+900w+」双加号。
- 数据必须真实、不编造；缺行业经验时强调方法论可迁移。

## HTML 简历工程规范（硬性要求）

每次输出的简历 HTML 必须包含：

- **顶部工具栏**：「✏️ 修改和编辑」（默认所有正文 `contenteditable="true"`，按钮仅切换 .editing 视觉样式）、「👁 预览」（模态框克隆当前 DOM 展示导出前 A4 排版）、「⬇️ 导出Word」（Blob application/msword 生成 .doc，base64 图片自动嵌入）、「⬇️ 导出PDF」（window.print()）、「📷 上传照片」（FileReader 读 base64 显示到 img；右侧 26×34mm 照片位 dashed 边框）、「🏷 标注JD关键能力」（data-jd + 侧栏过滤高亮）、「💾 保存历史」「📤 导出历史」「📥 导入历史」。
- **选中文本悬浮格式工具栏**：B / I / U / S + 增大/缩小字号 + 清除格式（用 `document.execCommand` 与自定义字号包裹）。
- **header 居中布局**：`header { position: relative; display: block; text-align: center; min-height: 36mm; display: flex; flex-direction: column; justify-content: center; }`——姓名块整块居中，照片位 `.photo-slot { position: absolute; top: 1mm; right: 0; }`（绝对定位右上，不挤压姓名）；`min-height: 36mm` 容纳 34mm 高的照片防止溢出覆盖正文。
- 所有正文元素默认 `contenteditable="true"`，移除 `contenteditable="false"`；标注不影响编辑，jd-match 仅视觉高亮。
- 打印白底：`@media print` 强制 `html, body { background:#ffffff !important; }`，`.jd-match` 清样式（background/box-shadow/outline/::before 全 transparent/none）。
- **打印边距（硬性，防页2贴顶/字体回退）**：`@media print` 中 `@page { size: A4; margin: 13mm 12mm; }`；`#resume { width: auto; padding: 0 !important; }`（**必须 `!important`**，否则会被 `@media (max-width:860px)` 里 `#resume { padding: 16mm 12.5mm }` 覆盖造成双重边距——注意这两处数值故意不同：媒体查询的 padding 是屏幕态预览用，print 态必须清零并由 @page margin 统一接管）。配合 Step 5 的 CDP 脚本（preferCSSPageSize:true）实现每页边距 + 字体正常。
- 导出 Word：Blob + application/msword + 完整 style 注入 + base64 图片嵌入；**文件名与 `<title>` 由 `getCurrentJobTitle()` 动态生成，不要写死**。
- 上传照片：先压缩（300×400 / JPEG 0.85）再检查 base64 大小 ≤ 2MB，**不要在压缩前拦截原图大小**；照片位下方加一行深灰提示小字（仅网页显示，预览/导出时移除）。**照片渲染用 FileReader.readAsDataURL（data: URL），禁用 URL.createObjectURL（file:// 下 blob: 挂起，onload/onerror 不触发）**；`#resume` 内容被 innerHTML 替换后照片事件用 `document.addEventListener('change')` 事件委托 + 局部 getElementById 重新绑定。

### 工程踩坑清单（已踩坑，必须规避）

1. **cp 模板必改项清单（JD 侧栏错位雷区）**：从通用版/旧简历复制生成新岗位 HTML 时，除 `#resume` 内容、`<title>`、Word 导出名、initData 外，**必须同步改 JS 里的 `JD` 数组（右侧侧栏能力列表）+ 全部 `data-jd` 标注**（1-N 全覆盖且与 JD 数组编号一一对应），否则侧栏显示旧岗位能力、点过滤高亮错位。JD 侧栏能力分类须与目标岗位 JD 职责/要求对齐（示例：某 PMO 岗拆出 7 条能力——项目集管理 / 重点事项推进与闭环 / 流程标准化与规范化 / 经营分析与数据驱动 / 风险管控与预警 / 跨部门协同与资源协调 / 多线程与书面表达）。
2. **项目"成果"段可编辑性**：项目"成果"是独立 `<p>` 段（不在 `<ul>` 内），手写 HTML 时最易漏 `contenteditable`（已踩坑：两份简历各 2 处成果段无法编辑）。**根治：JS 兜底 `ensureEditable()`**——初始化时遍历 `#resume` 下 `p, span, div, h1, h2, h3` 等正文元素，缺失 `contenteditable` 自动补 `true`（排除 photo-slot/toolbar/history/preview）。
3. **跨文件 IndexedDB 草稿污染防护**：WorkBuddy 静态服务所有 HTML 共享同一 origin 的 IndexedDB，**A 文件的自动草稿会覆盖 B 文件打开时的内容**（已踩坑：先编辑 A 岗位，再打开 B 岗位文件，B 的内容被 A 的草稿覆盖）。**修复：draft 写入带 `sourceFile: location.pathname`，恢复时双保险校验**——① 有 sourceFile 且 ≠ 当前 pathname → 跳过；② 旧草稿无 sourceFile → 用 `.target-role` 岗位名兜底匹配，不匹配也跳过。
4. **历史永不丢失三层保障**：① 基础历史作为 HTML 内嵌种子（`__history_init_data__`），每次初始化逐个检查 IndexedDB，缺失即自动补全，已存在的用户编辑版**绝不覆盖**；② 工具栏「📤 导出历史 / 📥 导入历史」一键全量备份/恢复（JSON 含照片 base64）；③ 修改代码绝不重建/覆盖 IndexedDB 已保存数据。
   - **种子内嵌 = 跨环境可见的唯一方案**：IndexedDB 按 origin 隔离，**预览面板（http://127.0.0.1:<port>）与外部浏览器（file://）的 IndexedDB 天然不互通，JS 无法自动同步**。唯一能让"预览面板和 file:// 都看到历史"的做法是**把历史种子内嵌进 HTML 文件本身**（种子随文件走，任何环境打开都由 `initHistoryImport` 自动导入）。
   - **生成新简历 HTML 时必须做的事**：把当前**全部岗位**历史的最新内容（从各 HTML 提取 `#resume` 完整块，div 计数法）组装为 `__history_init_data__` 注入**每一份** HTML（含工作台 + 各独立岗位文件），而不是留空 `[]`。否则新文件首次打开历史面板为空（已踩坑：两份独立文件 initData=[] 导致历史面板空）。**注意 `assets/resume-template-cn.html` 是起点模板，其种子本就应为 `[]`**——那是给「从零新建」用的，不是已交付简历。
   - **用户新编辑内容的跨环境搬运**：agent 无法读取用户浏览器 IndexedDB 里的最新编辑；若需把"用户最新编辑版"刷进种子，先请用户「📤 导出历史」给 JSON，再据此更新种子（或用户用「📥 导入历史」在另一环境恢复）。
   - **历史条目 DOM**：列表容器渲染的条目 class 为 `.history-item`，岗位名在 `.history-jobtitle`（CDP 验证时用 `.history-item` 而非 `#history-list li`）。
5. **JD 侧栏必须随「当前简历岗位」切换（跨岗位历史错配根治）**：`var JD` 是每份 HTML 写死的**单岗位**数组，但历史面板可存放**多个岗位**的快照。已踩坑：`loadHistoryItem` / `restoreDraft` 替换简历正文后只调 `renderJdList()` 重渲染、**从不更新 `JD` 数组** → 出现「正文是 A 岗位、侧栏 JD 却是 B 岗位」。
   - **根治方案**：① 新增 `JD_LIBRARY`（各岗位的 JD 能力数组，key 自定义）；② 新增 `matchJdKey(jobTitle)` 关键词模糊匹配 + `syncJdForJob(jobTitle)`（切换 `JD = lib.list.slice()` 并更新侧栏标题）；③ 侧栏 `<h4>` 加 `id="jd-panel-title"` 动态显示岗位名；④ 三处调用 `syncJdForJob`：`loadHistoryItem`（`entry.jobTitle`）/ `restoreDraft`（`draft.jobTitle`）/ 初始化（`getCurrentJobTitle()`）。
   - **快照 data-jd 编号必须与 JD_LIBRARY 对应数组的顺序一致**（已踩坑：某快照用了编号 1-7，但该 HTML 的 JD 数组只有 6 条 → 编号 7 长期悬空；后续补齐第 7 条才闭环）。
   - **CDP 验证此功能的坑：必须按岗位名实时匹配索引**。`loadHistoryItem` 会先 `saveHistorySnapshot('auto-before-load')`，把当前内容存为快照并 `unshift` 到列表最前 → **每次加载后历史列表重排**，用固定索引 `.h-load[i]` 会点错条目，表现为「滞后一拍」的**假 bug**。正确做法：每次点击前重新读 `.history-jobtitle` 列表，用 `indexOf(目标岗位名)` 取当前索引再点。
   - **评测新做法**：审查某岗位时，除核对 HTML 自身 JD 数组与正文口径，还要核对**历史快照各自 data-jd 编号体系**（不同岗位的 1-N 含义不同，不能互相套用）。
6. **JD 逐条覆盖度必须程序化统计**：人工通读容易漏掉「某条 JD 职责零覆盖」。**做法（CDP）**：遍历 `.jd-match` 收集 `data-jd`，按编号统计每条能力命中数，输出 1-N 覆盖表——命中数为 0 的即缺口。实测案例：靠此法发现某 JD 职责③（会议决策行动项管理与闭环）零覆盖，其余 6 条均 4-8 处。
   - **补缺口时的重复度陷阱**：为对齐 JD 加内容前，**先统计目标关键词在全文的既有次数**。已踩坑：想补"经营分析"，却发现自评①与自评③各已用 1 次（满额 2 次），直接加会违反「同一能力关键词 ≤2 次」。**解法**：改用 JD 的**近义表述**（如"经营决策"）替代，既对齐 JD 又不撞红线。同理，新增 bullet 用掉某个词后，要回头把其他 bullet 里的同义词删掉。
   - **补强素材的正确来源**：优先找「**档案有、简历却没用**」的真实数据（实测案例：档案里记着"人效 3.6 倍 + 持续更新机制"、"立项方案/执行计划表/跨部门沟通机制"，打招呼话术用了 3.6 倍、简历正文反而漏了）。
   - **JD 有要求但档案无证据时**：**绝不编造**。用真实素材做口径升级，并在交付说明里标注哪些是档案原文、哪些是合理归纳，交由用户核对（实测案例：档案无"经营分析会"证据，故只写"支撑管理层经营决策"，不写"参与经营分析会议"）。
   - **数据撞车检查**：补数据前先确认该数字是否已被别处以**不同含义**使用（实测案例：档案里的"覆盖 80% 核心品类"指 SOP 覆盖，某个项目 bullet 里的"80% 核心品类"指交易模式规模化——同词不同义，故自评只用"人效 3.6 倍"、避开"80% 核心品类"）。
7. **`window.print()` 必须在用户点击的同步栈内调用（导出 PDF 被 Chrome 拦截的根因）**：已踩坑——`exportPdf` 写成 `async`，先 `await saveHistorySnapshot('pdf')`（写 IndexedDB）再 `window.print()`，print() 落到 Promise 微任务栈而**失去 user gesture**，Chrome 判定为 print 滥用，弹「…重复出现问题」要求 reload，用户无法导出 PDF。
   - **修复模板（所有导出 PDF 的 HTML 统一照改）**：
     ```js
     function exportPdf() {          // 必须去掉 async
       if (document.body.classList.contains('jd-on')) setJdOn(false);
       autoAdjustMargins();
       window.print();               // 同步调用，保留 user gesture
       Promise.resolve(saveHistorySnapshot('pdf')).catch(function (e) { console.error(e); }); // fire-and-forget
     }
     ```
   - **规律**：任何"用户手势触发浏览器原生对话框/弹窗"的 API（`window.print()`、`showOpenFilePicker()`、`requestFullscreen()` 等）都**不能**放在 `await` 之后；要先把该 API 同步调用，其余副作用（写 IndexedDB、埋点等）一律改 fire-and-forget。导出 Word 不受影响（只 `download()` 不调原生对话框）。
   - **CDP 验证方法（两个坑）**：① 用 `Input.dispatchMouseEvent` 真实点击**会被浮层遮挡**（曾命中历史面板遮罩导致 print 未被调用）→ 改用 `Runtime.evaluate` 带 **`userGesture: true`** 派发 `.click()`，既激活用户手势又不受遮挡干扰；② **决定性判据**是调用栈而非 `userActivation.isActive`——stub 里记录 `new Error().stack`，必须含 `HTMLButtonElement.exportPdf` / `dispatchEvent` 帧才算同步栈（修复前是 Promise 微任务栈，无此帧）。另注意 shell→node 传参时 `'\n'` 会被转义成字面两字符，别用它 split 调用栈。
8. **岗位名归一化：同一岗位不能因名字长短不同留下两条历史记录**：`getCurrentJobTitle()` 的正则在「·」处截断（`/(?:求职意向|intention)[:：\s]*([^\s｜|·]+)/i`），自动保存产生**短名**（如「产品运营」），而内嵌种子/手动导入用**全名**（如「产品运营 · 经理（PMO 方向）」）→ `saveHistorySnapshot` 的严格相等去重失效 → 历史面板出现两条同一岗位。
   - **修复三件套**：① `isSameJob(a,b)`（相等或互为前缀即同岗位）；② `normalizeJobTitle()`（匹配到已有同岗位时统一用**更长的名字**，并把旧快照迁移到最终名下、删除旧条目），`saveHistorySnapshot` 里改用 `await normalizeJobTitle(getCurrentJobTitle())`；③ `dedupeHistoryEntries()`（启动时合并历史遗留重复条目，保留名字更长的、快照取更新的）。
   - **⚠️ 最大坑（第一版修复完全无效）**：`initHistoryImport()` **从不加载 IndexedDB 已有数据**——`histEntries` 只在**打开历史面板时**才由 `toggleHistoryPanel(true)` 里的 `loadHistoryIndex()` 填充。去重函数跑在**空数组**上等于没做。**必须在初始化最前面 `await loadHistoryIndex()`**，顺序为：`loadHistoryIndex` → `initHistoryImport` → `dedupeHistoryEntries` → `restoreDraft`。否则「打开页面后没点过历史面板就直接导出 PDF」照样产生重复（归一化同样依赖 `histEntries`）。
   - **教训（通用）**：给历史/存储类功能加新逻辑前，**先确认数据在内存的加载时机**，别默认"启动时已就绪"。
   - **连带修复**：`restoreDraft` 的旧草稿兜底匹配原用严格相等，而 `curName`（取自 `.target-role`，全名）与 `draft.jobTitle`（短名）永远不等 → **旧草稿恢复功能实际从未生效**；改 `!isSameJob(draft.jobTitle, curName)` 模糊匹配。
   - **CDP 验证要多场景才算过**：① 遗留清理（人为往 IndexedDB 注入短名条目 → 重载后应被合并）；② 不漏合并（导出 PDF / 改短名保存均不新增）；③ **不误合并**（改成完全不同的岗位名应正确新增为独立条目）；④ 不开历史面板直接导出 PDF（验证初始化顺序修复有效）。
9. **历史备份「导入后恢复不了编辑内容」= 导入严格相等匹配 + 种子占位时间戳用 now**：
   - **现象**：把修复前导出的备份 JSON（含自动保存的**短名**编辑条目 + 种子**全名**条目）导入修复后的 HTML，编辑版内容找不回，历史面板只剩模板种子版。
   - **根因（两层叠加，缺一不可）**：
     ① `importHistory` 循环用**严格相等 `jobTitle ===`** 在 `histEntries` 找已有条目 → 备份里的短名编辑条目匹配不到种子全名条目 → 被当「新增」插入（toast 显示「新增 2」），同岗位两条并存；
     ② 种子条目 `savedAtTs = 页面打开时刻(now)` 永远比用户真实编辑时间「新」→ 刷新触发 `dedupeHistoryEntries` 时保留「名字更长」的全名种子条目、短名编辑条目作 drop，且因 `dropTs < keepTs` 不迁移快照 → **直接 `del` 短名快照，编辑内容被物理删除**，只剩模板。
   - **修复三件套（3 份同结构 HTML 统一照改）**：
     ① `importHistory` 循环匹配改「相等或互为前缀」模糊归并（复用 `isSameJob` 语义）：命中后统一写入「名字更长」的条目与快照键、删除旧短键，导入当下即合并恢复、不再产生重复（toast 变「新增 0、更新 2、跳过 2」）；
     ② 新增 `var SEED_BASE_TS = new Date('2020-01-01T00:00:00+08:00').getTime()`，`initHistoryImport` 补种子时 `savedAtTs = SEED_BASE_TS + i`（**不再用 `now`**）；
     ③ 新增 `fixSeedTimestamps()`：启动顺序 `loadHistoryIndex` 之后、`initHistoryImport` 之前调用，把存量 `reason === '初始导入'` 且 `savedAtTs > SEED_BASE_TS` 的条目一次性降级回基准——**否则修复后重新导入仍会被旧版生成的「now 种子」时间戳挡住（永远 skip，无法覆盖）**。
   - **验证（CDP，真实触发导入按钮）**：导入 toast 应为「新增 0、更新 2、跳过 2」；面板条目数不增（无短名重复）；加载全名条目后正文含「编辑版独有片段」断言编辑版已恢复（从备份 JSON 的编辑版/种子版两个快照做文本 diff 提炼特征词）；刷新后再查 IndexedDB，快照键统一为全名、短键已删。
   - **通用规律 ①（最重要）**：「占位/兜底内容」绝不能用「页面打开时刻」当时间戳——种子、模板兜底条目一律用远古固定基准时间（如 2020-01-01），保证任何真实保存/导入（时间戳为真实时刻）都能按「更新的赢」覆盖它。凡是「内嵌种子 + 时间戳 PK」的历史设计都适用（含 dedupe 的快照取舍、导入的 skip/update 判定）。
   - **通用规律 ②**：导入/合并/去重/恢复类函数必须共用同一套 `isSameJob`（相等或互为前缀）语义；任何一处用严格相等匹配岗位名都是漏网——同一岗位名在系统内天然存在截断短名与全名两种形态（`getCurrentJobTitle()` 在「·」处截断所致）。新增任何按岗位名匹配的逻辑时，全局搜索所有 `jobTitle` 匹配入口逐一核对。

### 导出 PDF 六项样式要求

1. **照片导出无编辑元素**：`@media print` 里 `#photo-label { border: none !important; }`、`#photo-remove { display: none !important; }`（照片虚线边框 + ✕ 删除键仅编辑态显示）；Word 导出（getResumeHtml）同步移除。
2. **抬头姓名居中**：header 整块居中 + 照片绝对定位右上（见上「header 居中布局」）。
3. **页面底部填充**：@page margin 收窄（16mm 12.5mm → 13mm 12mm）、section/company-block margin 减小、允许内容跨页填满（li 不加 page-break-inside:avoid），避免每页底部空大段（CDP 实测：第 2 页 900+ 字连续填充）。
4. **标题分割线细淡**：`h2 { border-bottom: 1pt solid #b0b4bc; }`（原 1.5pt #333 太粗太深，0.5pt 又太淡；1pt 淡灰为定稿）。
5. **浮层元素必须全部隐藏（防 PDF 水印）**：`@media print` 中除工具栏/侧栏外，**必须显式隐藏所有 `position:fixed/absolute` 浮层**——`#toast`（showToast 提示浮窗）、`#fmt-pop`（选中文本悬浮格式工具栏）、`#history-panel`（历史面板）、`#preview-modal`（预览模态框）。**已踩坑**：`#toast` 用 `position:fixed; z-index:9999` 且未在 print 隐藏 → 导出 PDF 里出现"已恢复上次编辑内容""已自动恢复 N 份基础历史"等水印文字。验证方法：CDP `Emulation.setEmulatedMedia({media:'print'})` 后 `getComputedStyle` 检查这些元素为 `display:none`，且生成 PDF 后 pdfplumber 扫描不含提示类词汇（已恢复 / ✓ / 暂无历史 / 保存历史 等）。
6. **未上传照片时必须隐藏整个照片位（修复时波及 7 份历史 PDF）**：`@media print` 里**只隐藏 `.photo-tip`（说明小字）是不够的**——照片位本体是 `<label id="photo-label">`，内含 `<span class="photo-hint">📷 上传照片</span>` 与 `<button id="photo-remove">✕</button>`。导出 PDF 走 `window.print()`、**不经过 `getResumeHtml()` 的 clone 清理**，完全依赖 @media print CSS，因此必须在 print 块内补：
   ```css
   #photo-label:not(.has-photo) { display: none !important; }
   .photo-hint { display: none !important; }
   ```
   已踩坑：`#photo-remove` 隐藏了、`.photo-tip` 隐藏了，但 `<span class="photo-hint">📷 上传照片</span>` 漏了 → 每份未传照片的 PDF 右侧都打出「📷 上传照片」占位文字。**验证方法**：pdfplumber 全文扫描必须不含 `上传照片` 与 `📷`；对历史已交付 HTML 做全量扫描（`grep -c photo-hint`）确认无遗漏。修复后需**重导所有受影响 PDF**，不能只改 HTML。

## 版块内排版规范（HTML 结构，硬性偏好）

- **版块内行距**：紧凑不散。body line-height 1.5；li margin-bottom 2px、显式 line-height:1.5。
- **header 与照片位**：header 整块居中（姓名+联系方式），`.photo-slot` 绝对定位右上（top:1mm right:0），照片位 26×34mm、dashed 边框仅编辑态显示；`header min-height:36mm` 容纳照片防溢出（详见「HTML 简历工程规范」）。
- **标题分隔线**：所有 section `h2` 用 `border-bottom: 1pt solid #b0b4bc`（淡灰细线，定稿粗细）。
- **工作经历头部三段式**：
  - `.company-block` 容器，margin-bottom 16px 隔开不同公司。
  - 公司名 h3 单独一行居左。
  - `.role-line`（flex justify-between）= 岗位名(左) + 任职日期(右)，颜色 #555 深灰、字号同正文 9.5pt。
  - 公司背景 `.company-bg` 斜体（仅工作经历块斜体，8.5pt）。
  - bullet 关键词 `.duty-title` 加粗（仅 font-weight:700，字号同正文 9.5pt），关键词后正文不加粗。
- **项目经历头部 flex 自适应居中**：
  - `.project-head` flex：项目名 `flex:0 0 auto; white-space:nowrap`（左、不换行）；项目负责人 `flex:1 1 auto; text-align:center`（居中于「项目名右缘到日期左缘」区域，随项目名长度自适应）；项目日期 `flex:0 0 auto` 右对齐；三者 gap:10px，负责人不贴日期。
  - 角色用「项目负责人」（非「项目主理人」）；字号同正文、颜色深灰 #555。
  - 项目背景字号同正文 9.5pt（非斜体），「背景：」用 `<strong>` 加粗、其余不加粗。
- **教育背景**：`.edu-line`（flex justify-between），学历信息居左、时间 `.edu-date` 居右深灰 #555。
- **颜色口径**：「深灰」= #555（区别于正文近黑 #1a1a1a / muted #333）。

## 验证方法（CDP 实测要点）

- **bullet 行数验证**：渲染后对每个 `<li>` 用 Range 行框法实测行数（见「bullet 撰写底层逻辑」行数验证法），全部 ≤2 才通过。
- **contenteditable 可编辑性测试（要点）**：
  - headless 默认视口 800×600，目标元素在视口外时鼠标事件会落空——**先 `element.scrollIntoView({block:'center'})` 再取坐标**。
  - **判定标准用 `window.getSelection()` 的落点（startContainer 是否在目标元素内），不要用 `document.activeElement`**——headless 的焦点行为与真实浏览器有差异（实测：activeElement 显示项目标题但 selection 落点已在成果段内 = 可编辑）。
  - 顺带确认 `.jd-match` 等标注样式无 `pointer-events: none` / `user-select: none` 干扰编辑。
- **打印样式验证**：CDP `Emulation.setEmulatedMedia({media:'print'})` 后 `getComputedStyle` 检查关键项（照片边框 0、✕ display:none、**未传照片时 `#photo-label` 与 `.photo-hint` 必须 display:none**、标题线 1pt 淡灰、header textAlign center、photo-slot position absolute），再 `Page.printToPDF` 生成真实 PDF 用 pdfplumber 验证页数/字体/边距，并**扫描全文不含 `上传照片` / `📷`**（未传照片场景）。
- **模拟真实「📥 导入历史」按钮（文件选择注入法）**：headless Chrome 里直接 `input[type=file].click()` 会挂起等文件对话框。正确做法：`Page.enable` 后 `Page.setInterceptFileChooserDialog {enabled:true}` → `Runtime.evaluate` 带 `userGesture:true` 点 `btn-import` → 监听 `Page.fileChooserOpened` 事件取 `params.backendNodeId` → `DOM.setFileInputFiles {files:[备份JSON绝对路径], backendNodeId}` 完成注入 → 真实走一遍 `importHistory` 的 onchange 分支（可校验 toast / 面板条目 / IndexedDB 快照键）。验证「导入恢复」类功能必须用它，别用直接调函数（闭包内函数外部不可达）或手工改 IndexedDB（绕过了合并逻辑本身）。

## 中文 PDF 异体字根治（macOS headless Chrome 必做）

**现象**：macOS 用 headless Chrome 打印中文 PDF 时，系统字体（PingFang/Songti/STHeiti/Hiragino）被嵌入为 Type3/错误 ToUnicode，导致 ATS 文本提取出现康熙部首异体字（长→⻓、自→⾃、用→⽤、手→⼿…），关键词匹配全部失效。

**根治（已验证）**：在简历 HTML 内嵌 **Noto Sans SC 双字重**（Regular 400 + Bold 700）中文 webfont，Chrome 打印嵌入正确 Type0 字体、ToUnicode 正常，且保证正文(400)与一级标题/bullet 关键词(700)有清晰粗细对比。

1. 下载两个 woff2（@fontsource 的 chinese-simplified 子集，约 1.1MB 每个）：
   - `curl -sL -o noto400.woff2 "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc/files/noto-sans-sc-chinese-simplified-400-normal.woff2"`
   - `curl -sL -o noto700.woff2 "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-sc/files/noto-sans-sc-chinese-simplified-700-normal.woff2"`
2. **务必用 fonttools 把 family 名改为标准 "Noto Sans SC"**（@fontsource 该包默认 family 名为 "Noto Sans SC Thin"；不改正则 PDF 字体名带 Thin 字样；更关键：**若只嵌单字重，全文被渲染成同一字重，正文与关键词/bullet 标题失去粗细区分——已踩坑**）。把 nameID 1/4/6/16/17 分别改为 "Noto Sans SC" / "Noto Sans SC Regular|Bold" / "NotoSansSC-Regular|Bold"（含 nameID 17 的 style 名）。可直接执行：
   - `python3 -c "from fontTools.ttLib import TTFont; f=TTFont('noto400.woff2'); [setattr(r,'string','Noto Sans SC' if r.nameID in(1,16) else ('Noto Sans SC Regular' if r.nameID==4 else ('NotoSansSC-Regular' if r.nameID==6 else ('Regular' if r.nameID==17 else r.toUnicode())))) for r in f['name'].names if r.nameID in(1,4,6,16,17)]; f.save('noto400c.woff2')"`（700 同理改 Regular→Bold / -Regular→-Bold / 'Regular'→'Bold'）
3. base64 注入 HTML 的**两个** `@font-face`（`font-weight:400` 用 Regular、`font-weight:700` 用 Bold），`body` 字体栈首位为 `"Noto Sans SC"`。
4. 重新打印验证：`pdfplumber` 提取中文零异体字，字体列表出现 `NotoSansSC-Regular` + `NotoSansSC-Bold`（两个）。
- 内嵌双字重后 HTML ~3.1MB，但 Chrome 打印只嵌入用到的字形，PDF 仍 ~150KB。
- 若无网络：PDF 视觉无误但 ATS 有异体字风险，此时 .doc 才是 ATS 干净版本，交付说明中提示优先投 .doc。
- **正文禁用 U+2192「→」箭头（新踩坑）**：Noto Sans SC chinese-simplified 子集不含箭头 → 打印时回退 `PingFangSC-Regular`（带子集前缀嵌入，虽不产生异体字但不纯净，pdfplumber 能检出）。写法规避：流程箭头改顿号/括号叙述（如「声音收集、问题分析、整改闭环」），「A→B」改「由 A 缩短至 B」。验证：打印后 pdfplumber 字体列表应只剩 `NotoSansSC-Regular/Bold`（允许 AppleColorEmoji 仅当确有 emoji）。

## 历史版本留档与 Git 存档

- **历史页面功能**：简历 HTML 内实现「历史页面」侧边栏，导出 PDF/Word/手动保存时自动留档，同岗位覆盖最新内容，最多保留 30 份。存储为**纯 IndexedDB（零权限依赖）**——历史快照不写本地磁盘目录（弃用 File System Access API，因其权限失效/手势依赖/路径隔离导致「打开/加载」按钮无响应）。实现细节见 `references/history-feature.md`。
- **历史永不丢失三层保障**：① HTML 内嵌种子自动补全（`__history_init_data__`，初始化逐个检查缺失即恢复、已存在不覆盖）；②「📤 导出历史 / 📥 导入历史」一键全量备份/恢复（JSON 含照片 base64，时间戳新的赢）；③ 修改代码绝不覆盖 IndexedDB 已保存数据。详见「HTML 简历工程规范 → 工程踩坑清单」第 4 条。
- **本地 Git 存档**：简历项目目录建议纳入 Git 版本管理。`.gitignore` 需排除：`.DS_Store`、`.workbuddy/`（本地工作记忆，可能含薪资/离职原因等隐私）、`html/历史简历/`（旧版磁盘快照目录，已废弃但保留排除规则）、`*.png`（截图产物）。纳入：简历 HTML 源文件、投递 PDF、分析 MD。详见 `references/git-workflow.md`。

## 输出文件

| 文件 | 说明 |
|---|---|
| `求职简历工作台-通用版-<姓名>.html` | **主编辑器**：1 份 HTML 管理多岗位，内嵌各岗位初始历史，首次打开自动导入，历史面板「加载」切换岗位编辑。新岗位定制后在此「保存历史」留档 |
| `<公司>-<岗位>-<姓名>-简历.html` | 单岗位独立 HTML（通用版落地后退役，保留作历史快照） |
| `<公司>-<岗位>-<姓名>-简历.pdf` | 可直接投递的 A4 两页 PDF |
| `<公司>-<岗位>-分析与打招呼话术.md` | JD 解码、匹配度、Gap、Tailor 策略、打招呼话术 |

## 诚信约束

- 所有经历、职位、公司、数字必须来自用户提供的真实材料。
- 可重组表达、突出相关经验、翻译语言，但绝不杜撰。
- 不确定的数据标 `[待确认]`，不猜测数字。
- 匹配度是优化方向，不是保证数字；向用户说明真实上限取决于经历重合度。

### 数据溯源闸门（起草前强制，违反 = 打回）

1. **起草正文前，必须先从经历档案建立「数据 → 来源行号/原文」映射表**，逐条列出本简历要用到的每一个数字及其出处；禁止凭印象填充「看起来合理」的数字。
2. **常见错配雷区（已踩坑，必须规避）**：
   - **把 A 项目的数据套到 B 项目**：同一个数字在档案里属于某个具体项目，却被写到另一个项目下（实测案例：把「客诉率降低」的指标错配到交易模式项目，该数据实际来自「预约功能优化项目」）。
   - **编造档案里没有的数字**：凭印象写「抢单率提升 X%」「人效 N 倍」「处理周期从 12 天压到 5 天」这类**看似合理、档案里却查无出处**的数字，是最常见且最致命的一类错误。
   - **把平台/公司级整体结果错写成某个具体项目的成果**：平台级 GMV 增幅、整体转化率提升属于公司/平台层面，不能挂到单个项目名下。
3. **每条数据在简历里出现时，必须能在映射表里找到对应出处**；自查时逐项核对，发现无来源的数字立即删除或替换。
4. **交付前自查动作**：把简历里每个数字与映射表逐条对照，输出「数据 → 出处」对照清单供用户复核，**数字无出处的一律删除或替换，不保留、不稀释表述蒙混**。

## 资源

- `scripts/pdf_extract.py`：PDF 文本提取（处理嵌入字体编码问题）
- `scripts/html_to_pdf.py`：HTML 简历转 A4 PDF（基于 headless Chrome + CDP）
- `assets/resume-template-cn.html`：中文 A4 简历 HTML 模板（内置 JD 标注侧栏、历史留档、全部工程修复；正文为占位符，种子为 `[]`，可直接作为新岗位起点）
- `references/experience-archive.md`：通用经历档案模板（章节结构 + 填写说明 + 数据溯源表）
- `references/history-feature.md`：历史页面（纯 IndexedDB 存储，零权限依赖）实现细节
- `references/git-workflow.md`：本地 Git 存档规范
