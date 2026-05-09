const STORAGE_KEY = "literature-organizer.locale";
const SUPPORTED_LOCALES = ["zh-CN", "en"];

const TRANSLATIONS = {
  "zh-CN": {
    pageTitle: "文献整理程序",
    appTitle: "收件箱审阅台",
    languageLabel: "语言",
    scan: "重新扫描",
    applyAll: "应用全部",
    rebuild: "刷新总表",
    tabInbox: "收件箱",
    tabHistory: "历史记录",
    tabCatalog: "文献总表",
    tabFolders: "目录映射",
    tabSettings: "设置",
    inboxHeading: "待处理文件",
    inboxEmpty: "收件箱里还没有 PDF。",
    detailHeading: "识别结果",
    detailEmpty: "选中文件后，这里会显示标题、作者、年份、原因和摘要。",
    detailNotSelected: "未选择",
    actionHeading: "归档动作",
    actionEmpty: "这里会显示目标类别、建议文件名和确认按钮。",
    actionHint: "程序会先给出规则建议，你也可以手动修改后再归档。",
    labelTitle: "标题",
    labelAuthor: "第一作者",
    labelYear: "年份",
    labelReason: "识别原因",
    labelExcerpt: "首页摘要片段",
    labelCategory: "目标类别",
    labelFilename: "建议文件名",
    labelTarget: "目标路径",
    applyOne: "确认归档",
    historyHeading: "历史记录",
    historyRefresh: "刷新历史",
    historyClear: "清空历史",
    historySubtle: "这里会记录程序内操作，也会尽量识别你手动移动或重命名后的变化。",
    historyEmpty: "还没有历史记录。",
    catalogHeading: "文献总表",
    catalogPlaceholder: "搜索文件名、路径、分类",
    columnFilename: "文件名",
    columnPath: "相对路径",
    columnTop: "顶层",
    columnSub: "子目录",
    foldersHeading: "目录映射",
    foldersSubtle: "程序依靠 .organize_category 标记识别受管目录，所以你仍然可以手动改名或调整层级。",
    settingsHeading: "工作区",
    advancedHeading: "高级识别",
    advancedSubtle: "当前版本优先保证本地流程稳定可用，后续可以继续接入更高级别的识别能力。",
    settingsRoot: "根目录",
    settingsInbox: "收件箱",
    settingsReview: "待确认",
    settingsCatalog: "总表",
    settingsLog: "日志",
    settingsHistory: "历史",
    settingsLauncher: "统一入口",
    settingsLocale: "当前语言",
    settingsLocaleSource: "默认语言来源",
    settingsBehavior: "目录行为",
    confidenceHigh: "高",
    confidenceMedium: "中",
    confidenceLow: "低",
    confidenceReview: "待确认",
    confidenceUnknown: "未知",
    confidenceSuffix: "置信度",
    unknownValue: "未识别",
    emptyExcerpt: "没有提取到首页摘要。",
    historyDelete: "删除",
    historyDeleteLoading: "删除中...",
    historyDeleted: "已删除一条历史记录。",
    historyDeleteFailed: "删除历史失败：",
    historyClearConfirm: "要清空全部历史记录吗？这不会影响现有文献文件，只会清空历史日志。",
    historyClearLoading: "清空中...",
    historyCleared: "历史记录已清空。",
    historyClearFailed: "清空历史失败：",
    historyRefreshed: "历史记录和当前目录状态已刷新。",
    historyRefreshFailed: "刷新历史失败：",
    scanLoading: "扫描中...",
    scanDone: "收件箱已重新扫描。",
    scanFailed: "扫描失败：",
    applyOneLoading: "归档中...",
    applyAllLoading: "应用中...",
    applyDone: "已归档：",
    applyBatchDone: "已完成批量归档。",
    applyFailed: "归档失败：",
    applyBatchFailed: "批量归档失败：",
    rebuildLoading: "刷新中...",
    rebuildDone: "文献总表已刷新。",
    rebuildFailed: "刷新总表失败：",
    bootFailed: "启动失败：",
    folderSourceDiscovered: "已发现",
    folderSourceDefault: "默认补建",
    folderSourceFixed: "固定目录",
    folderSourceLabel: "来源",
    folderDuplicates: "重复 marker",
    folderKeyLabel: "分类键",
    categoryReview: "待确认",
    eventServiceStart: "服务启动",
    eventApplyOne: "单篇归档",
    eventApplyBatch: "批量归档",
    eventCatalogRebuild: "重建总表",
    eventManualChange: "手动变更",
    statusSuccess: "成功",
    statusApplied: "已应用",
    statusSkipped: "已跳过",
    statusMoved: "已移动",
    statusRemoved: "已移除",
    statusAdded: "已新增",
    statusFolderMoved: "目录已移动",
    statusFolderMissing: "目录缺失",
    statusFolderAdded: "目录已新增",
    statusInfo: "信息",
    statusError: "错误",
    localeName: "简体中文",
    localeSource: "本地选择 > 浏览器语言 > English",
    localeBehavior: "现有目录不自动改名；新建默认目录随当前语言变化",
    launcherScript: "organize.bat",
    gptConfigured: "已检测到 API Key",
    gptMissing: "未配置 API Key",
  },
  en: {
    pageTitle: "Literature Organizer",
    appTitle: "Inbox Review",
    languageLabel: "Language",
    scan: "Scan",
    applyAll: "Apply All",
    rebuild: "Refresh Catalog",
    tabInbox: "Inbox",
    tabHistory: "History",
    tabCatalog: "Catalog",
    tabFolders: "Folders",
    tabSettings: "Settings",
    inboxHeading: "Pending Files",
    inboxEmpty: "No PDF files in the inbox.",
    detailHeading: "Recognition Result",
    detailEmpty: "Select a file to see the title, author, year, reason, and excerpt.",
    detailNotSelected: "Not selected",
    actionHeading: "Archive Action",
    actionEmpty: "This panel shows the target category, suggested filename, and apply button.",
    actionHint: "The app suggests a category first, and you can still adjust it manually.",
    labelTitle: "Title",
    labelAuthor: "First Author",
    labelYear: "Year",
    labelReason: "Reason",
    labelExcerpt: "Excerpt",
    labelCategory: "Category",
    labelFilename: "Suggested Filename",
    labelTarget: "Target Path",
    applyOne: "Apply",
    historyHeading: "History",
    historyRefresh: "Refresh History",
    historyClear: "Clear History",
    historySubtle: "The app records internal actions and detected manual moves or renames.",
    historyEmpty: "No history yet.",
    catalogHeading: "Catalog",
    catalogPlaceholder: "Search filename, path, or category",
    columnFilename: "Filename",
    columnPath: "Relative Path",
    columnTop: "Top Level",
    columnSub: "Subfolders",
    foldersHeading: "Folder Mapping",
    foldersSubtle: "Managed folders are discovered via .organize_category markers, so you can still rename or move them manually.",
    settingsHeading: "Workspace",
    advancedHeading: "Advanced Recognition",
    advancedSubtle: "This version prioritizes a stable local workflow first. You can extend it later with more advanced recognition.",
    settingsRoot: "Root",
    settingsInbox: "Inbox",
    settingsReview: "Review",
    settingsCatalog: "Catalog",
    settingsLog: "Log",
    settingsHistory: "History",
    settingsLauncher: "Launcher",
    settingsLocale: "Current Language",
    settingsLocaleSource: "Default Locale Source",
    settingsBehavior: "Directory Behavior",
    confidenceHigh: "High",
    confidenceMedium: "Medium",
    confidenceLow: "Low",
    confidenceReview: "Review",
    confidenceUnknown: "Unknown",
    confidenceSuffix: "confidence",
    unknownValue: "Unknown",
    emptyExcerpt: "No excerpt was extracted.",
    historyDelete: "Delete",
    historyDeleteLoading: "Deleting...",
    historyDeleted: "History entry deleted.",
    historyDeleteFailed: "Failed to delete history: ",
    historyClearConfirm: "Clear all history records? This only removes history logs and does not touch your files.",
    historyClearLoading: "Clearing...",
    historyCleared: "History cleared.",
    historyClearFailed: "Failed to clear history: ",
    historyRefreshed: "History and folder state refreshed.",
    historyRefreshFailed: "Failed to refresh history: ",
    scanLoading: "Scanning...",
    scanDone: "Inbox scanned.",
    scanFailed: "Scan failed: ",
    applyOneLoading: "Applying...",
    applyAllLoading: "Applying...",
    applyDone: "Archived: ",
    applyBatchDone: "Batch archive complete.",
    applyFailed: "Archive failed: ",
    applyBatchFailed: "Batch archive failed: ",
    rebuildLoading: "Refreshing...",
    rebuildDone: "Catalog refreshed.",
    rebuildFailed: "Failed to refresh catalog: ",
    bootFailed: "Startup failed: ",
    folderSourceDiscovered: "Discovered",
    folderSourceDefault: "Default Rebuilt",
    folderSourceFixed: "Fixed",
    folderSourceLabel: "Source",
    folderDuplicates: "Duplicate marker",
    folderKeyLabel: "Key",
    categoryReview: "Review",
    eventServiceStart: "Service Start",
    eventApplyOne: "Single Archive",
    eventApplyBatch: "Batch Archive",
    eventCatalogRebuild: "Catalog Rebuild",
    eventManualChange: "Manual Change",
    statusSuccess: "Success",
    statusApplied: "Applied",
    statusSkipped: "Skipped",
    statusMoved: "Moved",
    statusRemoved: "Removed",
    statusAdded: "Added",
    statusFolderMoved: "Folder Moved",
    statusFolderMissing: "Folder Missing",
    statusFolderAdded: "Folder Added",
    statusInfo: "Info",
    statusError: "Error",
    localeName: "English",
    localeSource: "Saved choice > browser language > English",
    localeBehavior: "Existing folders keep their names; only newly created defaults follow the current language.",
    launcherScript: "organize.bat",
    gptConfigured: "API Key detected",
    gptMissing: "API Key not configured",
  },
};

