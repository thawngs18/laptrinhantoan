def truy_cap_phan_tu(tuple_data):
    firs_element = tuple_data[0]
    last_element = tuple_data[-1]
    return firs_element, last_element

input_tuple = input("Nhap tuple: ")
first,last = truy_cap_phan_tu(input_tuple)
print("Phan tu dau tien: ",first)
print("Phan tu cuoi cung: ",last)
