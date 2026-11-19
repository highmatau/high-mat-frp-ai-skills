#!/usr/bin/env python3
"""High-Mat FRP lookup and preliminary checks. Python 3 standard library only.

  hm_frp.py profile "IB 76x152x9.5"            section data, capacities, STEP link, published tables
  hm_frp.py beam-check CODE --span 3 --udl 2.5 [--point 1] [--limit 250] [--resin ve|pe] [--wet] [--temp 40] [--years 25]
  hm_frp.py find-beam --span 3 --udl 2.5 [--point 0] [--limit 250] [--family "I-Beam"] [...same conditions]
  hm_frp.py column CODE --length 3
  hm_frp.py grating --udl 5 | --line 2.7  --span 900 [--criterion L/300|L/200|5mm] [--type MG-S]
  hm_frp.py grating-info "MG-S 38X38X38"

Units: span and length m (grating span mm), udl kN/m (grating kPa), point kN at midspan, temp degC.
Loads are unfactored service loads, compared with High-Mat allowable actions. Self-weight is added.
Preliminary only: stability, local buckling, connections and bearing are not checked.
"""
import argparse, csv, os, sys

_H = os.path.dirname(os.path.abspath(__file__))
D = next((d for d in (os.path.join(_H, "..", "data"), _H, os.getcwd(), "/mnt/data")
          if os.path.exists(os.path.join(d, "profiles.csv"))), _H)   # skill layout, or flat upload (ChatGPT)
E_REF, G_REF, SHEAR_AREA = 20700.0, 3100.0, 0.6   # MPa, MPa, fraction of A (reproduces published tables)
LIMITS = [100, 150, 200, 250, 300, 350, 400, 600]


def rows(name):
    with open(os.path.join(D, name), newline="") as f:
        return list(csv.DictReader(f))


def num(x):
    return float(x) if x not in ("", None) else None


def norm(s):
    return s.upper().replace("HM", "").replace(" ", "").replace("-", "")


def find(items, query, what):
    q = norm(query)
    exact = [r for r in items if norm(r["code"]) == q]
    hits = exact or [r for r in items if q in norm(r["code"])]
    if not hits:
        sys.exit(f"No {what} matches '{query}'.")
    if len(hits) > 1:
        sys.exit(f"'{query}' matches several {what}s: " + "; ".join(r["code"] for r in hits))
    return hits[0]


def factors(resin, wet, temp):
    """(strength factor, modulus factor) from the High-Mat design guide."""
    ve = resin == "ve"
    cms, cme = ((0.85, 0.95) if ve else (0.80, 0.90)) if wet else (1.0, 1.0)
    if temp > 60:
        sys.exit("Above 60 degC the temperature factor must come from testing.")
    if temp > 32:
        cts = (1.444 - 0.0144 * temp) if ve else (1.308 - 0.0108 * temp)
        cte = (1.58 - 0.018 * temp) if ve else (1.444 - 0.0144 * temp)
    else:
        cts = cte = 1.0
    return cms * min(cts, 1.0), cme * min(cte, 1.0)


def beam(p, span, udl, point, resin, wet, temp, years):
    I, A, m = num(p["I_major_mm4"]), num(p["area_mm2"]), num(p["mass_kg_m"])
    Ma, Va = num(p["M_allow_kNm"]), num(p["V_allow_kN"])
    if None in (I, A, m, Ma, Va):
        return None
    fs, fe = factors(resin, wet, temp)
    w = udl + m * 9.80665 / 1000.0            # kN/m = N/mm
    L = span * 1000.0
    E, G, As = E_REF * fe, G_REF * fe, SHEAR_AREA * A
    P = point * 1000.0
    M = w * span ** 2 / 8 + point * span / 4
    V = w * span / 2 + point / 2
    db = 5 * w * L ** 4 / (384 * E * I) + P * L ** 3 / (48 * E * I)
    ds = w * L ** 2 / (8 * G * As) + P * L / (4 * G * As)
    kcr = 1 + years ** 0.25 / 6 if years else 1.0
    return dict(M=M, V=V, Ma=Ma * fs, Va=Va * fs, d_bend=db, d_shear=ds, d=(db + ds), d_long=(db + ds) * kcr,
                kcr=kcr, selfw=w - udl, fs=fs, fe=fe)


