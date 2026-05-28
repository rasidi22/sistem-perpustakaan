import os
import sys
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(
    sys.executable if getattr(sys, 'frozen', False)
    else __file__
)

def bst_ke_listBuku(root, data):
    
    if root is not None:
        bst_ke_listBuku(root.left, data)
        
        data.append({
            "kode": root.kode,
            "nama": root.nama,
            "penulis": root.penulis,
            "stok": root.stok
        })
        
        bst_ke_listBuku(root.right, data)
        
def simpan_buku(root):
    data = []
    bst_ke_listBuku(root, data)
    
    with open(os.path.join(BASE_DIR, "data", "buku.json"), "w") as file:
        json.dump(data, file, indent = 4)
        
def load_buku():
    root = None
    
    try:
        with open(os.path.join(BASE_DIR, "data", "buku.json"), 'r') as file:
            data = json.load(file)
            
            for item in data:
                buku = Buku(
                    item['kode'],
                    item['nama'],
                    item['penulis'],
                    item['stok']
                )
                root = insert(root, buku)
    except FileNotFoundError:
        pass
    
    return root

def bst_ke_listMahasiswa(root, data):
    if root is not None:
        bst_ke_listMahasiswa(root.left, data)
        
        data.append({
            "nim": root.nim,
            "nama": root.nama
        })
        bst_ke_listMahasiswa(root.right, data)
        
def simpan_mahasiswa(root):
    data = []
    
    bst_ke_listMahasiswa(root, data)
    
    with open(os.path.join(BASE_DIR, "data", "mahasiswa.json"), "w") as file:
        json.dump(data, file, indent = 4)
    
    
def load_mahasiswa():
    root = None

    try:
        with open(os.path.join(BASE_DIR, "data", "mahasiswa.json") , "r") as file:
            data = json.load(file)

            for item in data:
                mhs = mahasiswa(
                    item["nim"],
                    item["nama"]
                )
                root = insert_mahasiswa(root, mhs)

    except FileNotFoundError:
        pass

    return root



# Binary Search Tree (BST) untuk data buku start
class Buku:
    def __init__(self, kode, nama, penulis, stok):
        self.kode = kode
        self.nama = nama
        self.penulis = penulis
        self.stok = stok
        
        self.left = None
        self.right = None
        
        
def insert(root, buku):
    if root is None:
        return buku
    
    if buku.kode < root.kode:
        root.left = insert(root.left, buku)
    else:
        root.right = insert(root.right, buku)
    
    return root


def cari_buku(root, kode):
    if root is None:
        return None
    
    if kode == root.kode:
        return root
    
    elif kode < root.kode:
        return cari_buku(root.left,kode)
    else:
        return cari_buku(root.right, kode)
    
def tampil_buku(root):
    if root is not None:
        tampil_buku(root.left)
        print("kode :", root.kode)
        print("nama :", root.nama)
        print("penulis :", root.penulis)
        print("stok :", root.stok)
        print("-----------------------------")
        
        tampil_buku(root.right)
    
    

    
# binary search tree untuk data buku end

# binary search tree untuk data mahasiswa start
class mahasiswa:
    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        
        self.right = None
        self.left = None
        
        
def insert_mahasiswa(root, mahasiswa):
    if root is None:
        return mahasiswa
    
    if mahasiswa.nim < root.nim:
        root.left = insert_mahasiswa(root.left, mahasiswa)
    else:
        root.right = insert_mahasiswa(root.right, mahasiswa)
        
    return root

def cari_mahasiswa(root, nim):
    if root is None:
        return None
    
    if nim == root.nim:
        return root
    
    elif nim < root.nim:
        return cari_mahasiswa(root.left, nim)
    else:
        return cari_mahasiswa(root.right, nim)
    
def tampil_mahasiswa(root):
    if root is not None:
        tampil_mahasiswa(root.left)
        print("nama :", root.nama)
        print("nim :", root.nim)
        print("-----------------------------")
        tampil_mahasiswa(root.right)
        

root_mahasiswa = load_mahasiswa()

# binary search tree untuk data mahasiswa end

