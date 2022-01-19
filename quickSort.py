def quicksort(table: list, left=0, right=None):
    if right is None: right = len(table) - 1
    i, j = left, right
    pivot = table[(left + right) // 2]
    while i <= j:
        while table[i] < pivot:
            i += 1
        while table[j] > pivot:
            j -= 1
        if i <= j:
            table[i], table[j] = table[j], table[i]
            i += 1
            j -= 1
    if left < i: quicksort(table, left, j)
    if right > i: quicksort(table, i, right)
