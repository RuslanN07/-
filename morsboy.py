import tkinter as tk, random

N=10
FLEET=[4,3,3,2,2,2,1,1,1,1]
COL=dict(bg="#041a16",panel="#0b2b24",text="#d6ffef",grid="#0e4b3f",sea="#08211c",frame="#19c99b",ship="#8bffd0",ghost="#5be3b2",miss="#315e57",hit="#ff705d",sunk="#b5122a",accent="#9df5dc",warn="#ffd166",title="#8cf7e0")

def n8(x,y):
    for dx in(-1,0,1):
        for dy in(-1,0,1):
            if dx==dy==0: continue
            u,v=x+dx,y+dy
            if 0<=u<N and 0<=v<N: yield u,v

class Board:
    def __init__(s):
        s.g=[[0]*N for _ in range(N)]
        s.s=[]
    def can_place(s,x,y,l,h):
        c=[]
        for i in range(l):
            u,v=(x+i,y) if h else (x,y+i)
            if not(0<=u<N and 0<=v<N) or s.g[v][u]!=0: return False
            c.append((u,v))
        for a,b in c:
            for u,v in n8(a,b):
                if s.g[v][u]==1: return False
        return True
    def place(s,x,y,l,h):
        if not s.can_place(x,y,l,h): return False
        t=[]
        for i in range(l):
            u,v=(x+i,y) if h else (x,y+i)
            s.g[v][u]=1; t.append((u,v))
        s.s.append(set(t)); return True
    def remove_at(s,x,y):
        for ship in list(s.s):
            if (x,y) in ship:
                for u,v in ship: s.g[v][u]=0
                s.s.remove(ship); return len(ship)
        return 0
    def randomize(s):
        s.__init__()
        for k in FLEET:
            for _ in range(3000):
                h=bool(random.getrandbits(1))
                x=random.randint(0,(N-k) if h else N-1)
                y=random.randint(0,(N-1) if h else (N-k))
                if s.place(x,y,k,h): break
        return True
    def shoot(s,x,y):
        c=s.g[y][x]
        if c in(-1,2,3): return "repeat",None
        if c==0: s.g[y][x]=-1; return "miss",None
        s.g[y][x]=2
        for ship in s.s:
            if (x,y) in ship:
                if all(s.g[v][u]==2 for u,v in ship):
                    for u,v in ship: s.g[v][u]=3
                    for u,v in ship:
                        for a,b in n8(u,v):
                            if s.g[b][a]==0: s.g[b][a]=-1
                    return "sunk",ship
                return "hit",ship
        return "miss",None
    def all_sunk(s): return all(all(s.g[v][u]==3 for u,v in ship) for ship in s.s)

