# SLE-2: Profiling Report — BFS vs DFS on the 8-Puzzle

**Course:** 02AML204 – Introduction to Artificial Intelligence
**Repo:** IAI-SLE-25UAM072 (continuation of SLE-1)

## What this is
SLE-2 measures the real performance of two search algorithms on the same problem and justifies which is better using data, as required by the SLE-2 guideline.

- **Algorithm A:** Breadth-First Search (BFS) — uninformed
- **Algorithm B:** Depth-First Search (DFS) — informed, using the Manhattan-distance heuristic
- **Problem:** 8-puzzle, start state `(7,2,4,5,0,6,8,3,1)`, 0 = blank tile

## Files
| File | Purpose |
|---|---|
| `search_profiling.py` | BFS + DFS implementation and the profiling/timing harness |
| `SLE2_PRN_YourName.docx` | The completed SLE-2 report (fill in your PRN, Name, Division, Date before submitting) |

## How to run
```bash
python search_profiling.py
```
This runs each algorithm 3 times, prints the average time (ms), nodes expanded, and solution path length for both, and states which one is faster and which expands fewer nodes.

## Result summary

| Metric | BFS | DFS | Better |
|---|---|---|---|
| Avg. time (ms) | 80.14 | 0.96 | DFS |
| Nodes expanded | 62,797 | 283 | DFS |
| Path length (moves) | 20 | 20 | Same (both optimal) |

DFS reaches the same optimal 20-move solution as BFS but roughly 83× faster while expanding about 222× fewer nodes, because its heuristic directs the search toward the goal instead of exploring uniformly outward.

## AI contribution note
Claude (Anthropic) was used to write the BFS/DFS implementation, the profiling harness, and to draft the report structure from the SLE-2 guideline. The algorithm choice, running the code, verifying the numbers, and writing the final justification were done by the student.
