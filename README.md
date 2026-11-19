# High-Mat FRP AI Skills

A Claude skill and a ChatGPT custom GPT kit that give an AI assistant the published product data of **High-Mat Pty Ltd** (https://high-mat.com.au), an Australian supplier of pultruded and moulded FRP (fibre reinforced polymer) products.

> **Scope: High-Mat products only.**
> These skills work only with High-Mat's own products and published data: High-Mat pultruded profiles, High-Mat gratings and the related High-Mat items listed below. They are not a general FRP, steel, timber or aluminium design tool, and they must not be used to size or check products from any other manufacturer. If a question is about a non-High-Mat product, the assistant should say so instead of guessing.

> **Preliminary design only.** Results compare loads with High-Mat's published allowable values. They do not replace the High-Mat datasheets or a design by a qualified engineer. See [Limitations](#limitations).

## What the skills know

| Data | Contents |
|---|---|
| **121 pultruded profiles** | I-beams, wide flange, channels, angles, SHS, RHS, round tube, flat bar and plate. Dimensions, mass, area, second moments of area, allowable moment and shear, STEP model links |
| **Beam tables** | Allowable uniform load by span and deflection limit (L/100 to L/600) |
| **Column tables** | Allowable compression by effective length |
| **89 gratings** | Moulded and pultruded types: open area, mass, maximum clear span by load and deflection criterion |
| **Design basis notes** | Material properties, deflection with shear deformation, stair treads, handrails, fasteners, resin selection |
| **Lookup script** | `scripts/hm_frp.py` so the assistant calculates instead of estimating |

All data comes from the High-Mat website, captured 19 November 2026. Corrections and known data issues are listed in [`references/data-notes.md`](references/data-notes.md).

## What you can ask

- "Find the lightest HM I-beam for a 3 m span carrying 4.5 kN/m, limit L/250."
- "Check HM SHS 89x89x6.4 as a 2.5 m post under 20 kN."
- "Which High-Mat moulded grating can span 900 mm at 5 kPa to L/200?"
- "Give me the dimensions and STEP link for HM IB 127x254x9.5x9.5."

A worked example (a 3.0 m x 1.8 m maintenance platform with beam sheet and deck plan) is in the blog article: https://high-mat.com.au/high-mat-frp-ai-skills-claude-chatgpt/

## Repository layout

```
SKILL.md                  Claude skill definition (entry point)
scripts/hm_frp.py         Lookup and check script (Python 3, no dependencies)
references/               Design basis, data notes, product links
data/                     CSV data: profiles, beam tables, column tables, gratings, grating span tables
chatgpt/GPT-instructions.txt   Instructions for a ChatGPT custom GPT
```

## Use with Claude

1. Download this repository as a zip (green **Code** button, then **Download ZIP**).
2. In Claude, open **Settings, Capabilities, Skills** and upload the zip as a custom skill. In Claude Code, copy the folder to `~/.claude/skills/high-mat-frp`.
3. Ask a question about High-Mat products. Claude loads the skill when the question involves them.

Command-line check of the script:

```
python3 scripts/hm_frp.py find-beam --span 3 --udl 4.5 --limit 250 --family "I-Beam"
python3 scripts/hm_frp.py grating --udl 5 --span 900 --criterion L/200 --type MG-S
```

## Use with ChatGPT

1. Create a custom GPT (a ChatGPT plan with GPT creation is required).
2. Paste `chatgpt/GPT-instructions.txt` into the instructions.
3. Upload the files in `data/` and `references/`, and `scripts/hm_frp.py`, as knowledge.
4. Switch on **Code Interpreter** so the GPT can calculate.

## High-Mat links

| Topic | Link |
|---|---|
| High-Mat website | https://high-mat.com.au |
| Profile capacity tables | https://high-mat.com.au/pultruded-frp-profiles-capacity/ |
| Beam capacity and deflection calculator | https://high-mat.com.au/frp-beam-capacity-deflection-calculator/ |
| Grating selector | https://high-mat.com.au/high-mat-frp-grating-selector/ |
| Technical data for FRP pultrusions | https://high-mat.com.au/technical_frp_pultrusions/ |
| Structural design guideline | https://high-mat.com.au/high-mat-frp-profile-lrfd-design-guideline/ |
| FRP profile types | https://high-mat.com.au/frp-profiles-types/ |
| FRP grating | https://high-mat.com.au/frp-grating-australia/ |
| FRP handrails | https://high-mat.com.au/frp-handrails-australia/ |
| FRP design and engineering | https://high-mat.com.au/frp-design-engineering-australia/ |
| Blog: using these skills | https://high-mat.com.au/high-mat-frp-ai-skills-claude-chatgpt/ |

**Contact:** High-Mat Pty Ltd, Thornleigh NSW, Australia. Phone 1300 474 715. Email info@High-Mat.com.au

## Limitations

- Products: High-Mat only (see Scope above).
- Checks: moment, shear, deflection (including shear deformation) and published column capacity. The skills do **not** check lateral-torsional or local buckling, web crippling, connections, bearing, fatigue, fire, or temperature and moisture effects beyond the stated factors.
- Section properties marked as calculated in `data/profiles.csv` (`data_flag` column) were derived from section geometry; confirm them against the High-Mat datasheet.
- Final design must be verified by a qualified engineer. For project advice, contact High-Mat.

## Updates

Data is refreshed when High-Mat updates its published tables. Check `references/data-notes.md` for the capture date and corrections.

## Licence and trademarks

High-Mat names, product data and images belong to High-Mat Pty Ltd. The skill text and script are provided to help customers and engineers work with High-Mat's published data. Use of the data is subject to High-Mat's website terms.