class App:
    def __init__(s,root):
        s.r=root; root.title("Сонар-Морской Бой"); root.configure(bg=COL["bg"])
        sw,sh=root.winfo_screenwidth(),root.winfo_screenheight()
        s.c=tk.Canvas(root,width=sw,height=sh,bg=COL["bg"],highlightthickness=0); s.c.pack(fill="both",expand=True)
        s.pad=70
        uw=sw-320-2*s.pad; uh=sh-2*s.pad-140
        s.cell=min(uw//N, (uh//(2*N+2)))
        s.top=(s.pad+220, s.pad+60); s.bot=(s.pad+220, s.pad+60+(N+2)*s.cell); s.panel=(s.pad,s.pad+60)
        s.msg=tk.StringVar(value="Перетащи корабли. R — поворот. Старт — когда всё расставлено.")
        tk.Label(root,textvariable=s.msg,bg=COL["bg"],fg=COL["text"],font=("Segoe UI",13)).place(relx=.5,y=24,anchor="n")
        s.toolbar=tk.Frame(root,bg=COL["bg"]); s.toolbar.place(relx=.5,rely=1.0,x=0,y=-48,anchor="s")
        tk.Button(s.toolbar,text="Случайно",command=s.rand_player).grid(row=0,column=0,padx=6)
        tk.Button(s.toolbar,text="Очистить",command=s.clear_player).grid(row=0,column=1,padx=6)
        tk.Button(s.toolbar,text="Старт",command=s.start).grid(row=0,column=2,padx=6)
        tk.Button(s.toolbar,text="Новая игра",command=s.new_game).grid(row=0,column=3,padx=14)
        root.bind("<Button-1>",s.on_down); root.bind("<ButtonRelease-1>",s.on_up)
        root.bind("<Motion>",s.on_move); root.bind("<Key-r>",s.rotate); root.bind("<Key-n>",lambda e:s.new_game())
        s.new_game_state(); s.draw()
    def new_game_state(s):
        s.p, s.e = Board(), Board()
        s.phase="prep"; s.drag=None; s.horiz=True
        s.to_place={1:4,2:3,3:2,4:1}; s.ai_remain=[]; s.ai_targets=set(); s.last=(0,0)
    def new_game(s):
        s.new_game_state(); s.msg.set("Новая игра: расставь флот."); s.draw()
    def bbox(s,ox,oy,x,y):
        a=ox+x*s.cell; b=oy+y*s.cell; return a,b,a+s.cell,b+s.cell
    def cell_from(s,ox,oy,px,py):
        x=(px-ox)//s.cell; y=(py-oy)//s.cell
        return (x,y) if 0<=x<N and 0<=y<N else None
    def bg(s):
        w=int(s.c["width"]); h=int(s.c["height"])
        for i in range(4):
            s.c.create_oval(-260+i*230,-180+i*160,w+280-i*200,h+120-i*150,outline=COL["frame"],width=1)
        for _ in range(180):
            x=random.randint(0,w); y=random.randint(0,h)
            s.c.create_oval(x-1,y-1,x+1,y+1,fill=COL["accent"],outline="")
        s.c.create_text(w/2,18,fill=COL["title"],text="⟢  Натальин, ИстБД-24, 26.11  ⟣",font=("Bahnschrift",18,"bold"))
    def grid(s,ox,oy,cap,accent,head=True):
        s.c.create_rectangle(ox-12,oy-12,ox+N*s.cell+12,oy+N*s.cell+12,outline=accent,width=2)
        if head: s.c.create_text(ox+N*s.cell/2,oy-28,fill=accent,font=("Bahnschrift",14,"bold"),text=cap)
        for i in range(N):
            s.c.create_text(ox+i*s.cell+s.cell/2,oy-10,fill=COL["text"],text=chr(65+i))
            s.c.create_text(ox-14,oy+i*s.cell+s.cell/2,fill=COL["text"],text=str(i+1))
        for y in range(N):
            for x in range(N):
                x0,y0,x1,y1=s.bbox(ox,oy,x,y)
                s.c.create_rectangle(x0,y0,x1,y1,fill=COL["sea"],outline=COL["grid"])
    def cells(s,b,ox,oy,show):
        for y in range(N):
            for x in range(N):
                v=b.g[y][x]; x0,y0,x1,y1=s.bbox(ox,oy,x,y)
                if show and v==1: s.c.create_rectangle(x0+3,y0+6,x1-3,y1-6,fill=COL["ship"],outline="")
                if v==-1: s.c.create_oval(x0+12,y0+12,x1-12,y1-12,fill=COL["miss"],outline="")
                if v==2: s.c.create_oval(x0+8,y0+8,x1-8,y1-8,fill=COL["hit"],outline="")
                if v==3: s.c.create_rectangle(x0+6,y0+6,x1-6,y1-6,fill=COL["sunk"],outline="")
    def dock(s):
        x,y=s.panel; h=N*s.cell
        s.c.create_rectangle(x-10,y-20,x+200,y+h+20,fill=COL["panel"],outline=COL["frame"],width=2)
        s.c.create_text(x+95,y-28,fill=COL["text"],text="Док кораблей",font=("Bahnschrift",12,"bold"))
        s.pal=[]; yy=y+8
        for size in (4,3,2,1):
            s.c.create_rectangle(x+10,yy,x+186,yy+30,outline=COL["grid"])
            for i in range(size): s.c.create_rectangle(x+14+i*26,yy+6,x+14+i*26+22,yy+24,fill=COL["ship"],outline="")
            s.c.create_text(x+168,yy+15,fill=COL["text"],text=f"×{s.to_place.get(size,0)}")
            s.pal.append((size,(x+10,yy,x+186,yy+30))); yy+=36
        s.c.create_text(x+95,y+h+28,fill=COL["text"],text="Перетащи → верхняя сетка",font=("Segoe UI",10))
    def drag_preview(s):
        if not s.drag: return
        ex,ey=s.last; ox,oy=s.top; t=s.cell_from(ox,oy,ex,ey)
        if not t: return
        k=s.drag["size"]; h=s.drag["h"]; ok=s.p.can_place(*t,k,h)
        for i in range(k):
            u,v=(t[0]+i,t[1]) if h else (t[0],t[1]+i)
            if 0<=u<N and 0<=v<N:
                x0,y0,x1,y1=s.bbox(ox,oy,u,v)
                s.c.create_rectangle(x0+3,y0+3,x1-3,y1-3,outline=COL["ghost" if ok else "hit"],width=2)
        s.c.create_text(ox+N*s.cell/2,oy-44,fill=COL["text"],text=f"{'Горизонтальный' if h else 'Вертикальный'} {k}-палубный — {'OK' if ok else 'нельзя'}")
    def draw(s):
        s.c.delete("all"); s.bg()
        tx,ty=s.top; bx,by=s.bot
        s.grid(tx,ty,"ТВОЙ СЕКТОР",COL["accent"]); s.cells(s.p,tx,ty,True)
        s.grid(bx,by,"СЕКТОР БОТА",COL["warn"]); s.cells(s.e,bx,by,s.phase!="battle")
        if s.phase=="prep": s.dock(); s.drag_preview()
    def hit_pal(s,x,y):
        for size,(x0,y0,x1,y1) in s.pal:
            if x0<=x<=x1 and y0<=y<=y1: return size
        return None
    def rotate(s,_=None):
        if s.phase!="prep": return
        if s.drag: s.drag["h"]=not s.drag["h"]
        else: s.horiz=not s.horiz
        s.draw()
    def on_down(s,e):
        s.last=(e.x,e.y); tx,ty=s.top; bx,by=s.bot
        if s.phase=="prep":
            t=s.cell_from(tx,ty,e.x,e.y)
            if t and s.p.g[t[1]][t[0]]==1:
                z=s.p.remove_at(*t)
                if z: s.to_place[z]=s.to_place.get(z,0)+1; s.draw(); return
            sz=s.hit_pal(e.x,e.y)
            if sz and s.to_place.get(sz,0)>0: s.drag=dict(size=sz,h=s.horiz)
        elif s.phase=="battle":
            t=s.cell_from(bx,by,e.x,e.y)
            if t: s.player_shoot(*t)
    def on_move(s,e):
        s.last=(e.x,e.y)
        if s.phase=="prep" and s.drag: s.draw()
    def on_up(s,e):
        s.last=(e.x,e.y)
        if s.phase!="prep" or not s.drag: return
        t=s.cell_from(s.top[0],s.top[1],e.x,e.y); k=s.drag["size"]; h=s.drag["h"]
        if t and s.p.place(t[0],t[1],k,h): s.to_place[k]-=1
        s.drag=None; s.draw()
    def rand_player(s):
        if s.phase!="prep": return
        while not s.p.randomize(): pass
        s.to_place={1:0,2:0,3:0,4:0}; s.draw()
    def clear_player(s):
        if s.phase!="prep": return
        s.p=Board(); s.to_place={1:4,2:3,3:2,4:1}; s.drag=None; s.draw()
    def start(s):
        if s.phase!="prep": return
        if any(s.to_place.values()): s.msg.set("Расставь все корабли или нажми «Случайно»."); return
        while not s.e.randomize(): pass
        s.phase="battle"; s.msg.set("Бой! Стреляй по нижней сетке.")
        s.ai_remain=sorted(FLEET,reverse=True); s.refresh_ai_targets(); s.draw()
    def player_shoot(s,x,y):
        r,_=s.e.shoot(x,y)
        if r=="repeat": return
        s.draw()
        if s.e.all_sunk(): s.msg.set("Победа! (N — новая игра)"); s.phase="end"; return
        s.r.after(300, s.ai_turn if r=="miss" else lambda: s.msg.set("Попадание! Ходи ещё."))
    def ai_turn(s):
        if s.p.all_sunk(): s.msg.set("ИИ победил! (N — новая игра)"); s.phase="end"; return
        x,y=s.ai_choose(); r,ship=s.p.shoot(x,y); s.refresh_ai_targets()
        if r=="hit": s.msg.set(f"ИИ попал в {chr(65+x)}{y+1} и добивает…"); s.draw(); s.r.after(200,s.ai_turn); return
        if r=="sunk":
            L=len(ship); s.ai_remove_ship(L); s.msg.set(f"ИИ потопил {L}-палубник."); s.draw(); s.r.after(200,s.ai_turn); return
        s.msg.set("ИИ промахнулся. Твой ход."); s.draw()
    def refresh_ai_targets(s):
        s.ai_targets={(x,y) for y in range(N) for x in range(N) if s.p.g[y][x] not in (-1,2,3)}
    def ai_remove_ship(s,L):
        for i,v in enumerate(s.ai_remain):
            if v==L: s.ai_remain.pop(i); break
        s.refresh_ai_targets()
    def hits_groups(s,board):
        vis=set(); G=[]
        for y in range(N):
            for x in range(N):
                if board.g[y][x]==2 and (x,y) not in vis:
                    q=[(x,y)]; vis.add((x,y)); cur=[]
                    while q:
                        u,v=q.pop(); cur.append((u,v))
                        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                            a,b=u+dx,v+dy
                            if 0<=a<N and 0<=b<N and board.g[b][a]==2 and (a,b) not in vis:
                                vis.add((a,b)); q.append((a,b))
                    G.append(cur)
        return G
    def corridor_len(s,board,x,y,dx,dy):
        L=0; a,b=x+dx,y+dy
        while 0<=a<N and 0<=b<N and board.g[b][a] not in (-1,3):
            if board.g[b][a]==2: a+=dx; b+=dy; continue
            L+=1; a+=dx; b+=dy
        return L
    def target_mode_pick(s,board):
        gs=s.hits_groups(board)
        if not gs: return None
        best=None; sc=-1; mx=max(s.ai_remain) if s.ai_remain else 1
        for g in gs:
            if len(g)>=2:
                xs=sorted(g,key=lambda t:t[0]); ys=sorted(g,key=lambda t:t[1])
                if ys[0][1]==ys[-1][1]:
                    y=ys[0][1]; x0=min(x for x,_ in g); x1=max(x for x,_ in g); C=[]
                    if x0-1>=0 and board.g[y][x0-1] not in (-1,3,2): C.append((x0-1,y,(x1-x0+1)))
                    if x1+1<N and board.g[y][x1+1] not in (-1,3,2): C.append((x1+1,y,(x1-x0+1)))
                    for cx,cy,span in C:
                        room=1+s.corridor_len(board,cx,cy,-1,0)+s.corridor_len(board,cx,cy,1,0)
                        scc=min(mx,room)+span*0.25
                        if scc>sc: sc=scc; best=(cx,cy)
                else:
                    x=xs[0][0]; y0=min(y for _,y in g); y1=max(y for _,y in g); C=[]
                    if y0-1>=0 and board.g[y0-1][x] not in (-1,3,2): C.append((x,y0-1,(y1-y0+1)))
                    if y1+1<N and board.g[y1+1][x] not in (-1,3,2): C.append((x,y1+1,(y1-y0+1)))
                    for cx,cy,span in C:
                        room=1+s.corridor_len(board,cx,cy,0,-1)+s.corridor_len(board,cx,cy,0,1)
                        scc=min(mx,room)+span*0.25
                        if scc>sc: sc=scc; best=(cx,cy)
            else:
                hx,hy=g[0]
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    cx,cy=hx+dx,hy+dy
                    if 0<=cx<N and 0<=cy<N and board.g[cy][cx] not in (-1,3,2):
                        room=1+s.corridor_len(board,cx,cy,dx,dy)+s.corridor_len(board,cx,cy,-dx,-dy)
                        if min(mx,room)>sc: sc=min(mx,room); best=(cx,cy)
        return best
    def build_prob_map(s,board):
        rem=s.ai_remain[:] if s.ai_remain else [1]; B=board.g
        S=[[0]*N for _ in range(N)]; bad={-1,3}
        hits={(x,y) for y in range(N) for x in range(N) if B[y][x]==2}
        for L in rem:
            for h in (True,False):
                mx=N-L if h else N-1; my=N-1 if h else N-L
                for y in range(my+1):
                    for x in range(mx+1):
                        ok=True; cells=[]
                        for i in range(L):
                            u,v=(x+i,y) if h else (x,y+i)
                            if B[v][u] in bad: ok=False; break
                            cells.append((u,v))
                        if not ok: continue
                        if hits and not any((hx,hy) in cells for hx,hy in hits): continue
                        for u,v in cells:
                            if B[v][u] in (0,1): S[v][u]+=1
        return S
    def hunt_mode_pick(s,board):
        S=s.build_prob_map(board); mn=min(s.ai_remain) if s.ai_remain else 1; parity=2 if mn>=2 else 1
        best=None; sc=-1
        for y in range(N):
            for x in range(N):
                if (x+y)%parity: continue
                if (x,y) in s.ai_targets and S[y][x]>sc: sc=S[y][x]; best=(x,y)
        if best: return best
        P=[(x,y) for (x,y) in s.ai_targets]
        return random.choice(P) if P else (0,0)
    def ai_choose(s):
        t=s.target_mode_pick(s.p)
        return t if t and t in s.ai_targets else s.hunt_mode_pick(s.p)

if __name__=="__main__":
    random.seed()
    r=tk.Tk(); App(r); r.mainloop()
