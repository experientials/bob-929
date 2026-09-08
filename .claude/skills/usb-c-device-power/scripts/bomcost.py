#!/usr/bin/env python3
"""Roll up a USB/data/power BOM CSV: per-block and total cost, part/line counts,
DNP handling, and a JLCPCB Extended-part-fee flag.

Usage:
  python3 bomcost.py <bom.csv> [--include-dnp]

Expects the column header from bom-generation.md:
  RefDes,Qty,Block,Function,Value,MPN,Manufacturer,Package,LCSC,BasicExt,UnitUSD,ExtUSD,AltMPN,DNP,Notes

ExtUSD is trusted if present; otherwise it's computed as Qty*UnitUSD.
"""
import csv, sys
from collections import defaultdict

def num(x, d=0.0):
    try:
        return float(str(x).strip())
    except (ValueError, TypeError):
        return d

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    include_dnp = "--include-dnp" in sys.argv
    if not args:
        print(__doc__); sys.exit(1)
    path = args[0]

    rows = list(csv.DictReader(open(path, newline="")))
    blocks = defaultdict(lambda: {"lines": 0, "qty": 0, "cost": 0.0})
    total_cost = total_qty = total_lines = 0
    dnp_cost = dnp_lines = 0
    extended = []      # (RefDes, MPN) of Extended parts (feeder fee)
    single_source = [] # active parts with no AltMPN

    for r in rows:
        dnp = str(r.get("DNP", "")).strip().upper() in ("Y", "YES", "1", "TRUE")
        if dnp and not include_dnp:
            qty = int(num(r.get("Qty"), 0))
            ext = num(r.get("ExtUSD")) or qty * num(r.get("UnitUSD"))
            dnp_cost += ext; dnp_lines += 1
            continue
        qty = int(num(r.get("Qty"), 0))
        ext = num(r.get("ExtUSD")) or qty * num(r.get("UnitUSD"))
        blk = (r.get("Block") or "?").strip()
        b = blocks[blk]
        b["lines"] += 1; b["qty"] += qty; b["cost"] += ext
        total_cost += ext; total_qty += qty; total_lines += 1

        if str(r.get("BasicExt", "")).strip().lower().startswith("ext"):
            extended.append((r.get("RefDes", "?"), r.get("MPN", "")))
        mpn = (r.get("MPN") or "").strip()
        alt = (r.get("AltMPN") or "").strip()
        # flag active parts (have an MPN and a U-prefix refdes) with no 2nd source
        if mpn and str(r.get("RefDes", "")).strip().upper().startswith("U") and not alt:
            single_source.append((r.get("RefDes", "?"), mpn))

    w = max((len(b) for b in blocks), default=10)
    print(f"\n{'BLOCK':<{w}}  {'LINES':>5}  {'QTY':>4}  {'EXT USD':>9}")
    print("-" * (w + 24))
    for blk in sorted(blocks, key=lambda k: -blocks[k]["cost"]):
        b = blocks[blk]
        print(f"{blk:<{w}}  {b['lines']:>5}  {b['qty']:>4}  {b['cost']:>9.3f}")
    print("-" * (w + 24))
    print(f"{'TOTAL (populated)':<{w}}  {total_lines:>5}  {total_qty:>4}  {total_cost:>9.3f}")
    if dnp_lines:
        print(f"{'(excluded DNP)':<{w}}  {dnp_lines:>5}  {'':>4}  {dnp_cost:>9.3f}   "
              f"[+{dnp_cost:.2f} on the DNP variant build]")

    print(f"\nUnique populated lines: {total_lines} | total placements: {total_qty} | "
          f"BOM cost/board: ${total_cost:.2f}")
    if extended:
        print(f"\nExtended parts ({len(extended)}) — each adds a JLCPCB feeder fee; "
              f"prefer Basic where possible:")
        for rd, mpn in extended:
            print(f"  - {rd}: {mpn}")
    if single_source:
        print(f"\nSingle-source ICs (no AltMPN) — supply risk, add a 2nd source:")
        for rd, mpn in single_source:
            print(f"  - {rd}: {mpn}")
    print()

if __name__ == "__main__":
    main()
