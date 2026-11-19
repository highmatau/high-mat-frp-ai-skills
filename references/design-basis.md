# Design basis published by High-Mat

Sources: FRP Structural Design Guide, Profile Capacity Tables, Beam Capacity & Deflection Calculator, Grating Load & Span Tables, Stair Tread Selection Guide, Handrail Design Guide, Fasteners and Resin pages (URLs in `products-and-links.md`). Captured 2026-11-19.

## Contents
1. Material properties of pultruded profiles
2. Design format, factors and load combinations
3. Beam check method
4. Deflection limits and creep
5. Columns
6. Grating
7. Stair treads
8. Handrails and kickplates
9. Ladders
10. FRP fasteners
11. Resin selection

## 1. Material properties of pultruded profiles (characteristic minimums)

| Property | Minimum | Test |
|---|---|---|
| Longitudinal tensile strength | 207 MPa | ASTM D638 |
| Transverse tensile strength | 48 MPa | ASTM D638 |
| Longitudinal tensile modulus E | 20.7 GPa | ASTM D638 |
| Longitudinal compressive strength | 207 MPa | ASTM D6641 |
| Longitudinal compressive modulus | 20.7 GPa | ASTM D6641 |
| In-plane shear strength | 65 MPa | ASTM D5379 |
| In-plane shear modulus G | 3.1 GPa | ASTM D5379 |
| Interlaminar shear strength | 34 MPa | ASTM D2344 |
| Pin bearing strength, longitudinal | 160 MPa | ASTM D953 |
| Pin bearing strength, transverse | 124 MPa | ASTM D953 |

Values apply unless a project certificate states otherwise. Density and transverse modulus are not published; use the mass per metre in `profiles.csv`.

The online beam calculator states slightly different reference moduli (E = 23.0 GPa, G = 3.0 GPa). The published span tables are reproduced by E = 20.7 GPa, G = 3.1 GPa and shear area 0.6 A (see `data-notes.md`), so use those for preliminary work.

## 2. Design format, factors and load combinations

Design code named: ANSI/ACMA LRFD pre-standard for pultruded FRP; actions to AS/NZS 1170 for Australian projects.

- Design strength: `Ru <= lambda * phi * Rn`, with `Rn = Ro * C1 * C2 ...`
- The published `M_allow_kNm` and `V_allow_kN` are allowable (service-level) actions built on a short-term safety factor of 3, which High-Mat expresses as a conservative `lambda * phi = 1/3`. Compare them with unfactored service actions. Individual phi values by failure mode are not published.

Time effect factor lambda (for LRFD use):

| Combination | lambda |
|---|---|
| 1.4D | 0.4 |
| 1.2D + 1.6L + 0.5(Lr or S or R) | 0.8 occupancy live, 0.6 storage live, 1.0 impact |
| 1.2D + 1.6(Lr or S or R) + (L or 0.5W) | 0.75 |
| 1.2D + 1.0W + L + 0.5(Lr or S or R) | 1.0 |
| 1.2D + 1.0E + L + 0.2S | 1.0 |
| 0.9D + 1.0W, 0.9D + 1.0E | 1.0 |
| Flood, atmospheric ice | 0.75 |

Serviceability combinations: short-term `D + (L or 0.5S)` and `D + 0.5L + 0.4W`; long-term `D + 0.5L`.

End-use adjustment factors (apply to reference strength or modulus):

| Property | Resin | Moisture CM (sustained wet) | Temperature CT for 32 < T <= 60 degC |
|---|---|---|---|
| Strength | Vinyl ester | 0.85 | 1.444 - 0.0144 T |
| Strength | Polyester | 0.80 | 1.308 - 0.0108 T |
| Modulus | Vinyl ester | 0.95 | 1.58 - 0.018 T |
| Modulus | Polyester | 0.90 | 1.444 - 0.0144 T |

CT = 1.0 at or below 32 degC. Above 60 degC CT must come from testing. T in degC.

