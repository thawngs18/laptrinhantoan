def tao_tuple_tu_list(lst):
    return tuple(lst)

input_lst = input("nhap danh sach cac so (cach nhau bang dau phay) : ")
numbers = list(map(int, input_lst.split(",")))
my_tuple = tao_tuple_tu_list(numbers)
print("list: ",numbers)
print("tuple tu list:", my_tuple)
