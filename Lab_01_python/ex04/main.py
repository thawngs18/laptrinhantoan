from QuanLySinhVien import QuanLySinhVien

qlsv = QuanLySinhVien()
while (1 ==1 ):
    print("\nCHUONG TRINH QUAN LY SINH VIEN")
    print("========================= MENU =========================")
    print("1. Them sinh vien")
    print("2. Cap nhat thong tin sinh vien tai co id tuy chinh: ")
    print("3. Xoa sinh vien tai id")
    print("4. Tim kiem sinh vien theo ten")
    print("5. Sap xep sinh vien theo diem trung binh")
    print("6. Sap xep sinh vien theo ten")
    print("7. In danh sach sinh vien")
    print("0. Thoat")
    print("========================================================")

    key = int(input("\nNhap lua chon cua ban: "))
    if (key == 1):
        print("\nThem sinh vien")
        qlsv.nhapSinhVien()
        print("\nthem sinh vien thanh cong")
    elif (key == 2):
        if(qlsv.soLuongSinhVien() > 0):
            print("\ncap nhat thong tin sinh vien")
            print("\nnhap id sinh vien can cap nhat")
            id = int(input("\nid: "))
            qlsv.updateSinhVien(id)
        else:
            print("\ndanh sach sinh vien rong")
    elif (key == 3):
        if(qlsv.soLuongSinhVien() > 0):
            print("\nxoa sinh vien")
            print("\nnhap id sinh vien can xoa")
            id = int(input("\nid: "))
            if(qlsv.deleteById(id)):
                print("\nsinh vien da xoa")
            else:
                print("\nsinh vien khong ton tai")
        else:
            print("\ndanh sach sinh vien rong")
    elif (key == 4):
        if(qlsv.soLuongSinhVien() > 0):
            print("\ntim kiem sinh vien theo ten")
            print("\nnhap ten sinh vien can tim kiem")
            ten = input("\nName: ")
            kq = qlsv.findByName(ten)
            print("\nthong tin sinh vien tim thay: ")
            qlsv.showSinhVien(kq)
        else:
            print("\ndanh sach sinh vien rong")
    elif (key == 5):
        if(qlsv.soLuongSinhVien() > 0):
            qlsv.sortByDiemTB()
            print("\ndanh sach sinh vien sau khi sap xep: ")
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\ndanh sach sinh vien rong")
    elif (key == 6):
        if(qlsv.soLuongSinhVien() > 0):
            qlsv.sortByName()
            print("\ndanh sach sinh vien sau khi sap xep theo ten: ")
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\ndanh sach sinh vien rong")
    elif (key == 7):
        if(qlsv.soLuongSinhVien() > 0):
            print("\ndanh sach sinh vien: ")
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("\ndanh sach sinh vien rong")
    elif (key == 0):
        print("\nthoat chuong trinh")
        break
    else:
        print("\nlua chon khong hop le")
        print("\nhay chon lai chuc nang trong chuong trinh")
