def dao_nguoi_list(lst):
    return lst[::-1]
input_list = input("Nhap vao mot danh sach: ")
lst = input_list.split()
print("Danh sach sau khi dao nguoc la: ", dao_nguoi_list(lst))