const EVENT_TRANSLATION_KEYS = {
  service_start: "eventServiceStart",
  apply_one: "eventApplyOne",
  apply_batch: "eventApplyBatch",
  catalog_rebuild: "eventCatalogRebuild",
  manual_change_detected: "eventManualChange",
};

const STATUS_TRANSLATION_KEYS = {
  success: "statusSuccess",
  applied: "statusApplied",
  skipped_exists: "statusSkipped",
  moved: "statusMoved",
  removed: "statusRemoved",
  added: "statusAdded",
  folder_moved: "statusFolderMoved",
  folder_missing: "statusFolderMissing",
  folder_added: "statusFolderAdded",
  info: "statusInfo",
  error: "statusError",
};

const FOLDER_SOURCE_TRANSLATION_KEYS = {
  discovered: "folderSourceDiscovered",
  default_rebuilt: "folderSourceDefault",
  fixed: "folderSourceFixed",
};

const state = {
  locale: resolveInitialLocale(),
  inbox: [],
  history: [],
  catalog: [],
  folders: [],
  settings: null,
  selectedSource: null,
  draftBySource: {},
};

const ui = {
  tabs: [...document.querySelectorAll(".tab")],
  panels: [...document.querySelectorAll(".panel-view")],
  languageSelect: document.getElementById("language-select"),
  inboxList: document.getElementById("inbox-list"),
  inboxCount: document.getElementById("inbox-count"),
  detailEmpty: document.getElementById("detail-empty"),
  detailCard: document.getElementById("detail-card"),
  detailConfidence: document.getElementById("detail-confidence"),
  detailTitle: document.getElementById("detail-title"),
  detailAuthor: document.getElementById("detail-author"),
  detailYear: document.getElementById("detail-year"),
  detailReason: document.getElementById("detail-reason"),
  detailExcerpt: document.getElementById("detail-excerpt"),
  actionEmpty: document.getElementById("action-empty"),
  actionForm: document.getElementById("action-form"),
  categorySelect: document.getElementById("category-select"),
  filenameInput: document.getElementById("filename-input"),
  targetPreview: document.getElementById("target-preview"),
  applyOneBtn: document.getElementById("apply-one-btn"),
  applyAllBtn: document.getElementById("apply-all-btn"),
  scanBtn: document.getElementById("scan-btn"),
  rebuildBtn: document.getElementById("rebuild-btn"),
  historyRefreshBtn: document.getElementById("history-refresh-btn"),
  historyClearBtn: document.getElementById("history-clear-btn"),
  historyList: document.getElementById("history-list"),
  catalogBody: document.getElementById("catalog-body"),
  catalogSearch: document.getElementById("catalog-search"),
  folderGrid: document.getElementById("folder-grid"),
  settingsRoot: document.getElementById("settings-root"),
  gptStatus: document.getElementById("gpt-status"),
  statusBanner: document.getElementById("status-banner"),
};

