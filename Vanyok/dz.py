from collections import OrderedDict

m = int(input())
stud_amount = int(input())
stud = ''
st_lst = OrderedDict()
counter = 0
while counter != stud_amount:
    stud = input().split(' ')
    avg_mark = (int(stud[1]) + int(stud[2]) + int(stud[3]) + int(stud[4])) / 4
    st_lst.update({stud[0]: avg_mark})
    counter += 1

st_lst = OrderedDict(sorted(st_lst.items(), key=lambda x: x[1], reverse=True))

quarter = stud_amount / 4
p = m / quarter
for k, v in st_lst.items():
    print(k, p)