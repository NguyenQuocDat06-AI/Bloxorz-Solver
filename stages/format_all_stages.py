import os
import sys
import json
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

STAGES_DIR = os.path.dirname(os.path.abspath(__file__))

def format_stage(data: dict) -> str:
    """Format stage dict thành JSON trực quan với grid là ma trận 2D trên từng dòng."""
    lines = ["{"]
    lines.append(f'  "name": {json.dumps(data["name"], ensure_ascii=False)},')
    lines.append(f'  "difficulty": {json.dumps(data.get("difficulty", "Medium"), ensure_ascii=False)},')
    lines.append(f'  "start": [{data["start"][0]}, {data["start"][1]}],')
    lines.append(f'  "goal": [{data["goal"][0]}, {data["goal"][1]}],')
    
    # Grid: Ma trận 2D thể hiện trực quan từng hàng
    lines.append('  "grid": [')
    grid = data["grid"]
    for i, row in enumerate(grid):
        row_str = "    [" + ", ".join(str(val) for val in row) + "]"
        if i < len(grid) - 1:
            row_str += ","
        lines.append(row_str)
    
    has_bridges = "bridges" in data and bool(data["bridges"])
    has_switches = "switches" in data and bool(data["switches"])
    
    if has_bridges or has_switches:
        lines.append("  ],")
    else:
        lines.append("  ]")
        lines.append("}")
        return "\n".join(lines) + "\n"

    if has_bridges:
        lines.append('  "bridges": {')
        b_items = list(data["bridges"].items())
        for b_idx, (b_id, b_info) in enumerate(b_items):
            cells_str = ", ".join(f"[{c[0]}, {c[1]}]" for c in b_info["cells"])
            init_open = "true" if b_info.get("initial_open", False) else "false"
            lines.append(f'    "{b_id}": {{')
            lines.append(f'      "cells": [{cells_str}],')
            lines.append(f'      "initial_open": {init_open}')
            comma = "," if b_idx < len(b_items) - 1 else ""
            lines.append(f'    }}{comma}')
        if has_switches:
            lines.append("  },")
        else:
            lines.append("  }")

    if has_switches:
        lines.append('  "switches": [')
        sw_list = data["switches"]
        for sw_idx, sw in enumerate(sw_list):
            lines.append("    {")
            lines.append(f'      "pos": [{sw["pos"][0]}, {sw["pos"][1]}],')
            lines.append(f'      "type": "{sw["type"]}",')
            lines.append(f'      "behavior": "{sw.get("behavior", "toggle")}",')
            linked_str = json.dumps(sw.get("linked_bridges", []))
            lines.append(f'      "linked_bridges": {linked_str}')
            if "split_targets" in sw:
                st = sw["split_targets"]
                lines[-1] += ","
                lines.append(f'      "split_targets": [[{st[0][0]}, {st[0][1]}], [{st[1][0]}, {st[1][1]}]]')
            comma = "," if sw_idx < len(sw_list) - 1 else ""
            lines.append(f'    }}{comma}')
        lines.append("  ]")

    lines.append("}")
    return "\n".join(lines) + "\n"

def run():
    count = 0
    for f in sorted(os.listdir(STAGES_DIR)):
        if f.startswith("stage_") and f.endswith(".json"):
            fpath = os.path.join(STAGES_DIR, f)
            with open(fpath, "r", encoding="utf-8") as file:
                data = json.load(file)
            formatted = format_stage(data)
            with open(fpath, "w", encoding="utf-8") as file:
                file.write(formatted)
            count += 1
            print(f"✓ Đã định dạng lại ma trận trực quan: {f}")
    print(f"\n Hoàn tất định dạng {count} file stages JSON!")

if __name__ == "__main__":
    run()
