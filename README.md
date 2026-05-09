# Lite Literature Organizer

[简体中文](#简体中文) | [English](#english)

## 简体中文

`Lite Literature Organizer` 是一个轻量化的本地文献整理程序。它提供一个简单的网页界面，帮助你把新放入收件箱的 PDF 识别、预览、确认后再归档，同时兼容你在文件管理器里的手动整理。欢迎继续改进、扩展，或者按自己的研究工作流重构它。

### 它能做什么

- 扫描收件箱中的 PDF
- 基于本地规则提取标题、第一作者、年份和摘要片段
- 给出目标分类和建议文件名
- 在应用前允许人工确认和手动调整
- 记录历史操作与手动目录变化
- 通过 `.organize_category` marker 兼容目录重命名和层级调整
- 支持英语与简体中文界面

### 主要特点

- 本地优先：默认不依赖联网
- 轻量：后端只依赖 `pypdf`，其余使用 Python 标准库
- 双语：界面支持 English / 简体中文
- 可扩展：已经为更高级识别预留接口

### 快速开始

1. 安装 Python 3。
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 双击根目录下的 `organize.bat`。
4. 浏览器会自动打开本地网页应用。

默认示例工作区位于 `example_workspace/`。首次启动时，程序会根据浏览器语言创建默认目录：

- 中文环境下可能创建：`收件箱 / 待确认 / 文献总表.csv`
- 英文环境下可能创建：`inbox / review / catalog.csv`

程序不会因为切换界面语言而自动重命名已有目录或已有总表文件。

### 工作区规则

- `organize.bat` 是固定英文启动入口，不随界面语言变化
- `example_workspace/` 是默认演示工作区
- 受管分类目录通过 `.organize_category` 标记识别
- 你可以手动移动文件、重命名目录、调整层级，程序下次启动后会重新识别

### 当前限制

- 当前版本只处理 PDF
- 分类与识别主要依赖本地规则
- GPT / 更高级识别接口仍处于预留状态，默认不启用
- 目前以 Windows 使用体验为主

### 欢迎改进

欢迎提交 issue、fork 之后继续改进，或者直接按自己的工作流做二次开发。比较适合继续扩展的方向包括：

- 更稳的元数据提取
- 更细的分类规则
- 真正接入大模型辅助识别
- 更强的批量处理与冲突解决
- 更完整的测试覆盖

## English

`Lite Literature Organizer` is a lightweight local literature organizer. It provides a simple web UI for scanning PDFs dropped into an inbox, previewing extracted metadata, confirming archive decisions, and staying compatible with manual file moves or folder renames made in the file explorer. Improvements and adaptations are very welcome.

### What it does

- Scans PDFs from an inbox
- Extracts title, first author, year, and a short excerpt with local rules
- Suggests a target category and standardized filename
- Lets you review and adjust decisions before applying them
- Records app actions and detected manual workspace changes
- Uses `.organize_category` markers so managed folders can still be renamed or moved
- Supports both English and Simplified Chinese in the UI

### Highlights

- Local-first: no network required for the core workflow
- Lightweight: only `pypdf` is required beyond the Python standard library
- Bilingual UI: English and Simplified Chinese
- Extensible: higher-level recognition can be added later

### Quick start

1. Install Python 3.
2. Install the dependency:

```bash
pip install -r requirements.txt
```

3. Double-click `organize.bat`.
4. The browser opens the local web app automatically.

The default demo workspace lives in `example_workspace/`. On first launch, the app creates default folders based on the browser language:

- Chinese browsers may create `收件箱 / 待确认 / 文献总表.csv`
- English browsers may create `inbox / review / catalog.csv`

Existing folders and existing catalog files are preserved when the UI language changes.

### Workspace rules

- `organize.bat` is the fixed launcher name and does not change with the UI locale
- `example_workspace/` is the default demo workspace
- Managed category folders are recognized by `.organize_category` marker files
- You can still move files, rename folders, or change folder hierarchy manually

### Current limitations

- PDF only
- Classification is mostly rule-based
- GPT-assisted recognition is reserved for future integration
- The current release is Windows-first

### Contributions welcome

Feel free to open issues, fork the project, or adapt it to your own workflow. Good next directions include:

- more robust metadata extraction
- finer-grained classification rules
- real LLM-assisted recognition
- better batch handling and conflict resolution
- broader test coverage
