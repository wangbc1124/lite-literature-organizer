# Lite Literature Organizer

[简体中文](#简体中文) | [English](#english)

## 简体中文

`Lite Literature Organizer` 是一个轻量、安静、挺适合自己长期用的本地文献整理工具。

它的想法很简单：把新来的 PDF 先放进收件箱，程序帮你做第一轮识别和归档建议，你看一眼、改一改、点一下，再把它放到合适的位置。你也完全可以在文件管理器里自己挪文件、改目录名、换层级，程序下次启动时会尽量跟上你的手动整理，而不是跟你较劲。

这不是一个“全能学术平台”，更像一个认真打磨过的小工具。欢迎继续改，欢迎按自己的习惯接着折腾。

### 能做什么

- 扫描收件箱中的 PDF
- 提取标题、第一作者、年份和首页摘要片段
- 给出目标分类和建议文件名
- 应用前允许人工确认和手动修改
- 记录整理历史和手动目录变化
- 通过 `.organize_category` 兼容目录重命名和层级调整
- 支持英语与简体中文界面

### 适合谁

- 想把 PDF 整理这件事变得没那么烦的人
- 不想把所有东西塞进重量级文献管理软件的人
- 喜欢自己掌控目录结构，但又希望程序帮一点忙的人

### 快速开始

1. 安装 Python 3
2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 双击根目录下的 `organize.bat`
4. 浏览器会自动打开本地网页界面

默认示例工作区在 `example_workspace/`。首次启动时，程序会根据浏览器语言创建默认目录：

- 中文环境下可能创建：`收件箱 / 待确认 / 文献总表.csv`
- 英文环境下可能创建：`inbox / review / catalog.csv`

切换界面语言不会自动重命名你已经建好的目录或总表文件。

### 工作方式

- `organize.bat` 是固定英文启动入口，不随界面语言变化
- `example_workspace/` 是默认演示工作区
- 受管分类目录通过 `.organize_category` 标记识别
- 你可以手动移动文件、重命名目录、调整层级
- 程序下次启动后会重新扫描并更新状态

### 当前边界

- 目前只处理 PDF
- 识别和分类主要依赖本地规则
- 更高级的模型辅助识别还在预留阶段
- 当前版本以 Windows 体验为主

### 欢迎改进

如果你想把它改得更聪明、更顺手，下面这些方向都很值得：

- 更稳的元数据提取
- 更细的分类规则
- 真正接入大模型辅助识别
- 更强的批量处理和冲突处理
- 更完整的测试覆盖

如果你只是想把它改成更像你自己的工具，那也完全合理。

## English

`Lite Literature Organizer` is a lightweight local tool for keeping a PDF library in shape without turning the whole process into a project of its own.

The idea is simple: drop new papers into an inbox, let the app make a first pass at metadata extraction and file naming, review the suggestion, tweak it if needed, and archive it. You can still move files around manually, rename folders, or reorganize the hierarchy however you like. The app tries to follow your workspace instead of fighting it.

This is not trying to be an all-in-one academic platform. It is a small, focused tool for people who want a calmer way to keep literature organized. If you want to improve it, reshape it, or wire in your own workflow, please do.

### What it does

- Scans PDFs from an inbox
- Extracts title, first author, year, and a short first-page excerpt
- Suggests a target category and standardized filename
- Lets you review and edit decisions before applying them
- Records app history and detected manual workspace changes
- Uses `.organize_category` markers so managed folders can still be renamed or moved
- Supports both English and Simplified Chinese in the UI

### Who it is for

- People who want PDF organization to feel less annoying
- People who prefer folders over heavyweight reference managers
- People who still want manual control, but appreciate a little help

### Quick start

1. Install Python 3
2. Install the dependency

```bash
pip install -r requirements.txt
```

3. Double-click `organize.bat`
4. Your browser opens the local web app

The default demo workspace lives in `example_workspace/`. On first launch, the app creates default folders based on the browser language:

- Chinese browsers may create `收件箱 / 待确认 / 文献总表.csv`
- English browsers may create `inbox / review / catalog.csv`

Existing folders and existing catalog files are preserved when the UI language changes.

### How it works

- `organize.bat` is the fixed launcher name and does not change with the UI locale
- `example_workspace/` is the default demo workspace
- Managed folders are recognized through `.organize_category` marker files
- You can still move files, rename folders, and change folder hierarchy manually
- The app re-scans the workspace and updates its internal state on the next run

### Current scope

- PDF only
- Classification is mostly rule-based
- Model-assisted recognition is reserved for future integration
- The current release is Windows-first

### Contributions welcome

Some especially good directions:

- more robust metadata extraction
- finer-grained classification rules
- real LLM-assisted recognition
- better batch handling and conflict handling
- broader test coverage

And if you just want to turn it into something more personal for your own workflow, that is a perfectly good use of it too.
