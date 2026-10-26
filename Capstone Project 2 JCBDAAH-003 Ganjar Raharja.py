import json
import os

def input_tanggal(prompt):
    while True:
        tanggal = input(prompt)
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            return tanggal
        except ValueError:
            print("❌ Format tanggal harus YYYY-MM-DD (contoh: 2025-08-27).")

def input_angka(prompt, minimal=None, maksimal=None):
    while True:
        nilai = input(prompt)
        if not nilai.isdigit():
            print("❌ Masukkan angka yang valid.")
            continue
        nilai = int(nilai)
        if (minimal is not None and nilai < minimal) or \
           (maksimal is not None and nilai > maksimal):
            print(f"❌ Pilihan harus antara {minimal} dan {maksimal}.")
            continue
        return nilai
        
from datetime import datetime
# ================================
# File Penyimpanan
# ================================
FILE_DATA = "data_pasien.json"

# ================================
# Data Awal (Default)
# ================================
def format_id_pasien(num):
    return f"PSN{num:04d}"

pasien_default = [
    (format_id_pasien(1), "Andi", "1234567890123456", 30, "Jakarta", "Laki-laki"),
    (format_id_pasien(2), "Budi", "2345678901234567", 25, "Bandung", "Laki-laki"),
    (format_id_pasien(3), "Citra", "3456789012345678", 28, "Surabaya", "Perempuan"),
    (format_id_pasien(4), "Dedi", "4567890123456789", 40, "Semarang", "Laki-laki"),
    (format_id_pasien(5), "Eka", "5678901234567890", 35, "Yogyakarta", "Perempuan")
]

daftar_poli = [
    (1, "Poli Umum"),
    (2, "Poli Gigi"),
    (3, "Poli Anak"),
    (4, "Poli Jantung"),
    (5, "Poli Saraf")
]

daftar_dokter = {
    1: ["Dr. Agung", "Dr. Bambang"],
    2: ["Dr. Cinta", "Dr. Diyah"],
    3: ["Dr. Eko", "Dr. Frans"],
    4: ["Dr. Gilang", "Dr. Hilda"],
    5: ["Dr. Indah", "Dr. Jennie"]
}

kunjungan_default = [
    (1, "PSN0005", "2025-08-27", 1, "Dr. Agung"),
]

# ================================
# Load & Save Data
# ================================
def load_data():
    global pasien, kunjungan
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as f:
            data = json.load(f)
            pasien = [tuple(p) for p in data["pasien"]]
            kunjungan = [tuple(k) for k in data["kunjungan"]]
    else:
        pasien = pasien_default[:]
        kunjungan = kunjungan_default[:]
        save_data()

def save_data():
    with open(FILE_DATA, "w") as f:
        json.dump({"pasien": pasien, "kunjungan": kunjungan}, f, indent=4)

# ================================
# CRUD Pasien
# ================================
def tambah_pasien():
    global pasien
    # Cari nomor urut terbesar dari ID pasien yang sudah ada
    max_num = 0
    for p in pasien:
        try:
            num = int(p[0][3:])
            if num > max_num:
                max_num = num
        except:
            continue
    idbaru = format_id_pasien(max_num + 1)
    nama = input("Nama: ")
    while True:
        noktp = input("No KTP (16 digit angka): ")
        if not noktp.isdigit() or len(noktp) != 16:
            print("❌ No KTP harus 16 digit angka tanpa huruf!")
            continue
        # Cek apakah KTP sudah ada
        p = next((x for x in pasien if x[2] == noktp), None)
        if p:
            print(f"Pasien dengan No KTP {noktp} sudah terdaftar atas nama {p[1]}!")
            return
        break
    umur = input_angka("Umur: ", 0, 120)
    alamat = input("Alamat: ")
    while True:
        jk = input("Jenis Kelamin (L/P): ").upper()
        if jk in ("L", "P"):
            jk = "Laki-laki" if jk == "L" else "Perempuan"
            break
        print("❌ Masukkan L atau P.")
    pasien.append((idbaru, nama, noktp, umur, alamat, jk))
    save_data()
    print("✅ Pasien berhasil ditambahkan.")

def lihat_pasien():
    print("\n=== Daftar Pasien ===")
    for p in pasien:
        print(f"ID:{p[0]} | {p[1]} | KTP:{p[2]} | Umur:{p[3]} | {p[4]} | {p[5]}")

def lihat_pasien_by_id():
    idp = input("Masukkan ID pasien (format: PSNxxxx): ").upper()
    found = False
    for p in pasien:
        if p[0] == idp:
            print(f"ID:{p[0]} | {p[1]} | KTP:{p[2]} | Umur:{p[3]} | {p[4]} | {p[5]}")
            found = True
            break
    if not found:
        print("❌ ID pasien tidak ditemukan.")

