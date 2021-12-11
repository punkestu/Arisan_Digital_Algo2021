


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
 