## 3. Beam check method (simply supported, strong axis)

For UDL `w` (kN/m, including self-weight `m * 9.80665 / 1000`) and midspan point load `P` (kN) on span `L`:

- `M = w L^2 / 8 + P L / 4`, check `M <= M_allow * CM_s * CT_s`
- `V = w L / 2 + P / 2`, check `V <= V_allow * CM_s * CT_s`
- Bending deflection `5 w L^4 / (384 E I) + P L^3 / (48 E I)`
- Shear deflection `w L^2 / (8 G As) + P L / (4 G As)` with `As = 0.6 A`
- `E = 20.7 GPa * CM_e * CT_e`, `G = 3.1 GPa * CM_e * CT_e`

Not covered by published data and still required: lateral-torsional buckling of open sections, local flange and web buckling, web crippling at supports and point loads, connection bearing and net section, and torsion in channels and angles loaded off the shear centre.

## 4. Deflection limits and creep

High-Mat states no mandatory limit; confirm with the client. Suggested values it quotes from AS/NZS 1170.0 Table C1:

| Case | Limit |
|---|---|
| Roof member, visible sag | L/300 |
| Roof supporting brittle cladding | L/400 |
| Floor joist or beam, ripple or sag | L/300 |
| Normal floor, noticeable sag | L/400 |
| Floor supporting masonry walls | L/500 |
| Floor for operator or maintenance access (1 kN point) | L/250 |
| Lintel | L/240 and under 12 mm |

Long-term deflection under sustained load: `delta_total = delta_instant * Kcr(t)`, `Kcr(t) = 1 + t^(1/4) / 6`, t in years (ACMA Eq. 2.6-2). Example: 25 years gives 1.37.

## 5. Columns

`profile_column_tables.csv` gives allowable axial compression against effective length (1.5 to 7.5 m). Values that stay constant over short lengths indicate a local-buckling or crushing cap. The basis (end fixity, safety factor) is not stated beyond the general factor of 3; treat as pin-ended and confirm.

## 6. Grating

`grating_span_tables.csv` gives the maximum clear span for:

- Uniform load 2.5, 3, 4, 5 kPa
- Line load across the span 1.1, 2.7, 3.6, 4.5 kN/m

each at three criteria: L/300, L/200, and 5 mm absolute deflection.

Stated assumptions: isophthalic polyester with glass reinforcement (vinyl ester needs confirmation of equivalent properties); normal temperature; simply supported clear span; load perpendicular to the surface; no creep or load-duration reduction; displacement-based only, not a strength or safety-factor check. High-Mat says not to interpolate without an approved engineering method, and not to convert a line load to an area load.

Pultruded grating (PGI, PGT, HDPG) spans one way: bearing bars must run across the supports. Moulded grating (MG) carries load in both directions.

Code structure: thickness x mesh x mesh in mm (moulded); thickness x bar dimension x pitch (pultruded). Solid-top codes end in (3) or (5) for the top-plate thickness in mm.

## 7. Stair treads (38 mm thick moulded, with nosing)

All three: maximum recommended span 900 mm, tread width 995 mm, tread support 50 x 6.4 mm.

| | Mini mesh | Square mesh | Micro mesh |
|---|---|---|---|
| Aperture | 12 x 12 mm | 31 x 31 mm | 8 x 8 mm |
| Open area | 42% | 68% | 30% |
| Going | 287 mm | 272 mm | 287 mm |
| Deflection at 2.5 kPa, 900 span | 1.45 mm | 1.71 mm | 1.40 mm |
| Deflection at 4.0 kPa | 2.40 mm | 2.58 mm | 2.36 mm |
| Deflection at 200 kg point | 2.42 mm | 2.60 mm | 2.28 mm |
| Deflection at 400 kg point | 4.84 mm | 6.18 mm | 4.80 mm |