def ubah_pasien():
    global pasien
    lihat_pasien()
    idp = input("Masukkan ID pasien yang ingin diubah (format: PSNxxxx): ").upper()
    for i, p in enumerate(pasien):
        if p[0] == idp:
            nama, noktp, umur, alamat, jk = p[1], p[2], p[3], p[4], p[5]
            while True:
                print("\nData pasien yang bisa diubah:")
                print("1. Nama")
                print("2. No KTP")
                print("3. Umur")
                print("4. Alamat")
                print("5. Jenis Kelamin")
                print("0. Selesai")
                pilih = input("Pilih bagian data yang ingin diubah: ")
                if pilih == "1":
                    nama_baru = input(f"Nama baru ({nama}): ")
                    if nama_baru: nama = nama_baru
                elif pilih == "2":
                    while True:
                        noktp_baru = input(f"No KTP baru ({noktp}): ")
                        if noktp_baru:
                            if not noktp_baru.isdigit() or len(noktp_baru) != 16:
                                print("❌ No KTP harus 16 digit angka tanpa huruf!")
                                continue
                            duplikat = any(px[2] == noktp_baru and px[0] != idp for px in pasien)
                            if duplikat:
                                print(f"No KTP {noktp_baru} sudah dipakai!")
                                continue
                            noktp = noktp_baru
                        break
                elif pilih == "3":
                    umur_baru = input(f"Umur baru ({umur}): ")
                    if umur_baru.isdigit():
                        umur = int(umur_baru)
                elif pilih == "4":
                    alamat_baru = input(f"Alamat baru ({alamat}): ")
                    if alamat_baru: alamat = alamat_baru
                elif pilih == "5":            # <-- blok baru mulai dari sini
                    jk_baru = input(f"Jenis kelamin baru L/P ({jk}): ").upper()
                    if jk_baru in ("L", "P"):
                        jk = "Laki-laki" if jk_baru == "L" else "Perempuan"
                    elif jk_baru:
                        print("❌ Masukkan L atau P.")
                elif pilih == "0":
                    break
                else:
                    print("Pilihan tidak valid!")
            print("\nData baru pasien:")
            print(f"ID:{idp} | {nama} | KTP:{noktp} | Umur:{umur} | {alamat} | {jk}")
            konfirmasi = input("Simpan perubahan? (y/n): ").lower()
            if konfirmasi == "y":
                pasien[i] = (idp, nama, noktp, umur, alamat, jk)
                save_data()
                print("✅ Data pasien berhasil diubah.")
            else:
                print("❌ Perubahan dibatalkan.")
            return
    print("❌ ID pasien tidak ditemukan.")

def hapus_pasien():
    global pasien
    lihat_pasien()
    idp = input("Masukkan ID pasien yang ingin dihapus (format: PSNxxxx): ").upper()
    for p in pasien:
        if p[0] == idp:
            konfirmasi = input(f"Yakin ingin hapus pasien {p[1]}? (y/n): ").lower()
            if konfirmasi == "y":
                pasien = [x for x in pasien if x[0] != idp]
                # Hapus seluruh jadwal kunjungan pasien ini
                global kunjungan
                kunjungan = [k for k in kunjungan if k[1] != idp]
                save_data()
                print("🗑️ Pasien dan seluruh jadwal kunjungannya berhasil dihapus.")
            else:
                print("❌ Batal dihapus.")
            return
    print("❌ ID pasien tidak ditemukan.")

# ================================
# CRUD Kunjungan
# ================================
def tambah_kunjungan():
    global kunjungan
    lihat_pasien()
    idbaru = max((k[0] for k in kunjungan), default=0) + 1
    idpasien = input("Masukkan ID pasien (format: PSNxxxx): ").upper()
    if not any(p[0] == idpasien for p in pasien):
        print("❌ ID pasien tidak ditemukan.")
        return
    tanggal = input_tanggal("Tanggal kunjungan (YYYY-MM-DD): ")
    print("\n=== Pilih Poli ===")
    for idpoli, namapoli in daftar_poli:
        print(f"{idpoli}. {namapoli}")
    poli = input_angka("Pilih ID Poli: ", 1, len(daftar_poli))
    print("\n=== Pilih Dokter ===")
    for idx, dokter in enumerate(daftar_dokter[poli], 1):
        print(f"{idx}. {dokter}")
    dokter_idx = input_angka("Pilih nomor dokter: ", 1, len(daftar_dokter[poli]))
    dokter_nama = daftar_dokter[poli][dokter_idx-1]
    kunjungan.append((idbaru, idpasien, tanggal, poli, dokter_nama))
    save_data()
    print("✅ Jadwal kunjungan berhasil ditambahkan.")

