#!/usr/bin/env python3
"""Bootstrap html-ppt-dracula v2 component folders, examples, and registry.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "components"
BUNDLE_MAP = {
    "typography": "typography.css",
    "layout": "layout.css",
    "content": "content.css",
    "flow": "flow.css",
    "interactive": "interactive.css",
    "slides": "slides.css",
    "code": "code.css",
    "math": None,
}

COMPONENTS = [
    ("typography", "part-banner", ["static"], "长 deck Part 分段标题", "typography.partBanner"),
    ("typography", "section-kicker", ["static"], "章节/锚点 kicker", "typography.sectionKicker"),
    ("typography", "lead", ["static"], "页级一句导读", "typography.lead"),
    ("typography", "subhead", ["static"], "页内小节标题 h3.subhead", "typography.subhead"),
    ("typography", "footnote", ["static"], "页脚/图注", "typography.footnote"),
    ("layout", "grid-cards", ["cols-2", "cols-3", "cols-4"], "2/3/4 列卡片网格", "layout.gridCards"),
    ("layout", "split-row", ["default", "balanced"], "左右分栏", "layout.splitRow"),
    ("layout", "insight-panel", ["static"], "split 左栏 card 化", "layout.insightPanel"),
    ("layout", "arch-wrap", ["static"], "双栏 SVG/架构图", "layout.archWrap"),
    ("layout", "direction-card", ["static", "featured"], "研究方向四象限卡", "layout.directionCard"),
    ("layout", "columns3", ["static"], "产品三列摘要 legacy", "layout.columns3"),
    ("content", "card", ["static", "clickable"], "信息卡/可点击展开", "content.card"),
    ("content", "bullets", ["static"], "圆点列表", "content.bullets"),
    ("content", "timeline", ["static"], "目录/进度行+badge", "content.timeline"),
    ("content", "flow-stack", ["static", "clickable-items"], "纵向步骤栈", "content.flowStack"),
    ("content", "data-table", ["static"], "对照/结果表", "content.dataTable"),
    ("content", "metric-bar", ["static"], "一行核心结论", "content.metricBar"),
    ("content", "capabilities-grid", ["static"], "产品四能力 legacy", "content.capabilitiesGrid"),
    ("content", "mini-list", ["static"], "窄栏紧凑列表 legacy", "content.miniList"),
    ("content", "eval-list", ["static"], "Golden eval 行 + 可点 badge", "content.evalList"),
    ("flow", "icl-layout", ["static"], "问题+流程页容器", "flow.iclLayout"),
    ("flow", "issue-grid", ["static"], "缺陷/痛点并列", "flow.issueGrid"),
    ("flow", "pipeline-horizontal", ["highlight", "muted-steps"], "横向流程 3-7 步", "flow.pipelineHorizontal"),
    ("interactive", "detail-system", ["static"], "详情弹窗+trigger+template", "interactive.detailSystem"),
    ("interactive", "lightbox", ["static"], "SVG/截图放大 DOM", "interactive.lightbox"),
    ("interactive", "screens-grid", ["static"], "多截图网格 legacy", "interactive.screensGrid"),
    ("interactive", "roadmap-overlay", ["static"], "路线图全屏 overlay legacy", "interactive.roadmapOverlay"),
    ("interactive", "content-modal", ["static"], "JSON/文本内容弹窗", "interactive.contentModal"),
    ("code", "highlight-js", ["json", "plaintext"], "highlight.js 语法高亮（本地 vendor）", "code.highlightJs"),
    ("math", "katex", ["static"], "KaTeX 公式渲染 head 片段", "math.katex"),
    ("slides", "cover", ["static"], "封面页骨架", "slide.cover"),
    ("slides", "thanks", ["static"], "Thanks 末页", "slide.thanks"),
    ("slides", "takeaways", ["static"], "三要点页 legacy", "slide.takeaways"),
    ("slides", "elevator", ["static"], "电梯陈述页 legacy", "slide.elevator"),
]

PAIRS = {
    "content.card": ["interactive.detailSystem"],
    "content.evalList": ["interactive.contentModal", "code.highlightJs"],
    "layout.archWrap": ["interactive.lightbox"],
    "layout.directionCard": ["interactive.detailSystem"],
    "interactive.screensGrid": ["interactive.lightbox"],
    "interactive.contentModal": ["code.highlightJs"],
    "content.flowStack": ["interactive.detailSystem"],
    "layout.splitRow": ["layout.insightPanel"],
    "math.katex": ["interactive.detailSystem"],
}

CONFLICTS = {
    "layout.columns3": ["interactive.roadmapOverlay"],
}

EXAMPLES: dict[str, str] = {
    "typography.partBanner": '<p class="part-banner">Part I <span>· Survey 建图</span></p>',
    "typography.sectionKicker": '<p class="section-kicker">Seminar · 2026.05</p>',
    "typography.lead": '<p class="lead">从非结构化文本抽取实体间关系，输出三元组。</p>',
    "typography.subhead": '<h3 class="subhead">三层框架</h3>',
    "typography.footnote": '<p class="footnote">数据来源：Comprehensive Survey (2024)</p>',
    "layout.gridCards": """<div class="grid-cards cols-3">
  <article class="card"><h3>表示层</h3><p>词向量 → 上下文编码</p></article>
  <article class="card"><h3>编码层</h3><p>BiLSTM / Transformer</p></article>
  <article class="card"><h3>预测层</h3><p>关系分类头</p></article>