function resolveInitialLocale() {
  const saved = window.localStorage.getItem(STORAGE_KEY);
  if (saved && SUPPORTED_LOCALES.includes(saved)) {
    return saved;
  }
  const browser = navigator.language || navigator.userLanguage || "";
  return browser.toLowerCase().startsWith("zh") ? "zh-CN" : "en";
}

function t(key) {
  return TRANSLATIONS[state.locale][key] || TRANSLATIONS.en[key] || key;
}

function apiUrl(path) {
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}lang=${encodeURIComponent(state.locale)}`;
}

function confidenceLabel(confidence) {
  if (confidence === "high") return t("confidenceHigh");
  if (confidence === "medium") return t("confidenceMedium");
  if (confidence === "low") return t("confidenceLow");
  if (confidence === "review") return t("confidenceReview");
  return t("confidenceUnknown");
}

function eventLabel(eventType) {
  return t(EVENT_TRANSLATION_KEYS[eventType] || "statusInfo");
}

function statusLabel(status) {
  return t(STATUS_TRANSLATION_KEYS[status] || "statusInfo");
}

function folderSourceLabel(source) {
  return t(FOLDER_SOURCE_TRANSLATION_KEYS[source] || "statusInfo");
}

function showBanner(message, type = "info") {
  ui.statusBanner.textContent = message;
  ui.statusBanner.className = `status-banner ${type}`;
}

function clearBanner() {
  ui.statusBanner.textContent = "";
  ui.statusBanner.className = "status-banner hidden";
}

function setButtonState(button, { loading = false, label = null } = {}) {
  if (!button) return;
  if (label !== null) {
    button.dataset.defaultLabel = button.dataset.defaultLabel || button.textContent;
    button.textContent = label;
  } else if (button.dataset.defaultLabel) {
    button.textContent = button.dataset.defaultLabel;
  }
  button.disabled = loading;
  button.classList.toggle("loading", loading);
}

function currentDraft() {
  return state.selectedSource ? state.draftBySource[state.selectedSource] : null;
}

function applyStaticTranslations() {
  document.documentElement.lang = state.locale;
  document.title = t("pageTitle");
  ui.languageSelect.value = state.locale;

  const mapping = {
    "app-title": "appTitle",
    "language-label": "languageLabel",
    "scan-btn": "scan",
    "apply-all-btn": "applyAll",
    "rebuild-btn": "rebuild",
    "tab-inbox": "tabInbox",
    "tab-history": "tabHistory",
    "tab-catalog": "tabCatalog",
    "tab-folders": "tabFolders",
    "tab-settings": "tabSettings",
    "inbox-heading": "inboxHeading",
    "detail-heading": "detailHeading",
    "action-heading": "actionHeading",
    "label-title": "labelTitle",
    "label-author": "labelAuthor",
    "label-year": "labelYear",
    "label-reason": "labelReason",
    "label-excerpt": "labelExcerpt",
    "label-category": "labelCategory",
    "label-filename": "labelFilename",
    "label-target": "labelTarget",
    "apply-one-btn": "applyOne",
    "history-heading": "historyHeading",
    "history-refresh-btn": "historyRefresh",
    "history-clear-btn": "historyClear",
    "history-subtle": "historySubtle",
    "catalog-heading": "catalogHeading",
    "column-filename": "columnFilename",
    "column-path": "columnPath",
    "column-top": "columnTop",
    "column-sub": "columnSub",
    "folders-heading": "foldersHeading",
    "folders-subtle": "foldersSubtle",
    "settings-heading": "settingsHeading",
    "advanced-heading": "advancedHeading",
    "advanced-subtle": "advancedSubtle",
    "action-hint": "actionHint",
  };

  Object.entries(mapping).forEach(([id, key]) => {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = t(key);
    }
  });

  ui.catalogSearch.placeholder = t("catalogPlaceholder");
}

function categoryOptions() {
  const options = state.folders
    .filter((folder) => folder.key !== "review")
    .map((folder) => ({
      key: folder.key,
      label: `${folder.label} / ${folder.relative_path}`,
      relativePath: folder.relative_path,
    }));

  options.push({
    key: "review",
    label: `${t("categoryReview")} / ${state.settings?.review_dir || t("categoryReview")}`,
    relativePath: state.settings?.review_dir || t("categoryReview"),
  });

  return options;
}

async function fetchJson(path, options) {
  const response = await fetch(apiUrl(path), options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = payload.error || `${response.status} ${response.statusText}`;
    throw new Error(message);
  }
  return payload;
}

function renderInbox() {
  ui.inboxCount.textContent = String(state.inbox.length);
  if (!state.inbox.length) {
    ui.inboxList.className = "inbox-list empty-state";
    ui.inboxList.textContent = t("inboxEmpty");
    state.selectedSource = null;
    renderDetail();
    return;
  }

  ui.inboxList.className = "inbox-list";
  ui.inboxList.innerHTML = "";

  state.inbox.forEach((item) => {
    if (!state.draftBySource[item.source_name]) {
      state.draftBySource[item.source_name] = {
        source_name: item.source_name,
        category_key: item.category_key,
        filename: item.proposed_filename,
      };
    }

    const button = document.createElement("button");
    button.className = `inbox-item${state.selectedSource === item.source_name ? " active" : ""}`;
    button.type = "button";
    button.innerHTML = `
      <h3>${item.source_name}</h3>
      <p>${item.title || t("unknownValue")}</p>
      <p>${item.category_label} · ${confidenceLabel(item.confidence)} ${t("confidenceSuffix")}</p>
    `;
    button.addEventListener("click", () => {
      state.selectedSource = item.source_name;
      renderInbox();
      renderDetail();
    });
    ui.inboxList.appendChild(button);
  });

  if (!state.selectedSource) {
    state.selectedSource = state.inbox[0].source_name;
  }
  renderDetail();
}

function renderDetail() {
  const item = state.inbox.find((entry) => entry.source_name === state.selectedSource);
  if (!item) {
    ui.detailEmpty.classList.remove("hidden");
    ui.detailEmpty.textContent = t("detailEmpty");
    ui.detailCard.classList.add("hidden");
    ui.actionEmpty.classList.remove("hidden");
    ui.actionEmpty.textContent = t("actionEmpty");
    ui.actionForm.classList.add("hidden");
    ui.detailConfidence.className = "status-pill muted";
    ui.detailConfidence.textContent = t("detailNotSelected");
    return;
  }

  ui.detailEmpty.classList.add("hidden");
  ui.detailCard.classList.remove("hidden");
  ui.actionEmpty.classList.add("hidden");
  ui.actionForm.classList.remove("hidden");

  ui.detailConfidence.className = `status-pill ${item.confidence}`;
  ui.detailConfidence.textContent = `${confidenceLabel(item.confidence)} ${t("confidenceSuffix")}`;
  ui.detailTitle.textContent = item.title || t("unknownValue");
  ui.detailAuthor.textContent = item.author || t("unknownValue");
  ui.detailYear.textContent = item.year || t("unknownValue");
  ui.detailReason.textContent = item.reason || "";
  ui.detailExcerpt.textContent = item.excerpt || t("emptyExcerpt");

  const draft = state.draftBySource[item.source_name];
  const options = categoryOptions();
  ui.categorySelect.innerHTML = options.map((option) => `<option value="${option.key}">${option.label}</option>`).join("");
  ui.categorySelect.value = draft.category_key;
  ui.filenameInput.value = draft.filename;
  updateTargetPreview();
}

function updateTargetPreview() {
  const draft = currentDraft();
  if (!draft) return;
  const option = categoryOptions().find((entry) => entry.key === draft.category_key);
  const dir = option?.relativePath || draft.category_key;
  ui.targetPreview.textContent = `${dir}/${draft.filename}`;
}

function renderHistory() {
  if (!state.history.length) {
    ui.historyList.className = "history-list empty-state";
    ui.historyList.textContent = t("historyEmpty");
    return;
  }

  ui.historyList.className = "history-list";
  ui.historyList.innerHTML = state.history
    .map((event) => {
      const pathLine =
        event.before_path || event.after_path
          ? `<p class="subtle">${event.before_path || "-"} -> ${event.after_path || "-"}</p>`
          : "";
      const pillClass = event.status === "success" ? "high" : event.status === "error" ? "review" : "medium";
      return `
        <article class="history-item">
          <div class="history-head">
            <strong>${eventLabel(event.event_type)}</strong>
            <div class="inline-actions">
              <span class="status-pill ${pillClass}">${statusLabel(event.status)}</span>
              <button class="button small ghost history-delete-btn" type="button" data-history-id="${event.id || ""}">${t("historyDelete")}</button>
            </div>
          </div>
          <p>${event.source || t("statusInfo")}</p>
          ${pathLine}
          <p class="subtle">${event.detail || ""}</p>
          <p class="subtle">${event.timestamp}</p>
        </article>
      `;
    })
    .join("");

  ui.historyList.querySelectorAll(".history-delete-btn").forEach((button) => {
    button.addEventListener("click", async () => {
      const entryId = button.dataset.historyId;
      if (!entryId) return;
      await deleteHistoryEntry(entryId, button);
    });
  });
}

function renderCatalog() {
  const query = ui.catalogSearch.value.trim().toLowerCase();
  const rows = state.catalog.filter((row) => {
    if (!query) return true;
    return [row.filename, row.relative_path, row.subfolders, row.top_level].join(" ").toLowerCase().includes(query);
  });

  ui.catalogBody.innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td>${row.filename}</td>
          <td>${row.relative_path}</td>
          <td>${row.top_level}</td>
          <td>${row.subfolders}</td>
        </tr>
      `
    )
    .join("");
}