def lihat_kunjungan():

    print("\n=== Daftar Kunjungan ===")
    for k in kunjungan:
        p_list = [x for x in pasien if x[0] == k[1]]
        if not p_list:
            continue  # skip kunjungan yang pasiennya sudah dihapus
        p = p_list[0]
        poli_nama = next((n for i, n in daftar_poli if i == k[3]), "-")
        dokter_nama = k[4]
        print(f"ID:{k[0]} | Pasien:{p[1]} | Tanggal:{k[2]} | Poli:{poli_nama} | Dokter:{dokter_nama}")

def lihat_kunjungan_by_id():
    idk = input("Masukkan ID kunjungan: ")
    found = False
    for k in kunjungan:
        if str(k[0]) == idk:
            p_list = [x for x in pasien if x[0] == k[1]]
            if not p_list:
                continue
            p = p_list[0]
            poli_nama = next((n for i, n in daftar_poli if i == k[3]), "-")
            dokter_nama = k[4]
            print(f"ID:{k[0]} | Pasien:{p[1]} | Tanggal:{k[2]} | Poli:{poli_nama} | Dokter:{dokter_nama}")
            found = True
    if not found:
        print("❌ ID kunjungan tidak ditemukan.")

def lihat_kunjungan_by_poli():
    print("\n=== Pilih Poli ===")
    for idpoli, namapoli in daftar_poli:
        print(f"{idpoli}. {namapoli}")
    poli = input_angka("Pilih ID Poli: ", 1, len(daftar_poli))
    found = False
    for k in kunjungan:
        if k[3] == poli:
            p_list = [x for x in pasien if x[0] == k[1]]
            if not p_list:
                continue
            p = p_list[0]
            poli_nama = next((n for i, n in daftar_poli if i == k[3]), "-")
            dokter_nama = k[4]
            print(f"ID:{k[0]} | Pasien:{p[1]} | Tanggal:{k[2]} | Poli:{poli_nama} | Dokter:{dokter_nama}")
            found = True
    if not found:
        print("❌ Tidak ada kunjungan untuk poliklinik tersebut.")

def lihat_kunjungan_by_tanggal():
    tanggal = input("Masukkan tanggal kunjungan (YYYY-MM-DD): ")
    found = False
    for k in kunjungan:
        if k[2] == tanggal:
            p_list = [x for x in pasien if x[0] == k[1]]
            if not p_list:
                continue
            p = p_list[0]
            poli_nama = next((n for i, n in daftar_poli if i == k[3]), "-")
            dokter_nama = k[4]
            print(f"ID:{k[0]} | Pasien:{p[1]} | Tanggal:{k[2]} | Poli:{poli_nama} | Dokter:{dokter_nama}")
            found = True
    if not found:
        print("❌ Tidak ada kunjungan pada tanggal tersebut.")

def lihat_data():
    while True:
        print("""
=== Lihat Data ===
1. Lihat Data Pasien
2. Lihat Data Kunjungan
0. Kembali
""")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            while True:
                print("1. Lihat Semua Pasien\n2. Lihat Pasien by ID\n0. Kembali")
                sub = input("Pilih: ")
                if sub == "1":
                    lihat_pasien()
                elif sub == "2":
                    lihat_pasien_by_id()
                elif sub == "0":
                    break
                else:
                    print("❌ Pilihan tidak valid!")
        elif pilih == "2":
            while True:
                print("1. Lihat Semua Kunjungan\n2. Lihat Kunjungan Berdasarkan\n0. Kembali")
                sub = input("Pilih: ")
                if sub == "1":
                    lihat_kunjungan()
                elif sub == "2":
                    while True:
                        print("1. Berdasarkan ID\n2. Berdasarkan Poliklinik\n3. Berdasarkan Tanggal\n0. Kembali")
                        sub2 = input("Pilih: ")
                        if sub2 == "1":
                            lihat_kunjungan_by_id()
                        elif sub2 == "2":
                            lihat_kunjungan_by_poli()
                        elif sub2 == "3":
                            lihat_kunjungan_by_tanggal()
                        elif sub2 == "0":
                            break
                        else:
                            print("❌ Pilihan tidak valid!")
                elif sub == "0":
                    break
                else:
                    print("❌ Pilihan tidak valid!")
        elif pilih == "0":
            break
        else:
            print("❌ Pilihan tidak valid!")

