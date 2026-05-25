# Quiz Markdown Schema

本规范定义“题目 Markdown / 答案 Markdown”的标准格式，目标是让 `scripts/validate_quiz_markdown.py` 与 `scripts/build_quiz_data.py` 稳定解析。

## 1. 文件级约束

- 编码：UTF-8
- 每章建议两份文件：题目与含答案
- 两份文件的二级标题 `## ...` 必须按顺序一致

## 2. 标题层级

- 每个题目分节必须用二级标题：

```md
## 一、标题
```

## 3. 小题编号（题目）

主编号推荐：

```md
1. ...
2. ...
```

可选主编号（全节统一）：

```md
（1）...
（2）...
```

约束：

- 同一节主编号连续（1..n）
- 同一节不要混用 `1.` 与 `（1）`
- 代码块中的数字行不参与编号识别

## 4. 答案块（答案）

每节推荐包含答案锚点：

```md
答案：
1. ...
2. ...
```

或：

```md
**答案：**
- (1) ...
- (2) ...
```

约束：

- 答案题号覆盖题号
- 题号唯一
- 单题节可允许整段答案不编号

## 5. 执行流程

1. 运行校验：

```bash
python scripts/validate_quiz_markdown.py --project-root <repo_root>
```

2. 运行构建：

```bash
python scripts/build_quiz_data.py --project-root <repo_root> --strict
```