</div>""",
    "layout.splitRow": """<div class="split-row balanced">
  <div class="insight-panel">
    <p class="lead">Joint 统一优化，缓解 Pipeline 错误传播。</p>
  </div>
  <button type="button" class="arch-panel" data-diagram-cap="Joint RE">
    <h3>Joint / End-to-End</h3>
    <svg viewBox="0 0 300 88" xmlns="http://www.w3.org/2000/svg"><rect x="96" y="18" width="108" height="52" rx="5" fill="#22232f" stroke="#8be9fd"/></svg>
  </button>
</div>""",
    "layout.insightPanel": """<div class="insight-panel">
  <p class="lead">ICL 将示例作为上下文，无需梯度更新。</p>
</div>""",
    "layout.archWrap": """<div class="arch-wrap">
  <button type="button" class="arch-panel" data-diagram-cap="Pipeline RE">
    <h3>Pipeline</h3>
    <svg viewBox="0 0 300 88" xmlns="http://www.w3.org/2000/svg"><text x="150" y="44" text-anchor="middle" fill="#f8f8f2" font-size="10">NER → RE</text></svg>
  </button>
  <button type="button" class="arch-panel" data-diagram-cap="Joint RE">
    <h3>Joint</h3>
    <svg viewBox="0 0 300 88" xmlns="http://www.w3.org/2000/svg"><text x="150" y="44" text-anchor="middle" fill="#8be9fd" font-size="10">联合模型</text></svg>
  </button>
</div>""",
    "layout.directionCard": """<div class="grid-cards cols-3">
  <button type="button" class="card direction-card detail-trigger featured" data-detail-id="detail-featured">
    <h3>跨语言 RE</h3><p>低资源语言迁移与对齐</p><span class="dir-tag">Future</span>
  </button>
  <button type="button" class="card direction-card detail-trigger" data-detail-id="detail-open">
    <h3>开放关系</h3><p>开放域关系发现</p>
  </button>
</div>""",
    "layout.columns3": """<div class="cols-3">
  <div class="col"><h3>近期</h3><ul><li>完善文档</li><li>单元测试</li></ul></div>
  <div class="col"><h3>中期</h3><ul><li>插件 API</li><li>主题切换</li></ul></div>
  <div class="col"><h3>远期</h3><ul><li>协作编辑</li><li>云端发布</li></ul></div>
</div>""",
    "content.card": """<article class="card">
  <h3>Prompt-tuning</h3>
  <p>冻结 PLM，仅优化 soft prompt 向量。</p>
</article>""",
    "content.bullets": r"""<ul class="bullets">
  <li>输出：$\langle h, r, t \rangle$ 三元组</li>
  <li>Joint 模型共享表示，相互纠错</li>
