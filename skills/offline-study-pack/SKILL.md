---
name: offline-study-pack
description: Build an offline, self-contained study compendium (电子书/学习资料汇编) about a codebase's real external integrations. Inventories actual dependencies, downloads primary sources (markdown-first), fact-checks every claim against them, writes reader-calibrated Q&A chapters grounded in repo evidence, and assembles README + combined Markdown + single-file HTML. Use when the user asks to 整理离线学习资料, 下载文档做汇编, 生成电子书, prepare offline reading for a trip, or wants an external-perspective review of integrated tools with curated docs.
---

# Offline Study Pack

Produce a fully-offline study compendium about the external tools/practices a codebase actually uses (or misuses). The deliverable teaches a specific human, so calibration and grounding matter more than volume.

Three quality contracts (confirm with user, these are the defaults):
1. **Accurate with sources** — every load-bearing claim verifiable in a downloaded file.
2. **Fully offline** — no claim depends on a URL the reader can't open on a plane.
3. **Reader-friendly** — Q&A chapters + single-file HTML.

## Workflow

### 1. Inventory before promising

Never pick topics from memory. Enumerate real integrations:

- Python: `pyproject.toml` dependencies; JS: every `package.json` (monorepo: glob `apps/*/package.json` etc.)
- Rank by blast radius: money paths (billing, LLM spend, compute) > reliability > periphery.
- Grep for usage intensity to rank (e.g. `rg -io 'seedance|gemini|stripe' src --no-filename | sort | uniq -c | sort -rn`).
- Look for "pain evidence": probe scripts, workaround files, `*_limit.py`, TODO clusters — these mark chapters where the team already bled.
- Also check for **deprecated/EOL dependencies** (the single most valuable find; e.g. a driver past its EOL date). Flag these as the only deadline-bearing chapters.

Present ranked topic list, let the user cut/add. Ask about hand-rolled subsystems worth an "external perspective" chapter (billing, feature flags, deploy pipeline are common).

### 2. Calibrate the reader (do not skip)

Before writing anything long, run a short quiz: 4–6 questions, A/B/C options, mixing concept checks and "what do you actually do when X breaks". From the answers, state the calibration explicitly, e.g.:

> Concepts mid-level, operations delegated to agents → explain *why* and decision frameworks; commands only as recipes for their agent; define each term at first use with an example from THEIR repo.

### 3. Pilot one chapter first

Write one full chapter on the user's hottest pain point. Get feedback on depth, question choice, table/analogy density. Only then mass-produce.

### 4. Download sources, markdown-first

Create `<pack>/sources/`, one manifest of `filename|url` lines, fetch in parallel.

Priority order per source:
1. `https://<docs-site>/llms-full.txt` or `/llms.txt` (E2B, fal, OpenRouter, Stripe... growing list — always try)
2. `.md` suffix on doc URLs (docs.anthropic.com, docs.stripe.com support this)
3. `raw.githubusercontent.com` paths for docs that live in repos (FastAPI, httpx, Prometheus, READMEs)
4. Plain HTML with `-A "Mozilla/5.0"` for static sites (martinfowler.com, redis.io, readthedocs, AWS docs)

After fetch: `ls -la | awk '$5<3000'` — tiny files are 404s; retry with alternate paths. JS-only sites (volcengine, platform.openai.com) usually can't be captured: **say so in the chapter and list the exact questions to check online later**. Never silently drop a source.

Name files `NN-source.ext` where NN = chapter number.

### 5. Fact-check before writing

For every number you intend to print (TTLs, prices, limits, EOL dates, command syntax): grep the downloaded file first. Unverifiable → hedge or omit. This step is what makes contract #1 true.

### 6. Chapter template

One `chapters/NN-题目.md` per topic:

```markdown
# 第 N 章 标题（一句话立场，不是名词）

> **一句话导读**：结论先行。
> **关联代码**：repo paths + grep counts（"heartbeat 212 处" 这种证据）
> **本章资料**：sources/ 文件名 — 标题（原始 URL）

## Q1. （读者真会问的问题，不是教科书目录）
...每章 4–8 个 Q&A...

## Qn. 本章一页纸
- 按行动优先级的 bullet list，含给 agent 的自查任务
```

Style rules from calibration + these invariants: ground every chapter in repo evidence; state trade-offs as decisions ("现在不该上 X，转折信号是 Y"); tables for comparisons; "自查点" phrased as tasks the user can hand to their agent verbatim.

### 7. Assemble

```
<pack>/
├── README.md          # reading order, per-chapter one-liners + repo anchors, source manifest notes, post-trip action list (priority-ordered)
├── 汇编-全一册.md      # cat README chapters/*.md
├── 汇编-全一册.html    # scripts/build_html.py (self-contained, dark-mode)
├── chapters/
└── sources/
```

Build HTML: `python3 scripts/build_html.py <combined.md> <out.html>` (needs `pip install markdown`; script is in this skill's `scripts/`).

### 8. Deliver

Report: location, size, file count, which sources failed and their online-check questions, top-3 chapters to read first. Offer device copy (scp to phone/tablet — Termux shared storage `~/storage/shared/Documents/` makes it visible to reader apps).

## Pitfalls

- Writing from memory because "I know Redis" — the one number you don't check is the one that's wrong.
- Downloading 50 sources but citing none per-claim — sources must map to chapters (NN- prefix).
- One depth for all readers — the quiz is cheap, a mis-pitched 14-chapter book is not.
- Chapter = feature tour of a tool. Wrong. Chapter = "what your code does today, what the standard is, the delta, the action".