# fitur peminjaman buku start
peminjaman = []

def pinjam_buku(root_buku, root_mahasiswa):
    
    nim = input("Masukkan NIM mahasiswa: ")
    kode = input("Masukkan kode buku: ")
    
    # cari mahasiswa
    mahasiswa = cari_mahasiswa(root_mahasiswa, nim)
    if mahasiswa is None:
        print("Mahasiswa tidak ditemukan")
        return
    
    # cari buku
    buku = cari_buku(root_buku, kode)
    if buku is None:
        print("Buku tidak ditemukan")
        return
    
    buku.stok -= 1
    
    tanggal_pinjam = datetime.now()
    
    
    maks_kembali = tanggal_pinjam + timedelta(days=7)
    
    data = {
        "nim": mahasiswa.nim,
        "nama": mahasiswa.nama,
        "kode_buku": buku.kode,
        "nama_buku": buku.nama,
        "tanggal_pinjam": tanggal_pinjam.strftime("%Y-%m-%d"),
        "maks_kembali": maks_kembali.strftime("%Y-%m-%d")
    }
    peminjaman.append(data)
    simpan_peminjaman()
    
    print("Buku berhasil dipinjam")
    
    
def tampil_peminjaman():
    for data in peminjaman:
        print("------------------------------")
        print("nim              :", data['nim'])
        print("nama             :", data['nama'])
        print("kode buku        :", data['kode_buku'])
        print("nama buku        :", data['nama_buku'])
        print("tanggal pinjam   :", data['tanggal_pinjam'])
        print("maksimal kembali :", data['maks_kembali'])
        print("------------------------------")


def simpan_peminjaman():
    with open(os.path.join(BASE_DIR, "data", "peminjaman.json"), "w") as file:
        json.dump(peminjaman, file, indent = 4)
        
def load_peminjaman():
    global peminjaman
    
    try:
        with open(os.path.join(BASE_DIR, "data", "peminjaman.json"), "r") as file:
            data = json.load(file)
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                peminjaman = data[0]
            elif isinstance(data, list):
                peminjaman = data
            else:
                peminjaman = []
    except FileNotFoundError:
        peminjaman = []
        
#fitur peminjaman buku end

# fitur pengembalian buku start
def kembalikan_buku(root_buku):
    nim = input("Masukkan NIM mahasiswa: ")
    kode = input("Masukkan kode buku: ")
    
    ditemukan = False
    for data in peminjaman:
        if data['nim'] == nim and data['kode_buku'] == kode:
           ditemukan = True
           
        #    cari buku di bst
        buku = cari_buku(root_buku, kode)
        
        # tambah stok buku
        if buku:
            buku.stok += 1
            
        tanggal_kembali = datetime.now()
        
        batas_kembali = datetime.strptime(data["maks_kembali"], "%Y-%m-%d")
        
        terlambat = (tanggal_kembali - batas_kembali).days
        
        if terlambat < 0:
            terlambat = 0
            
        denda = terlambat * 2000
        
        print("\n=====pengembalian buku=====")
        print("nama buku :", data['nama_buku'])
        print("terlambat :", terlambat, "hari")
        print("denda :Rp", denda)
        
        # hapus data peminjaman
        peminjaman.remove(data)
        simpan_buku(root_buku)
        simpan_peminjaman()
        
        print("Buku berhasil dikembalikan")
        
        break
    if not ditemukan:
        print("Data peminjaman tidak ditemukan")

root_buku = load_buku()
load_peminjaman()





# gui aplikasi start
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# =========================
# WINDOW UTAMA
# =========================
window = tk.Tk()
window.title("Perpustakaan ITH")
window.geometry("1000x650")
window.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Arial", 11), rowheight=28)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

# =========================
# HEADER
# =========================
header = tk.Frame(window, bg="#1e3a5f", height=80)
header.pack(fill="x")

judul = tk.Label(
    header,
    text="SISTEM PERPUSTAKAAN ITH",
    font=("Arial", 24, "bold"),
    bg="#1e3a5f",
    fg="white"
)
judul.pack(pady=20)
label_jam = tk.Label(
    header,
    text="",
    font=("Arial", 14, "bold"),
    bg="#1e3a5f",
    fg="white"
)