</ul>""",
    "content.timeline": """<div class="timeline">
  <div class="tl-row"><span class="tl-chapter">Intro</span><span class="tl-desc">RE 定义与范式</span><span class="tl-badge muted">—</span></div>
  <div class="tl-row"><span class="tl-chapter">PLMs</span><span class="tl-desc">Prompt vs ICL</span><span class="tl-badge">SyRuP · GPT-RE</span></div>
</div>""",
    "content.flowStack": """<div class="flow-stack">
  <button type="button" class="flow-item detail-trigger" data-detail-id="detail-step1">
    <span class="flow-num">01</span>
    <div><strong>Recall</strong><span class="flow-desc">检索相似示例</span></div>
  </button>
</div>""",
    "content.dataTable": """<table class="data-table">
  <thead><tr><th>方法</th><th>F1</th><th>备注</th></tr></thead>
  <tbody><tr><td>GPT-RE</td><td class="highlight">72.4</td><td>5-shot ICL</td></tr></tbody>
</table>""",
    "content.metricBar": '<p class="metric-bar"><strong>结论：</strong> ICL 在少样本场景优于 fine-tune。</p>',
    "content.capabilitiesGrid": """<div class="grid-cards">
  <article class="card"><h3>检索增强</h3><div class="tags"><span class="tag">RAG</span><span class="tag">向量</span></div></article>
  <article class="card"><h3>知识图谱</h3><div class="tags"><span class="tag">KG</span><span class="tag">三元组</span></div></article>
  <article class="card"><h3>混合推理</h3><div class="tags"><span class="tag">LLM</span></div></article>
  <article class="card"><h3>可视化</h3><div class="tags"><span class="tag">UI</span></div></article>
</div>""",
    "content.miniList": """<div class="col">
  <h3>下一步</h3>
  <ul><li>集成 Zotero MCP</li><li>批量导出 PDF</li><li>多语言界面</li></ul>
</div>""",
    "content.evalList": """<p class="arch-sub">点击 golden 文件名或基线 badge 查看详情（可滚轮浏览）</p>
<div class="eval-list">
  <div class="eval-row">
    <div class="eval-name">表分类</div>
    <div class="eval-cmd">table_classify_eval --report-id 1</div>
    <button type="button" class="eval-link" data-golden="table_classify">golden_tables.json</button>
    <button type="button" class="eval-badge pass" data-baseline="table_classify">26/26</button>
  </div>
</div>
<p class="eval-foot">推荐顺序：table_classify → ingest --force → relation → smoke → analysis</p>""",
    "flow.iclLayout": """<div class="icl-layout">
  <div class="issue-grid">
    <div class="issue-card"><span class="issue-num">1</span><div><strong>示例选择</strong><p>随机示例效果不稳定</p></div></div>
  </div>
  <div class="pipeline-wrap"><h3 class="subhead">R3 Pipeline</h3><div class="pipeline-h"><span class="pipe-step is-highlight"><span class="pipe-n">1</span><strong>Recall</strong></span></div></div>
</div>""",
    "flow.issueGrid": """<div class="issue-grid">
  <div class="issue-card"><span class="issue-num">A</span><div><strong>标签噪声</strong><p>自动标注质量参差</p></div></div>
  <div class="issue-card"><span class="issue-num">B</span><div><strong>上下文长度</strong><p>示例占用 token 预算</p></div></div>
</div>""",
    "flow.pipelineHorizontal": """<div class="pipeline-wrap">
  <h3 class="subhead">SyRuP 流程</h3>
  <div class="pipeline-h">
    <span class="pipe-step"><span class="pipe-n">1</span><strong>检索</strong></span>
    <span class="pipe-arrow">→</span>
    <span class="pipe-step is-highlight"><span class="pipe-n">2</span><strong>排序</strong><span class="pipe-tag">核心</span></span>
    <span class="pipe-arrow">→</span>
    <span class="pipe-step is-muted"><span class="pipe-n">3</span><strong>预测</strong></span>
  </div>
</div>""",
    "interactive.detailSystem": """<!-- Triggers use data-detail-id; templates live outside deck -->
<button type="button" class="card detail-trigger" data-detail-id="detail-demo">
  <h3>点击查看详情</h3><p>摘要文字</p>
</button>
<template id="detail-demo">
  <h4>背景</h4><p>详情正文，支持 $E=mc^2$。</p>
