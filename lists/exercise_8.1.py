def chop(lst):
    lst.pop(0)
    lst.pop(-1)

def middle(lst):
    new_lst = lst[1:-1]
    return new_lst

chop([1, 2, 3, 4])
print(middle([1, 2, 3, 4]))