function renderFolders() {
  ui.folderGrid.innerHTML = state.folders
    .map((folder) => {
      const duplicates = folder.duplicates.length
        ? `<p class="subtle">${t("folderDuplicates")}</p><code>${folder.duplicates.join("\n")}</code>`
        : "";
      return `
        <article class="folder-card">
          <h3>${folder.label}</h3>
          <p class="subtle">${t("folderKeyLabel")}: <strong>${folder.key}</strong></p>
          <code>${folder.relative_path}</code>
          ${folder.marker_file ? `<code>${folder.marker_file}</code>` : ""}
          <p class="subtle">${t("folderSourceLabel")}: ${folderSourceLabel(folder.source)}</p>
          ${duplicates}
        </article>
      `;
    })
    .join("");
}

function renderSettings() {
  if (!state.settings) return;
  ui.settingsRoot.innerHTML = `
    <dt>${t("settingsRoot")}</dt><dd>${state.settings.root}</dd>
    <dt>${t("settingsInbox")}</dt><dd>${state.settings.inbox_dir}</dd>
    <dt>${t("settingsReview")}</dt><dd>${state.settings.review_dir}</dd>
    <dt>${t("settingsCatalog")}</dt><dd>${state.settings.catalog_file}</dd>
    <dt>${t("settingsLog")}</dt><dd>${state.settings.log_file}</dd>
    <dt>${t("settingsHistory")}</dt><dd>${state.settings.history_file || "history_log.jsonl"}</dd>
    <dt>${t("settingsLauncher")}</dt><dd>${state.settings.launcher_script || t("launcherScript")}</dd>
    <dt>${t("settingsLocale")}</dt><dd>${t("localeName")}</dd>
    <dt>${t("settingsLocaleSource")}</dt><dd>${t("localeSource")}</dd>
    <dt>${t("settingsBehavior")}</dt><dd>${t("localeBehavior")}</dd>
  `;
  ui.gptStatus.innerHTML = `
    <strong>${state.settings.gpt_configured ? t("gptConfigured") : t("gptMissing")}</strong>
    <code>${state.settings.gpt_status}</code>
  `;
}

