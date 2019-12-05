def gotDouble(num):
    for pos in range(len(num)-1):
        if num[pos] == num[pos+1] and (pos==0 or num[pos] != num[pos-1]) and (pos==len(num)-2 or num[pos] != num[pos+2]):
            return True
    return False




def isvalid(num):
    valid=False
    for digit in range(1,len(num)):
        if num[digit]<num[digit-1]:
            return False
        if gotDouble(num):
            valid = True
    return valid


print( sum([1 for num in range(231832,767347) if isvalid(str(num))]))