label_jam.pack()


def update_jam():
    waktu = datetime.now().strftime("%H:%M:%S")
    tanggal = datetime.now().strftime("%d-%m-%Y")

    label_jam.config(text=f"{tanggal} | {waktu}")

    label_jam.after(1000, update_jam)


update_jam()

# =========================
# FRAME UTAMA
# =========================
menu_frame = tk.Frame(window, bg="#dce6f2", width=250)
menu_frame.pack(side="left", fill="y")

content_frame = tk.Frame(window, bg="white")
content_frame.pack(side="right", expand=True, fill="both")

label_halaman = tk.Label(
    content_frame,
    text="Dashboard",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#1e3a5f"
)
label_halaman.pack(pady=20)

table_frame = tk.Frame(content_frame, bg="white")
table_frame.pack(expand=True, fill="both", padx=20, pady=10)


# =========================
# MEMBERSIHKAN CONTENT
# =========================
def clear_table_frame():
    for widget in table_frame.winfo_children():
        widget.destroy()


# =========================
# TABEL BUKU
# =========================
def tampil_tabel_buku():
    clear_table_frame()
    label_halaman.config(text="Data Buku")

    tree = ttk.Treeview(
        table_frame,
        columns=("Kode", "Nama", "Penulis", "Stok"),
        show="headings"
    )

    for col in ("Kode", "Nama", "Penulis", "Stok"):
        tree.heading(col, text=col)

    tree.column("Kode", width=100)
    tree.column("Nama", width=300)
    tree.column("Penulis", width=250)
    tree.column("Stok", width=100)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    def isi_tabel(root):
        if root is not None:
            isi_tabel(root.left)
            tree.insert(
                "",
                tk.END,
                values=(root.kode, root.nama, root.penulis, root.stok)
            )
            isi_tabel(root.right)

    isi_tabel(root_buku)


# =========================
# TABEL MAHASISWA
# =========================
def tampil_tabel_mahasiswa():
    clear_table_frame()
    label_halaman.config(text="Data Mahasiswa")

    tree = ttk.Treeview(
        table_frame,
        columns=("NIM", "Nama"),
        show="headings"
    )

    tree.heading("NIM", text="NIM")
    tree.heading("Nama", text="Nama")

    tree.column("NIM", width=200)
    tree.column("Nama", width=400)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    def isi_tabel(root):
        if root is not None:
            isi_tabel(root.left)
            tree.insert(
                "",
                tk.END,
                values=(root.nim, root.nama)
            )
            isi_tabel(root.right)

    isi_tabel(root_mahasiswa)


# =========================
# TABEL PEMINJAMAN
# =========================
def tampil_tabel_peminjaman():
    clear_table_frame()
    label_halaman.config(text="Data Peminjaman")

    tree = ttk.Treeview(
        table_frame,
        columns=("NIM", "Nama", "Kode Buku", "Nama Buku", "Tanggal Pinjam", "Maks Kembali"),
        show="headings"
    )

    for col in ("NIM", "Nama", "Kode Buku", "Nama Buku", "Tanggal Pinjam", "Maks Kembali"):
        tree.heading(col, text=col)

    tree.column("NIM", width=120)
    tree.column("Nama", width=160)
    tree.column("Kode Buku", width=100)
    tree.column("Nama Buku", width=180)
    tree.column("Tanggal Pinjam", width=130)
    tree.column("Maks Kembali", width=130)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    for data in peminjaman:
        tree.insert(
            "",
            tk.END,
            values=(
                data["nim"],
                data["nama"],
                data["kode_buku"],
                data["nama_buku"],
                data["tanggal_pinjam"],
                data["maks_kembali"]
            )
        )


# =========================
# DASHBOARD
# =========================
def tampil_dashboard():
    clear_table_frame()
    label_halaman.config(text="Dashboard")

    tk.Label(
        table_frame,
        text="Selamat Datang di Sistem Perpustakaan ITH",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#1e3a5f"
    ).pack(pady=30)

    tk.Label(
        table_frame,
        text="Gunakan menu di sebelah kiri untuk mengelola data buku, mahasiswa, peminjaman, dan pengembalian.",
        font=("Arial", 12),
        bg="white",
        fg="black"
    ).pack(pady=10)