</template>

<div class="detail-overlay" id="detail-overlay" role="dialog" aria-modal="true" aria-label="详情" aria-hidden="true">
  <button type="button" class="overlay-backdrop" id="detail-backdrop" aria-label="关闭详情"></button>
  <div class="detail-panel" id="detail-panel">
    <button type="button" class="overlay-close" id="detail-close" aria-label="关闭">×</button>
    <h3 id="detail-title"></h3>
    <div id="detail-body"></div>
  </div>
</div>""",
    "interactive.lightbox": """<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="大图预览" aria-hidden="true">
  <button type="button" class="overlay-backdrop" id="lightbox-backdrop" aria-label="关闭预览"></button>
  <div class="lightbox-inner">
    <button type="button" class="overlay-close" id="lightbox-close" aria-label="关闭">×</button>
    <img id="lightbox-img" src="" alt="" />
    <p class="lightbox-cap" id="lightbox-cap"></p>
  </div>
</div>""",
    "interactive.screensGrid": """<div class="screen-rows">
  <div class="screen-row">
    <button type="button" class="shot-tile" data-src="https://placehold.co/800x500/22232f/8be9fd?text=Screen+1" data-cap="Dashboard">
      <img src="https://placehold.co/800x500/22232f/8be9fd?text=Screen+1" alt="" loading="lazy" />
      <span class="shot-cap">Dashboard</span>
    </button>
    <button type="button" class="shot-tile" data-src="https://placehold.co/800x500/22232f/bd93f9?text=Screen+2" data-cap="Editor">
      <img src="https://placehold.co/800x500/22232f/bd93f9?text=Screen+2" alt="" loading="lazy" />
      <span class="shot-cap">Editor</span>
    </button>
  </div>
</div>""",
    "interactive.roadmapOverlay": """<div class="roadmap-grid" role="group" aria-label="展望要点，点击查看全屏">
  <button type="button" class="roadmap-tile" aria-haspopup="dialog" aria-controls="roadmap-full">
    <h3>近期</h3>
    <div class="roadmap-body"><ul><li>完善文档</li><li>CI 集成</li></ul></div>
  </button>
  <button type="button" class="roadmap-tile" aria-haspopup="dialog" aria-controls="roadmap-full">
    <h3>中期</h3>
    <div class="roadmap-body"><ul><li>插件生态</li><li>API 开放</li></ul></div>
  </button>
</div>

<div class="roadmap-full" id="roadmap-full" role="dialog" aria-modal="true" aria-labelledby="roadmap-full-title" aria-hidden="true">
  <button type="button" class="roadmap-full-backdrop" id="roadmap-full-backdrop" tabindex="-1" aria-label="关闭全屏"></button>
  <div class="roadmap-full-panel">
    <button type="button" class="roadmap-full-close" id="roadmap-full-close" aria-label="关闭">×</button>
    <p class="roadmap-full-kicker">Roadmap · 项目展望</p>
    <h2 class="roadmap-full-title" id="roadmap-full-title"></h2>
    <div class="roadmap-full-body" id="roadmap-full-body"></div>
  </div>
</div>""",
    "interactive.contentModal": """<div id="content-modal" class="content-modal" role="dialog" aria-modal="true" aria-hidden="true" aria-label="详情">
  <button type="button" class="content-modal-backdrop" id="content-modal-backdrop" tabindex="-1" aria-label="关闭"></button>
  <div class="content-modal-inner">
    <button type="button" class="content-modal-close" id="content-modal-close" aria-label="关闭">×</button>
    <h3 id="content-modal-title" class="content-modal-title"></h3>
    <pre class="content-modal-body dracula-scroll"><code id="content-modal-code" class="language-json"></code></pre>
  </div>
</div>""",
    "code.highlightJs": """<!-- Copy vendor/highlightjs/ next to your deck; paste in <head> -->
<link rel="stylesheet" href="vendor/highlightjs/dracula.css" />
<script src="vendor/highlightjs/highlight.min.js"></script>
<script src="vendor/highlightjs/json.min.js"></script>""",
    "math.katex": """<!-- Paste in <head> -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous" />
