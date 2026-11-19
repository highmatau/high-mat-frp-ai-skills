# Notes on the published data

The CSV files reproduce high-mat.com.au as captured on 2026-11-19 (checksummed against the site). The items below are places where the published data is inconsistent, so that you can warn the user instead of passing an error on. Where a value is corrected here, the CSV says so in `data_flag`.

## Beam span tables

**Deflection-limit columns.** The source table headers are `L/100, L/150, L/200, L/250, L/300, L/300, L/400, L/600` (one label duplicated). The website patches the display to read `L/300, L/400, L/500` for the last columns before L/600. The numbers themselves scale exactly as `L/100, L/150, L/200, L/250, L/300, L/350, L/400, L/600` (all 1,911 cells satisfy `w(L/n) = w(L/100) * 100 / n` within rounding), so `profile_beam_tables.csv` uses those labels. If a user quotes an "L/500" value from the website, it is the L/400 value.

For RHS, SHS and equal angle the source also repeats the L/300 column; the repeat is removed in the CSV.

**Deflection only.** The loads are not capped by strength. Example: HM CS 203x56x6.4x6.4 at 1.5 m lists 39.5 kN/m at L/100, which gives M = 11.1 kNm against a published allowable of 2.7 kNm. Always check M and V.

**Basis.** The tables are reproduced (median error under 1%) by a simply supported beam with E = 20.7 GPa, G = 3.1 GPa and shear area 0.6 A, i.e. shear deflection is included. The online calculator page instead states E = 23.0 GPa and G = 3.0 GPa. Use 20.7 and 3.1.

**Cut-off.** Loads below about 1.0 kN/m are left blank in the source. A blank is "not published", not zero.

## Profiles with suspect values

| Code | Issue |
|---|---|
| HM CS 152x50x9.5x9.5 | I major is 6.62E+05 in the source data; the website overrides it on display to 6.62E+06. CSV uses 6.62E+06 |
| HM CS 305x76x12.7x12.7 | Section properties are a copy of HM CS 292x70 (height 292, width 70, same area and I). Do not calculate with them |
| HM CS 292x70 and 305x76 | Allowable moment (12.3 and 11.7 kNm) is lower than the smaller HM CS 254x70 (20.5 kNm). May reflect local buckling; confirm |
| HM IB 102x203x12.7x12.7 | Web thickness given as 127 mm (should be 12.7) and area as 1881 mm2 (about 4900 expected) |
| HM IB 45x180x9x12 | I minor (1.05E+07) exceeds I major (1.03E+07); implausible for a 45 mm flange |
| HM RHS 51x25x3, 51x25x6.4 | I values are one to two orders too large and I minor exceeds I major. Do not use |
| HM SHS 50x50x6.4 | Thickness given as 64 mm (should be 6.4) |
| HM WF 203x203x9.5x9.5 | I minor 1.33E+06 looks ten times low against neighbouring sizes |
| HM EA 76x76x6.4 | I minor 1.16E+04 looks ten times low |
| HM SHS 89x89x6.4 | Beam span table is identical to HM SHS 76x76x9.5; likely copied. Verify by calculation |
| HM WF 152x152x6.4, 203x203x6.4, 254x254x9.5 | Allowable moment (about 3 to 10 kNm) is far below the thicker size of the same depth; thin-flange local buckling probably governs. Quote as published and note it |

## Profiles with no data beyond code and STEP model

HM CS 90x35x5x5; HM WF 102x102x8x8, 203x203x12.7; HM RHS 100x50x5, 100x75x5, 101x51x6.4, 150x100x6.4; HM SHS 102x102x9.5, 127x127x8, 25x25x6.4; HM EA 127x127x12.7; HM RT 102x9.5, 25x3.2, 32x6.4, 38x6.4; all flat plate (FP) and flat strip (FS).

Column table only: HM CS 76x38x6.4x6.4, HM SHS 152x152x9.5 and x12.7, and the round tubes listed in `profile_column_tables.csv`.

For solid rectangles and round tubes you may compute A and I from the nominal dimensions (state that you did), with E and G from `design-basis.md`.

## Code conventions that trip people up

- I-beam codes are **width x height x flange t x web t** (HM IB 76x152 is 152 deep). C channel and wide flange are **height x width x t x t**.
- Angle `cg_height` and `cg_length` are the centroid offsets from the heel. For doubly symmetric sections they are published as 0.
- `I_major` and `I_minor` for equal angles appear to be principal-axis values, not geometric x-x and y-y.

## Grating table

- `HM MG-S 40X40X40` is listed with dimensions "HMMG-ST40x40x40(5)" and links to the solid-top product page. Its numbers (72.25% open, 19.98 kg/m2) are consistent with an open square mesh; the link is wrong on the site.
- `HM MG-MINI 38x40x40` is listed as "30 x 40 x 40" and links to the 30 mm product. The spans and mass (24.4 kg/m2) are consistent with 38 mm.
- `HM MG-S 13X51X51`, `25X51X51`, `51X51X51` are listed as 50 x 50 mesh; `23X80X80` as 79 x 79.
- Solid-top (MG-ST) open area is 0 by definition.
- At deeper sections the L/200 span can exceed the 5 mm span; take the smallest of the criteria that apply to the project.

## Design guide

The strength-combination table and the time-effect table disagree on two companion factors (seismic: 1.0L against 0.5L; roof: "1.0L or 0.5W" against "0.5L or 0.5W"). Use AS/NZS 1170.0 combinations for Australian work.

## Corrections applied 2026-11-19 (site and this dataset)
Calculated from section geometry (sharp-corner model, density 1896 kg/m3, E=20.7 GPa, G=3.1 GPa): CS 305x76 section properties; IB 102x203x12.7 area and web thickness; RHS 51x25x3 and 51x25x6.4 I values; IB 45x180 I minor; WF 203x203x9.5 I minor; EA 76x76x6.4 I minor; EA 127x127x12.7 properties; SHS 89x89x6.4 beam table. Treat calculated values as preliminary until confirmed by High-Mat datasheets.
CS 152x42x6.4 and CS 292x70x12.7 exist in the data but have no product page yet.
