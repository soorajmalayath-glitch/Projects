


import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ─────────────────────────────────────────
# DB CONNECTION
# ─────────────────────────────────────────
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sooraj@1607",
        database="testdb"
    )

# ─────────────────────────────────────────
# DB OPERATIONS
# ─────────────────────────────────────────
def add_student(Name, Age, Physics, Maths, Chemistry):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    Total = Physics + Maths + Chemistry
    Average = round(Total / 3, 2)
    cursor.execute(
        "INSERT INTO students (Name, Age, Physics, Maths, Chemistry, Total, Average) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (Name, Age, Physics, Maths, Chemistry, Total, Average)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return Total, Average

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def update_student(student_id, Name=None, Age=None, Physics=None, Maths=None, Chemistry=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        return None
    Name      = Name      if Name      is not None else existing["Name"]
    Age       = Age       if Age       is not None else existing["Age"]
    Physics   = Physics   if Physics   is not None else existing["Physics"]
    Maths     = Maths     if Maths     is not None else existing["Maths"]
    Chemistry = Chemistry if Chemistry is not None else existing["Chemistry"]
    Total   = Physics + Maths + Chemistry
    Average = round(Total / 3, 2)
    cursor.execute(
        "UPDATE students SET Name=%s, Age=%s, Physics=%s, Maths=%s, "
        "Chemistry=%s, Total=%s, Average=%s WHERE id=%s",
        (Name, Age, Physics, Maths, Chemistry, Total, Average, student_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return Total, Average

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Name FROM students WHERE id = %s", (student_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return None
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return row["Name"]

# ─────────────────────────────────────────
# COLOUR PALETTE & FONTS
# ─────────────────────────────────────────
BG        = "#0f1117"
PANEL     = "#1a1d27"
CARD      = "#22263a"
ACCENT    = "#4f8ef7"
ACCENT2   = "#7c5cfc"
SUCCESS   = "#2ecc71"
DANGER    = "#e74c3c"
WARNING   = "#f39c12"
TEXT      = "#e8eaf0"
SUBTEXT   = "#8b90a8"
BORDER    = "#2e3250"

FONT_HEAD = ("Courier New", 22, "bold")
FONT_SUB  = ("Courier New", 11)
FONT_BODY = ("Courier New", 10)
FONT_LBL  = ("Courier New", 10, "bold")
FONT_BTN  = ("Courier New", 10, "bold")

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def labeled_entry(parent, label, row, col=0, width=18):
    tk.Label(parent, text=label, bg=PANEL, fg=SUBTEXT, font=FONT_LBL,
             anchor="w").grid(row=row, column=col, sticky="w", padx=(0, 8), pady=4)
    var = tk.StringVar()
    e = tk.Entry(parent, textvariable=var, bg=CARD, fg=TEXT, insertbackground=ACCENT,
                 font=FONT_BODY, width=width, relief="flat",
                 highlightthickness=1, highlightcolor=ACCENT, highlightbackground=BORDER)
    e.grid(row=row, column=col+1, sticky="ew", pady=4)
    return var, e

def accent_btn(parent, text, cmd, color=ACCENT, width=14):
    return tk.Button(parent, text=text, command=cmd, bg=color, fg="white",
                     font=FONT_BTN, relief="flat", cursor="hand2",
                     activebackground=ACCENT2, activeforeground="white",
                     padx=10, pady=6, width=width)

def clear_entries(*vars_):
    for v in vars_:
        v.set("")

# ─────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────
class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.configure(bg=BG)
        self.geometry("1100x700")
        self.resizable(True, True)
        self._build_ui()

    # ── TOP HEADER ───────────────────────
    def _build_ui(self):
        hdr = tk.Frame(self, bg=PANEL, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="▸ STUDENT MANAGEMENT SYSTEM",
                 bg=PANEL, fg=ACCENT, font=FONT_HEAD).pack(side="left", padx=24)
        tk.Label(hdr, text="MySQL · CRUD Interface",
                 bg=PANEL, fg=SUBTEXT, font=FONT_SUB).pack(side="left", padx=8)

        # ── BODY: sidebar + main ──────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=0, pady=0)

        sidebar = tk.Frame(body, bg=PANEL, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.main = tk.Frame(body, bg=BG)
        self.main.pack(side="left", fill="both", expand=True, padx=16, pady=16)

        self._build_sidebar(sidebar)
        self._show_view()   # default tab

    # ── SIDEBAR BUTTONS ──────────────────
    def _build_sidebar(self, parent):
        tk.Label(parent, text="MENU", bg=PANEL, fg=SUBTEXT,
                 font=("Courier New", 9, "bold")).pack(pady=(20, 6))
        sep = tk.Frame(parent, bg=BORDER, height=1)
        sep.pack(fill="x", padx=16, pady=4)

        nav_items = [
            ("⊕  Add Student",    self._show_add),
            ("≡  View All",       self._show_view),
            ("◉  Search by ID",   self._show_search),
            ("✎  Update Student", self._show_update),
            ("✕  Delete Student", self._show_delete),
        ]
        for label, cmd in nav_items:
            btn = tk.Button(parent, text=label, command=cmd,
                            bg=PANEL, fg=TEXT, font=FONT_BTN,
                            relief="flat", anchor="w", padx=20, pady=10,
                            cursor="hand2", activebackground=CARD,
                            activeforeground=ACCENT, width=22)
            btn.pack(fill="x")

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=12)
        tk.Label(parent, text="v1.0  |  testdb", bg=PANEL,
                 fg=SUBTEXT, font=("Courier New", 8)).pack(side="bottom", pady=12)

    # ── CLEAR MAIN FRAME ─────────────────
    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _section_title(self, title, color=ACCENT):
        tk.Label(self.main, text=title, bg=BG, fg=color,
                 font=("Courier New", 14, "bold")).pack(anchor="w", pady=(0, 12))

    # ─────────────────────────────────────
    # 1. ADD
    # ─────────────────────────────────────
    def _show_add(self):
        self._clear_main()
        self._section_title("⊕  Add New Student")
        card = tk.Frame(self.main, bg=PANEL, padx=24, pady=20)
        card.pack(fill="x")
        card.columnconfigure(1, weight=1)

        self._av_name,  _ = labeled_entry(card, "Name",      0)
        self._av_age,   _ = labeled_entry(card, "Age",       1)
        self._av_phy,   _ = labeled_entry(card, "Physics",   2)
        self._av_mat,   _ = labeled_entry(card, "Maths",     3)
        self._av_chem,  _ = labeled_entry(card, "Chemistry", 4)

        self._add_status = tk.Label(self.main, text="", bg=BG, font=FONT_BODY)
        self._add_status.pack(anchor="w", pady=6)

        bf = tk.Frame(self.main, bg=BG)
        bf.pack(anchor="w", pady=4)
        accent_btn(bf, "Add Student", self._do_add, color=SUCCESS).pack(side="left", padx=(0, 8))
        accent_btn(bf, "Clear", lambda: clear_entries(
            self._av_name, self._av_age, self._av_phy, self._av_mat, self._av_chem
        ), color=SUBTEXT, width=8).pack(side="left")

    def _do_add(self):
        try:
            name = self._av_name.get().strip()
            age  = int(self._av_age.get())
            phy  = float(self._av_phy.get())
            mat  = float(self._av_mat.get())
            chem = float(self._av_chem.get())
            if not name:
                raise ValueError("Name cannot be empty")
            total, avg = add_student(name, age, phy, mat, chem)
            self._add_status.config(
                fg=SUCCESS,
                text=f"✔  '{name}' added!  Total: {total}  |  Average: {avg}"
            )
            clear_entries(self._av_name, self._av_age, self._av_phy, self._av_mat, self._av_chem)
        except mysql.connector.Error as e:
            self._add_status.config(fg=DANGER, text=f"DB Error: {e}")
        except ValueError as e:
            self._add_status.config(fg=WARNING, text=f"Input Error: {e}")

    # ─────────────────────────────────────
    # 2. VIEW ALL
    # ─────────────────────────────────────
    def _show_view(self):
        self._clear_main()
        self._section_title("≡  All Students")

        rf = tk.Frame(self.main, bg=BG)
        rf.pack(anchor="e", pady=(0, 8))
        accent_btn(rf, "⟳ Refresh", self._show_view, width=10).pack()

        cols = ("ID", "Name", "Age", "Physics", "Maths", "Chemistry", "Total", "Average")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                         background=CARD, fieldbackground=CARD,
                         foreground=TEXT, font=FONT_BODY, rowheight=26,
                         borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                         background=PANEL, foreground=ACCENT,
                         font=FONT_LBL, relief="flat")
        style.map("Custom.Treeview", background=[("selected", ACCENT2)])

        frame = tk.Frame(self.main, bg=CARD)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="Custom.Treeview")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        widths = [50, 160, 50, 80, 80, 90, 70, 80]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        try:
            rows = get_all_students()
            for r in rows:
                tree.insert("", "end", values=(
                    r["Id"], r["Name"], r["Age"],
                    r["Physics"], r["Maths"], r["Chemistry"],
                    r["Total"], r["Average"]
                ))
            tk.Label(self.main, text=f"{len(rows)} record(s) found.",
                     bg=BG, fg=SUBTEXT, font=FONT_BODY).pack(anchor="w", pady=4)
        except mysql.connector.Error as e:
            tk.Label(self.main, text=f"DB Error: {e}", bg=BG,
                     fg=DANGER, font=FONT_BODY).pack(anchor="w")

    # ─────────────────────────────────────
    # 3. SEARCH BY ID
    # ─────────────────────────────────────
    def _show_search(self):
        self._clear_main()
        self._section_title("◉  Search Student by ID")

        sf = tk.Frame(self.main, bg=PANEL, padx=24, pady=16)
        sf.pack(fill="x")

        tk.Label(sf, text="Student ID:", bg=PANEL, fg=SUBTEXT, font=FONT_LBL).pack(side="left")
        self._sv_id = tk.StringVar()
        e = tk.Entry(sf, textvariable=self._sv_id, bg=CARD, fg=TEXT,
                     insertbackground=ACCENT, font=FONT_BODY, width=10,
                     relief="flat", highlightthickness=1,
                     highlightcolor=ACCENT, highlightbackground=BORDER)
        e.pack(side="left", padx=10)
        accent_btn(sf, "Search", self._do_search, width=10).pack(side="left")

        self._search_result = tk.Frame(self.main, bg=BG)
        self._search_result.pack(fill="x", pady=12)

    def _do_search(self):
        for w in self._search_result.winfo_children():
            w.destroy()
        try:
            sid = int(self._sv_id.get())
            row = get_student_by_id(sid)
            if row:
                card = tk.Frame(self._search_result, bg=PANEL, padx=24, pady=16)
                card.pack(fill="x")
                fields = [("ID", row["Id"]), ("Name", row["Name"]),
                          ("Age", row["Age"]), ("Physics", row["Physics"]),
                          ("Maths", row["Maths"]), ("Chemistry", row["Chemistry"]),
                          ("Total", row["Total"]), ("Average", row["Average"])]
                for i, (k, v) in enumerate(fields):
                    tk.Label(card, text=f"{k}:", bg=PANEL, fg=SUBTEXT,
                             font=FONT_LBL, width=12, anchor="w").grid(row=i, column=0, sticky="w", pady=3)
                    tk.Label(card, text=str(v), bg=PANEL, fg=TEXT,
                             font=FONT_BODY, anchor="w").grid(row=i, column=1, sticky="w", pady=3)
            else:
                tk.Label(self._search_result, text=f"No student found with ID {sid}.",
                         bg=BG, fg=WARNING, font=FONT_BODY).pack(anchor="w")
        except ValueError:
            tk.Label(self._search_result, text="Please enter a valid numeric ID.",
                     bg=BG, fg=DANGER, font=FONT_BODY).pack(anchor="w")
        except mysql.connector.Error as e:
            tk.Label(self._search_result, text=f"DB Error: {e}",
                     bg=BG, fg=DANGER, font=FONT_BODY).pack(anchor="w")

    # ─────────────────────────────────────
    # 4. UPDATE
    # ─────────────────────────────────────
    def _show_update(self):
        self._clear_main()
        self._section_title("✎  Update Student")

        top = tk.Frame(self.main, bg=PANEL, padx=24, pady=14)
        top.pack(fill="x")
        tk.Label(top, text="Student ID:", bg=PANEL, fg=SUBTEXT, font=FONT_LBL).pack(side="left")
        self._uv_id = tk.StringVar()
        tk.Entry(top, textvariable=self._uv_id, bg=CARD, fg=TEXT,
                 insertbackground=ACCENT, font=FONT_BODY, width=10,
                 relief="flat", highlightthickness=1,
                 highlightcolor=ACCENT, highlightbackground=BORDER).pack(side="left", padx=10)
        accent_btn(top, "Load", self._do_load_update, width=8).pack(side="left")

        self._update_form = tk.Frame(self.main, bg=BG)
        self._update_form.pack(fill="x", pady=8)

    def _do_load_update(self):
        for w in self._update_form.winfo_children():
            w.destroy()
        try:
            sid = int(self._uv_id.get())
            row = get_student_by_id(sid)
            if not row:
                tk.Label(self._update_form, text=f"No student with ID {sid}.",
                         bg=BG, fg=WARNING, font=FONT_BODY).pack(anchor="w")
                return

            card = tk.Frame(self._update_form, bg=PANEL, padx=24, pady=16)
            card.pack(fill="x")
            card.columnconfigure(1, weight=1)

            tk.Label(card, text="Leave blank to keep existing value.",
                     bg=PANEL, fg=SUBTEXT, font=("Courier New", 9)).grid(
                row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

            self._uu_name, _ = labeled_entry(card, "Name",      1)
            self._uu_age,  _ = labeled_entry(card, "Age",       2)
            self._uu_phy,  _ = labeled_entry(card, "Physics",   3)
            self._uu_mat,  _ = labeled_entry(card, "Maths",     4)
            self._uu_chem, _ = labeled_entry(card, "Chemistry", 5)

            # Pre-fill current values
            self._uu_name.set(row["Name"])
            self._uu_age.set(row["Age"])
            self._uu_phy.set(row["Physics"])
            self._uu_mat.set(row["Maths"])
            self._uu_chem.set(row["Chemistry"])

            self._update_status = tk.Label(self._update_form, text="", bg=BG, font=FONT_BODY)
            self._update_status.pack(anchor="w", pady=4)

            accent_btn(self._update_form, "Save Changes",
                       lambda s=sid: self._do_update(s), color=WARNING).pack(anchor="w")

        except ValueError:
            tk.Label(self._update_form, text="Enter a valid numeric ID.",
                     bg=BG, fg=DANGER, font=FONT_BODY).pack(anchor="w")

    def _do_update(self, sid):
        try:
            name = self._uu_name.get().strip() or None
            age  = int(self._uu_age.get())  if self._uu_age.get().strip()  else None
            phy  = float(self._uu_phy.get()) if self._uu_phy.get().strip()  else None
            mat  = float(self._uu_mat.get()) if self._uu_mat.get().strip()  else None
            chem = float(self._uu_chem.get())if self._uu_chem.get().strip() else None
            result = update_student(sid, name, age, phy, mat, chem)
            if result is None:
                self._update_status.config(fg=WARNING, text="Student not found.")
            else:
                total, avg = result
                self._update_status.config(
                    fg=SUCCESS,
                    text=f"✔  Updated!  New Total: {total}  |  New Average: {avg}"
                )
        except mysql.connector.Error as e:
            self._update_status.config(fg=DANGER, text=f"DB Error: {e}")
        except ValueError as e:
            self._update_status.config(fg=WARNING, text=f"Input Error: {e}")

    # ─────────────────────────────────────
    # 5. DELETE
    # ─────────────────────────────────────
    def _show_delete(self):
        self._clear_main()
        self._section_title("✕  Delete Student", color=DANGER)

        card = tk.Frame(self.main, bg=PANEL, padx=24, pady=20)
        card.pack(fill="x")

        tk.Label(card, text="Student ID:", bg=PANEL, fg=SUBTEXT, font=FONT_LBL).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self._dv_id = tk.StringVar()
        tk.Entry(card, textvariable=self._dv_id, bg=CARD, fg=TEXT,
                 insertbackground=ACCENT, font=FONT_BODY, width=14,
                 relief="flat", highlightthickness=1,
                 highlightcolor=ACCENT, highlightbackground=BORDER).grid(
            row=0, column=1, sticky="ew", pady=6)

        self._delete_status = tk.Label(self.main, text="", bg=BG, font=FONT_BODY)
        self._delete_status.pack(anchor="w", pady=6)

        accent_btn(self.main, "Delete Student", self._do_delete, color=DANGER).pack(anchor="w")

    def _do_delete(self):
        try:
            sid = int(self._dv_id.get())
            row = get_student_by_id(sid)
            if not row:
                self._delete_status.config(fg=WARNING, text=f"No student with ID {sid}.")
                return
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete student '{row['Name']}' (ID {sid})?\nThis cannot be undone."
            )
            if confirm:
                name = delete_student(sid)
                self._delete_status.config(
                    fg=SUCCESS, text=f"✔  '{name}' (ID {sid}) deleted successfully."
                )
                self._dv_id.set("")
        except ValueError:
            self._delete_status.config(fg=DANGER, text="Enter a valid numeric ID.")
        except mysql.connector.Error as e:
            self._delete_status.config(fg=DANGER, text=f"DB Error: {e}")


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()