<!-- Paste before </body> -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>""",
    "slide.cover": """<!-- Inside <section class="slide" id="s-cover"><div class="inner"> … -->
<p class="section-kicker">Seminar · 2026.05</p>
<h1>关系抽取文献阅读</h1>
<p class="sub">以 Comprehensive Survey 为主线 · 约 15 min</p>
<div class="cover-line" aria-hidden="true"></div>""",
    "slide.thanks": """<!-- <section class="slide slide-thanks" id="s-thanks"><div class="inner"> … -->
<div class="thanks-hero">
  <h2 class="thanks-title">谢谢</h2>
  <p class="sub">Q &amp; A</p>
</div>
<footer class="thanks-foot">RE Seminar · 2026</footer>""",
    "slide.takeaways": """<p class="kicker">Takeaways</p>
<h2>收获分享</h2>
<div class="take-grid">
  <article class="take"><div class="label">Survey 坐标</div><p class="kw">先建图再填论文</p></article>
  <article class="take"><div class="label">ICL 路线</div><p class="kw"><em>Recall-Retrieve-Reason</em> 三阶段</p></article>
  <article class="take"><div class="label">零样本</div><p class="kw">中文场景需专门评测</p></article>
</div>""",
    "slide.elevator": """<p class="kicker">One line</p>
