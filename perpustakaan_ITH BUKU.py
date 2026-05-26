"""
Sistem Layanan Perpustakaan ITH
Ujian Akhir Semester - Struktur Data 2024/2025

Struktur Data yang digunakan:
- Dictionary (Hash Map) : penyimpanan data mahasiswa dengan NIM sebagai kunci -> O(1) lookup
- List (Array)          : penyimpanan koleksi buku
- List (Array)          : penyimpanan data peminjaman aktif
- List (Array)          : penyimpanan riwayat pengembalian

Cara menjalankan:
    python perpustakaan_ITH.py

Requirements:
    Python 3.x (tkinter sudah termasuk bawaan Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


# ============================================================
#  DATABASE (in-memory)
# ============================================================

# Array of dict untuk data buku
daftar_buku = [
    {"kode": "BK001", "judul": "Algoritma dan Pemrograman",        "penulis": "Rinaldi Munir",    "penerbit": "Informatika",        "tahun": 2021, "jenis": "Buku Teks",             "stok": 3, "tersedia": 3},
    {"kode": "BK002", "judul": "Struktur Data dan Algoritma",       "penulis": "Moh. Sjukani",     "penerbit": "Mitra Wacana Media", "tahun": 2020, "jenis": "Buku Referensi",        "stok": 2, "tersedia": 2},
    {"kode": "BK003", "judul": "Pemrograman Python Dasar",          "penulis": "Agus Kurniawan",   "penerbit": "Elex Media",         "tahun": 2022, "jenis": "Buku Teks",             "stok": 4, "tersedia": 4},
    {"kode": "BK004", "judul": "Matematika Diskrit",                "penulis": "Rinaldi Munir",    "penerbit": "Informatika",        "tahun": 2019, "jenis": "Buku Referensi",        "stok": 2, "tersedia": 2},
    {"kode": "BK005", "judul": "Basis Data",                        "penulis": "Fathansyah",       "penerbit": "Informatika",        "tahun": 2018, "jenis": "Buku Referensi",        "stok": 3, "tersedia": 3},
    {"kode": "BK006", "judul": "Jaringan Komputer",                 "penulis": "James F. Kurose",  "penerbit": "Erlangga",           "tahun": 2021, "jenis": "Buku Teks",             "stok": 2, "tersedia": 2},
    {"kode": "BK007", "judul": "Kecerdasan Buatan",                 "penulis": "Rich & Knight",    "penerbit": "McGraw-Hill",        "tahun": 2019, "jenis": "Buku Referensi",        "stok": 1, "tersedia": 1},
    {"kode": "BK008", "judul": "Sistem Operasi",                    "penulis": "William Stallings","penerbit": "Prentice Hall",      "tahun": 2020, "jenis": "Buku Referensi",        "stok": 2, "tersedia": 2},
    {"kode": "BK009", "judul": "Pengembangan Sistem Informasi Perpustakaan Digital", "penulis": "Ahmad Fauzi", "penerbit": "ITH Press", "tahun": 2023, "jenis": "Tugas Akhir Mahasiswa", "stok": 1, "tersedia": 1},
    {"kode": "BK010", "judul": "Rekayasa Perangkat Lunak",          "penulis": "Ian Sommerville",  "penerbit": "Erlangga",           "tahun": 2022, "jenis": "Buku Teks",             "stok": 2, "tersedia": 2},
    {"kode": "BK011", "judul": "Biografi B.J. Habibie",             "penulis": "Tim Penulis",      "penerbit": "Gramedia",           "tahun": 2018, "jenis": "Buku Biografi",         "stok": 2, "tersedia": 2},
    {"kode": "BK012", "judul": "Kalkulus Jilid 1",                  "penulis": "James Stewart",    "penerbit": "Erlangga",           "tahun": 2020, "jenis": "Buku Teks",             "stok": 3, "tersedia": 3},
]

# Hash Map (dictionary) untuk data mahasiswa — NIM sebagai kunci, akses O(1)
data_mahasiswa = {}

# Array untuk peminjaman aktif & riwayat
peminjaman_aktif = []
riwayat_pengembalian = []
pinjam_counter = [1]  # pakai list agar bisa dimodifikasi dari dalam fungsi


# ============================================================
#  HELPER
# ============================================================

def today_str():
    return datetime.today().strftime("%Y-%m-%d")

def fmt_tgl(d):
    if not d:
        return "-"
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except:
        return d

def add_days(d, n):
    dt = datetime.strptime(d, "%Y-%m-%d")
    return (dt + timedelta(days=n)).strftime("%Y-%m-%d")

def diff_days(a, b):
    da = datetime.strptime(a, "%Y-%m-%d")
    db = datetime.strptime(b, "%Y-%m-%d")
    return (da - db).days

def cari_buku(kode):
    for b in daftar_buku:
        if b["kode"] == kode:
            return b
    return None

def gen_kode_buku():
    return "BK" + str(len(daftar_buku) + 1).zfill(3)

def gen_id_pinjam():
    id_ = "P" + str(pinjam_counter[0]).zfill(4)
    pinjam_counter[0] += 1
    return id_


# ============================================================
#  APLIKASI UTAMA
# ============================================================

class PerpustakaanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Perpustakaan ITH")
        self.root.geometry("1100x680")
        self.root.configure(bg="#F0EDE8")
        self.root.resizable(True, True)

        self._setup_style()
        self._build_ui()
        self.show_tab("dashboard")

    # ----------------------------------------------------------
    #  STYLE
    # ----------------------------------------------------------
    def _setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Warna utama
        BG       = "#F0EDE8"
        WHITE    = "#FFFFFF"
        BORDER   = "#E0DDD8"
        ACCENT   = "#185FA5"
        TEXT     = "#1A1A1A"
        TEXT2    = "#666666"
        HOVER    = "#E6F1FB"

        self.style.configure("TFrame", background=BG)
        self.style.configure("White.TFrame", background=WHITE)

        # Notebook (tab)
        self.style.configure("TNotebook", background=BG, borderwidth=0)
        self.style.configure("TNotebook.Tab",
            background=WHITE, foreground=TEXT2,
            padding=[14, 8], font=("Helvetica", 10),
            borderwidth=0)
        self.style.map("TNotebook.Tab",
            background=[("selected", ACCENT), ("active", HOVER)],
            foreground=[("selected", WHITE), ("active", ACCENT)])

        # Treeview (tabel)
        self.style.configure("Treeview",
            background=WHITE, foreground=TEXT,
            rowheight=30, fieldbackground=WHITE,
            font=("Helvetica", 10), borderwidth=0)
        self.style.configure("Treeview.Heading",
            background="#F5F5F0", foreground=TEXT2,
            font=("Helvetica", 9, "bold"), relief="flat", padding=[6, 5])
        self.style.map("Treeview",
            background=[("selected", HOVER)],
            foreground=[("selected", ACCENT)])

        # Button
        self.style.configure("Primary.TButton",
            background=ACCENT, foreground=WHITE,
            font=("Helvetica", 10, "bold"), padding=[12, 6],
            relief="flat", borderwidth=0)
        self.style.map("Primary.TButton",
            background=[("active", "#0C447C")])

        self.style.configure("Danger.TButton",
            background="#FCEBEB", foreground="#A32D2D",
            font=("Helvetica", 9), padding=[8, 4],
            relief="flat", borderwidth=0)
        self.style.map("Danger.TButton",
            background=[("active", "#F7C1C1")])

        self.style.configure("Success.TButton",
            background="#EAF3DE", foreground="#3B6D11",
            font=("Helvetica", 9), padding=[8, 4],
            relief="flat", borderwidth=0)
        self.style.map("Success.TButton",
            background=[("active", "#C0DD97")])

        # Entry & Label
        self.style.configure("TEntry",
            padding=[6, 5], relief="flat",
            fieldbackground="#FAFAFA", font=("Helvetica", 10))
        self.style.configure("TCombobox",
            padding=[6, 5], relief="flat",
            font=("Helvetica", 10))
        self.style.configure("TLabel",
            background=WHITE, foreground=TEXT,
            font=("Helvetica", 10))
        self.style.configure("Title.TLabel",
            background=WHITE, foreground=TEXT,
            font=("Helvetica", 13, "bold"))
        self.style.configure("Sub.TLabel",
            background=WHITE, foreground=TEXT2,
            font=("Helvetica", 9))
        self.style.configure("StatVal.TLabel",
            background="#F0EDE8", foreground=TEXT,
            font=("Helvetica", 22, "bold"))
        self.style.configure("StatLbl.TLabel",
            background="#F0EDE8", foreground=TEXT2,
            font=("Helvetica", 9))
        self.style.configure("Header.TLabel",
            background="#1A1A1A", foreground=WHITE,
            font=("Helvetica", 11, "bold"),
            padding=[16, 10])
        self.style.configure("Sidebar.TFrame", background="#1A1A1A")

        self.ACCENT = ACCENT
        self.WHITE  = WHITE
        self.BG     = BG
        self.TEXT   = TEXT
        self.TEXT2  = TEXT2
        self.BORDER = BORDER

    # ----------------------------------------------------------
    #  BUILD UI
    # ----------------------------------------------------------
    def _build_ui(self):
        # Header bar
        header = tk.Frame(self.root, bg="#1A1A1A", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📚  Sistem Perpustakaan ITH",
                 bg="#1A1A1A", fg="white",
                 font=("Helvetica", 13, "bold")).pack(side="left", padx=16, pady=12)
        self.lbl_date = tk.Label(header, text="", bg="#1A1A1A", fg="#888888",
                                 font=("Helvetica", 9))
        self.lbl_date.pack(side="right", padx=16)
        self.lbl_date.config(text=datetime.today().strftime("%A, %d %B %Y"))

        # Body
        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg="#1E1E1E", width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.nav_buttons = {}
        nav_items = [
            ("dashboard",  "🏠  Dashboard"),
            ("buku",       "📚  Data Buku"),
            ("mahasiswa",  "👥  Mahasiswa"),
            ("pinjam",     "📖  Peminjaman"),
            ("kembali",    "📤  Pengembalian"),
            ("riwayat",    "🕐  Riwayat"),
        ]
        tk.Label(sidebar, text="MENU", bg="#1E1E1E", fg="#555555",
                 font=("Helvetica", 8, "bold")).pack(anchor="w", padx=16, pady=(16, 6))

        for key, label in nav_items:
            btn = tk.Button(sidebar, text=label, anchor="w",
                            bg="#1E1E1E", fg="#AAAAAA",
                            font=("Helvetica", 10),
                            relief="flat", bd=0,
                            padx=16, pady=9, cursor="hand2",
                            command=lambda k=key: self.show_tab(k))
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2A2A2A", fg="white") if b.cget("bg") != self.ACCENT else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1E1E1E", fg="#AAAAAA") if b.cget("bg") != self.ACCENT else None)
            self.nav_buttons[key] = btn

        # Content area
        self.content = tk.Frame(body, bg=self.BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Buat semua frame tab
        self.frames = {}
        self.frames["dashboard"] = self._build_dashboard()
        self.frames["buku"]      = self._build_buku()
        self.frames["mahasiswa"] = self._build_mahasiswa()
        self.frames["pinjam"]    = self._build_pinjam()
        self.frames["kembali"]   = self._build_kembali()
        self.frames["riwayat"]   = self._build_riwayat()

        for f in self.frames.values():
            f.place(relwidth=1, relheight=1)

    def show_tab(self, name):
        for key, btn in self.nav_buttons.items():
            if key == name:
                btn.config(bg=self.ACCENT, fg="white")
            else:
                btn.config(bg="#1E1E1E", fg="#AAAAAA")

        self.frames[name].lift()

        refresh = {
            "dashboard": self.refresh_dashboard,
            "buku":      self.refresh_buku,
            "mahasiswa": self.refresh_mahasiswa,
            "pinjam":    self.refresh_pinjam,
            "kembali":   self.refresh_kembali,
            "riwayat":   self.refresh_riwayat,
        }
        refresh[name]()

    # ----------------------------------------------------------
    #  HELPER UI
    # ----------------------------------------------------------
    def _card(self, parent, title=None):
        outer = tk.Frame(parent, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=14, pady=8)

        card = tk.Frame(outer, bg=self.WHITE,
                        highlightbackground=self.BORDER,
                        highlightthickness=1)
        card.pack(fill="both", expand=True)

        if title:
            tk.Label(card, text=title, bg=self.WHITE, fg=self.TEXT,
                     font=("Helvetica", 11, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
            ttk.Separator(card, orient="horizontal").pack(fill="x", padx=14)

        return card

    def _treeview(self, parent, columns, col_widths):
        frame = tk.Frame(parent, bg=self.WHITE)
        frame.pack(fill="both", expand=True, padx=14, pady=8)

        scroll_y = ttk.Scrollbar(frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        tv = ttk.Treeview(frame, columns=columns, show="headings",
                          yscrollcommand=scroll_y.set,
                          xscrollcommand=scroll_x.set)
        tv.pack(fill="both", expand=True)

        scroll_y.config(command=tv.yview)
        scroll_x.config(command=tv.xview)

        for col, w in zip(columns, col_widths):
            tv.heading(col, text=col)
            tv.column(col, width=w, minwidth=60)

        tv.tag_configure("overdue", background="#FFF0F0")
        tv.tag_configure("ok",      background=self.WHITE)

        return tv

    def _form_row(self, parent, label, widget_type="entry", values=None, default=""):
        row = tk.Frame(parent, bg=self.WHITE)
        row.pack(fill="x", padx=14, pady=4)
        tk.Label(row, text=label, bg=self.WHITE, fg=self.TEXT2,
                 font=("Helvetica", 9, "bold"), width=22, anchor="w").pack(side="left")

        if widget_type == "entry":
            var = tk.StringVar(value=default)
            e = ttk.Entry(row, textvariable=var, width=30)
            e.pack(side="left", fill="x", expand=True)
            return var

        elif widget_type == "combo":
            var = tk.StringVar(value=default or (values[0] if values else ""))
            cb = ttk.Combobox(row, textvariable=var, values=values, width=28, state="readonly")
            cb.pack(side="left", fill="x", expand=True)
            return var

        elif widget_type == "spinbox":
            var = tk.IntVar(value=int(default) if default else 1)
            sb = tk.Spinbox(row, textvariable=var, from_=1, to=9999,
                            width=10, relief="flat", bg="#FAFAFA",
                            font=("Helvetica", 10))
            sb.pack(side="left")
            return var

    def _stat_card(self, parent, label, value_var, col):
        f = tk.Frame(parent, bg="#F0EDE8", padx=16, pady=12)
        f.grid(row=0, column=col, sticky="nsew", padx=6, pady=6)
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(f, text=label, bg="#F0EDE8", fg=self.TEXT2,
                 font=("Helvetica", 9)).pack(anchor="w")
        tk.Label(f, textvariable=value_var, bg="#F0EDE8", fg=self.TEXT,
                 font=("Helvetica", 22, "bold")).pack(anchor="w")

    # ----------------------------------------------------------
    #  DASHBOARD
    # ----------------------------------------------------------
    def _build_dashboard(self):
        frame = tk.Frame(self.content, bg=self.BG)

        # Header
        hdr = tk.Frame(frame, bg=self.BG)
        hdr.pack(fill="x", padx=14, pady=(14, 4))
        tk.Label(hdr, text="Dashboard", bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 14, "bold")).pack(side="left")

        # Stats
        stat_frame = tk.Frame(frame, bg=self.BG)
        stat_frame.pack(fill="x", padx=14, pady=(0, 8))

        self.sv_buku   = tk.StringVar(value="0")
        self.sv_mhs    = tk.StringVar(value="0")
        self.sv_pinjam = tk.StringVar(value="0")
        self.sv_telat  = tk.StringVar(value="0")

        self._stat_card(stat_frame, "Total Buku",   self.sv_buku,   0)
        self._stat_card(stat_frame, "Mahasiswa",    self.sv_mhs,    1)
        self._stat_card(stat_frame, "Dipinjam",     self.sv_pinjam, 2)
        self._stat_card(stat_frame, "Terlambat",    self.sv_telat,  3)

        # Tabel peminjaman aktif
        card = self._card(frame, "Peminjaman Aktif")
        cols = ["NIM", "Nama", "Judul Buku", "Tgl Pinjam", "Batas Kembali", "Status"]
        ws   = [100, 160, 260, 100, 110, 90]
        self.tv_dash = self._treeview(card, cols, ws)

        return frame

    def refresh_dashboard(self):
        self.sv_buku.set(str(len(daftar_buku)))
        self.sv_mhs.set(str(len(data_mahasiswa)))
        self.sv_pinjam.set(str(len(peminjaman_aktif)))
        tod = today_str()
        telat = sum(1 for p in peminjaman_aktif if diff_days(tod, p["batas"]) > 0)
        self.sv_telat.set(str(telat))

        for row in self.tv_dash.get_children():
            self.tv_dash.delete(row)

        for p in reversed(peminjaman_aktif[:8]):
            late   = diff_days(tod, p["batas"]) > 0
            status = "Terlambat" if late else "Aktif"
            tag    = "overdue" if late else "ok"
            self.tv_dash.insert("", "end", values=(
                p["nim"], p["nama"], p["judul"],
                fmt_tgl(p["tgl"]), fmt_tgl(p["batas"]), status
            ), tags=(tag,))

    # ----------------------------------------------------------
    #  DATA BUKU
    # ----------------------------------------------------------
    def _build_buku(self):
        frame = tk.Frame(self.content, bg=self.BG)

        # Toolbar
        tb = tk.Frame(frame, bg=self.BG)
        tb.pack(fill="x", padx=14, pady=(14, 6))
        tk.Label(tb, text="Data Buku", bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(tb, text="+ Tambah Buku", style="Primary.TButton",
                   command=self.modal_tambah_buku).pack(side="right")

        # Cari
        cari_frame = tk.Frame(frame, bg=self.BG)
        cari_frame.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(cari_frame, text="Cari:", bg=self.BG, fg=self.TEXT2,
                 font=("Helvetica", 9)).pack(side="left")
        self.sv_cari_buku = tk.StringVar()
        self.sv_cari_buku.trace_add("write", lambda *_: self.refresh_buku())
        ttk.Entry(cari_frame, textvariable=self.sv_cari_buku, width=40).pack(side="left", padx=6)

        # Tabel
        card = self._card(frame)
        cols = ["Kode", "Judul Buku", "Penulis", "Penerbit", "Tahun", "Jenis", "Tersedia/Stok"]
        ws   = [70, 240, 160, 140, 60, 140, 100]
        self.tv_buku = self._treeview(card, cols, ws)

        # Tombol aksi bawah tabel
        ak = tk.Frame(card, bg=self.WHITE)
        ak.pack(fill="x", padx=14, pady=6)
        ttk.Button(ak, text="🗑  Hapus Terpilih", style="Danger.TButton",
                   command=self.hapus_buku).pack(side="left")

        return frame

    def refresh_buku(self):
        q = self.sv_cari_buku.get().lower()
        for row in self.tv_buku.get_children():
            self.tv_buku.delete(row)
        for b in daftar_buku:
            if q in b["judul"].lower() or q in b["penulis"].lower() or q in b["penerbit"].lower():
                self.tv_buku.insert("", "end", iid=b["kode"], values=(
                    b["kode"], b["judul"], b["penulis"],
                    b["penerbit"], b["tahun"], b["jenis"],
                    f"{b['tersedia']} / {b['stok']}"
                ))

    def modal_tambah_buku(self):
        win = tk.Toplevel(self.root)
        win.title("Tambah Buku")
        win.geometry("460x380")
        win.configure(bg=self.WHITE)
        win.grab_set()

        tk.Label(win, text="Tambah Buku Baru", bg=self.WHITE, fg=self.TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 10))
        ttk.Separator(win, orient="horizontal").pack(fill="x", padx=16, pady=(0, 10))

        v_judul    = self._form_row(win, "Judul Buku")
        v_penulis  = self._form_row(win, "Penulis")
        v_penerbit = self._form_row(win, "Penerbit")
        v_tahun    = self._form_row(win, "Tahun Terbit", default=str(datetime.today().year))
        v_jenis    = self._form_row(win, "Jenis Buku", "combo",
                        ["Buku Teks", "Buku Referensi", "Buku Biografi",
                         "Tugas Akhir Mahasiswa", "Jurnal Ilmiah", "Fiksi", "Lainnya"])
        v_stok     = self._form_row(win, "Jumlah Stok", "spinbox", default="1")

        def simpan():
            judul    = v_judul.get().strip()
            penulis  = v_penulis.get().strip()
            penerbit = v_penerbit.get().strip()
            jenis    = v_jenis.get()
            try:
                tahun = int(v_tahun.get())
                stok  = int(v_stok.get())
            except:
                messagebox.showerror("Error", "Tahun dan stok harus berupa angka!", parent=win)
                return

            if not judul or not penulis or not penerbit:
                messagebox.showerror("Error", "Harap isi semua field!", parent=win)
                return

            kode = gen_kode_buku()
            daftar_buku.append({
                "kode": kode, "judul": judul, "penulis": penulis,
                "penerbit": penerbit, "tahun": tahun, "jenis": jenis,
                "stok": stok, "tersedia": stok
            })
            win.destroy()
            self.refresh_buku()
            self.refresh_dashboard()
            messagebox.showinfo("Berhasil", f"Buku '{judul}' ({kode}) berhasil ditambahkan!")

        btn_frame = tk.Frame(win, bg=self.WHITE)
        btn_frame.pack(fill="x", padx=16, pady=14)
        ttk.Button(btn_frame, text="Batal",  command=win.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(btn_frame, text="Simpan", style="Primary.TButton", command=simpan).pack(side="right")

    def hapus_buku(self):
        sel = self.tv_buku.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin dihapus!")
            return
        kode = sel[0]
        if messagebox.askyesno("Konfirmasi", f"Hapus buku {kode}?"):
            global daftar_buku
            daftar_buku = [b for b in daftar_buku if b["kode"] != kode]
            self.refresh_buku()
            self.refresh_dashboard()

    # ----------------------------------------------------------
    #  DATA MAHASISWA (Hash Map)
    # ----------------------------------------------------------
    def _build_mahasiswa(self):
        frame = tk.Frame(self.content, bg=self.BG)

        tb = tk.Frame(frame, bg=self.BG)
        tb.pack(fill="x", padx=14, pady=(14, 6))
        tk.Label(tb, text="Data Mahasiswa", bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(tb, text="+ Tambah Mahasiswa", style="Primary.TButton",
                   command=self.modal_tambah_mhs).pack(side="right")

        cari_frame = tk.Frame(frame, bg=self.BG)
        cari_frame.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(cari_frame, text="Cari:", bg=self.BG, fg=self.TEXT2,
                 font=("Helvetica", 9)).pack(side="left")
        self.sv_cari_mhs = tk.StringVar()
        self.sv_cari_mhs.trace_add("write", lambda *_: self.refresh_mahasiswa())
        ttk.Entry(cari_frame, textvariable=self.sv_cari_mhs, width=40).pack(side="left", padx=6)

        card = self._card(frame)
        cols = ["NIM", "Nama", "Program Studi", "Angkatan", "Status Pinjam"]
        ws   = [100, 200, 180, 80, 120]
        self.tv_mhs = self._treeview(card, cols, ws)

        ak = tk.Frame(card, bg=self.WHITE)
        ak.pack(fill="x", padx=14, pady=6)
        ttk.Button(ak, text="🗑  Hapus Terpilih", style="Danger.TButton",
                   command=self.hapus_mhs).pack(side="left")

        return frame

    def refresh_mahasiswa(self):
        q = self.sv_cari_mhs.get().lower()
        for row in self.tv_mhs.get_children():
            self.tv_mhs.delete(row)
        for nim, m in data_mahasiswa.items():
            if q in nim or q in m["nama"].lower():
                aktif = sum(1 for p in peminjaman_aktif if p["nim"] == nim)
                status = f"Pinjam {aktif}" if aktif > 0 else "Aktif"
                self.tv_mhs.insert("", "end", iid=nim, values=(
                    nim, m["nama"], m["prodi"], m["angkatan"], status
                ))

    def modal_tambah_mhs(self):
        win = tk.Toplevel(self.root)
        win.title("Tambah Mahasiswa")
        win.geometry("440x300")
        win.configure(bg=self.WHITE)
        win.grab_set()

        tk.Label(win, text="Tambah Mahasiswa Baru", bg=self.WHITE, fg=self.TEXT,
                 font=("Helvetica", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 10))
        ttk.Separator(win, orient="horizontal").pack(fill="x", padx=16, pady=(0, 10))

        v_nim      = self._form_row(win, "NIM")
        v_nama     = self._form_row(win, "Nama Lengkap")
        v_prodi    = self._form_row(win, "Program Studi", "combo",
                        ["Ilmu Komputer", "Teknik Informatika", "Sistem Informasi",
                         "Teknik Elektro", "Teknik Mesin", "Manajemen", "Akuntansi"])
        v_angkatan = self._form_row(win, "Angkatan", default=str(datetime.today().year))

        def simpan():
            nim      = v_nim.get().strip()
            nama     = v_nama.get().strip()
            prodi    = v_prodi.get()
            try:
                angkatan = int(v_angkatan.get())
            except:
                messagebox.showerror("Error", "Angkatan harus berupa angka!", parent=win)
                return

            if not nim or not nama:
                messagebox.showerror("Error", "Harap isi semua field!", parent=win)
                return
            # Cek duplikat NIM — O(1) karena hash map
            if nim in data_mahasiswa:
                messagebox.showerror("Error", f"NIM {nim} sudah terdaftar!", parent=win)
                return

            data_mahasiswa[nim] = {"nim": nim, "nama": nama, "prodi": prodi, "angkatan": angkatan}
            win.destroy()
            self.refresh_mahasiswa()
            self.refresh_dashboard()
            messagebox.showinfo("Berhasil", f"Mahasiswa {nama} ({nim}) berhasil didaftarkan!")

        btn_frame = tk.Frame(win, bg=self.WHITE)
        btn_frame.pack(fill="x", padx=16, pady=14)
        ttk.Button(btn_frame, text="Batal",  command=win.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(btn_frame, text="Simpan", style="Primary.TButton", command=simpan).pack(side="right")

    def hapus_mhs(self):
        sel = self.tv_mhs.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih mahasiswa yang ingin dihapus!")
            return
        nim = sel[0]
        if messagebox.askyesno("Konfirmasi", f"Hapus mahasiswa {nim}?"):
            del data_mahasiswa[nim]
            self.refresh_mahasiswa()
            self.refresh_dashboard()

    # ----------------------------------------------------------
    #  PEMINJAMAN
    # ----------------------------------------------------------
    def _build_pinjam(self):
        frame = tk.Frame(self.content, bg=self.BG)

        tk.Label(frame, text="Peminjaman", bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 14, "bold")).pack(anchor="w", padx=14, pady=(14, 8))

        # Form catat pinjam
        form_card = self._card(frame, "Catat Peminjaman Baru")

        self.sv_pinjam_nim   = self._form_row(form_card, "NIM Mahasiswa")
        self.sv_pinjam_nim.trace_add("write", lambda *_: self._autofill_mhs())

        self.lbl_mhs_info = tk.Label(form_card, text="", bg=self.WHITE,
                                     fg="#185FA5", font=("Helvetica", 9))
        self.lbl_mhs_info.pack(anchor="w", padx=14, pady=(0, 4))

        # Dropdown buku tersedia
        row = tk.Frame(form_card, bg=self.WHITE)
        row.pack(fill="x", padx=14, pady=4)
        tk.Label(row, text="Buku", bg=self.WHITE, fg=self.TEXT2,
                 font=("Helvetica", 9, "bold"), width=22, anchor="w").pack(side="left")
        self.sv_pinjam_buku = tk.StringVar()
        self.cb_buku = ttk.Combobox(row, textvariable=self.sv_pinjam_buku, width=46, state="readonly")
        self.cb_buku.pack(side="left")
        self.cb_buku.bind("<<ComboboxSelected>>", lambda _: self._autofill_buku())

        self.lbl_buku_info = tk.Label(form_card, text="", bg=self.WHITE,
                                      fg="#185FA5", font=("Helvetica", 9))
        self.lbl_buku_info.pack(anchor="w", padx=14, pady=(0, 4))

        self.sv_tgl_pinjam = self._form_row(form_card, "Tanggal Pinjam",  default=today_str())
        self.sv_tgl_batas  = self._form_row(form_card, "Batas Pengembalian", default=add_days(today_str(), 7))

        ttk.Button(form_card, text="✔  Catat Peminjaman",
                   style="Primary.TButton",
                   command=self.catat_pinjam).pack(anchor="w", padx=14, pady=10)

        # Tabel pinjam aktif
        card2 = self._card(frame, "Daftar Peminjaman Aktif")
        cols  = ["ID", "NIM", "Nama", "Judul Buku", "Tgl Pinjam", "Batas Kembali", "Status"]
        ws    = [70, 95, 150, 230, 95, 110, 90]
        self.tv_pinjam = self._treeview(card2, cols, ws)

        return frame

    def _autofill_mhs(self):
        nim = self.sv_pinjam_nim.get().strip()
        m   = data_mahasiswa.get(nim)  # O(1) hash map lookup
        if m:
            self.lbl_mhs_info.config(text=f"✓  {m['nama']} — {m['prodi']}")
        else:
            self.lbl_mhs_info.config(text="NIM tidak ditemukan" if len(nim) > 4 else "")

    def _autofill_buku(self):
        val = self.sv_pinjam_buku.get()
        if val:
            kode = val.split(" — ")[0]
            b    = cari_buku(kode)
            if b:
                self.lbl_buku_info.config(text=f"{b['jenis']} · {b['tersedia']} stok tersedia")

    def refresh_pinjam(self):
        # Update dropdown buku tersedia
        avail = [f"{b['kode']} — {b['judul']} ({b['tersedia']} tersedia)"
                 for b in daftar_buku if b["tersedia"] > 0]
        self.cb_buku["values"] = avail

        # Update tabel
        tod = today_str()
        for row in self.tv_pinjam.get_children():
            self.tv_pinjam.delete(row)
        for p in peminjaman_aktif:
            late   = diff_days(tod, p["batas"]) > 0
            status = "Terlambat" if late else "Aktif"
            tag    = "overdue" if late else "ok"
            self.tv_pinjam.insert("", "end", values=(
                p["id"], p["nim"], p["nama"], p["judul"],
                fmt_tgl(p["tgl"]), fmt_tgl(p["batas"]), status
            ), tags=(tag,))

    def catat_pinjam(self):
        nim       = self.sv_pinjam_nim.get().strip()
        buku_val  = self.sv_pinjam_buku.get()
        tgl       = self.sv_tgl_pinjam.get().strip()
        batas     = self.sv_tgl_batas.get().strip()

        if not nim or not buku_val or not tgl or not batas:
            messagebox.showerror("Error", "Harap isi semua field!")
            return

        mhs = data_mahasiswa.get(nim)
        if not mhs:
            messagebox.showerror("Error", "NIM tidak ditemukan di database!")
            return

        kode = buku_val.split(" — ")[0]
        buku = cari_buku(kode)
        if not buku or buku["tersedia"] < 1:
            messagebox.showerror("Error", "Buku tidak tersedia!")
            return

        id_pinjam = gen_id_pinjam()
        peminjaman_aktif.append({
            "id": id_pinjam, "nim": nim, "nama": mhs["nama"],
            "kode": kode, "judul": buku["judul"],
            "tgl": tgl, "batas": batas
        })
        buku["tersedia"] -= 1

        self.sv_pinjam_nim.set("")
        self.sv_pinjam_buku.set("")
        self.lbl_mhs_info.config(text="")
        self.lbl_buku_info.config(text="")

        self.refresh_pinjam()
        self.refresh_dashboard()
        messagebox.showinfo("Berhasil",
            f"Peminjaman {id_pinjam} berhasil dicatat!\nBatas kembali: {fmt_tgl(batas)}")

    # ----------------------------------------------------------
    #  PENGEMBALIAN
    # ----------------------------------------------------------
    def _build_kembali(self):
        frame = tk.Frame(self.content, bg=self.BG)

        tk.Label(frame, text="Pengembalian", bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 14, "bold")).pack(anchor="w", padx=14, pady=(14, 8))

        # Filter
        fil = tk.Frame(frame, bg=self.BG)
        fil.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(fil, text="Cari ID / NIM:", bg=self.BG, fg=self.TEXT2,
                 font=("Helvetica", 9)).pack(side="left")
        self.sv_cari_kembali = tk.StringVar()
        self.sv_cari_kembali.trace_add("write", lambda *_: self.refresh_kembali())
        ttk.Entry(fil, textvariable=self.sv_cari_kembali, width=30).pack(side="left", padx=6)

        tk.Label(fil, text="Tgl Kembali:", bg=self.BG, fg=self.TEXT2,
                 font=("Helvetica", 9)).pack(side="left", padx=(16, 0))
        self.sv_tgl_kembali = tk.StringVar(value=today_str())
        self.sv_tgl_kembali.trace_add("write", lambda *_: self.refresh_kembali())
        ttk.Entry(fil, textvariable=self.sv_tgl_kembali, width=12).pack(side="left", padx=6)

        card = self._card(frame)
        cols = ["ID", "NIM", "Nama", "Judul Buku", "Batas Kembali", "Keterlambatan", "Denda"]
        ws   = [70, 95, 150, 230, 110, 110, 100]
        self.tv_kembali = self._treeview(card, cols, ws)

        ak = tk.Frame(card, bg=self.WHITE)
        ak.pack(fill="x", padx=14, pady=6)
        ttk.Button(ak, text="✔  Proses Pengembalian", style="Success.TButton",
                   command=self.proses_kembali).pack(side="left")

        return frame

    def refresh_kembali(self):
        q           = self.sv_cari_kembali.get().lower()
        tgl_kembali = self.sv_tgl_kembali.get().strip() or today_str()
        for row in self.tv_kembali.get_children():
            self.tv_kembali.delete(row)
        for p in peminjaman_aktif:
            if q in p["id"].lower() or q in p["nim"] or q in p["nama"].lower():
                try:
                    late  = diff_days(tgl_kembali, p["batas"])
                    denda = late * 1000 if late > 0 else 0
                except:
                    late, denda = 0, 0
                tag    = "overdue" if late > 0 else "ok"
                ket    = f"{late} hari" if late > 0 else "-"
                d_str  = f"Rp {denda:,}".replace(",", ".") if denda > 0 else "-"
                self.tv_kembali.insert("", "end", iid=p["id"], values=(
                    p["id"], p["nim"], p["nama"], p["judul"],
                    fmt_tgl(p["batas"]), ket, d_str
                ), tags=(tag,))

    def proses_kembali(self):
        sel = self.tv_kembali.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih peminjaman yang ingin dikembalikan!")
            return

        id_pinjam   = sel[0]
        tgl_kembali = self.sv_tgl_kembali.get().strip() or today_str()
        idx = next((i for i, p in enumerate(peminjaman_aktif) if p["id"] == id_pinjam), None)
        if idx is None:
            return

        p    = peminjaman_aktif[idx]
        late = diff_days(tgl_kembali, p["batas"])
        denda = late * 1000 if late > 0 else 0

        # Simpan ke riwayat
        riwayat_pengembalian.append({
            **p,
            "tgl_kembali": tgl_kembali,
            "keterlambatan": max(late, 0),
            "denda": denda
        })

        # Tambah kembali stok buku
        b = cari_buku(p["kode"])
        if b:
            b["tersedia"] += 1

        # Hapus dari aktif
        peminjaman_aktif.pop(idx)

        self.refresh_kembali()
        self.refresh_dashboard()

        pesan = f"Buku '{p['judul']}' berhasil dikembalikan."
        if denda > 0:
            pesan += f"\nDenda keterlambatan: Rp {denda:,}".replace(",", ".")
        messagebox.showinfo("Pengembalian Berhasil", pesan)

    # ----------------------------------------------------------
    #  RIWAYAT
    # ----------------------------------------------------------
    def _build_riwayat(self):
        frame = tk.Frame(self.content, bg=self.BG)

        tk.Label(frame, text="Riwayat Pengembalian", bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 14, "bold")).pack(anchor="w", padx=14, pady=(14, 8))

        card = self._card(frame)
        cols = ["ID", "NIM", "Nama", "Judul Buku", "Tgl Pinjam", "Tgl Kembali", "Terlambat", "Denda"]
        ws   = [70, 95, 140, 210, 95, 95, 80, 100]
        self.tv_riwayat = self._treeview(card, cols, ws)

        return frame

    def refresh_riwayat(self):
        for row in self.tv_riwayat.get_children():
            self.tv_riwayat.delete(row)
        for r in reversed(riwayat_pengembalian):
            denda_str = f"Rp {r['denda']:,}".replace(",", ".") if r["denda"] > 0 else "-"
            ket_str   = f"{r['keterlambatan']} hari" if r["keterlambatan"] > 0 else "-"
            tag       = "overdue" if r["denda"] > 0 else "ok"
            self.tv_riwayat.insert("", "end", values=(
                r["id"], r["nim"], r["nama"], r["judul"],
                fmt_tgl(r["tgl"]), fmt_tgl(r["tgl_kembali"]),
                ket_str, denda_str
            ), tags=(tag,))


# ============================================================
#  ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app  = PerpustakaanApp(root)
    root.mainloop()
