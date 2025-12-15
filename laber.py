import tkinter as tk
import random
from collections import deque

CELLS = 10
P = 28
NEI = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DELAY = 60

def gen_maze(c, num_exits=3):
    n = 2 * c + 1
    g = [[1] * n for _ in range(n)]
    R = C = c
    
    vr = [[False] * C for _ in range(R)]
    r = c // 2
    k = c // 2
    st = [(r, k)]
    vr[r][k] = True
    g[2 * r + 1][2 * k + 1] = 0
    
    while st:
        r, k = st[-1]
        cand = []
        for dr, dc in NEI:
            nr, nc = r + dr, k + dc
            if 0 <= nr < R and 0 <= nc < C and not vr[nr][nc]:
                cand.append((dr, dc, nr, nc))
        if cand:
            dr, dc, nr, nc = random.choice(cand)
            g[2 * r + 1 + dr][2 * k + 1 + dc] = 0
            g[2 * nr + 1][2 * nc + 1] = 0
            vr[nr][nc] = True
            st.append((nr, nc))
        else:
            st.pop()
    
    sides = ["N", "S", "W", "E"]
    random.shuffle(sides)
    exits_created = 0
    
    for side in sides:
        if exits_created >= num_exits:
            break
        if side == "N":
            x = 2 * random.randrange(C) + 1
            if g[1][x] == 0 and g[0][x] == 1:
                g[0][x] = 0
                exits_created += 1
        elif side == "S":
            x = 2 * random.randrange(C) + 1
            if g[2 * R - 1][x] == 0 and g[2 * R][x] == 1:
                g[2 * R][x] = 0
                exits_created += 1
        elif side == "W":
            y = 2 * random.randrange(R) + 1
            if g[y][1] == 0 and g[y][0] == 1:
                g[y][0] = 0
                exits_created += 1
        elif side == "E":
            y = 2 * random.randrange(R) + 1
            if g[y][2 * C - 1] == 0 and g[y][2 * C] == 1:
                g[y][2 * C] = 0
                exits_created += 1
    
    while exits_created < num_exits:
        side = random.choice(["N", "S", "W", "E"])
        if side == "N":
            x = 2 * random.randrange(C) + 1
            g[0][x] = 0
        elif side == "S":
            x = 2 * random.randrange(C) + 1
            g[2 * R][x] = 0
        elif side == "W":
            y = 2 * random.randrange(R) + 1
            g[y][0] = 0
        elif side == "E":
            y = 2 * random.randrange(R) + 1
            g[y][2 * C] = 0
        exits_created += 1
    
    return g

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.N = 2 * CELLS + 1
        self.title("Лабиринт DFS")
        self.resizable(False, False)
        
        top = tk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)
        
        tk.Button(top, text="Сгенерировать", command=self.generate, width=12).pack(side="left", padx=2)
        tk.Button(top, text="Старт DFS", command=self.start, width=10).pack(side="left", padx=2)
        tk.Button(top, text="Сброс", command=self.reset, width=8).pack(side="left", padx=2)
        
        tk.Label(top, text="Выходы:").pack(side="left", padx=(15, 5))
        self.exit_var = tk.IntVar(value=3)
        tk.Spinbox(top, from_=1, to=4, width=4, textvariable=self.exit_var).pack(side="left", padx=2)
        
        self.msg = tk.StringVar(value="Готово.")
        tk.Label(self, textvariable=self.msg, font=("Arial", 10), height=2).pack(fill="x", padx=5, pady=(0, 5))
        
        self.cv = tk.Canvas(self, width=self.N * P, height=self.N * P, bg="white")
        self.cv.pack(padx=5, pady=5)
        
        self.g = [[1] * self.N for _ in range(self.N)]
        self.rect = [[None] * self.N for _ in range(self.N)]
        self.start_cell = (self.N // 2, self.N // 2)
        self.exits = []
        self.robot = None
        self.vis = set()
        self.stack = []
        self.run = False
        self.fin = False
        
        self.generate()

    def generate(self):
        if self.run:
            return
        
        self.fin = False
        self.vis.clear()
        self.stack.clear()
        
        num_exits = self.exit_var.get()
        self.g = gen_maze(CELLS, num_exits)
        
        self.exits = [(r, c) for r in range(self.N) for c in range(self.N) if self.g[r][c] == 0 and (r in (0, self.N - 1) or c in (0, self.N - 1))]
        
        self.cv.delete("all")
        self.robot = None
        
        for r in range(self.N):
            for c in range(self.N):
                x0, y0 = c * P, r * P
                x1, y1 = x0 + P, y0 + P
                
                if (r, c) in self.exits:
                    fill = "#a0ffa0"
                elif self.g[r][c] == 1:
                    fill = "#101010"
                else:
                    fill = "#ffffff"
                
                self.rect[r][c] = self.cv.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#c0c0c0")
        
        if self.g[self.start_cell[0]][self.start_cell[1]] == 1:
            t = self.nearest_free(self.start_cell)
            if t:
                self.start_cell = t
        
        self.place(self.start_cell, True)
        self.msg.set(f"Старт: {self.start_cell}. Выходов: {len(self.exits)}.")

    def nearest_free(self, orig):
        sr, sc = orig
        seen = {(sr, sc)}
        q = deque([(sr, sc)])
        
        while q:
            r, c = q.popleft()
            if self.g[r][c] == 0:
                return (r, c)
            for dr, dc in NEI:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.N and 0 <= nc < self.N and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return None

    def place(self, pos, new=False):
        r, c = pos
        cx, cy = c * P + P / 2, r * P + P / 2
        rad = P * 0.35
        
        if self.robot is None or new:
            self.robot = self.cv.create_oval(cx - rad, cy - rad, cx + rad, cy + rad, fill="#ff3030")
            return
        
        self.cv.coords(self.robot, cx - rad, cy - rad, cx + rad, cy + rad)

    def reset(self):
        if self.run:
            return
        
        self.vis.clear()
        self.stack.clear()
        self.fin = False
        
        for r in range(self.N):
            for c in range(self.N):
                if (r, c) in self.exits:
                    fill = "#a0ffa0"
                elif self.g[r][c] == 1:
                    fill = "#101010"
                else:
                    fill = "#ffffff"
                self.cv.itemconfig(self.rect[r][c], fill=fill)
        
        self.place(self.start_cell)
        self.msg.set("Сброшено.")

    def start(self):
        if self.run or self.fin:
            return
        
        if self.g[self.start_cell[0]][self.start_cell[1]] == 1:
            self.msg.set("Старт в стене. Сгенерируйте снова.")
            return
        
        self.run = True
        self.vis.clear()
        self.stack = [(self.start_cell, [self.start_cell])]
        self.msg.set("Поиск выхода DFS...")
        self.after(DELAY, self.step)

    def step(self):
        if not self.stack:
            self.run = False
            self.fin = True
            self.msg.set("Путь не найден.")
            return
        
        (r, c), path = self.stack.pop()
        
        if (r, c) in self.vis:
            self.after(DELAY, self.step)
            return
        
        self.vis.add((r, c))
        
        if (r, c) != self.start_cell and self.g[r][c] == 0:
            self.cv.itemconfig(self.rect[r][c], fill="#d6ecff")
        
        self.place((r, c))
        
        if (r, c) in self.exits and (r, c) != self.start_cell:
            self.run = False
            self.fin = True
            self.msg.set(f"Найден выход: {(r, c)}")
            self.highlight(path)
            return
        
        for dr, dc in NEI[::-1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.N and 0 <= nc < self.N and self.g[nr][nc] == 0 and (nr, nc) not in self.vis:
                self.stack.append(((nr, nc), path + [(nr, nc)]))
        
        self.after(DELAY, self.step)

    def highlight(self, path):
        def go(i):
            if i >= len(path):
                return
            
            r, c = path[i]
            if (r, c) != self.start_cell and self.g[r][c] == 0:
                self.cv.itemconfig(self.rect[r][c], fill="#ffd860")
            
            self.place((r, c))
            self.after(20, lambda: go(i + 1))
        
        go(0)

if __name__ == "__main__":
    App().mainloop()
