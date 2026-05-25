(function () {
  const STORAGE_KEY = "quiz-web-answers-v1";
  const SAVE_DELAY_MS = 300;

  const state = {
    chapterIndex: 0,
    answers: {},
    saveTimer: null,
    revealRef: false,
  };

  const chapters = Array.isArray(window.QUIZ_DATA) ? window.QUIZ_DATA : [];

  const tabsEl = document.getElementById("chapter-tabs");
  const contentEl = document.getElementById("content");
  const chapterIndicatorEl = document.getElementById("chapter-indicator");
  const saveIndicatorEl = document.getElementById("save-indicator");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const submitBtn = document.getElementById("submit-btn");
  const hideRefBtn = document.getElementById("hide-ref-btn");

  function setupMarkdown() {
    if (window.marked && typeof window.marked.setOptions === "function") {
      window.marked.setOptions({ breaks: true, gfm: true });
    }
  }

  function renderMarkdown(markdown) {
    const source = markdown || "";
    if (window.marked && typeof window.marked.parse === "function") {
      return window.marked.parse(source);
    }
    return source.replaceAll("\n", "<br/>");
  }

  function loadAnswers() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return {};
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (error) {
      console.warn("Failed to parse saved answers:", error);
      return {};
    }
  }

  function saveAnswers() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.answers));
    saveIndicatorEl.textContent = "已自动保存";
  }

  function queueSave() {
    saveIndicatorEl.textContent = "保存中...";
    window.clearTimeout(state.saveTimer);
    state.saveTimer = window.setTimeout(saveAnswers, SAVE_DELAY_MS);
  }

  function setAnswer(questionId, value) {
    state.answers[questionId] = value;
    queueSave();
  }

  function renderTabs() {
    tabsEl.innerHTML = "";
    chapters.forEach(function (chapter, index) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chapter-tab";
      btn.textContent = chapter.title;
      if (index === state.chapterIndex) btn.classList.add("active");
      btn.addEventListener("click", function () {
        state.chapterIndex = index;
        state.revealRef = false;
        render();
      });
      tabsEl.appendChild(btn);
    });
  }

  function createQuestion(question, questionIndex) {
    const wrapper = document.createElement("article");
    wrapper.className = "question-card";

    const questionTitle = document.createElement("p");
    questionTitle.className = "question-title";
    questionTitle.textContent = "小题 " + (question.label || String(questionIndex + 1));
    wrapper.appendChild(questionTitle);

    const stem = document.createElement("div");
    stem.className = "question-stem";
    stem.innerHTML = renderMarkdown(question.stem || "");
    wrapper.appendChild(stem);

    const textarea = document.createElement("textarea");
    textarea.className = "question-answer";
    textarea.placeholder = "在此填写你的答案...";
    textarea.value = state.answers[question.id] || "";
    textarea.addEventListener("input", function (event) {
      setAnswer(question.id, event.target.value);
    });
    wrapper.appendChild(textarea);

    const reference = document.createElement("div");
    reference.className = "reference-panel";
    if (state.revealRef) reference.classList.add("visible");

    const title = document.createElement("p");
    title.className = "reference-title";
    title.textContent = "参考答案";
    reference.appendChild(title);

    const body = document.createElement("div");
    body.innerHTML = renderMarkdown(question.reference || "（暂无参考答案）");
    reference.appendChild(body);
    wrapper.appendChild(reference);

    return wrapper;
  }

  function createSection(section) {
    const card = document.createElement("section");
    card.className = "section-card";

    const title = document.createElement("h3");
    title.textContent = section.title;
    card.appendChild(title);

    if (section.preamble) {
      const preamble = document.createElement("div");
      preamble.innerHTML = renderMarkdown(section.preamble);
      card.appendChild(preamble);
    }

    (section.questions || []).forEach(function (question, questionIndex) {
      card.appendChild(createQuestion(question, questionIndex));
    });
    return card;
  }

  function renderChapter(chapter) {
    contentEl.innerHTML = "";

    const introCard = document.createElement("section");
    introCard.className = "chapter-intro";

    const heading = document.createElement("h2");
    heading.textContent = chapter.title;
    introCard.appendChild(heading);

    if (chapter.intro) {
      const introBody = document.createElement("div");
      introBody.innerHTML = renderMarkdown(chapter.intro);
      introCard.appendChild(introBody);
    }
    contentEl.appendChild(introCard);

    (chapter.sections || []).forEach(function (section) {
      contentEl.appendChild(createSection(section));
    });
  }

  function updateToolbar() {
    prevBtn.disabled = state.chapterIndex <= 0;
    nextBtn.disabled = state.chapterIndex >= chapters.length - 1;
    chapterIndicatorEl.textContent = "第 " + (state.chapterIndex + 1) + " / " + chapters.length + " 章";
  }

  function renderEmpty() {
    contentEl.innerHTML =
      '<section class="chapter-intro"><h2>暂无题目数据</h2><p>请先运行打包命令生成 <code>quiz-data.js</code>。</p></section>';
    chapterIndicatorEl.textContent = "-";
    prevBtn.disabled = true;
    nextBtn.disabled = true;
    submitBtn.disabled = true;
    hideRefBtn.disabled = true;
  }

  function render() {
    if (!chapters.length) {
      renderEmpty();
      return;
    }
    renderTabs();
    renderChapter(chapters[state.chapterIndex]);
    updateToolbar();
  }

  function bindToolbarEvents() {
    prevBtn.addEventListener("click", function () {
      if (state.chapterIndex <= 0) return;
      state.chapterIndex -= 1;
      state.revealRef = false;
      render();
    });

    nextBtn.addEventListener("click", function () {
      if (state.chapterIndex >= chapters.length - 1) return;
      state.chapterIndex += 1;
      state.revealRef = false;
      render();
    });

    submitBtn.addEventListener("click", function () {
      state.revealRef = true;
      render();
    });

    hideRefBtn.addEventListener("click", function () {
      state.revealRef = false;
      render();
    });
  }

  function init() {
    setupMarkdown();
    state.answers = loadAnswers();
    bindToolbarEvents();
    render();
    saveIndicatorEl.textContent = "已加载本地记录";
  }

  init();
})();
