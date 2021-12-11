import json #import modul json
import os #import modul os
import random #import modul random
from datetime import datetime as dt #import modul datetime dengan alias dt

DBPATH = "./arisan.db.json" #path untuk database utama

def read(fileP): #fungsi untuk membaca file json dengan parameter path untuk filenya
    with open(fileP, 'r') as _file: #membuka file dan disimpan kedalam _file sebagai hanya baca
        try: #coba lakukan perintah dibawah
            res = json.load(_file) #load data json dari _file menjadi data python dan disimpan kedalam res
            return res #ekspos res ke luar
        except ValueError as e: #jika gagal lakukan perintah dibawah
            return {} #return dictionary kosong

def write(fileP, data, verbose = False): #fungsi untuk menulis data ke file dengan parameter fileP untuk path file, data untuk data yang ingin ditulis, verbose(jika ingin menampilkan info setelah write maka jadikan True)
    with open(fileP, 'w') as _file: #buka file dan simpan ke _file sebagai hanya tulis
        json.dump(data, _file) #overwrite semua data dalam file json dan ganti dengan data yang ada dalam variabel data
        if(verbose): #jika verbose true
            print((" "*35)+"database terupdate") #tampilkan info tambahan
            os.system("delay 0.5") #tahan terminal agar tidak melanjutkan pekerjaan selama 0.5 detik
    return 1 #return 1 sebagai parameter keberhasilan

