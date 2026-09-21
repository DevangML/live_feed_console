# 🎬 BUILD READY — Option A

**Project:** `/Users/devang/Desktop/live_feed_console/`  
**Scope:** 247 LOC (polling) → 3,500 LOC (full system)  
**Syllabus:** 1,175 rows (Parts 0-16)  
**Timeline:** 7-8 weeks @ 27 h/week  
**Status:** Ready to expand

---

## What You Have

| Item | Location | Purpose |
|---|---|---|
| **Project** | `~/Desktop/live_feed_console/` | Real polling engine + tests (247 LOC) |
| **Vault** | ProtonDrive Obsidian | 42-note concept graph (no plugins needed) |
| **Coach** | `/teach-me console` | Tracks progress, enforces gates |
| **Matrix** | `_bmad-output/live_console/` | 1,175-row traceability (all mapped) |
| **Expansion Plan** | `OPTION_A_EXPANSION_PLAN.md` | 7 layers to add (220 lines, read this next) |

---

## The 7 Layers (Read the Plan First)

**Layer 0 → Tooling** (Week 0)  
Hand-write every config: `package.json`, `vite.config.ts`, `tsconfig.json`

**Layer 1 → Vanilla** (Weeks 1-2)  
Framework-free widget: vanilla TS, DOM, event delegation  
*Covers Part 3-4 (JS + DOM)*

**Layer 2 → Backend** (Week 3)  
Mock server with failure modes: slow, flaky, 429, CORS, malformed responses  
*Covers Part 5 (Networking)*

**Layer 3 → React** (Weeks 4-5)  
Dashboard UI: components, hooks, routing, state management  
*Covers Part 7-8 (TS + React)*

**Layer 4 → a11y & Perf** (Week 6)  
Accessibility: ARIA, keyboard nav. Performance: profiling, optimization  
*Covers Part 9-10 (a11y + Performance)*

**Layer 5 → Narrative** (Week 7)  
Architecture decisions: 15+ ADRs, feature briefs, design choices  
*Covers Part 15-16 (Architecture + System Design)*

**Layer 6 → Polish** (Week 8)  
Advanced features: view transitions, streaming UI, concurrent rendering  
*Covers Part 8 ceiling tests*

---

## Next Move

1. **Read** `OPTION_A_EXPANSION_PLAN.md` (this directory)
2. **Open** your Proton Drive Obsidian vault
3. **Navigate** to `Home.md` in vault
4. **Review** the four clusters (Request Path, Document, Head, Version Control)
5. **Run** `/teach-me console`
6. **File the receipt** when you're ready to start Layer 0

The coach will gate you through all 7 layers, tracking every concept.

---

## Coverage Verification

When all layers are built:

```bash
cd ~/Desktop/live_feed_console
python3 ~/Desktop/interview_prep/projects/live-console-dashboard/scripts/coverage/build_matrix.py --paths
```

Should show: **578 artefacts cited, 578 present** (every row has a file)

---

**up:** `/teach-me console` · **vault:** ProtonDrive Obsidian · **plan:** OPTION_A_EXPANSION_PLAN.md