async function loadInbox() {
  const data = await fetchJson("/api/inbox");
  state.inbox = data.items;
  renderInbox();
}

async function loadHistory() {
  const data = await fetchJson("/api/history");
  state.history = data.events;
  renderHistory();
}

async function loadCatalog() {
  const data = await fetchJson("/api/catalog");
  state.catalog = data.rows;
  renderCatalog();
}

async function loadFolders() {
  const data = await fetchJson("/api/folders");
  state.folders = data.folders;
  renderFolders();
}

async function loadSettings() {
  state.settings = await fetchJson("/api/settings");
  renderSettings();
}

async function deleteHistoryEntry(entryId, button) {
  setButtonState(button, { loading: true, label: t("historyDeleteLoading") });
  try {
    const data = await fetchJson("/api/history/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: entryId }),
    });
    state.history = data.events;
    renderHistory();
    showBanner(t("historyDeleted"), "success");
  } catch (error) {
    showBanner(`${t("historyDeleteFailed")}${error.message}`, "error");
  } finally {
    setButtonState(button, { loading: false });
  }
}

async function clearHistory() {
  if (!window.confirm(t("historyClearConfirm"))) return;
  setButtonState(ui.historyClearBtn, { loading: true, label: t("historyClearLoading") });
  try {
    const data = await fetchJson("/api/history/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clear_all: true }),
    });
    state.history = data.events;
    renderHistory();
    showBanner(t("historyCleared"), "success");
  } catch (error) {
    showBanner(`${t("historyClearFailed")}${error.message}`, "error");
  } finally {
    setButtonState(ui.historyClearBtn, { loading: false });
  }
}

