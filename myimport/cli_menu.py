from os import system
import msvcrt

def menu_creator(menu, heading):
    
    pointed_menu = []
    for i in menu:
        pointed_menu.append(['  ', i])
    pointed_menu[0][0] = '->'

    p = 0
    p_next = 0
    while True:
        print(heading.upper())
        for i in pointed_menu:
            print(i[0], i[1])

        key = ord(msvcrt.getch())
        if key == 27:   # ESC
            break

        elif key == 13: # Enter
            return p

        elif key == 224:    # Special keys (arrows, f keys, ins, del, etc.)
            key = ord(msvcrt.getch())
            if key == 80 and p < len(menu)-1:   # Down arrow
                p_next = p + 1
            elif key == 72 and p > 0:   # Up arrow
                p_next = p - 1

        pointed_menu[p][0] = '  '
        pointed_menu[p_next][0] = '->'
        p = p_next

        system('cls')



