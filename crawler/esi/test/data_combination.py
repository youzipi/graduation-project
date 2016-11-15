a = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8],
    [3, 6, 9],
    [4, 5, 7]
]
b = [[0 for j in range(10)] for i in range(10)]

for arr in a:
    length = len(arr)
    for current_index in range(length):
        current = arr[current_index]
        for forward_index in range(current_index + 1, length):
            forward = arr[forward_index]
            b[current][forward] += 1

for arr in b:
    print arr

print b[2][4]  # 2

for i in range(10):
    for j in range(10):
        if b[i][j] > 0:
            print 'item1:{0},item2:{1},count:{2}'.format(i, j, b[i][j])
