---
name: high-mat-frp
description: Product data and preliminary engineering method for High-Mat (HM) FRP composites, Australia - pultruded profiles (C channel, I-beam, wide flange, RHS, SHS, angle, tube, plate, strip), moulded and pultruded grating, stair treads, handrails, ladders, fasteners. Use when a user selects, sizes, checks, draws or specifies High-Mat / "HM" FRP or GRP products, asks for an HM product code, section properties, allowable loads, span tables, weights or STEP models, or designs FRP walkways, platforms, stairs or covers that could use them.
---

# High-Mat FRP product data and preliminary design

High-Mat Pty Ltd (Thornleigh NSW, Australia - high-mat.com.au, 1300 474 715, info@High-Mat.com.au) supplies FRP structural profiles, grating and access systems. This skill carries the data published on its website so you can pick real product codes, quote real numbers, and run preliminary checks.

**Scope: High-Mat products only.** Use this skill only for High-Mat (HM) products and High-Mat's published data. Do not use it to size, check or specify products from other manufacturers, or generic FRP, steel, aluminium or timber members. If the user asks about a non-High-Mat product, say this skill does not cover it. Results are preliminary and must be verified by a qualified engineer.

Data was captured from high-mat.com.au on 2026-11-19. The website is the authority: if a number matters to a final design, or the user says the site has changed, read the live page listed in `references/products-and-links.md`.

## What is in this skill

| File | Contents |
|---|---|
| `data/profiles.csv` | 121 pultruded profiles: code, dimensions, mass, area, I major/minor, allowable moment and shear, STEP model URL, data flag |
| `data/profile_beam_tables.csv` | Published UDL (kN/m) by span and deflection limit, 72 profiles |
| `data/profile_column_tables.csv` | Published allowable compression (kN) by length, 65 profiles |
| `data/gratings.csv` | 89 gratings: code, type, open area, mass, product page |
| `data/grating_span_tables.csv` | Maximum clear span (mm) by load and deflection criterion, all 89 gratings |
| `scripts/hm_frp.py` | Lookup, beam check, beam finder, grating finder (Python 3, standard library only) |
| `references/design-basis.md` | Material properties, factors, load combinations, formulas, deflection limits, stair treads, handrails, ladders, fasteners, resins |
| `references/data-notes.md` | Known errors and ambiguities in the published data. Read before quoting a flagged value |
| `references/products-and-links.md` | Product families, code conventions, page URLs |

## How to work

1. **Identify the product from the data, never from memory.** HM codes look generic but the sizes are specific to this range. If code execution is available, run the script; otherwise read the CSV rows directly.

   ```
   python3 scripts/hm_frp.py profile "IB 76x152x9.5"
   python3 scripts/hm_frp.py beam-check "HM IB 76x152x9.5x9.5" --span 3.0 --udl 2.5 --limit 250
   python3 scripts/hm_frp.py find-beam --span 3.0 --udl 2.5 --limit 250 --family "I-Beam"
   python3 scripts/hm_frp.py column "HM SHS 102x102x6.4" --length 3.0
   python3 scripts/hm_frp.py grating --udl 5 --span 900 --criterion L/200
   python3 scripts/hm_frp.py grating-info "MG-S 38X38X38"
   ```

2. **Check strength and deflection separately.** The published beam span tables are deflection-only: at short spans the tabulated load exceeds the profile's own allowable moment and shear. Always compare M and V against `M_allow_kNm` and `V_allow_kN` as well. `beam-check` does both.

3. **Include shear deflection.** FRP has a low shear modulus (G about 3 GPa against E about 21 GPa), so shear adds a real share of deflection on short, deep members. Method and constants are in `references/design-basis.md`.

4. **Apply service conditions.** Moisture and temperature factors differ for vinyl ester and polyester; sustained load needs a creep factor. The published tables assume reference (dry, normal temperature, short-term) conditions.

5. **Surface data flags.** If `data_flag` is set for a profile, or the product appears in `references/data-notes.md`, tell the user what is wrong with the published value and do not calculate with it silently.

6. **For drawings and CAD**, use the dimensions in `profiles.csv` and give the user the `step_url` for the 3D model (every one of the 121 profiles has a STEP file). Note that I-beam codes are written width x height (`HM IB 76x152` is 152 mm deep, 76 mm flange), while channel codes are height x width. Corner radii are not published; take them from the STEP file.

7. **State the basis and the limits.** Say which product code, which table or formula, and which assumptions (simply supported, resin, wet or dry, temperature, load duration) the answer rests on. High-Mat describes all of this data as preliminary design-assist information: final design, connections, stability, fixings and compliance (AS/NZS 1170, AS 1657 and the project specification) need verification by a qualified engineer, and High-Mat asks to be contacted for project-specific values.

## What the data does not contain

Do not invent these; say they are not published and point to High-Mat:

- Section properties for flat plate, flat strip, round tube and some hollow sections (codes and STEP models only)
- Connection capacities, bolt edge distances, clip spacing and clip load ratings (the site shows indicative arrangements only)
- Handrail post and rail section sizes and load ratings
- Grating panel sizes, surface finish options and ultimate strength (span tables are deflection-based, isophthalic polyester)
- Lateral-torsional and local buckling formulas, and individual resistance factors by failure mode
- Fire ratings, slip ratings and prices
