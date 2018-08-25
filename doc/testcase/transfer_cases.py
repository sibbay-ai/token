
matrix =[ \
    {"interD-1"}, \
    {"accD-1", "accD-2", "accD-3", "accD-4", "accD-5"}, \
    {"contSD-1", "contSD-2"}, \
    {"buySellSD-1", "buySellSD-2"}, \
    {"destAddrZD-1", "destAddrZD-2"}, \
    {"destAddrBsFD-1","destAddrBsFD-2"}, \
    {"lockBD-1","lockBD-2","lockBD-3","lockBD-4"}, \
    {"tokenBD-1", "tokenBD-2"}, \
    {"contBD-1", "contBD-2"}, \
    {"fundBD-1", "fundBd-2"}, \
    {"valueBD-1", "valueBD-2"}, \
    {"sellPD-1", "sellPD-2", "sellPD-3"}, \
    {"senderBD-1", "senderBD-2"}, \
    {"fundAccD-1", "fundAccD-2", "fundAccD-3"} 
]

len_matrix = len(matrix)
print("length of matrix:", len_matrix)

max_ret = 1
ret = {}
cnt = 1

for i in range(len_matrix):
    max_ret = max_ret * len(matrix[i])
    print("len matrix:", len(matrix[i]))

print("max-ret:", max_ret)

def group_ret():
    group = "Test"
    for i in range(len(matrix)):
        group = group + "_" + ret[i]
    print(cnt, group)



def search(i):
    if i == (len_matrix - 1):
        for mem in matrix[i]:
            ret[i] = mem
            group_ret()
            global cnt
            cnt = cnt + 1
        return
    for mem in matrix[i]:
        ret[i] = mem
        search(i+1)

search(0)
