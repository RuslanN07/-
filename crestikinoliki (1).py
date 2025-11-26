import tkinter as tk

SZ, PAD = 360, 20
CELL = (SZ - 2*PAD)//3
GRID = [(i, j) for i in range(3) for j in range(3)]
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

class TTT:
    def __init__(self):
        self.root = tk.Tk(); self.root.title("Крестики-нолики (X вы)")
        self.c = tk.Canvas(self.root, width=SZ, height=SZ+110, bg="#0e0f14", highlightthickness=0)
        self.c.pack()
        self.c.bind("<Button-1>", self.click); self.root.bind("r", lambda e: self.reset())
        self.restart_btn = None
        self.reset(); self.draw_board(); self.label("Ваш ход (X). Нажмите R для рестарта.")
        self.root.mainloop()

    def reset(self):
        self.board = ['']*9; self.game_over = False
        self.c.delete("all"); self.draw_board(); self._remove_button()

    def _remove_button(self):
        if self.restart_btn:
            self.restart_btn.destroy(); self.restart_btn = None

    def label(self, txt):
        self.c.delete("lbl")
        self.c.create_text(SZ//2, SZ+30, text=txt, fill="#cbd5e1", font=("Segoe UI", 14), tags="lbl")

    def _show_restart_button(self):
        if self.restart_btn: return
        self.restart_btn = tk.Button(self.root, text="Начать заново", font=("Segoe UI", 12),
                                     bg="#1f2937", fg="#e5e7eb", activebackground="#374151",
                                     relief="flat", padx=12, pady=6, command=self.reset)
        self.c.create_window(SZ//2, SZ+70, window=self.restart_btn)

    def draw_board(self):
        for i in range(1,3):
            x = PAD + i*CELL
            self.c.create_line(x, PAD, x, SZ-PAD, fill="#334155", width=4, capstyle=tk.ROUND)
            y = PAD + i*CELL
            self.c.create_line(PAD, y, SZ-PAD, y, fill="#334155", width=4, capstyle=tk.ROUND)
        for idx, v in enumerate(self.board):
            if v: self.draw_mark(idx, v)

    def draw_mark(self, idx, v):
        i, j = divmod(idx, 3); x0=PAD+j*CELL; y0=PAD+i*CELL; x1=x0+CELL; y1=y0+CELL
        m = CELL*0.2
        if v=='X':
            self.c.create_line(x0+m,y0+m,x1-m,y1-m, fill="#22d3ee", width=10, capstyle=tk.ROUND)
            self.c.create_line(x0+m,y1-m,x1-m,y0+m, fill="#22d3ee", width=10, capstyle=tk.ROUND)
        else:
            self.c.create_oval(x0+m,y0+m,x1-m,y1-m, outline="#f472b6", width=10)

    def click(self, e):
        if self.game_over: return
        if not (PAD<=e.x<=SZ-PAD and PAD<=e.y<=SZ-PAD): return
        j = (e.x-PAD)//CELL; i = (e.y-PAD)//CELL; k = int(i*3+j)
        if self.board[k]: return
        self.board[k] = 'X'; self.draw_mark(k,'X')
        if self.end_if_any(): return
        self.ai_move(); self.end_if_any()

    def end_if_any(self):
        w = winner(self.board)
        if w or not any(v=='' for v in self.board):
            self.game_over=True
            self.label("Вы выиграли!" if w=='X' else ("Компьютер выиграл." if w=='O' else "Ничья."))
            self._show_restart_button()
            return True
        return False

    def ai_move(self):
        best, best_k = -10**9, None
        for k in legal(self.board):
            b = self.board[:]; b[k]='O'
            sc = minimax(b, False, depth=0, alpha=-10**9, beta=10**9)
            if sc>best: best, best_k = sc, k
        if best_k is not None:
            self.board[best_k]='O'; self.draw_mark(best_k,'O')
            self.label("Ваш ход (X).")

def winner(b):
    for a,b1,c in LINES:
        if b[a] and b[a]==b[b1]==b[c]: return b[a]
    return None

def legal(b): return [i for i,v in enumerate(b) if not v]

def line_score(line, b, me, opp):
    vals = [b[i] for i in line]
    if opp in vals and me in vals: return 0
    cnt = vals.count(me); cnto=vals.count(opp)
    return (1,3,9,50)[cnt] if cnto==0 else ( -1,-3,-9,-50)[cnto]

def heuristic(b, me='O', opp='X'):
    w = winner(b)
    if w==me: return 1000
    if w==opp: return -1000
    s = sum(line_score(l,b,me,opp) for l in LINES)
    bonus = (3 if b[4]==me else -3 if b[4]==opp else 0)
    corners = [0,2,6,8]
    bonus += sum(1 for i in corners if b[i]==me) - sum(1 for i in corners if b[i]==opp)
    return s + bonus

def minimax(b, maxp, depth, alpha, beta):
    w = winner(b)
    if w or not legal(b): return heuristic(b)
    if depth>=6: return heuristic(b) - depth*0.1
    if maxp:
        best = -10**9
        for k in legal(b):
            b[k]='O'
            best = max(best, minimax(b, False, depth+1, alpha, beta))
            b[k]=''; alpha = max(alpha, best)
            if beta<=alpha: break
        return best
    else:
        best = 10**9
        for k in legal(b):
            b[k]='X'
            best = min(best, minimax(b, True, depth+1, alpha, beta))
            b[k]=''; beta = min(beta, best)
            if beta<=alpha: break
        return best

if __name__ == "__main__":
    TTT()