Selection: micro mesh for public or frequent pedestrian use and drop-through control; mini mesh for general industrial access; square mesh where drainage and debris shedding come first. Standards named as relevant: AS 1657, AS 1428.1, AS 4586.

## 8. Handrails and kickplates

Modular system in circular or square rail, with an omega top-rail option, fittings, kickplate and pre-made stanchion assemblies; edge-mounted or top-mounted stanchions. Typical geometry from the High-Mat detail, aligned with AS 1657:2018:

| Item | Value |
|---|---|
| Stanchion spacing | 1500 mm maximum, centre to centre |
| Handrail height | 900 to 1100 mm above walking surface |
| Rail spacing | 450 mm maximum between rails |
| End projection | 250 mm maximum unsupported |
| Toe-board gap | 10 mm maximum |

Member sizes and load ratings are project-specific and not published.

## 9. Ladders

Fixed FRP ladders with wall-mounted, floor-mounted, walk-through and caged arrangements, splice kits and extendable rails. Published references: side rails 51 x 51 x 4 mm pultruded; rungs 31.75 mm fluted FRP; rung spacing 250 to 300 mm. Hoop spacing, bracket spacing and anchors are project-verified (AS 1657 where specified).

## 10. FRP fasteners (bolts, hex nuts, round and square washers, threaded rod)

| Property | Reference value |
|---|---|
| Density | 2.2 to 2.35 g/cm3 |
| Water absorption, 24 h | 0.05% max |
| Longitudinal tensile strength | 1200 MPa min |
| Shear strength | 260 MPa min |
| Interlaminar shear strength | 50 MPa min |
| Flexural strength | 960 MPa min (350 MPa min at 150 degC) |
| Torsion strength | 800 MPa |

| Size | Nut across flats | Nut height (D / 2D) | Nut across corners | Round washer OD x hole x t | Square washer width x hole x t |
|---|---|---|---|---|---|
| M12 | 19 | 12 / 24 | 21.9 | 27 x 14 x 2.5 | 30 x 13 x 4 |
| M16 | 24 | 16 / 32 | 27.7 | 32 x 18 x 3 | 50 x 17 x 5 |
| M20 | 30 | 20 / 40 | 34.6 | 40 x 22 x 3 | 50 x 21 x 5 |

Dimensions in mm. These are rod-material properties, not joint capacities. Do not apply steel torque values or replace steel bolts one-for-one; check bearing, creep, temperature and thread engagement for the joint.

## 11. Resin selection

Two systems for profiles and moulded grating:

- **Vinyl ester**: harshest chemical service, better alkali and acid resistance; petrochemical, wastewater, mining, plating; direct and frequent chemical contact.
- **Isophthalic polyester**: general purpose, splash and spill exposure; the economical default.

Maximum service temperature in common chemicals (degC), from the High-Mat chemical resistance guide. N/R means not recommended.

| Chemical | Vinyl ester: conc %, max degC | Iso polyester: conc %, max degC |
|---|---|---|
| Acetic acid | 50, 82 | 50, 52 |
| Ammonium hydroxide | 28, 38 | N/R |
| Chlorine water | saturated, 93 | saturated, 27 |
| Chromic acid | 10, 65 | 5, 21 |
| Ethanol | 50, 38 | 50, 24 |
| Gasoline | 100, 82 | 100, 27 |
| Hydrochloric acid | 37, 65 | 37, 24 |
| Hydrogen peroxide | 30, 65 | 5, 38 |
| Nitric acid | 20, 49 | 20, 21 |
| Phosphoric acid | 100, 99 | 100, 49 |
| Sodium hydroxide | 25, 82 | N/R |
| Sulfuric acid | 75, 38 | 25, 24 |
| Water, distilled | 100, 82 | 100, 77 |
| Most chloride, nitrate and sulfate salts | all, 99 | all, 60 to 82 |
| Benzene | N/R | N/R |

The full table (about 60 chemicals) is at https://high-mat.com.au/composite-resin-systems/. It is a reference only; confirm for the actual duty.