<h2>HybridRAG</h2>
<p class="elevator"><span>知识图谱</span> + <em>向量检索</em> · <em>LLM 推理</em></p>""",
}


def bundle_for_category(cat: str) -> str | None:
    return BUNDLE_MAP.get(cat)


def write_component_files(cat: str, slug: str, key: str, variants: list[str], reuse: str) -> None:
    folder = COMP / cat / slug
    folder.mkdir(parents=True, exist_ok=True)

    bundle = bundle_for_category(cat)
    css_file = folder / "component.css"
    if cat not in ("math", "code"):
        css_file.write_text(
            f"/* See components/_bundles/{bundle} for {key} */\n",
            encoding="utf-8",
        )

    example = EXAMPLES.get(key, f"<!-- Example: {key} -->")
    if key == "code.highlightJs":
        (folder / "component.html").write_text(
            '<pre class="code-block dracula-scroll"><code class="language-json">{\n  "items": [{ "id": "demo", "expect_type": "subsidiaries" }]\n}</code></pre>\n',
            encoding="utf-8",
        )
    else:
        (folder / "component.html").write_text(example.strip() + "\n", encoding="utf-8")

    if key == "interactive.roadmapOverlay":
        (folder / "component.js").write_text(ROADMAP_JS.strip() + "\n", encoding="utf-8")
    if key == "interactive.contentModal":
        (folder / "component.js").write_text(CONTENT_MODAL_JS.strip() + "\n", encoding="utf-8")

    if cat in ("math", "code"):
        (folder / "head.html").write_text(example.strip() + "\n", encoding="utf-8")

    readme = folder / "README.md"
    readme.write_text(
        f"# {key}\n\n"
        f"**Reuse:** {reuse}\n\n"
        f"**Variants:** {', '.join(variants)}\n\n"
        f"**Bundle:** `{bundle or 'head.html'}`\n\n"
        f"Copy `component.html` into a slide `.inner` or append overlay DOM after `</main>`.\n",
        encoding="utf-8",
    )


ROADMAP_JS = """
(function () {
  var deck = document.getElementById("deck");
  var roadmapFull = document.getElementById("roadmap-full");
  var roadmapFullTitle = document.getElementById("roadmap-full-title");
  var roadmapFullBody = document.getElementById("roadmap-full-body");
  var roadmapFullClose = document.getElementById("roadmap-full-close");
  var roadmapFullBackdrop = document.getElementById("roadmap-full-backdrop");
  var roadmapLastFocus = null;

  function openRoadmapFull(tile) {
    if (!roadmapFull || !roadmapFullTitle || !roadmapFullBody) return;
    var title = tile.querySelector("h3");
    var body = tile.querySelector(".roadmap-body");
    roadmapLastFocus = document.activeElement;
    roadmapFullTitle.textContent = title ? title.textContent : "";
    roadmapFullBody.innerHTML = body ? body.innerHTML : "";
    roadmapFull.classList.add("is-open");
    roadmapFull.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("lightbox-open");
    if (deck) deck.style.overflow = "hidden";
    if (roadmapFullClose) roadmapFullClose.focus();
  }

  function closeRoadmapFull() {
    if (!roadmapFull || !roadmapFull.classList.contains("is-open")) return;
    roadmapFull.classList.remove("is-open");
    roadmapFull.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("lightbox-open");
    if (deck) deck.style.overflow = "";
    if (roadmapLastFocus && roadmapLastFocus.focus) roadmapLastFocus.focus();
  }

  document.querySelectorAll(".roadmap-tile").forEach(function (tile) {
    tile.addEventListener("click", function () { openRoadmapFull(tile); });
  });
  if (roadmapFullClose) roadmapFullClose.addEventListener("click", closeRoadmapFull);
  if (roadmapFullBackdrop) roadmapFullBackdrop.addEventListener("click", closeRoadmapFull);
})();
"""

CONTENT_MODAL_JS = """
(function () {
  var modal = document.getElementById("content-modal");
  var titleEl = document.getElementById("content-modal-title");
  var bodyEl = document.getElementById("content-modal-code");
  var closeBtn = document.getElementById("content-modal-close");
  var backdrop = document.getElementById("content-modal-backdrop");
  var deck = document.getElementById("deck");
  if (!modal || !titleEl || !bodyEl) return;

  function highlightBody(text, lang) {
    lang = lang || "plaintext";
    bodyEl.removeAttribute("data-highlighted");
    if (lang === "plaintext") {
      bodyEl.className = "";
      bodyEl.textContent = text;
      return;
    }
    bodyEl.className = "language-" + lang;
    if (typeof hljs !== "undefined" && hljs.getLanguage && hljs.getLanguage(lang)) {
      try {
        var out = hljs.highlight(text, { language: lang, ignoreIllegals: true });
        bodyEl.innerHTML = out.value;
        bodyEl.classList.add("hljs");
        return;
      } catch (err) {}
    }
    bodyEl.textContent = text;
  }

  window.openContentModal = function (title, body, lang) {
    titleEl.textContent = title;
    highlightBody(body, lang || "plaintext");
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("lightbox-open");
    if (deck) deck.style.overflow = "hidden";
    if (closeBtn) closeBtn.focus();
  };

  function closeModal() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    var lightbox = document.getElementById("lightbox");
    if (!lightbox || !lightbox.classList.contains("is-open")) {
      document.documentElement.classList.remove("lightbox-open");
      if (deck) deck.style.overflow = "";
    }
  }

  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (backdrop) backdrop.addEventListener("click", closeModal);
  document.addEventListener("keydown", function (e) {
    if (modal.classList.contains("is-open") && e.key === "Escape") {
      e.preventDefault();
      e.stopPropagation();
      closeModal();
    }
  }, true);
})();
"""


def main() -> None:
    entries = []
    for cat, slug, variants, reuse, key in COMPONENTS:
        css_path = f"components/{cat}/{slug}/component.css"
        if cat in ("math", "code"):
            css_path = f"components/{cat}/{slug}/head.html"
        write_component_files(cat, slug, key, variants, reuse)
        entry = {
            "key": key,
            "category": cat,
            "variants": variants,
            "files": {
                "css": css_path,
                "html": f"components/{cat}/{slug}/component.html",
            },
            "requires": ["framework.dracula"],
            "pairsWith": PAIRS.get(key, []),
            "reuse": reuse,
            "doc": f"references/component-catalog.md#{slug}",
        }
        if key == "interactive.roadmapOverlay":
            entry["files"]["script"] = f"components/{cat}/{slug}/component.js"
        if key == "interactive.contentModal":
            entry["files"]["script"] = f"components/{cat}/{slug}/component.js"
        if key in CONFLICTS:
            entry["conflicts"] = CONFLICTS[key]
        entries.append(entry)

    registry = {
        "version": "2.0.0",
        "categories": ["typography", "layout", "content", "flow", "interactive", "code", "math", "slides"],
        "components": entries,
    }
    (COMP / "registry.json").write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} components to {COMP / 'registry.json'}")


if __name__ == "__main__":
    main()
