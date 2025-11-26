import os
import math
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

CANVAS_W, CANVAS_H = 900, 600

# 1 класс
class Square:
    def __init__(self, sid: str, x: float, y: float, size: float, color: str):
        self.sid = sid
        # три атрибута: x, y, size
        self.x = float(x)
        self.y = float(y)
        self.size = float(size)
        self.color = color

    # 4 метода (функции)
    @staticmethod
    def from_list(row, canvas_w=CANVAS_W, canvas_h=CANVAS_H):
        if len(row) != 5:
            raise ValueError(f"ожидалось 5 полей (id,x,y,size,color), получили {len(row)}")
        sid, xs, ys, ss, color = row
        sid = str(sid).strip()
        if not sid:
            raise ValueError("id не должен быть пустым")
        try:
            x = float(xs)
            y = float(ys)
            size = float(ss)
        except Exception:
            raise ValueError("x, y, size должны быть числами")
        if size <= 0:
            raise ValueError("size должен быть > 0")
        half = size/2
        if x - half < 0 or y - half < 0 or x + half > canvas_w or y + half > canvas_h:
            raise ValueError("квадрат выходит за пределы холста")
        _root = tk._default_root or tk.Tk()
        try:
            _root.winfo_rgb(color)
        except Exception:
            raise ValueError("некорректный цвет (используйте #RRGGBB или имя tk)")
        return Square(sid, x, y, size, color)

    def rotate_around(self, cx, cy, angle_deg):
        rad = math.radians(angle_deg)
        dx, dy = self.x - cx, self.y - cy
        nx =  dx*math.cos(rad) - dy*math.sin(rad)
        ny =  dx*math.sin(rad) + dy*math.cos(rad)
        self.x, self.y = cx + nx, cy + ny

    def is_on_axis(self, cx, tol=0.5):
        return abs(self.x - cx) <= tol

    def bbox(self):
        h = self.size / 2
        return (self.x - h, self.y - h, self.x + h, self.y + h)

class SquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ЛР Вариант 28 — Квадраты")
        self.squares = []
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *a: self.apply_filter())
        self.build_gui()

    def build_gui(self):
        top = tk.Frame(self.root)
        top.pack(padx=10, pady=10, fill='x')

        tk.Button(top, text="Загрузить CSV", command=self.load_csv).grid(row=0, column=0, padx=5)
        tk.Button(top, text="Сохранить CSV", command=self.save_csv).grid(row=0, column=1, padx=5)
        tk.Button(top, text="Поворот", command=self.rotate_dialog).grid(row=0, column=2, padx=5)
        tk.Button(top, text="Сегментация (симметрия)", command=self.show_symmetry_segmentation).grid(row=0, column=3, padx=5)
        tk.Button(top, text="Визуализировать", command=self.draw_scene).grid(row=0, column=4, padx=5)
        tk.Button(top, text="Раскрасить сегменты", command=self.colorize_by_segment).grid(row=0, column=5, padx=5)

        tk.Entry(top, textvariable=self.search_var, width=22).grid(row=0, column=6, padx=(20,5))
        tk.Label(top, text="Фильтр по id/цвету").grid(row=0, column=7, padx=(0,5))

        tf = tk.Frame(self.root)
        tf.pack(padx=10, fill='both')
        self.tree = ttk.Treeview(tf, columns=("ID","X","Y","Size","Color"),
                                 show='headings', height=12)
        for col,w in [("ID",160),("X",80),("Y",80),("Size",80),("Color",120)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor='center')
        sb = ttk.Scrollbar(tf, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side='left', fill='y')
        sb.pack(side='left', fill='y')
        self.tree.bind('<Double-1>', self.on_double_click)

        # начало графики
        self.canvas = tk.Canvas(self.root, width=CANVAS_W, height=CANVAS_H, bg="white")
        self.canvas.pack(padx=10, pady=10)
        self.draw_scene()

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if not path:
            return
        good, errors = [], []
        with open(path, encoding='utf-8') as f:
            r = csv.reader(f)
            header_checked = False
            for nr, row in enumerate(r, start=1):
                if not header_checked:
                    header_checked = True
                    if row and row[0].lower() == "id":
                        continue
                try:
                    sq = Square.from_list(row, CANVAS_W, CANVAS_H)
                    good.append(sq)
                except Exception as e:
                    errors.append((nr, row, str(e)))
        self.squares = good
        self.refresh_tree()
        self.draw_scene()
        if errors:
            base, _ = os.path.splitext(path)
            log_path = base + "_errors.log"
            with open(log_path, "w", encoding="utf-8") as log:
                log.write(f"Ошибки загрузки файла {os.path.basename(path)}\n\n")
                for nr, row, err in errors:
                    log.write(f"Строка {nr}: {row} — {err}\n")
            messagebox.showwarning(
                "Загрузка завершена с ошибками",
                f"Пропущено {len(errors)} строк. Подробности в {os.path.basename(log_path)}"
            )

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files","*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id","x","y","size","color"])
            for s in self.squares:
                w.writerow([s.sid, f"{s.x:.1f}", f"{s.y:.1f}", f"{s.size:.1f}", s.color])
        messagebox.showinfo("Готово", "CSV сохранён.")

    def refresh_tree(self, filtered=None):
        data = filtered if filtered is not None else self.squares
        self.tree.delete(*self.tree.get_children())
        for s in data:
            self.tree.insert('', 'end',
                             values=(s.sid, f"{s.x:.1f}", f"{s.y:.1f}", f"{s.size:.1f}", s.color))

    def apply_filter(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.refresh_tree()
            return
        def ok(s: Square):
            return term in s.sid.lower() or term in s.color.lower()
        filtered = [s for s in self.squares if ok(s)]
        self.refresh_tree(filtered)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        col  = self.tree.identify_column(event.x)
        if not item or not col:
            return
        idx = self.tree.index(item)
        ci  = int(col.replace('#','')) - 1
        s   = self.squares[idx]
        old = self.tree.item(item, 'values')[ci]
        if ci in (1,2,3):
            new = simpledialog.askfloat("Изменить",
                                        ["X","Y","Size"][ci-1] if ci>0 else "X",
                                        initialvalue=float(old))
            if new is None:
                return
            try:
                if ci == 1:
                    x = float(new); h = s.size/2
                    if x - h < 0 or x + h > CANVAS_W: raise ValueError
                    s.x = x
                elif ci == 2:
                    y = float(new); h = s.size/2
                    if y - h < 0 or y + h > CANVAS_H: raise ValueError
                    s.y = y
                else:
                    size = float(new)
                    if size <= 0: raise ValueError
                    h = size/2
                    if s.x - h < 0 or s.x + h > CANVAS_W or s.y - h < 0 or s.y + h > CANVAS_H:
                        raise ValueError
                    s.size = size
            except Exception:
                messagebox.showerror("Ошибка", "Недопустимое значение/вне холста.")
                return
        elif ci == 4:
            new = simpledialog.askstring("Цвет", "Новый цвет (#RRGGBB или имя tk):", initialvalue=old)
            if new is None:
                return
            try:
                self.root.winfo_rgb(new)
                s.color = new
            except Exception:
                messagebox.showerror("Ошибка", "Некорректный цвет.")
                return
        else:
            new = simpledialog.askstring("ID", "Новый ID:", initialvalue=s.sid)
            if new is None:
                return
            s.sid = new.strip()
        self.refresh_tree()
        self.draw_scene()

    def draw_scene(self):
        self.canvas.delete('all')
        cx, cy = CANVAS_W/2, CANVAS_H/2
        self.canvas.create_line(cx, 0, cx, CANVAS_H, fill="#eeeeee")
        self.canvas.create_line(0, cy, CANVAS_W, cy, fill="#eeeeee")
        for s in self.squares:
            x1,y1,x2,y2 = s.bbox()
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=s.color, outline='black')
            self.canvas.create_text(s.x, s.y, text=s.sid, font=("Arial",8))

    def symmetry_groups(self, tol=2.0):
        cx = CANVAS_W/2
        left_buckets = {}
        right_buckets = {}
        center = set()
        def key_for(s: Square):
            return (round(s.y,1), round(s.size,1))
        for i,s in enumerate(self.squares):
            if s.is_on_axis(cx, tol):
                center.add(i)
            elif s.x < cx:
                left_buckets.setdefault(key_for(s), []).append(i)
            else:
                right_buckets.setdefault(key_for(s), []).append(i)
        paired = set()
        for k, left_ids in left_buckets.items():
            right_ids = right_buckets.get(k, [])
            m = min(len(left_ids), len(right_ids))
            if m > 0:
                L = sorted(left_ids, key=lambda i: self.squares[i].x)
                R = sorted(right_ids, key=lambda i: self.squares[i].x, reverse=True)
                for a,b in zip(L[:m], R[:m]):
                    xa = self.squares[a].x
                    xb = self.squares[b].x
                    if abs((2*cx - xa) - xb) <= tol:
                        paired.add(a); paired.add(b)
        all_ids = set(range(len(self.squares)))
        single = all_ids - paired - center
        return {"paired": paired, "center": center, "single": single}

    def show_symmetry_segmentation(self):
        groups = self.symmetry_groups()
        counts = {
            "Зеркальные пары": len(groups["paired"]),
            "На оси": len(groups["center"]),
            "Одиночные": len(groups["single"]),
        }
        self._draw_pie(counts, "Симметричная сегментация")

    def _draw_pie(self, counts: dict, title: str):
        self.canvas.delete('all')
        total = sum(counts.values())
        if total == 0:
            return
        cx, cy = CANVAS_W/2, CANVAS_H/2
        r = min(CANVAS_W, CANVAS_H)/2 - 100
        self.canvas.create_text(cx, 40, text=title, font=("Arial",16,"bold"))
        palette = ["#81c784","#64b5f6","#e57373","#ffd54f","#ba68c8"]
        start = 0
        items = list(counts.items())
        for i, (label, cnt) in enumerate(items):
            extent = 360 * cnt / total
            arc = self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                                         start=start, extent=extent,
                                         fill=palette[i % len(palette)],
                                         outline='white', width=2)
            self.canvas.tag_bind(arc, '<Button-1>',
                lambda e, l=label, c=cnt: messagebox.showinfo(
                    'Сегмент', f"{l}: {c} ({c/total*100:.1f}%)"))
            start += extent
        lx, ly = cx + r + 40, cy - r
        for i, (label, cnt) in enumerate(items):
            y = ly + i*30
            self.canvas.create_rectangle(lx, y, lx+20, y+15,
                                         fill=palette[i % len(palette)], outline='black')
            self.canvas.create_text(lx+25, y+7,
                                    text=f"{label}: {cnt} ({cnt/total*100:.1f}%)",
                                    anchor='w', font=("Arial",12))

    def colorize_by_segment(self):
        groups = self.symmetry_groups()
        for i in groups["paired"]:
            self.squares[i].color = "#81c784"
        for i in groups["center"]:
            self.squares[i].color = "#64b5f6"
        for i in groups["single"]:
            self.squares[i].color = "#e57373"
        self.draw_scene()

    def rotate_dialog(self):
        angle = simpledialog.askfloat("Поворот", "Угол (в градусах):", initialvalue=15.0)
        if angle is None:
            return
        cx, cy = CANVAS_W/2, CANVAS_H/2
        for s in self.squares:
            s.rotate_around(cx, cy, angle)
            h = s.size/2
            if s.x - h < 0 or s.x + h > CANVAS_W or s.y - h < 0 or s.y + h > CANVAS_H:
                s.rotate_around(cx, cy, -angle)
        self.draw_scene()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from tkinter import ttk
        root.style = ttk.Style()
        if "clam" in root.style.theme_names():
            root.style.theme_use("clam")
    except Exception:
        pass
    app = SquareApp(root)
    root.mainloop()
