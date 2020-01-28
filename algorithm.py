from queue import Queue
from constants import board_size_x, board_size_y, start_field


def check(x, y):
    t = (0 <= x < board_size_x and 0 <= y < board_size_y)
    return t


def bfs(start_x, start_y, end_x, end_y):
    q = Queue()
    q.put([start_y, start_x])
    step = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    used = [[False] * board_size_x for _ in range(board_size_y)]
    parent = [[[-1, -1]] * board_size_x for _ in range(board_size_y)]
    while not q.empty():
        a = q.get()
        if a == [end_y, end_x]:
            break
        for i in step:
            if check(a[1] + i[1], a[0] + i[0]) and start_field[a[0] + i[0]][a[1] + i[1]] == 0 \
                    and not used[a[0] + i[0]][a[1] + i[1]]:
                used[a[0] + i[0]][a[1] + i[1]] = True
                parent[a[0] + i[0]][a[1] + i[1]] = a
                q.put([a[0] + i[0], a[1] + i[1]])
    ans = [[end_y, end_x]]
    while parent[end_y][end_x] != [-1, -1]:
        ans.append(parent[end_y][end_x])
        x = parent[end_y][end_x][1]
        end_y = parent[end_y][end_x][0]
        end_x = x
    ans = list(reversed(ans))
    return ans
