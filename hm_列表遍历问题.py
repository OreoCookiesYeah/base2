list1 = [10, 20, 30, 40, 50]
# for num in list1:
#     print(num)
#     if num == 30 or num == 40:
#         list1.remove(num)
# print(list1)


# 不要对同一个列表 边遍历 边增删元素
temp_list = []
for num in list1:
    print(num)
    if num == 30 or num == 40:
        # list1.remove(num)
        # 遍历时,不直接删除目标数据,先记录下来
        temp_list.append(num)

# 遍历完原列表,再逐一删除每个目标数据
for target_num in temp_list:
    list1.remove(target_num)
# print(list1)