def report_beam(p, r, span, limit):
    lim = span * 1000 / limit
    ok_m, ok_v, ok_d = r["M"] <= r["Ma"], r["V"] <= r["Va"], r["d"] <= lim
    print(f"{p['code']}  ({p['family']}, {p['mass_kg_m']} kg/m)   simply supported span {span} m")
    print(f"  factors: strength x{r['fs']:.3f}, modulus x{r['fe']:.3f}; self-weight {r['selfw']:.3f} kN/m included")
    print(f"  Moment   {r['M']:.2f} kNm  vs allowable {r['Ma']:.2f}  -> {'OK' if ok_m else 'FAIL'}  ({r['M']/r['Ma']*100:.0f}%)")
    print(f"  Shear    {r['V']:.2f} kN   vs allowable {r['Va']:.2f}  -> {'OK' if ok_v else 'FAIL'}  ({r['V']/r['Va']*100:.0f}%)")
    print(f"  Deflection {r['d']:.1f} mm (bending {r['d_bend']:.1f} + shear {r['d_shear']:.1f}) = L/{span*1000/r['d']:.0f}"
          f"  vs L/{limit} = {lim:.1f} mm -> {'OK' if ok_d else 'FAIL'}")
    if r["kcr"] > 1:
        print(f"  If the whole load is sustained: x{r['kcr']:.2f} creep -> {r['d_long']:.1f} mm = L/{span*1000/r['d_long']:.0f}")
    if p["data_flag"]:
        print(f"  DATA FLAG: {p['data_flag']}")
    print("  Not checked: lateral-torsional and local buckling, web crippling, connections, bearing.")
    return ok_m and ok_v and ok_d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    def cond(s):
        s.add_argument("--span", type=float, required=True); s.add_argument("--udl", type=float, default=0.0)
        s.add_argument("--point", type=float, default=0.0); s.add_argument("--limit", type=float, default=250)
        s.add_argument("--resin", choices=["ve", "pe"], default="pe"); s.add_argument("--wet", action="store_true")
        s.add_argument("--temp", type=float, default=23.0); s.add_argument("--years", type=float, default=0.0)
    s = sub.add_parser("profile"); s.add_argument("code")
    s = sub.add_parser("beam-check"); s.add_argument("code"); cond(s)
    s = sub.add_parser("find-beam"); cond(s); s.add_argument("--family", default="")
    s = sub.add_parser("column"); s.add_argument("code"); s.add_argument("--length", type=float, required=True)
    s = sub.add_parser("grating"); s.add_argument("--udl", type=float); s.add_argument("--line", type=float)
    s.add_argument("--span", type=float, required=True); s.add_argument("--criterion", default="L/300"); s.add_argument("--type", default="")
    s = sub.add_parser("grating-info"); s.add_argument("code")
    a = ap.parse_args()

    if a.cmd == "profile":
        p = find(rows("profiles.csv"), a.code, "profile")
        for k, v in p.items():
            if v != "":
                print(f"{k:18} {v}")
        bt = [r for r in rows("profile_beam_tables.csv") if r["code"] == p["code"]]
        if bt:
            print("\nPublished UDL (kN/m) at deflection limit - deflection only, check M and V separately")
            print("span_m  " + "  ".join(f"L/{x:<5}" for x in LIMITS))
            for r in bt:
                print(f"{r['span_m']:<7} " + "  ".join(f"{r[f'w_kN_m_at_L/{x}'] or '-':<7}" for x in LIMITS))
        ct = [r for r in rows("profile_column_tables.csv") if r["code"] == p["code"]]
        if ct:
            print("\nAllowable compression: " + ", ".join(f"{r['length_m']} m: {r['compression_allow_kN']} kN" for r in ct))

    elif a.cmd == "beam-check":
        p = find(rows("profiles.csv"), a.code, "profile")
        r = beam(p, a.span, a.udl, a.point, a.resin, a.wet, a.temp, a.years)
        if r is None:
            sys.exit(f"{p['code']}: section properties or capacities are not published.")
        sys.exit(0 if report_beam(p, r, a.span, a.limit) else 1)

    elif a.cmd == "find-beam":
        out = []
        for p in rows("profiles.csv"):
            if a.family and a.family.lower() not in (p["family"] + " " + p["type"]).lower():
                continue
            r = beam(p, a.span, a.udl, a.point, a.resin, a.wet, a.temp, a.years)
            if r and r["M"] <= r["Ma"] and r["V"] <= r["Va"] and r["d"] <= a.span * 1000 / a.limit:
                out.append((float(p["mass_kg_m"]), p, r))
        if not out:
            sys.exit("No published profile passes moment, shear and deflection for these inputs.")
        print(f"Lightest profiles passing M, V and L/{a.limit:g} at {a.span} m (UDL {a.udl} kN/m, point {a.point} kN):")
        for m, p, r in sorted(out, key=lambda t: t[0])[:10]:
            print(f"  {p['code']:26} {m:5.1f} kg/m  M {r['M']/r['Ma']*100:3.0f}%  V {r['V']/r['Va']*100:3.0f}%  defl L/{a.span*1000/r['d']:.0f}"
                  + ("   [DATA FLAG]" if p["data_flag"] else ""))

    elif a.cmd == "column":
        p = find(rows("profiles.csv"), a.code, "profile")
        ct = [(float(r["length_m"]), float(r["compression_allow_kN"])) for r in rows("profile_column_tables.csv") if r["code"] == p["code"]]
        if not ct:
            sys.exit(f"{p['code']}: no column table published.")
        longer = [c for c in ct if c[0] >= a.length]
        if not longer:
            sys.exit(f"{p['code']}: table ends at {ct[-1][0]} m ({ct[-1][1]} kN); {a.length} m is outside the published range.")
        L, P = longer[0]
        print(f"{p['code']}: allowable compression {P} kN at {L} m (next tabulated length at or above {a.length} m; not interpolated)")
        if p["data_flag"]:
            print(f"DATA FLAG: {p['data_flag']}")

    elif a.cmd == "grating":
        if (a.udl is None) == (a.line is None):
            sys.exit("Give exactly one of --udl (kPa) or --line (kN/m).")
        kind, load = ("UDL", a.udl) if a.udl is not None else ("LINE", a.line)
        col = {"L/300": "max_span_mm_L/300", "L/200": "max_span_mm_L/200", "5MM": "max_span_mm_5mm"}.get(a.criterion.upper())
        if not col:
            sys.exit("criterion must be L/300, L/200 or 5mm")
        sp = [r for r in rows("grating_span_tables.csv") if r["load_type"] == kind]
        levels = sorted({float(r["load"]) for r in sp})
        use = [x for x in levels if x >= load]
        if not use:
            sys.exit(f"Load {load} exceeds the highest tabulated value ({levels[-1]}).")
        g = {r["code"]: r for r in rows("gratings.csv")}
        out = [(float(g[r["code"]]["mass_kg_m2"]), r["code"], int(r[col])) for r in sp
               if float(r["load"]) == use[0] and int(r[col]) >= a.span and (not a.type or a.type.upper() in r["code"].upper())]
        if not out:
            sys.exit("No tabulated grating reaches that span.")
        print(f"Gratings spanning >= {a.span:g} mm at {use[0]:g} {'kPa' if kind=='UDL' else 'kN/m'} (tabulated level at or above {load:g}), {a.criterion}; lightest first:")
        for m, c, s_ in sorted(out)[:12]:
            print(f"  {c:26} {m:6.2f} kg/m2  max span {s_} mm  open {g[c]['open_area_pct']}%  {g[c]['family']}")
        print("Deflection-based, isophthalic polyester, simply supported; strength and fixings need separate checks.")

    elif a.cmd == "grating-info":
        g = find(rows("gratings.csv"), a.code, "grating")
        for k, v in g.items():
            print(f"{k:16} {v}")
        print("load        L/300  L/200  5mm   (max clear span, mm)")
        for r in rows("grating_span_tables.csv"):
            if r["code"] == g["code"]:
                print(f"{r['load']:>4} {r['unit']:5}  {r['max_span_mm_L/300']:>5}  {r['max_span_mm_L/200']:>5}  {r['max_span_mm_5mm']:>5}")


if __name__ == "__main__":
    main()
