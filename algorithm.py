from constants import board_size_x, board_size_y, start_field
from queue import Queue


def check(x, y):
    t = (0 <= x < board_size_x and 0 <= y < board_size_y)
    return t


def bfs(start, end):
    start_h, start_w = start[0], start[1]
    end_h, end_w = end[0], end[1]
    q = Queue()
    q.put([start_h, start_w])
    steps = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    used = [[False for i in range(board_size_x)] for _ in range(board_size_y)]
    used[start_h][start_w] = True
    parent = [[[-1, -1] for i in range(board_size_x)] for _ in range(board_size_y)]
    while not q.empty():
        h, w = q.get()
        if [h, w] == [end_h, end_w]:
            break
        for step in steps:
            if check(w + step[0], h + step[1]) and not used[h + step[1]][w + step[0]] and \
               start_field[h + step[1]][w + step[0]] == 0:
                parent[h + step[1]][w + step[0]] = [w, h]
                used[h + step[1]][w + step[0]] = True
                q.put([h + step[1], w + step[0]])
    h, w = end_h, end_w
    ans = [[w, h]]
    while parent[h][w] != [-1, -1]:
        ans.append(parent[h][w])
        w, h = parent[h][w]
    ans = list(reversed(ans))
    return ans
