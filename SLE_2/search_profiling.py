"""
SLE-2 Profiling Report - Supporting Code
Course: 02AML204 - Introduction to Artificial Intelligence

Compares Breadth-First Search (BFS, uninformed) against A* Search
(informed, Manhattan-distance heuristic) on the classic 8-puzzle problem.

For each algorithm we measure:
  - Average execution time (ms) over multiple runs
  - Number of nodes expanded (states popped from the frontier and explored)
  - Solution path length (moves)

Run:  python search_profiling.py
"""

import time
import heapq
from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# A solvable shuffled 8-puzzle start state (0 = blank).
# This one needs a longer solution path (~16+ moves) so the timing
# and node-count difference between BFS and A* is clearly visible,
# instead of both finishing in well under 1 ms.
START = (7, 2, 4, 5, 0, 6, 8, 3, 1)

MOVES = {
    0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
    3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
    6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
}


def neighbors(state):
    zero = state.index(0)
    for nz in MOVES[zero]:
        new_state = list(state)
        new_state[zero], new_state[nz] = new_state[nz], new_state[zero]
        yield tuple(new_state)


def manhattan(state):
    dist = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        goal_idx = val - 1 if val != 0 else 8
        r1, c1 = divmod(idx, 3)
        r2, c2 = divmod(goal_idx, 3)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist


def bfs(start):
    """Uninformed search. Returns (path_length, nodes_expanded)."""
    frontier = deque([(start, 0)])
    visited = {start}
    nodes_expanded = 0
    while frontier:
        state, depth = frontier.popleft()
        nodes_expanded += 1
        if state == GOAL:
            return depth, nodes_expanded
        for nxt in neighbors(state):
            if nxt not in visited:
                visited.add(nxt)
                frontier.append((nxt, depth + 1))
    return None, nodes_expanded


def astar(start):
    """Informed search with Manhattan-distance heuristic."""
    counter = 0  # tie-breaker for heap
    frontier = [(manhattan(start), counter, start, 0)]
    visited = {start: 0}
    nodes_expanded = 0
    while frontier:
        _, _, state, depth = heapq.heappop(frontier)
        nodes_expanded += 1
        if state == GOAL:
            return depth, nodes_expanded
        for nxt in neighbors(state):
            new_depth = depth + 1
            if nxt not in visited or new_depth < visited[nxt]:
                visited[nxt] = new_depth
                counter += 1
                heapq.heappush(frontier, (new_depth + manhattan(nxt), counter, nxt, new_depth))
    return None, nodes_expanded


def profile(fn, start, runs=3):
    times = []
    path_len = nodes = None
    for _ in range(runs):
        t0 = time.perf_counter()
        path_len, nodes = fn(start)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)  # ms
    avg_time = sum(times) / len(times)
    return avg_time, nodes, path_len, times


if __name__ == "__main__":
    print("Start state:", START)
    print("Goal state :", GOAL)
    print("=" * 60)

    bfs_time, bfs_nodes, bfs_path, bfs_runs = profile(bfs, START, runs=3)
    astar_time, astar_nodes, astar_path, astar_runs = profile(astar, START, runs=3)

    print(f"BFS   -> avg time: {bfs_time:.3f} ms | nodes expanded: {bfs_nodes} "
          f"| path length: {bfs_path} | individual runs (ms): {[round(t,3) for t in bfs_runs]}")
    print(f"A*    -> avg time: {astar_time:.3f} ms | nodes expanded: {astar_nodes} "
          f"| path length: {astar_path} | individual runs (ms): {[round(t,3) for t in astar_runs]}")

    print("=" * 60)
    faster = "A*" if astar_time < bfs_time else "BFS"
    fewer_nodes = "A*" if astar_nodes < bfs_nodes else "BFS"
    print(f"Faster algorithm: {faster}")
    print(f"Fewer nodes expanded: {fewer_nodes}")
