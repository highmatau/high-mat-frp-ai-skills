# High-Mat FRP AI skills

A Claude skill and a ChatGPT custom GPT kit that give AI assistants High-Mat's published pultruded FRP data: 121 profiles, beam and column capacity tables, 89 gratings, STEP model links and design notes. Use them for preliminary section selection, load checks and grating selection.

Preliminary design only. Final design must be verified by a qualified engineer. Data source: https://high-mat.com.au

## Contents

| Folder | Purpose |
|---|---|
| repository root | Claude skill: `SKILL.md`, `scripts/`, `references/`, `data/` |
| `chatgpt/` | Custom GPT instructions |
| `data/` | CSV data used by both kits |

## Use with Claude

1. Download this repository as a zip (Code, Download ZIP).
2. Add it as a custom skill in Claude (Settings, Capabilities, Skills), or copy the folder to `~/.claude/skills/` for Claude Code.
3. Ask, for example: "Find the lightest HM I-beam for a 3 m span at 4.5 kN/m, limit L/250."

Command line check:

```
python3 scripts/hm_frp.py find-beam --span 3 --udl 4.5 --limit 250 --family "I-Beam"
python3 scripts/hm_frp.py grating --udl 5 --span 900 --criterion L/200 --type MG-S
```

## Use with ChatGPT

1. Create a custom GPT.
2. Paste `chatgpt/GPT-instructions.txt` into the instructions.
3. Upload the files from `data/`, the files from `references/` and `scripts/hm_frp.py` as knowledge. Enable Code Interpreter.

## Data notes

Known data issues and corrections are in `references/data-notes.md`.

Blog article with a worked example: https://high-mat.com.au/high-mat-frp-ai-skills-claude-chatgpt/