async function boot() {
  clearBanner();
  applyStaticTranslations();
  await Promise.all([loadSettings(), loadFolders(), loadInbox(), loadCatalog(), loadHistory()]);
}

async function setLocale(locale, { persist = true } = {}) {
  const nextLocale = SUPPORTED_LOCALES.includes(locale) ? locale : "en";
  if (persist) {
    window.localStorage.setItem(STORAGE_KEY, nextLocale);
  }
  state.locale = nextLocale;
  await boot();
}

ui.tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    ui.tabs.forEach((entry) => entry.classList.toggle("active", entry === tab));
    ui.panels.forEach((panel) => panel.classList.toggle("active", panel.dataset.panel === tab.dataset.tab));
  });
});

ui.languageSelect.addEventListener("change", async () => {
  await setLocale(ui.languageSelect.value);
});

ui.categorySelect.addEventListener("change", () => {
  const draft = currentDraft();
  if (!draft) return;
  draft.category_key = ui.categorySelect.value;
  updateTargetPreview();
});

ui.filenameInput.addEventListener("input", () => {
  const draft = currentDraft();
  if (!draft) return;
  draft.filename = ui.filenameInput.value;
  updateTargetPreview();
});

ui.actionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const draft = currentDraft();
  if (!draft) return;
  setButtonState(ui.applyOneBtn, { loading: true, label: t("applyOneLoading") });
  try {
    const data = await fetchJson("/api/inbox/apply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items: [draft] }),
    });
    state.inbox = data.items;
    state.catalog = data.catalog_rows;
    delete state.draftBySource[draft.source_name];
    state.selectedSource = state.inbox[0]?.source_name || null;
    renderInbox();
    renderCatalog();
    await loadHistory();
    showBanner(`${t("applyDone")}${draft.source_name}`, "success");
  } catch (error) {
    showBanner(`${t("applyFailed")}${error.message}`, "error");
  } finally {
    setButtonState(ui.applyOneBtn, { loading: false });
  }
});