def header(): #fungsi untuk menampilkan header program
    print("ARISAN DIGITAL".center(100," ")) #menampilkan string biasa namun dengan center 100
    print("build with python3".center(100," ")) #sama
    print("oleh : Bima & Stefani".center(100," ") #)sama
    print("=============================".center(100," ")) #sama

def menu(): #untuk menampilkan menu utama
    header() #memanggil header
    print("==========MAIN MENU==========".center(100," ")) #menampilkan string biasa namun dengan center 100
    print("  [1] Undi Arisan            ".center(100," ")) #sama
    print("  [2] Bayar Arisan           ".center(100," ")) #sama
    print("  [3] Tambah Peserta         ".center(100," ")) #sama
    print("  [4] Remove Peserta         ".center(100," ")) #sama
    print("  [5] Data Peserta           ".center(100," ")) #sama
    print("  [6] Riwayat Pembayaran     ".center(100," ")) #sama
    print("  [i] Info Tentang Arisan    ".center(100," ")) #sama
    print("  [r] Reset Arisan           ".center(100," ")) #sama
    print("  [?] Bantuan                ".center(100," ")) #sama
    print("  [x] Tutup Aplikasi         ".center(100," ")) #sama
    print("=============================".center(100," ")) #sama
    return input((" "*35)+"input >> ") #mendapatkan input lalu di ekspos ke luar(return)

def undiPeserta(data): #untuk undi peserta dengan parameter data arisan
    header() #memanggil header
    print("===========UNDIAN============".center(100," ")) #menampilkan label dengan center 100
    if len(data["peserta"])<data["minPeserta"]: #cek apakah jumlah peserta telah memenuhi jumlah minimal peserta
        print("peserta tidak memenuhi batas minimal".center(100," ")) #info
        input((" "*35)+"tekan enter untuk lanjut...") #menunggu input dari user untuk lanjut
        return data #return data tanpa modifikasi
    if len(data["bayar"])<len(data["peserta"]): #cek apakah semua sudah membayar
        print("semua peserta harus membayar terlebih dahulu".center(100," ")) #info
        input((" "*35)+"tekan enter untuk lanjut...") #menunggu input dari user untuk lanjut
        return data #return data tanpa modifikasi
    if input((" "*35)+"anda yakin akan mengundi?[y/n]:") == "y": #input untuk konfirmasi pengundian dan jika user setuju maka lanjut kebawah
        print("sedang mengundi...".center(100," ")) #info
        undian = random.randrange(len(data["peserta"])) #random undian dengan range 0 sampai banyaknya peserta-1
        while data["peserta"][undian] in data["dapat"]: #cek apakah peserta sudah dapat arisan jika iya maka lakukan loop agar dapat diundi ulang
            undian = random.randrange(len(data["peserta"])) #pengundian ulang
        os.system("delay 1") #delay 1 detik
        data["dapat"].append(data["peserta"][undian]) #tambahkan peserta yang mendapat arisan kedalam database
        data["bayar"].clear() #bersihkan list peserta yang sudah membayar
        print(f"Selamat pada \"{data['peserta'][undian]}\" telah mendapatkan arisan hari ini".center(100," ")) #info
        input((" "*35)+"tekan enter untuk lanjut...") #tunggu input dari user
    write(DBPATH, data, True) #tulis data terbaru kedalam file database
    return data #ekspos data yang baru

def tabelPeserta(data): #untuk menampilkan tabel peserta
    print("No  | Bayar | Dapat | Nama   ".center(100," ")) #header kolom
    print("-----------------------------".center(100," ")) #separator
    num = 1 #untuk mendapatkan nomer baris
    for peserta in data["peserta"]: #loop data[peserta] kedalam variabel peserta
        print(" "*34,f"{num:<4}|",
              ("  *  " if peserta in data["bayar"] else "     "),"|",
              ("  *  " if peserta in data["dapat"] else "     "),"|",
              peserta) #tampilkan data peserta (No | status pembayaran | status dapat | nama)
        num+=1 #tambahkan num setiap akhir baris
    print("=============================".center(100," ")) #separator
    
def bayar(data, nama): #untuk menambahkan data pembayaran kedalam database
    data["bayar"].append(nama) #menambahkan nama yang membayar kedalam database
    data["riwayat"].append([nama,dt.now().strftime("%d/%m/%Y %H:%M:%S")]) #menambahkan data waktu kedalam database
    return data #ekspos data yang baru

def printKwitansi(kwitansi): #untuk menampilkan kwitansi
    print((" "*35)+"======================================================") #separator
    print((" "*35)+"Atas nama: ",kwitansi[0]) #menampilkan nama
    print((" "*35)+"Telah membayar arisan pada",kwitansi[1]) #menampilkan tanggal dan waktu pembayaran
    print((" "*35)+"======================================================") #separator

def listKwitansi(data): #tampilkan daftar riwayat pembayaran
    header() #tampilkan header
    print("========LIST KWITANSI============".center(100," ")) #label
    print("ID  |       Tanggal       | Nama".center(100," ")) #header kolom
    print("---------------------------------".center(100," ")) #separator
    id = 0 #id untuk tiap riwayat pembayaran
    for kw in data["riwayat"]: #loop data riwayat pembayaran kedalam variabel kw
        print((" "*33),f"{id:<4}|",kw[1],"|",kw[0]) #tampilkan data pembayaran
        id+=1 #tambah id tiap data pembayaran
    print("=================================".center(100," ")) #separator
    print() #enter tambahan
    input((" "*35)+"tekan enter untuk lanjut...") #tunggu input untuk lanjut
    
def formBayar(data, log): #menampilkan form pembayaran
    header() #panggil header
    print("=======FORM PEMBAYARAN=======".center(100," ")) #label
    tabelPeserta(data) #tampilkan tabel peserta
    nama = input((" "*35)+" Masukan nama: ") #input nama yang ingin melakukan pembayaran
    if nama in data["peserta"]:# cek apakah nama tersebut termasuk peserta
        if nama in data["bayar"]: #cek apakah nama tersebut sudah bayar
            print("peserta ini sudah membayar".center(100," ")) #info
            input((" "*35)+"tekan enter untuk lanjut...") #tunggu input
        else: #jika belum bayar
            data = bayar(data,nama) #tambahkan data pembayaran kedalam database menggunakan fungsi bayar
            printKwitansi(data["riwayat"][-1]) #tampilkan kwitansi
    else: #jika nama tersebut bukan peserta
        print("peserta tidak ditemukan".center(100," ")) #info
        input((" "*35)+"tekan enter untuk lanjut...") #tunggu input
    write(DBPATH, data, True) #tulis data kedalam database
    return data #ekspos data terbaru ke luar

def tambahPeserta(data): #untuk menambahkan peserta
    while True: #lakukan loop
        os.system("cls") #bersihkan layar
        header() #panggil header
        print("========TAMBAH PESERTA=======".center(100," ")) #label
        nama = input((" "*35)+" Masukan nama: ") #inputkan nama yg ingin ditambahkan
        if nama in data["peserta"]: #jika nama tersebut sudah ada dalam list peserta
            print("peserta dengan nama tersebut sudah ada mohon gunakan nama lain".center(100," ")) #info
            input((" "*35)+"tekan enter untuk lanjut...") #tunggu input
            continue #skip kode dibawah lalu naik ke atas lagi
        data["peserta"].append(nama) #tambahkan nama yang ingin ditambahkan ke dalam data
        if len(data["peserta"])>data["minPeserta"]: #jika jumlah peserta menjadi lebih dari minimal peserta
            data["target"] = len(data["peserta"])*data["iuran"] #ubah target menyesuaikan dengan jumlah peserta
        else: #jika tidak
            target = data["minPeserta"]*data["iuran"] 
            if(data["target"]!=target): #cek apakah target berbeda dengan target minimal
                data["target"] = target #kembalikan target menjadi target minimal
        if input((" "*35)+"apakah mau langsung bayar?[y/n]: ") == "y": #konfirmasi apakah mau langsung membayar arisan jika setuju maka lanjut kebawah
            data = bayar(data, nama) #tambah data pembayaran
            printKwitansi(data["riwayat"][-1]) #tampilkan kwitansi
        write(DBPATH, data, True) #tulis kedalam database
        break #hentikan loop
    return data #ekspos data terbaru

def removePeserta(data): #untuk meremove peserta
    header() #menampilkan header
    print("========REMOVE PESERTA=======".center(100," ")) #label
    tabelPeserta(data) #menampilkan tabel peserta
    nama = input((" "*35)+" Masukan nama: ") #input nama peserta yang ingin diremove
    if nama in data["peserta"]: #jika nama termasuk dalam peserta
        if input((" "*35)+"apakah anda yakin akan remove?[y/n]: ") == "y":
            data["peserta"].remove(nama)
            if nama in data["bayar"]: data["bayar"].remove(nama)
            if nama in data["dapat"]: data["dapat"].remove(nama)
            log.append({"time":dt.now().strftime("%d/%m/%Y %H:%M:%S"),"command":"remove","value":nama})
            if len(data["peserta"])>data["minPeserta"]:
                data["target"] = len(data["peserta"])*data["iuran"]
                log.append({"time":dt.now().strftime("%d/%m/%Y %H:%M:%S"),"command":"target","value":data["target"]})
            else:
                target = data["minPeserta"]*data["iuran"]
                if(data["target"]!=target):
                    data["target"] = target
                    log.append({"time":dt.now().strftime("%d/%m/%Y %H:%M:%S"),"command":"target","value":target})
    else:
        print("peserta tidak ditemukan".center(100," "))
        input((" "*35)+"tekan enter untuk lanjut...")
    write(DBPATH, data, True)
    write(LOGBOOK, log)
    return data, log   
    
def summaryPeserta(data):
    header()
    print("=======SUMMARY PESERTA=======".center(100," "))
    tabelPeserta(data)
    input((" "*35)+"tekan enter untuk lanjut...")

def printInfoArisan(data):
    header()
    print("=========INFO ARISAN=========".center(100," "))
    print((" "*35)+"  Target arisan   : Rp.",data["target"])
    print((" "*35)+"  Iuran arisan    : Rp.",data["iuran"])
    print((" "*35)+"  Minimal Peserta :",data["minPeserta"])
    print((" "*35)+"  Total Peserta   :",len(data["peserta"]))
    print((" "*35)+"  -> Sudah bayar  :",len(data["bayar"]))
    print((" "*35)+"  -> Sudah dapat  :",len(data["dapat"]))
    print("=============================".center(100," "))
    print()
    input((" "*35)+"tekan enter untuk lanjut...")

def resetArisan(data, log):
    while True:
        os.system("clear")
        header()
        print("========RESET ARISAN=========".center(100," "))
        target = input((" "*35)+"  Masukan target arisan   : ")
        if not target.isnumeric():
            print((" "*35)+"Harap masukan data Integer saja")
            input((" "*35)+"tekan enter untuk ulang...")
            continue
        target = int(target)
        minPes = input((" "*35)+"  Masukan minimal peserta : ")
        if not minPes.isnumeric():
            print((" "*35)+"Harap masukan data Integer saja")
            input((" "*35)+"tekan enter untuk ulang...")
            continue
        minPes = int(minPes)
        if minPes<2:
            print((" "*35)+"Minimal peserta untuk arisan harus >= 2")
            input((" "*35)+"tekan enter untuk ulang...")
            continue
        opsi = input((" "*35)+"Anda yakin akan reset arisan?[y/n/ulang]:")
        if opsi =="y":
            data["minPeserta"] = minPes
            data["target"] = target
            data["iuran"] = target/minPes
            data["peserta"] = []
            data["bayar"] = []
            data["dapat"] = []
            data["riwayat"] = []
            log.append({"time":dt.now().strftime("%d/%m/%Y %H:%M:%S"),"command":"reset","value":{
                "minPeserta":minPes,
                "target":target,
                "iuran":target/minPes,
                "peserta":[],
                "bayar":[],
                "dapat":[],
                "riwayat":[]
            }})
        elif opsi == "ulang" or opsi == "u":
            continue
        break
    write(DBPATH, data, True)
    write(LOGBOOK, log)
    return data, log


def help():
    header()
    print("====================HELP=====================".center(100," "))
    print("[1] Undi Arisan                                                       ".center(100," "))
    print("    Untuk mengundi peserta yang akan mendapatkan arisan dengan syarat:".center(100," "))
    print("    1. Jumlah peserta arisan memenuhi batas minimal peserta arisan    ".center(100," "))
    print("    2. Seluruh peserta arisan telah membayar iuran                    ".center(100," "))
    print()
    print("[2] Bayar arisan                                                      ".center(100," "))
    print("    Untuk membayarkan iuran peserta arisan. Akan tampil tabel peserta ".center(100," "))
    print("    dan harus menginputkan nama peserta yang akan membayar            ".center(100," "))
    print()
    print("[3] Tambah Peserta                                                    ".center(100," "))
    print("    Untuk menambahkan peserta baru dengan syarat:                     ".center(100," "))
    print("    1. Tidak boleh ada peserta dengan nama yang sama                  ".center(100," "))
    print()
    print("[4] Remove Peserta                                                    ".center(100," "))
    print("    Untuk menghapus peserta dengan syarat:                            ".center(100," "))
    print("    1. Peserta harus termasuk dalam peserta arisan                    ".center(100," "))
    print()
    print("[5] Data Peserta                                                      ".center(100," "))
    print("    Untuk menampilkan data peserta berupa nama, dan status pada arisan".center(100," "))
    print()
    print("[6] Riwayat Pembayaran                                                ".center(100," "))
    print("    Untuk menampilkan list riwayat pembayaran iuran arisan            ".center(100," "))
    print()
    print("[i] Info Tentang Arisan                                               ".center(100," "))
    print("    Untuk menampilkan info tentang arisan berupa data target arisan,  ".center(100," "))
    print("    iuran, jumlah peserta, dll                                        ".center(100," "))
    print()
    print("[r] Reset Arisan                                                      ".center(100," "))
    print("    Untuk mereset arisan dengan mengosongkan semua list peserta dan   ".center(100," "))
    print("    membuat target dan iuran baru                                     ".center(100," "))
    print()
    print("[?] Bantuan                                                           ".center(100," "))
    print("    Untuk menampilkan menu bantuan ini :)                             ".center(100," "))
    print()
    print("[x] Tutup Aplikasi                                                    ".center(100," "))
    print("    Untuk menutup aplikasi                                            ".center(100," "))
    input((" "*35)+"tekan enter untuk lanjut...")

def main():
    data = read(DBPATH)
    log = read(LOGBOOK)
    while True:
        os.system("clear")
        opsi = menu()
        os.system("clear")
        if opsi == "1":
            data,log = undiPeserta(data, log)
        elif opsi == "2":
            data,log = formBayar(data, log)
        elif opsi == "3":
            data,log = tambahPeserta(data, log)
        elif opsi == "4":
            data,log = removePeserta(data, log)
        elif opsi == "5":
            summaryPeserta(data)
        elif opsi == "6":
            listKwitansi(data)
        elif opsi == "i":
            printInfoArisan(data)
        elif opsi == "r":
            data,log = resetArisan(data, log)
        elif opsi == "?":
            help()
        elif opsi == "x":
            break
    write(DBPATH, data, True)
    write(LOGBOOK, log)
    os.system("clear")
    print(":)bye")
    
main()
