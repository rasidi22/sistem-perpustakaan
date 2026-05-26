import json
from datetime import datetime, timedelta

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
    
    with open("buku.json", 'w') as file:
        json.dump(data, file, indent = 4)
        
def load_buku():
    root = None
    
    try:
        with open("buku.json", 'r')as file:
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
    
    with open("mahasiswa.json", "w") as file:
        json.dump(data, file, indent = 4)
    
    
def load_mahasiswa():
    root = None
    
    try:
        with open("mahasiswa.json", 'r') as file:
            data = []
            
            bst_ke_listMahasiswa(root, data)
            
            for item in data:
                mahasiswa = mahasiswa(
                    item['nim'],
                    item['nama']
                )
                root = insert_mahasiswa(root, mahasiswa)
                
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

m1 = mahasiswa("23005", "Rasidi")
m2 = mahasiswa("23002", "Fajar")
m3 = mahasiswa("23008", "Aldi")

root_mahasiswa = insert_mahasiswa(root_mahasiswa, m1)
root_mahasiswa = insert_mahasiswa(root_mahasiswa, m2)
root_mahasiswa = insert_mahasiswa(root_mahasiswa, m3)
simpan_mahasiswa(root_mahasiswa)

print("\nDATA MAHASISWA")
tampil_mahasiswa(root_mahasiswa)


hasil = cari_mahasiswa(root_mahasiswa, "23002")

if hasil:
    print("\nMahasiswa ditemukan")
    print("Nama :", hasil.nama)

else:
    print("Mahasiswa tidak ditemukan")
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
    with open("peminjaman.json", "w") as file:
        json.dump(peminjaman, file, indent = 4)
        
def load_peminjaman():
    global peminjaman
    
    try:
        with open("peminjaman.json", "r") as file:
            peminjaman = json.load(file)
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

# tambah data
b1 = Buku("B05", "Python", "Andi", 5)
b2 = Buku("B02", "Struktur Data", "Budi", 3)
b3 = Buku("B08", "AI Dasar", "Caca", 2)

# insert ke BST
root_buku = insert(root_buku, b1)
root_buku = insert(root_buku, b2)
root_buku = insert(root_buku, b3)

simpan_buku(root_buku)



# tampil data
tampil_buku(root_buku)


hasil = cari_buku(root_buku, "B02")

if hasil:
    print("Data ditemukan")
    print(hasil.nama)

else:
    print("Data tidak ditemukan")
# pinjam_buku(root_buku, root_mahasiswa)

kembalikan_buku(root_buku)