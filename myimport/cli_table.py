from os import system
import msvcrt

def table_printer(table, pointer=False):
    # rows = len(table)
    cols = len(table[0])

    if pointer:
        cols-=1

    max_col_len = []
    for _ in range(cols):
        max_col_len.append(0)

    for i in range(len(max_col_len)):
        for r in table:
            if max_col_len[i] < len(r[i]):
                max_col_len[i] = len(r[i])

    # first
    if pointer:
        print(end='   ')
    print(end='+-')
    for i in range(cols):
        print('-' * max_col_len[i], end='-+-')
    print(end='\b \n')

    # heading
    if pointer:
        print(end='   ')
    print(end='| ')
    for i in range(cols):
        print(table[0][i].ljust(max_col_len[i]), end=' | ')
    print()

    if pointer:
        print(end='   ')
    print(end='+-')
    for i in range(cols):
        print('-' * max_col_len[i], end='-+-')
    print(end='\b \n')

    # rows
    for i in table[1:]:
        if pointer:
            print(i[-1], end=' ')
        print(end='| ')
        for j in range(cols):
            print(i[j].ljust(max_col_len[j]), end=' | ')
        print()

    # last
    if pointer:
        print(end='   ')
    print(end='+-')
    for i in range(cols):
        print('-' * max_col_len[i], end='-+-')
    print(end='\b \n')


def point_to_table(table, heading):
    pointer_table = table
    for i in pointer_table:
        i.append('  ')
    pointer_table[1][-1] = '->'

    p = 0
    p_next = 0
    while True:
        print(heading.upper())
        table_printer(pointer_table, True)

        key = ord(msvcrt.getch())
        if key == 27:   # ESC
            break

        elif key == 13: # Enter
            return p

        elif key == 224:    # Special keys (arrows, f keys, ins, del, etc.)
            key = ord(msvcrt.getch())
            if key == 80 and p < len(pointer_table)-2:   # Down arrow
                p_next = p + 1
            elif key == 72 and p > 0:   # Up arrow
                p_next = p - 1

        pointer_table[p+1][-1] = '  '
        pointer_table[p_next+1][-1] = '->'
        p = p_next

        system('cls')

