def tinh_tong_so_chan(lst):
    tong = 0
    for i in lst:
        if i % 2 == 0:
            tong += i
    return tong
 
input_list =  input("nhap danh sach cac so: (cach nhau bang giau phay: )") 
numbers = list(map(int, input_list.split(',')))
print("tong cac so chan trong danh sach la:", tinh_tong_so_chan(numbers))