# =========================
# TAMBAH BUKU
# =========================
def tambah_buku_gui():
    form = tk.Toplevel(window)
    form.title("Tambah Buku")
    form.geometry("400x400")
    form.configure(bg="white")

    tk.Label(form, text="Kode Buku", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_kode = tk.Entry(form, font=("Arial", 11))
    entry_kode.pack(pady=5)

    tk.Label(form, text="Nama Buku", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_nama = tk.Entry(form, font=("Arial", 11))
    entry_nama.pack(pady=5)

    tk.Label(form, text="Penulis", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_penulis = tk.Entry(form, font=("Arial", 11))
    entry_penulis.pack(pady=5)

    tk.Label(form, text="Stok", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_stok = tk.Entry(form, font=("Arial", 11))
    entry_stok.pack(pady=5)

    def simpan():
        global root_buku

        kode = entry_kode.get()
        nama = entry_nama.get()
        penulis = entry_penulis.get()
        stok = entry_stok.get()

        if kode == "" or nama == "" or penulis == "" or stok == "":
            messagebox.showerror("Error", "Semua data harus diisi")
            return

        if not stok.isdigit():
            messagebox.showerror("Error", "Stok harus berupa angka")
            return

        if cari_buku(root_buku, kode) is not None:
            messagebox.showerror("Error", "Kode buku sudah terdaftar")
            return

        buku_baru = Buku(kode, nama, penulis, int(stok))
        root_buku = insert(root_buku, buku_baru)

        simpan_buku(root_buku)
        tampil_tabel_buku()

        messagebox.showinfo("Sukses", "Buku berhasil ditambahkan")
        form.destroy()

    tk.Button(
        form,
        text="Simpan",
        bg="#1e3a5f",
        fg="white",
        width=15,
        height=2,
        command=simpan
    ).pack(pady=20)


# =========================
# TAMBAH MAHASISWA
# =========================
def tambah_mahasiswa_gui():
    form = tk.Toplevel(window)
    form.title("Tambah Mahasiswa")
    form.geometry("400x300")
    form.configure(bg="white")

    tk.Label(form, text="NIM", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_nim = tk.Entry(form, font=("Arial", 11))
    entry_nim.pack(pady=5)

    tk.Label(form, text="Nama Mahasiswa", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_nama = tk.Entry(form, font=("Arial", 11))
    entry_nama.pack(pady=5)

    def simpan():
        global root_mahasiswa

        nim = entry_nim.get()
        nama = entry_nama.get()

        if nim == "" or nama == "":
            messagebox.showerror("Error", "Semua data harus diisi")
            return

        if cari_mahasiswa(root_mahasiswa, nim) is not None:
            messagebox.showerror("Error", "NIM sudah terdaftar")
            return

        mahasiswa_baru = mahasiswa(nim, nama)
        root_mahasiswa = insert_mahasiswa(root_mahasiswa, mahasiswa_baru)

        simpan_mahasiswa(root_mahasiswa)
        tampil_tabel_mahasiswa()

        messagebox.showinfo("Sukses", "Mahasiswa berhasil ditambahkan")
        form.destroy()

    tk.Button(
        form,
        text="Simpan",
        bg="#1e3a5f",
        fg="white",
        width=15,
        height=2,
        command=simpan
    ).pack(pady=25)


# =========================
# CARI BUKU
# =========================
def cari_buku_gui():
    form = tk.Toplevel(window)
    form.title("Cari Buku")
    form.geometry("400x300")
    form.configure(bg="white")

    tk.Label(form, text="Masukkan Kode Buku", bg="white", font=("Arial", 12, "bold")).pack(pady=10)
    entry_kode = tk.Entry(form, font=("Arial", 12))
    entry_kode.pack(pady=10)

    hasil = tk.Label(form, text="", bg="white", font=("Arial", 11), justify="left")
    hasil.pack(pady=20)

    def cari():
        kode = entry_kode.get()

        if kode == "":
            messagebox.showerror("Error", "Kode buku harus diisi")
            return

        buku = cari_buku(root_buku, kode)

        if buku is None:
            hasil.config(text="Buku tidak ditemukan")
        else:
            hasil.config(
                text=f"Kode    : {buku.kode}\n"
                     f"Nama    : {buku.nama}\n"
                     f"Penulis : {buku.penulis}\n"
                     f"Stok    : {buku.stok}"
            )

    tk.Button(
        form,
        text="Cari",
        bg="#1e3a5f",
        fg="white",
        width=15,
        height=2,
        command=cari
    ).pack(pady=10)


# =========================
# CARI MAHASISWA
# =========================
def cari_mahasiswa_gui():
    form = tk.Toplevel(window)
    form.title("Cari Mahasiswa")
    form.geometry("400x300")
    form.configure(bg="white")

    tk.Label(form, text="Masukkan NIM", bg="white", font=("Arial", 12, "bold")).pack(pady=10)
    entry_nim = tk.Entry(form, font=("Arial", 12))
    entry_nim.pack(pady=10)

    hasil = tk.Label(form, text="", bg="white", font=("Arial", 11), justify="left")
    hasil.pack(pady=20)

    def cari():
        nim = entry_nim.get()

        if nim == "":
            messagebox.showerror("Error", "NIM harus diisi")
            return

        mhs = cari_mahasiswa(root_mahasiswa, nim)

        if mhs is None:
            hasil.config(text="Mahasiswa tidak ditemukan")
        else:
            hasil.config(
                text=f"NIM  : {mhs.nim}\n"
                     f"Nama : {mhs.nama}"
            )

    tk.Button(
        form,
        text="Cari",
        bg="#1e3a5f",
        fg="white",
        width=15,
        height=2,
        command=cari
    ).pack(pady=10)


# =========================
# PINJAM BUKU
# =========================
def pinjam_buku_gui():
    form = tk.Toplevel(window)
    form.title("Pinjam Buku")
    form.geometry("400x350")
    form.configure(bg="white")

    tk.Label(form, text="NIM Mahasiswa", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_nim = tk.Entry(form, font=("Arial", 11))
    entry_nim.pack(pady=5)

    tk.Label(form, text="Kode Buku", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_kode = tk.Entry(form, font=("Arial", 11))
    entry_kode.pack(pady=5)

    def proses_pinjam():
        nim = entry_nim.get()
        kode = entry_kode.get()

        if nim == "" or kode == "":
            messagebox.showerror("Error", "Semua data harus diisi")
            return

        mhs = cari_mahasiswa(root_mahasiswa, nim)
        if mhs is None:
            messagebox.showerror("Error", "Mahasiswa tidak ditemukan")
            return

        buku = cari_buku(root_buku, kode)
        if buku is None:
            messagebox.showerror("Error", "Buku tidak ditemukan")
            return

        if buku.stok <= 0:
            messagebox.showerror("Error", "Stok buku habis")
            return

        buku.stok -= 1

        tanggal_pinjam = datetime.now()
        maks_kembali = tanggal_pinjam + timedelta(days=7)

        data = {
            "nim": mhs.nim,
            "nama": mhs.nama,
            "kode_buku": buku.kode,
            "nama_buku": buku.nama,
            "tanggal_pinjam": tanggal_pinjam.strftime("%Y-%m-%d"),
            "maks_kembali": maks_kembali.strftime("%Y-%m-%d")
        }

        peminjaman.append(data)

        simpan_buku(root_buku)
        simpan_peminjaman()

        tampil_tabel_peminjaman()

        messagebox.showinfo("Sukses", "Buku berhasil dipinjam")
        form.destroy()

    tk.Button(
        form,
        text="Pinjam",
        bg="#1e3a5f",
        fg="white",
        width=15,
        height=2,
        command=proses_pinjam
    ).pack(pady=25)


# =========================
# KEMBALIKAN BUKU
# =========================
def kembalikan_buku_gui():
    form = tk.Toplevel(window)
    form.title("Kembalikan Buku")
    form.geometry("400x350")
    form.configure(bg="white")

    tk.Label(form, text="NIM Mahasiswa", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_nim = tk.Entry(form, font=("Arial", 11))
    entry_nim.pack(pady=5)

    tk.Label(form, text="Kode Buku", bg="white", font=("Arial", 11)).pack(pady=5)
    entry_kode = tk.Entry(form, font=("Arial", 11))
    entry_kode.pack(pady=5)

    def proses_kembali():
        nim = entry_nim.get()
        kode = entry_kode.get()

        if nim == "" or kode == "":
            messagebox.showerror("Error", "Semua data harus diisi")
            return

        ditemukan = None

        for data in peminjaman:
            if data["nim"] == nim and data["kode_buku"] == kode:
                ditemukan = data
                break

        if ditemukan is None:
            messagebox.showerror("Error", "Data peminjaman tidak ditemukan")
            return

        buku = cari_buku(root_buku, kode)

        if buku is not None:
            buku.stok += 1

        tanggal_kembali = datetime.now()
        batas_kembali = datetime.strptime(ditemukan["maks_kembali"], "%Y-%m-%d")

        terlambat = (tanggal_kembali - batas_kembali).days

        if terlambat < 0:
            terlambat = 0

        denda = terlambat * 2000

        peminjaman.remove(ditemukan)

        simpan_buku(root_buku)
        simpan_peminjaman()

        tampil_tabel_peminjaman()

        messagebox.showinfo(
            "Pengembalian Berhasil",
            f"Nama Buku : {ditemukan['nama_buku']}\n"
            f"Terlambat : {terlambat} hari\n"
            f"Denda     : Rp {denda}"
        )

        form.destroy()

    tk.Button(
        form,
        text="Kembalikan",
        bg="#1e3a5f",
        fg="white",
        width=15,
        height=2,
        command=proses_kembali
    ).pack(pady=25)


# =========================
# BUTTON MENU
# =========================
def tombol_menu(text, command):
    return tk.Button(
        menu_frame,
        text=text,
        font=("Arial", 11, "bold"),
        bg="#1e3a5f",
        fg="white",
        width=24,
        height=2,
        relief="flat",
        cursor="hand2",
        command=command
    )


btn_dashboard = tombol_menu("Dashboard", tampil_dashboard)
btn_dashboard.pack(pady=(30, 8))

btn_lihat_buku = tombol_menu("Lihat Buku", tampil_tabel_buku)
btn_lihat_buku.pack(pady=8)

btn_tambah_buku = tombol_menu("Tambah Buku", tambah_buku_gui)
btn_tambah_buku.pack(pady=8)

btn_cari_buku = tombol_menu("Cari Buku", cari_buku_gui)
btn_cari_buku.pack(pady=8)

btn_lihat_mahasiswa = tombol_menu("Lihat Mahasiswa", tampil_tabel_mahasiswa)
btn_lihat_mahasiswa.pack(pady=8)

btn_tambah_mahasiswa = tombol_menu("Tambah Mahasiswa", tambah_mahasiswa_gui)
btn_tambah_mahasiswa.pack(pady=8)

btn_cari_mahasiswa = tombol_menu("Cari Mahasiswa", cari_mahasiswa_gui)
btn_cari_mahasiswa.pack(pady=8)

btn_pinjam = tombol_menu("Pinjam Buku", pinjam_buku_gui)
btn_pinjam.pack(pady=8)

btn_kembali = tombol_menu("Kembalikan Buku", kembalikan_buku_gui)
btn_kembali.pack(pady=8)

btn_peminjaman = tombol_menu("Lihat Peminjaman", tampil_tabel_peminjaman)
btn_peminjaman.pack(pady=8)

btn_keluar = tombol_menu("Keluar", window.destroy)
btn_keluar.pack(pady=25)


# =========================
# TAMPILAN AWAL
# =========================
tampil_dashboard()

# =========================
# RUN PROGRAM
# =========================
window.mainloop()
# gui aplikasi end