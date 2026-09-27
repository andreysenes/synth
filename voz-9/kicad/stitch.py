#!/usr/bin/env python3
"""Fecha as poucas ligações que o autorroteador deixou abertas.

Procura nas duas faces. Onde a trilha muda de lado, entra um furo.
"""

import heapq

import pcbnew

GRID = 0.5
WIDTH = 0.5
CLEAR = 0.35
NEED = WIDTH / 2 + CLEAR
VIA_R = 0.8


def mm(value):
    return pcbnew.ToMM(value)


def iu(value):
    return int(pcbnew.FromMM(value))


def _mark(bucket, x, y, radius):
    rad = radius + NEED
    x0 = int((x - rad) / GRID)
    x1 = int((x + rad) / GRID) + 1
    y0 = int((y - rad) / GRID)
    y1 = int((y + rad) / GRID) + 1
    for ix in range(x0, x1):
        for iy in range(y0, y1):
            if (ix * GRID - x) ** 2 + (iy * GRID - y) ** 2 <= rad * rad:
                bucket.add((ix, iy))


def _mark_seg(bucket, x1, y1, x2, y2, radius):
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    steps = max(1, int(length / 0.35))
    for i in range(steps + 1):
        t = i / steps
        _mark(bucket, x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, radius)


def route_pair(board, net_name, ax, ay, bx, by):
    front, back, via_block = set(), set(), set()

    def block_both(x, y, radius):
        _mark(front, x, y, radius)
        _mark(back, x, y, radius)
        rad = radius + VIA_R + CLEAR
        for ix in range(int((x - rad) / GRID), int((x + rad) / GRID) + 1):
            for iy in range(int((y - rad) / GRID), int((y + rad) / GRID) + 1):
                if (ix * GRID - x) ** 2 + (iy * GRID - y) ** 2 <= rad * rad:
                    via_block.add((ix, iy))

    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() in (net_name, ""):
                continue
            block_both(
                mm(pad.GetPosition().x),
                mm(pad.GetPosition().y),
                max(mm(pad.GetSize().x), mm(pad.GetSize().y)) / 2,
            )
    for item in board.GetTracks():
        if item.GetNetname() == net_name:
            continue
        if item.GetClass() == "PCB_VIA":
            block_both(mm(item.GetPosition().x), mm(item.GetPosition().y), VIA_R)
            continue
        bucket = front if item.GetLayer() == pcbnew.F_Cu else back
        _mark_seg(
            bucket,
            mm(item.GetStart().x),
            mm(item.GetStart().y),
            mm(item.GetEnd().x),
            mm(item.GetEnd().y),
            mm(item.GetWidth()) / 2,
        )
        x1, y1 = mm(item.GetStart().x), mm(item.GetStart().y)
        x2, y2 = mm(item.GetEnd().x), mm(item.GetEnd().y)
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        steps = max(1, int(length / 0.4))
        for i in range(steps + 1):
            t = i / steps
            px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            rad = mm(item.GetWidth()) / 2 + VIA_R + CLEAR
            for ix in range(int((px - rad) / GRID), int((px + rad) / GRID) + 1):
                for iy in range(int((py - rad) / GRID), int((py + rad) / GRID) + 1):
                    if (ix * GRID - px) ** 2 + (iy * GRID - py) ** 2 <= rad * rad:
                        via_block.add((ix, iy))

    def open_cell(ix, iy, layer):
        if not (1.5 <= ix * GRID <= 298.5 and 1.5 <= iy * GRID <= 298.5):
            return False
        return (ix, iy) not in (front if layer == 0 else back)

    start = (round(ax / GRID), round(ay / GRID))
    goal = (round(bx / GRID), round(by / GRID))
    heap = []
    came = {}
    cost = {}
    for layer in (0, 1):
        if open_cell(*start, layer):
            state = (start[0], start[1], layer)
            heap.append((0, state))
            came[state] = None
            cost[state] = 0
    found = None
    while heap:
        _, cur = heapq.heappop(heap)
        if (cur[0], cur[1]) == goal:
            found = cur
            break
        ix, iy, layer = cur
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (ix + dx, iy + dy, layer)
            if nxt in cost or not open_cell(nxt[0], nxt[1], layer):
                continue
            cost[nxt] = cost[cur] + 1
            came[nxt] = cur
            heuristic = abs(nxt[0] - goal[0]) + abs(nxt[1] - goal[1])
            heapq.heappush(heap, (cost[nxt] + heuristic, nxt))
        other = (ix, iy, 1 - layer)
        if other not in cost and open_cell(ix, iy, 1 - layer) and (ix, iy) not in via_block:
            cost[other] = cost[cur] + 5
            came[other] = cur
            heuristic = abs(ix - goal[0]) + abs(iy - goal[1])
            heapq.heappush(heap, (cost[other] + heuristic, other))
    if found is None:
        return False

    states = []
    while found is not None:
        states.append(found)
        found = came[found]
    states.reverse()
    net = board.FindNet(net_name)
    points = [(ax, ay, states[0][2])]
    for state in states:
        points.append((state[0] * GRID, state[1] * GRID, state[2]))
    points.append((bx, by, states[-1][2]))

    slim = [points[0]]
    for point in points[1:]:
        prev = slim[-1]
        if abs(point[0] - prev[0]) < 1e-6 and abs(point[1] - prev[1]) < 1e-6 and point[2] == prev[2]:
            continue
        if len(slim) >= 2 and point[2] == prev[2] == slim[-2][2]:
            a, b = slim[-2], prev
            if (abs(a[0] - b[0]) < 1e-6 and abs(b[0] - point[0]) < 1e-6) or (
                abs(a[1] - b[1]) < 1e-6 and abs(b[1] - point[1]) < 1e-6
            ):
                slim[-1] = point
                continue
        slim.append(point)

    for left, right in zip(slim, slim[1:]):
        if left[2] != right[2]:
            via = pcbnew.PCB_VIA(board)
            via.SetPosition(pcbnew.VECTOR2I(iu(right[0]), iu(right[1])))
            via.SetWidth(iu(1.6))
            via.SetDrill(iu(0.6))
            via.SetNet(net)
            board.Add(via)
            continue
        if abs(left[0] - right[0]) < 1e-6 and abs(left[1] - right[1]) < 1e-6:
            continue
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I(iu(left[0]), iu(left[1])))
        track.SetEnd(pcbnew.VECTOR2I(iu(right[0]), iu(right[1])))
        track.SetWidth(iu(WIDTH))
        track.SetLayer(pcbnew.F_Cu if left[2] == 0 else pcbnew.B_Cu)
        track.SetNet(net)
        board.Add(track)
    return True