ui.applyAllBtn.addEventListener("click", async () => {
  if (!state.inbox.length) return;
  setButtonState(ui.applyAllBtn, { loading: true, label: t("applyAllLoading") });
  try {
    const items = state.inbox.map((item) => state.draftBySource[item.source_name]);
    const data = await fetchJson("/api/inbox/apply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items }),
    });
    state.inbox = data.items;
    state.catalog = data.catalog_rows;
    state.draftBySource = {};
    state.selectedSource = state.inbox[0]?.source_name || null;
    renderInbox();
    renderCatalog();
    await loadHistory();
    showBanner(t("applyBatchDone"), "success");
  } catch (error) {
    showBanner(`${t("applyBatchFailed")}${error.message}`, "error");
  } finally {
    setButtonState(ui.applyAllBtn, { loading: false });
  }
});

ui.scanBtn.addEventListener("click", async () => {
  setButtonState(ui.scanBtn, { loading: true, label: t("scanLoading") });
  try {
    const data = await fetchJson("/api/inbox/scan", { method: "POST" });
    state.inbox = data.items;
    state.selectedSource = state.inbox[0]?.source_name || null;
    renderInbox();
    showBanner(t("scanDone"), "success");
  } catch (error) {
    showBanner(`${t("scanFailed")}${error.message}`, "error");
  } finally {
    setButtonState(ui.scanBtn, { loading: false });
  }
});

