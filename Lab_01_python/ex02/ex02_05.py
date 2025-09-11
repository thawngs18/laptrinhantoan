so_gio_lam = int(input("nhap so gio lam: "))
luong_gio = int(input("nhap thu lao tren moi gio lam tieu chuan: "))
gio_tieu_chuan = 44
gio_vuot_chuan = max(0,so_gio_lam-gio_tieu_chuan)
luong_thu = gio_tieu_chuan * luong_gio + gio_vuot_chuan * 1.5 * luong_gio
print("thu lao cua ban la: ", luong_thu)