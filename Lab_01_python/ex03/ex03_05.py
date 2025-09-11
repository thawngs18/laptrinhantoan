def dem_so_lan_xuat_hien(lst):
    count = {};
    for item in lst:
        if item in count:
            count[item] += 1
        else:
            count[item] = 1
    return count

input_string = input("nhap danh sach cac tu  (cach nhau dau phay) :")
word_list = input_string.split(",")
count_dict = dem_so_lan_xuat_hien(word_list)
print("so lan xuat hien cua cac tu trong danh sach la:",count_dict)