ui.rebuildBtn.addEventListener("click", async () => {
  setButtonState(ui.rebuildBtn, { loading: true, label: t("rebuildLoading") });
  try {
    const data = await fetchJson("/api/catalog/rebuild", { method: "POST" });
    state.catalog = data.rows;
    state.folders = data.folders;
    renderCatalog();
    renderFolders();
    await loadHistory();
    showBanner(t("rebuildDone"), "success");
  } catch (error) {
    showBanner(`${t("rebuildFailed")}${error.message}`, "error");
  } finally {
    setButtonState(ui.rebuildBtn, { loading: false });
  }
});

ui.historyRefreshBtn.addEventListener("click", async () => {
  setButtonState(ui.historyRefreshBtn, { loading: true, label: t("rebuildLoading") });
  try {
    const data = await fetchJson("/api/history/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{}",
    });
    state.history = data.events;
    state.catalog = data.rows;
    state.folders = data.folders;
    renderHistory();
    renderCatalog();
    renderFolders();
    showBanner(t("historyRefreshed"), "success");
  } catch (error) {
    showBanner(`${t("historyRefreshFailed")}${error.message}`, "error");
  } finally {
    setButtonState(ui.historyRefreshBtn, { loading: false });
  }
});

ui.historyClearBtn.addEventListener("click", clearHistory);
ui.catalogSearch.addEventListener("input", renderCatalog);

boot().catch((error) => {
  console.error(error);
  ui.inboxList.className = "inbox-list empty-state";
  ui.inboxList.textContent = `${t("bootFailed")}${error.message}`;
  showBanner(`${t("bootFailed")}${error.message}`, "error");
});
