import json
import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import deque
from core.board import Board, TileType, SwitchBehavior, Switch, Bridge
from core.problem import BloxorzProblem, Action

def solve_with_bfs(problem: BloxorzProblem):
    start = problem.get_initial_state()
    if problem.is_goal(start):
        return []
    
    queue = deque([(start, [])])
    visited = {start}
    
    while queue:
        state, path = queue.popleft()
        if problem.is_goal(state):
            return path
        
        for action in problem.get_actions(state):
            nxt = problem.get_successor(state, action)
            if nxt is not None and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [action.value]))
    return None

def main():
    stages_data = []

    # Màn 1–5: cơ bản.

    # Màn 01.
    stages_data.append({
        "filename": "stage_01.json",
        "name": "Stage 01 - The Beginning",
        "difficulty": "Easy",
        "start": [1, 1],
        "goal": [4, 7],
        "grid": [
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
        ]
    })

    # Màn 02.
    stages_data.append({
        "filename": "stage_02.json",
        "name": "Stage 02 - S-Curve",
        "difficulty": "Easy",
        "start": [1, 1],
        "goal": [7, 7],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 9, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1]
        ]
    })

    # Màn 03.
    stages_data.append({
        "filename": "stage_03.json",
        "name": "Stage 03 - Narrow Spiral",
        "difficulty": "Easy-Medium",
        "start": [1, 1],
        "goal": [4, 4],
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 0, 1, 9, 0, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
    })

    # Màn 04.
    stages_data.append({
        "filename": "stage_04.json",
        "name": "Stage 04 - Stepping Stones",
        "difficulty": "Medium",
        "start": [1, 1],
        "goal": [7, 8],
        "grid": [
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 9, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        ]
    })

    # Màn 05.
    stages_data.append({
        "filename": "stage_05.json",
        "name": "Stage 05 - The Labyrinth Island",
        "difficulty": "Medium",
        "start": [1, 1],
        "goal": [5, 6],
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 9, 1],
            [0, 0, 1, 1, 1, 1, 1, 1]
        ]
    })

    # Màn 6–9: ô yếu.

    # Màn 06.
    stages_data.append({
        "filename": "stage_06.json",
        "name": "Stage 06 - Fragile Runway",
        "difficulty": "Medium",
        "start": [1, 1],
        "goal": [1, 9],
        "grid": [
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 2, 2, 2, 2, 2, 1, 9, 1],
            [1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]
        ]
    })

    # Màn 07.
    stages_data.append({
        "filename": "stage_07.json",
        "name": "Stage 07 - Checkerboard Fragile",
        "difficulty": "Medium-Hard",
        "start": [1, 1],
        "goal": [4, 7],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 2, 1, 0],
            [1, 1, 1, 1, 1, 2, 1, 2, 1],
            [0, 0, 1, 1, 2, 1, 2, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 9, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1]
        ]
    })

    # Màn 08.
    stages_data.append({
        "filename": "stage_08.json",
        "name": "Stage 08 - The Thin Bridge",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [3, 8],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 2, 2, 0, 0, 0, 0],
            [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 9, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        ]
    })

    # Màn 09.
    stages_data.append({
        "filename": "stage_09.json",
        "name": "Stage 09 - Fragile Matrix",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [5, 5],
        "grid": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 2, 1, 1],
            [1, 2, 2, 1, 2, 2, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 2, 2, 1, 2, 2, 1],
            [1, 1, 1, 1, 1, 9, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
    })

    # Màn 10–15: cầu và công tắc.

    # Màn 10.
    stages_data.append({
        "filename": "stage_10.json",
        "name": "Stage 10 - First Bridge",
        "difficulty": "Medium",
        "start": [1, 1],
        "goal": [1, 7],
        "grid": [
            [1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 3, 3, 3, 1, 9, 1],
            [1, 4, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0]
        ],
        "bridges": {
            "b1": {
                "cells": [[1, 3], [1, 4], [1, 5]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 1],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 11.
    stages_data.append({
        "filename": "stage_11.json",
        "name": "Stage 11 - Heavy Switch Trial",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [5, 8],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 5, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 3, 3, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 9, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        ],
        "bridges": {
            "b1": {
                "cells": [[3, 4], [3, 5]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 1],
                "type": "HEAVY_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 12.
    stages_data.append({
        "filename": "stage_12.json",
        "name": "Stage 12 - Dual Bridge Causeway",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [1, 13],
        "grid": [
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 9, 1, 1],
            [1, 4, 1, 1, 0, 0, 1, 1, 4, 1, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
        ],
        "bridges": {
            "b1": {
                "cells": [[1, 4], [1, 5]],
                "initial_open": False
            },
            "b2": {
                "cells": [[1, 10], [1, 11]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 1],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            },
            {
                "pos": [2, 8],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b2"]
            }
        ]
    })

    # Màn 13.
    stages_data.append({
        "filename": "stage_13.json",
        "name": "Stage 13 - Toggle Bypass",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [6, 7],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 4, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 3, 3, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 9]
        ],
        "bridges": {
            "b1": {
                "cells": [[3, 4], [3, 5]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 2],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 14.
    stages_data.append({
        "filename": "stage_14.json",
        "name": "Stage 14 - Permanent Gate",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [4, 7],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 5, 1, 1, 3, 3, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 9, 1]
        ],
        "bridges": {
            "b1": {
                "cells": [[2, 4], [2, 5]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 1],
                "type": "HEAVY_SWITCH",
                "behavior": "perm_open",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 15.
    stages_data.append({
        "filename": "stage_15.json",
        "name": "Stage 15 - The Island Outpost",
        "difficulty": "Hard",
        "start": [1, 1],
        "goal": [6, 1],
        "grid": [
            [1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 5, 1],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 3, 3, 3, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0],
            [1, 9, 1, 0, 0, 0, 0, 0]
        ],
        "bridges": {
            "b1": {
                "cells": [[3, 2], [3, 3], [3, 4]],
                "initial_open": True
            }
        },
        "switches": [
            {
                "pos": [1, 6],
                "type": "HEAVY_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 16–20: phối hợp cơ chế và tách khối.

    # Màn 16.
    stages_data.append({
        "filename": "stage_16.json",
        "name": "Stage 16 - Fragile Pass with Bridge",
        "difficulty": "Hard-Expert",
        "start": [1, 1],
        "goal": [1, 8],
        "grid": [
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 2, 2, 3, 3, 1, 9, 1],
            [1, 4, 1, 2, 2, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        ],
        "bridges": {
            "b1": {
                "cells": [[1, 5], [1, 6]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 1],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 17.
    stages_data.append({
        "filename": "stage_17.json",
        "name": "Stage 17 - The Perilous Peak",
        "difficulty": "Hard-Expert",
        "start": [1, 1],
        "goal": [3, 8],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 2, 2, 1, 1, 0, 0, 0],
            [0, 1, 2, 2, 5, 1, 3, 3, 9],
            [0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1]
        ],
        "bridges": {
            "b1": {
                "cells": [[3, 6], [3, 7]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [3, 4],
                "type": "HEAVY_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 18.
    stages_data.append({
        "filename": "stage_18.json",
        "name": "Stage 18 - Teleport Split Trial",
        "difficulty": "Expert",
        "start": [1, 1],
        "goal": [5, 8],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 6, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 4, 3, 1, 9, 1],
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 1]
        ],
        "bridges": {
            "b1": {
                "cells": [[5, 6]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 2],
                "type": "SPLIT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": [],
                "split_targets": [[4, 4], [4, 7]]
            },
            {
                "pos": [5, 5],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 19.
    stages_data.append({
        "filename": "stage_19.json",
        "name": "Stage 19 - The Citadel Maze",
        "difficulty": "Expert",
        "start": [1, 1],
        "goal": [6, 9],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 5, 1, 3, 3, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1],
            [0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 1]
        ],
        "bridges": {
            "b1": {
                "cells": [[2, 4], [2, 5]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 2],
                "type": "HEAVY_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            }
        ]
    })

    # Màn 20.
    stages_data.append({
        "filename": "stage_20.json",
        "name": "Stage 20 - Grandmaster Void",
        "difficulty": "Master",
        "start": [1, 1],
        "goal": [5, 11],
        "grid": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 4, 1, 3, 3, 1, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9]
        ],
        "bridges": {
            "b1": {
                "cells": [[2, 4], [2, 5]],
                "initial_open": False
            },
            "b2": {
                "cells": [[3, 10], [4, 10]],
                "initial_open": False
            }
        },
        "switches": [
            {
                "pos": [2, 2],
                "type": "SOFT_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b1"]
            },
            {
                "pos": [2, 7],
                "type": "HEAVY_SWITCH",
                "behavior": "toggle",
                "linked_bridges": ["b2"]
            }
        ]
    })

    print(f"Bắt đầu kiểm thử tính hợp lệ và tìm đường giải cho {len(stages_data)} màn chơi...")
    out_dir = "stages"
    os.makedirs(out_dir, exist_ok=True)

    verified_count = 0
    for s in stages_data:
        filepath = os.path.join(out_dir, s["filename"])
        save_obj = {
            "name": s["name"],
            "difficulty": s["difficulty"],
            "start": s["start"],
            "goal": s["goal"],
            "grid": s["grid"]
        }
        if "bridges" in s:
            save_obj["bridges"] = s["bridges"]
        if "switches" in s:
            save_obj["switches"] = s["switches"]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_obj, f, indent=2)

        board = Board.from_json(filepath)
        problem = BloxorzProblem(board)
        sol = solve_with_bfs(problem)

        if sol is not None:
            print(f"✅ {s['filename']:<14} | {s['name']:<32} | {s['difficulty']:<12} | Steps: {len(sol)}")
            verified_count += 1
        else:
            print(f"❌ {s['filename']:<14} | {s['name']:<32} | KHÔNG TÌM THẤY LỜI GIẢI!")

    print(f"\n=======================================================")
    print(f"🎉 TỔNG KẾT: {verified_count}/{len(stages_data)} MÀN CHƠI ĐÃ ĐƯỢC XÁC THỰC 100% CÓ LỜI GIẢI!")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