def ubah_kunjungan():
    global kunjungan
    lihat_kunjungan()
    idk = input_angka("Masukkan ID kunjungan yang ingin diubah: ")
    for i, k in enumerate(kunjungan):
        if k[0] == idk:
            tanggal, poli, dokter_nama = k[2], k[3], k[4]
            while True:
                print("\nData kunjungan yang bisa diubah:")
                print("1. Tanggal")
                print("2. Poli")
                print("3. Dokter")
                print("0. Selesai")
                pilih = input("Pilih: ")
                if pilih == "1":
                    tanggal_baru = input(f"Tanggal baru ({tanggal}): ")
                    if tanggal_baru: tanggal = tanggal_baru
                elif pilih == "2":
                    print("\n=== Pilih Poli ===")
                    for idpoli, namapoli in daftar_poli:
                        print(f"{idpoli}. {namapoli}")
                    poli = input_angka("Pilih ID Poli: ", 1, len(daftar_poli))
                    print("\n=== Pilih Dokter ===")
                    for idx, dokter in enumerate(daftar_dokter[poli], 1):
                        print(f"{idx}. {dokter}")
                    dokter_idx = input_angka("Pilih nomor dokter: ", 1, len(daftar_dokter[poli]))
                    dokter_nama = daftar_dokter[poli][dokter_idx-1]
                elif pilih == "3":
                    print("\n=== Pilih Dokter ===")
                    for idx, dokter in enumerate(daftar_dokter[poli], 1):
                        print(f"{idx}. {dokter}")
                    dokter_idx = input_angka("Pilih nomor dokter: ", 1, len(daftar_dokter[poli]))
                    dokter_nama = daftar_dokter[poli][dokter_idx-1]
                elif pilih == "0":
                    break
            print("\nData baru kunjungan:")
            poli_nama = next((n for i, n in daftar_poli if i == poli), "-")
            print(f"ID:{k[0]} | Pasien:{k[1]} | Tanggal:{tanggal} | Poli:{poli_nama} | Dokter:{dokter_nama}")
            konfirmasi = input("Simpan perubahan? (y/n): ").lower()
            if konfirmasi == "y":
                kunjungan[i] = (k[0], k[1], tanggal, poli, dokter_nama)
                save_data()
                print("✅ Kunjungan berhasil diubah.")
            else:
                print("❌ Perubahan dibatalkan.")
            return
    print("❌ ID kunjungan tidak ditemukan.")

def hapus_kunjungan():
    global kunjungan
    lihat_kunjungan()
    idk = input_angka("Masukkan ID kunjungan yang ingin dihapus: ")
    for k in kunjungan:
        if k[0] == idk:
            konfirmasi = input(f"⚠️ Yakin ingin hapus kunjungan ID {idk}? (y/n): ").lower()
            if konfirmasi == "y":
                kunjungan = [x for x in kunjungan if x[0] != idk]
                save_data()
                print("🗑️ Kunjungan berhasil dihapus.")
            else:
                print("❌ Batal dihapus.")
            return
    print("❌ ID kunjungan tidak ditemukan.")

# ================================
# Menu Utama
# ================================
def menu():
    while True:
        print("""
=== Sistem Data Pasien ===
1. Lihat Data
2. Tambah Pasien / Kunjungan
3. Ubah Pasien / Kunjungan
4. Hapus Pasien / Kunjungan
0. Keluar
""")
        pilih = input("Pilih menu: ")

        if pilih == "1":
            lihat_data()

        elif pilih == "2":
            while True:
                print("1. Tambah Pasien\n2. Tambah Kunjungan\n0. Kembali")
                sub = input("Pilih: ")
                if sub == "1":
                    tambah_pasien()
                elif sub == "2":
                    tambah_kunjungan()
                elif sub == "0":
                    break
                else:
                    print("❌ Pilihan tidak valid!")

        elif pilih == "3":
            while True:
                print("1. Ubah Pasien\n2. Ubah Kunjungan\n0. Kembali")
                sub = input("Pilih: ")
                if sub == "1":
                    ubah_pasien()
                elif sub == "2":
                    ubah_kunjungan()
                elif sub == "0":
                    break
                else:
                    print("❌ Pilihan tidak valid!")

        elif pilih == "4":
            while True:
                print("1. Hapus Pasien\n2. Hapus Kunjungan\n0. Kembali")
                sub = input("Pilih: ")
                if sub == "1":
                    hapus_pasien()
                elif sub == "2":
                    hapus_kunjungan()
                elif sub == "0":
                    break
                else:
                    print("❌ Pilihan tidak valid!")

        elif pilih == "0":
            print("👋 Keluar dari sistem...")
            break
        else:
            print("❌ Pilihan tidak valid!")

# ================================
# Main
# ================================
if __name__ == "__main__":
    load_data()
    menu()
    
