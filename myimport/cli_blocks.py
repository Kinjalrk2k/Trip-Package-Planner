def print_in_blocks(li, bp):
    dli = []
    temp_list = []

    for i in range(len(li)):
        temp_list.append(li[i])
        if i != 0 and (i+1)%bp == 0:
            dli.append(temp_list)
            temp_list = []

    cols = bp

    max_col_len = []
    for _ in range(cols):
        max_col_len.append(0)

    for i in range(len(max_col_len)):
        for r in dli:
            if max_col_len[i] < len(r[i]):
                max_col_len[i] = len(r[i])

    print(end='+-')
    for i in range(cols):
        print('-' * max_col_len[i], end='-+-')
    print(end='\b \n')

    for i in dli:
        print(end='| ')
        for j in range(cols):
            print(i[j].ljust(max_col_len[j]), end=' | ')
        print()

        print(end='+-')
        for i in range(cols):
            print('-' * max_col_len[i], end='-+-')
        print(end='\b \n')