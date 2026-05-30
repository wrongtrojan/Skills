# Component Catalog (v2)

Registry schema lives in `components/registry.json`. This catalog documents all **31** component keys.

> **Note:** v1 `components/schema.md` is removed; use this file + registry as the contract.

## Framework

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `framework.dracula` | Base shell: `tokens.css`, `base.css`, `runtime.js`, `shell.html` | — | all components |

## Typography

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `typography.partBanner` | Part 分段标题 `.part-banner` | static | — |
| `typography.sectionKicker` | 学术 kicker `.section-kicker` | static | — |
| `typography.lead` | 页级导读 `.lead` | static | — |
| `typography.subhead` | 小节标题 `h3.subhead` | static | — |
| `typography.footnote` | 脚注/图注 `.footnote` | static | — |

## Layout

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `layout.gridCards` | 2/3/4 列卡片网格 | cols-2, cols-3, cols-4 | — |
| `layout.splitRow` | 左右分栏 | default, balanced | `layout.insightPanel` |
| `layout.insightPanel` | split 左栏强调块 | static | `layout.splitRow` |
| `layout.archWrap` | 双栏 SVG 架构图 | static | `interactive.lightbox` |
| `layout.directionCard` | 研究方向卡（可点详情） | static, featured | `interactive.detailSystem` |
| `layout.columns3` | 产品三列展望 legacy | static | conflicts `interactive.roadmapOverlay` |

## Content

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `content.card` | 信息卡 | static, clickable | `interactive.detailSystem` |
| `content.bullets` | 圆点列表 | static | `math.katex` |
| `content.timeline` | 目录/进度行 | static | — |
| `content.flowStack` | 纵向步骤栈 | static, clickable-items | `interactive.detailSystem` |
| `content.dataTable` | 对照表 | static | — |
| `content.metricBar` | 一行结论条 | static | — |
| `content.capabilitiesGrid` | 四能力 + tags | static | — |
| `content.miniList` | 单栏紧凑列表 | static | — |

## Flow

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `flow.iclLayout` | 问题 + pipeline 页容器 | static | `flow.issueGrid`, `flow.pipelineHorizontal` |
| `flow.issueGrid` | 痛点并列 | static | — |
| `flow.pipelineHorizontal` | 横向流程 3–7 步 | highlight, muted-steps | — |

## Interactive

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `interactive.detailSystem` | detail overlay + `<template>` | static | `content.card`, `layout.directionCard`, `content.flowStack`, `math.katex` |
| `interactive.lightbox` | 截图/SVG 放大 DOM | static | `layout.archWrap`, `interactive.screensGrid` |
| `interactive.screensGrid` | 截图网格 `.shot-tile` | static | `interactive.lightbox` |
| `interactive.roadmapOverlay` | 2×2 路线图全屏 | static | conflicts `layout.columns3`; needs `component.js` |

## Math

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `math.katex` | KaTeX CDN head 片段 | static | `interactive.detailSystem` |

## Slides

| Key | Purpose | Variants | pairsWith |
|-----|---------|----------|-----------|
| `slide.cover` | 封面骨架 | static | `typography.sectionKicker` |
| `slide.thanks` | Thanks 末页 | static | — |
| `slide.takeaways` | 三要点 `.take-grid` | static | — |
| `slide.elevator` | 电梯陈述 `.elevator` | static | — |

## CSS Bundles

Styles are consolidated in `components/_bundles/`:

- `typography.css` — kickers, lead, sub, cover-line
- `layout.css` — grids, split, arch-wrap, columns3
- `content.css` — cards, bullets, timeline, tables, tags
- `flow.css` — flow-stack, issue-grid, pipeline
- `interactive.css` — detail, lightbox, screens, roadmap
- `slides.css` — thanks, elevator, takeaways
- `legacy.css` — extra decoration, legacy lightbox aliases

Each `component.css` points to its bundle via comment.

## Conflicts

- Do not combine `layout.columns3` and `interactive.roadmapOverlay` on the same outlook slide.
