
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from MonopolyConstants import *
import MonopolyConstants as mc
import random
import time

last_player = 'p0'
BOT_DIFFICULTY = "Normal"


def change_last_player(last_player_from):
    global last_player
    last_player = last_player_from


def hide(widget, *args, **kwargs):
    if widget in info:
        pis[widget] = info[widget].geometry()
        info[widget].hide()

def hide_pack(widget):
    if widget in info:
        pis[widget] = info[widget].geometry()
        info[widget].hide()

def hide_grid(widget):
    if widget in info:
        pis[widget] = info[widget].geometry()
        info[widget].hide()

def show(widget, *args, **kwargs):
    if widget in info and widget in pis:
        info[widget].setGeometry(pis[widget])
        info[widget].show()

def show_pack(widget):
    if widget in info and widget in pis:
        info[widget].setGeometry(pis[widget])
        info[widget].show()

def show_grid(widget):
    if widget in info and widget in pis:
        info[widget].setGeometry(pis[widget])
        info[widget].show()

def debt_update(player, amount, to):
    p_debts[player][to] += amount
    info['status'].setText('You cant afford to pay. Your debt increased.')
    if sum(p_debts[player].values()) > p_worths[player]:
        info['status'].setText('You are bankrupt!')

def transaction(player, amount):
    p_bals[player] += amount
    p_worths[player] += amount

    # Убрал всё бесполезное


# def transaction(player, amount):
#     # Проверяем, существует ли игрок
#     if player not in p_bals or player not in p_worths:
#         raise ValueError(f"Player {player} not found in balances or worths")
#
#     # Обновляем баланс и капитал
#     p_bals[player] += amount
#     p_worths[player] += amount
#
#     # Безопасное обновление интерфейса
#     prop_box = info.get(player + '_prop_box')
#     if prop_box:
#         if prop_box.count() > 0:  # Проверяем, есть ли элементы
#             prop_box.item(0).setText(f'Player {player[1]} Balance: £{p_bals[player]}')
#         if prop_box.count() > 1:  # Проверяем второй элемент
#             prop_box.item(1).setText(f'Player {player[1]} Worth: £{p_worths[player]}')
#     else:
#         print(f"Warning: Property box for {player} not found")

def hide_enlarge():
    widgets = [
        'prop_enlarge_name', 'prop_enlarge_gap', 'prop_enlarge_cost', 'prop_enlarge_rent',
        'prop_enlarge_rent1', 'prop_enlarge_rent2', 'prop_enlarge_rent3', 'prop_enlarge_rent4',
        'prop_enlarge_rent5', 'prop_enlarge_gap2', 'prop_enlarge_hcost', 'prop_enlarge_mortgage',
        'prop_enlarge'
    ]
    for widget in widgets:
        hide_pack(widget)

def show_enlarge():
    widgets = [
        'prop_enlarge_name', 'prop_enlarge_gap', 'prop_enlarge_cost', 'prop_enlarge_rent',
        'prop_enlarge_rent1', 'prop_enlarge_rent2', 'prop_enlarge_rent3', 'prop_enlarge_rent4',
        'prop_enlarge_rent5', 'prop_enlarge_gap2', 'prop_enlarge_hcost', 'prop_enlarge_mortgage',
        'prop_enlarge'
    ]
    for widget in widgets:
        show_pack(widget)

def enlarge_update():
    prop = cur_pos[mc.cur_player]
    if prop not in info:
        return

    if info[prop]['type'] == 'property':
        show_enlarge()
        info['prop_enlarge_c'].setStyleSheet(f"background-color: {info[prop]['colour']};")
        info['prop_enlarge_name'].setText(prop)
        info['prop_enlarge_cost'].setText(f"Cost: £{info[prop]['cost']}")
        info['prop_enlarge_rent'].setText(f"Rent: £{info[prop]['rent']}")
        info['prop_enlarge_rent1'].setText(f"1 House: £{info[prop]['rent1']}")
        info['prop_enlarge_rent2'].setText(f"2 Houses: £{info[prop]['rent2']}")
        info['prop_enlarge_rent3'].setText(f"3 Houses: £{info[prop]['rent3']}")
        info['prop_enlarge_rent4'].setText(f"4 Houses: £{info[prop]['rent4']}")
        info['prop_enlarge_rent5'].setText(f"Hotel: £{info[prop]['rent5']}")
        info['prop_enlarge_hcost'].setText(f"House/Hotel Cost: £{info[prop]['HCost']}")
        info['prop_enlarge_mortgage'].setText(f"Mortgage: £{info[prop]['mortgage']}")
    elif info[prop]['type'] == 'railroad':
        show_enlarge()
        info['prop_enlarge_c'].setStyleSheet(f"background-color: {info[prop]['colour']}; border: none;")
        info['prop_enlarge_name'].setText(prop)
        info['prop_enlarge_cost'].setText(f"Cost: £{info[prop]['cost']}")
        info['prop_enlarge_rent'].setText(f"1 Railroad: £{info[prop]['rent']}")
        info['prop_enlarge_rent1'].setText(f"2 Railroads: £{info[prop]['rent1']}")
        info['prop_enlarge_rent2'].setText(f"3 Railroads: £{info[prop]['rent2']}")
        info['prop_enlarge_rent3'].setText(f"4 Railroads: £{info[prop]['rent3']}")
        info['prop_enlarge_rent4'].setText("")
        info['prop_enlarge_rent5'].setText("")
        info['prop_enlarge_hcost'].setText("")
        info['prop_enlarge_mortgage'].setText(f"Mortgage: £{info[prop]['mortgage']}")
    elif info[prop]['type'] == 'utility':
        show_enlarge()
        info['prop_enlarge_c'].setStyleSheet(f"background-color: {info[prop]['colour']}; border: none;")
        info['prop_enlarge_name'].setText(prop)
        info['prop_enlarge_cost'].setText(f"Cost: £{info[prop]['cost']}")
        info['prop_enlarge_rent'].setText("If 1 Utility owned then rent is\n4 times amount\nshown on dice.")
        info['prop_enlarge_rent1'].setText("If 2 Utilities owned then rent is\n10 times amount\nshown on dice.")
        info['prop_enlarge_rent2'].setText("")
        info['prop_enlarge_rent3'].setText("")
        info['prop_enlarge_rent4'].setText("")
        info['prop_enlarge_rent5'].setText("")
        info['prop_enlarge_hcost'].setText("")
        info['prop_enlarge_mortgage'].setText(f"Mortgage: £{info[prop]['mortgage']}")
    elif info[prop]['type'] == 'chance':
        show_enlarge()
        info['prop_enlarge_c'].setStyleSheet(f"background-color: {info[prop]['colour']}; border: none;")
        info['prop_enlarge_name'].setText("Chance")
        info['prop_enlarge_cost'].setText("")
        info['prop_enlarge_rent'].setText("")
        info['prop_enlarge_rent1'].setText("")
        info['prop_enlarge_rent2'].setText("")
        info['prop_enlarge_rent3'].setText("")
        info['prop_enlarge_rent4'].setText("")
        info['prop_enlarge_rent5'].setText("")
        info['prop_enlarge_hcost'].setText("")
        info['prop_enlarge_mortgage'].setText("")
    elif info[prop]['type'] == 'community':
        show_enlarge()
        info['prop_enlarge_c'].setStyleSheet(f"background-color: {info[prop]['colour']}; border: none;")
        info['prop_enlarge_name'].setText("Community Chest")
        info['prop_enlarge_cost'].setText("")
        info['prop_enlarge_rent'].setText("")
        info['prop_enlarge_rent1'].setText("")
        info['prop_enlarge_rent2'].setText("")
        info['prop_enlarge_rent3'].setText("")
        info['prop_enlarge_rent4'].setText("")
        info['prop_enlarge_rent5'].setText("")
        info['prop_enlarge_hcost'].setText("")
        info['prop_enlarge_mortgage'].setText("")

def isFree(prop):
    tot = 1
    ond = "non"
    for i in po_props:
        if i != mc.cur_player:
            if prop not in po_props[i]:
                tot += 1
            else:
                ond = i
    if prop in po_props[mc.cur_player]:
        return "buy player"
    # if tot == len(ps):
    #     return "non"
    # else:
    #     return ond
    return ond

def rent(payer, payee, am):
    if info[cur_pos[payer]]['type'] == 'property':
        rentn = 'rent' + str(hs[cur_pos[payer]])
        if rentn == 'rent0':
            rentn = 'rent'
        rentt = int(info[cur_pos[payer]][rentn])
    elif info[cur_pos[payer]]['type'] == 'railroad':
        t = 0
        for i in po_props[payee]:
            if info[i]['type'] == 'railroad':
                t += 1
        if t == 1:
            rentt = int(info[cur_pos[payer]]['rent'])
        else:
            rentt = int(info[cur_pos[payer]]['rent' + str(t - 1)])
    else:
        t = 0
        for i in po_props[payee]:
            if info[i]['type'] == 'utility':
                t += 1
        if t == 1:
            rentt = 4 * am
        else:
            rentt = 10 * am

    if p_bals[payer] >= rentt:
        transaction(payer, rentt * -1)
        transaction(payee, rentt)
    else:
        debt_update(payer, rentt)

def hide_house(wid):
    hide(wid)

def all_house(p):
    hide_house(info[p]['h1'])
    hide_house(info[p]['h2'])
    hide_house(info[p]['h3'])
    hide_house(info[p]['h4'])

def show_house(h, p):
    if h == 0:
        all_house(p)
        show(info[p]['h1'])
        info[p]['h1'].setStyleSheet("background-color: dark green;")
        hide_house(info[p]['h1'])
    elif h == 5:
        all_house(p)
        show(info[p]['h1'])
        info[p]['h1'].setStyleSheet("background-color: dark red;")
    else:
        for i in range(1, h + 1):
            show(info[p]['h' + str(i)])

def add_house(p):
    global hs
    hs[p] += 1
    if hs[p] == 6:
        hs[p] = 0
    show_house(hs[p], p)

def hide_player(prop, *args, **kwargs):
    for player in args:
        if prop in info and player in info[prop]:
            hide(info[prop][player])

def show_player(prop, *args, **kwargs):
    for player in args:
        if prop in info and player in info[prop]:
            show(info[prop][player])

def hide_all_players(name):
    hide_player(name, 'p1')
    hide_player(name, 'p2')

def show_all_players(name):
    show_player(name, 'p1')
    show_player(name, 'p2')

# def move_to_jail():
#     hide_player(cur_pos[mc.cur_player], mc.cur_player)
#     show_player('Just Visiting', mc.cur_player + '_jail')
#     cur_pos[mc.cur_player] = 'In Jail'
#     p_in_j[mc.cur_player] = 0

# def jail_checks(Free):
#     if p_in_j.get(mc.cur_player, 0) == 4:
#         Free = True
#     if Free:
#         hide_player('Just Visiting', mc.cur_player + '_jail')
#         show_player('Just Visiting', mc.cur_player)
#         cur_pos[mc.cur_player] = 'Just Visiting'
#         if mc.cur_player in p_in_j:
#             del p_in_j[mc.cur_player]
#         info['status'].setText('You are free from jail.')
#         change_turn()
#
#
# def pay_50():
#     if p_bals[mc.cur_player] >= 50:
#         transaction(mc.cur_player, -50)
#         jail_checks(True)
#
#
# def checkEvents(am, current):
#     prop = cur_pos[mc.cur_player]
#     enlarge_update()
#
#     if info[prop]['type'] in ['property', 'railroad', 'utility']:
#         other = isFree(cur_pos[mc.cur_player])
#         if other != 'non':
#             rent(mc.cur_player, other, am)
#         else:
#             show_enlarge()
#     else:
#         hide_enlarge()
#
#     lb = names.index(current)
#     ub = names.index(current) + am
#
#     for i in range(lb + 1, ub + 1):
#         if i >= len(names):
#             i -= 40
#         if names[i] == 'Go':
#             transaction(mc.cur_player, 200)
#             info['status'].setText('You passed Go collect £200')
#             break
#
#     if prop == 'Go To Jail':
#         move_to_jail()
#     elif prop == 'In Jail':
#         jail_checks(False)
#
#     if prop == 'Super Tax':
#         transaction(mc.cur_player, -100)
#         info['status'].setText('Pay £100 in Super Tax!')
#     elif prop == 'Income Tax':
#         transaction(mc.cur_player, -200)
#         info['status'].setText('Pay £200 in Income Tax!')


# def move_player(self, player, am, Free):
#     global can_buy_right_now
#     current = cur_pos[player]
#
#     if current != 'In Jail':
#         c = names.index(current)
#         can_buy_right_now = False
#
#         for i in range(am):
#             hide_player(cur_pos[player], player)
#             c += 1
#             if c > 39:
#                 c -= 40
#             cur_pos[player] = names[c]
#             show_player(cur_pos[player], player)
#             QApplication.processEvents()
#             time.sleep(0.3)
#
#         info['status'].setText(f'You landed on {cur_pos[player]}.')
#         can_buy_right_now = True
#         checkEvents(am, current)
#     else:
#         jail_checks(Free)


# def blank(x, s1, s2, s3, s4, s5, s6, s7, s8, s9):
#     for s in [s1, s2, s3, s4, s5, s6, s7, s8, s9]:
#         x.itemConfigure(s, visible=False)


# def dnum(x, num, f1d, f2d, f3d, f4d, f5d, f6d, s1, s2, s3, s4, s5, s6, s7, s8, s9):
#     blank(x, s1, s2, s3, s4, s5, s6, s7, s8, s9)
#     for i in locals()[f'f{num}d']:
#         x.itemConfigure(i, visible=True)
#     return num


# def roll(self, s1, s2, s3, s4, s5, s6, s7, s8, s9, dice1, dice2, f1d, f2d, f3d, f4d, f5d, f6d, roll_label, Pturn, T):
#     global last_player
#
#     if last_player == Pturn:
#         if len(ps) > 1:
#             info['status'].setText('End Turn to roll.')
#         else:
#             num1 = dnum(dice1, random.randint(1, 6), f1d, f2d, f3d, f4d, f5d, f6d, s1, s2, s3, s4, s5, s6, s7, s8, s9)
#             num2 = dnum(dice2, random.randint(1, 6), f1d, f2d, f3d, f4d, f5d, f6d, s1, s2, s3, s4, s5, s6, s7, s8, s9)
#             total = num1 + num2
#             roll_label.setText(str(total))
#
#             Free = (num1 == num2)
#             QApplication.processEvents()
#             time.sleep(0.5)
#             move_player(self, Pturn, total, Free)
#
#             last_player = f'p{int(last_player[1]) + 1}'
#             if last_player == 'p7':
#                 last_player = 'p1'
#     else:
#         num1 = dnum(dice1, random.randint(1, 6), f1d, f2d, f3d, f4d, f5d, f6d, s1, s2, s3, s4, s5, s6, s7, s8, s9)
#         num2 = dnum(dice2, random.randint(1, 6), f1d, f2d, f3d, f4d, f5d, f6d, s1, s2, s3, s4, s5, s6, s7, s8, s9)
#         total = num1 + num2
#         roll_label.setText(str(total))
#
#         Free = (num1 == num2)
#         QApplication.processEvents()
#         time.sleep(0.5)
#         move_player(self, Pturn, total, Free)
#
#         last_player = f'p{int(last_player[1]) + 1}'
#         if last_player == 'p7':
#             last_player = 'p1'


# def change_turn():
#     global last_player
#
#     if mc.cur_player in p_in_j:
#         p_in_j[mc.cur_player] += 1
#         jail_checks(False)
#
#     MonopolyConstants.change_cur_player()
#
#     if mc.cur_player in p_in_j:
#         info['status'].setText(
#             f'Roll doubles to be free.\n Pay £50 to be free.\n Wait 3 turns to be free.\n Turn {p_in_j[mc.cur_player]}/3.')
#         show(info['pay_50_button'])
#     else:
#         temp = pis.get(info['pay_50_button'], None)
#         hide(info['pay_50_button'])
#         if temp:
#             pis[info['pay_50_button']] = temp
#
#     info['turn_label'].setText(f"Player {mc.cur_player[1]}'s turn")
#
#     if mc.cur_player == "p2":
#         bot_turn()


def Buy(prop):
    po_props[mc.cur_player].append(prop)
    transaction(mc.cur_player, int(info[prop]['cost']) * -1)
    p_worths[mc.cur_player] += int(info[prop]['mortgage'])
    transaction(mc.cur_player, 0)

    # Убрал всё бесполезное в функции


def check_group(col, prop):
    if col not in ['blue', 'brown']:
        t = 0
        for i in po_props[mc.cur_player]:
            if info[i]['colour'] == col:
                t += 1
        return t == 3
    else:
        t = 0
        for i in po_props[mc.cur_player]:
            if info[i]['colour'] == col:
                t += 1
        return t == 2

def build():
    def check_group(col, prop):
        if col not in ['blue', 'brown']:
            t = 0
            for i in po_props[mc.cur_player]:
                if info[i]['colour'] == col:
                    t += 1
            return t == 3
        else:
            t = 0
            for i in po_props[mc.cur_player]:
                if info[i]['colour'] == col:
                    t += 1
            return t == 2

    prop = cur_pos[mc.cur_player]
    col = info[prop]['colour']

    if info[prop]['type'] == 'property':
        if p_bals[mc.cur_player] >= int(info[prop]['HCost']):
            if check_group(col, prop):
                add_house(prop)
                transaction(mc.cur_player, int(info[prop]['HCost']) * -1)
            else:
                info['status'].setText('You need to own all the\nproperties in the\ncolour group to buy a house.')
        else:
            info['status'].setText('Not enough money.')
    else:
        info['status'].setText("You can't build here.")


# def bot_turn():
#     if mc.cur_player == "p2":
#         if BOT_DIFFICULTY == "Easy":
#             prop = cur_pos["p2"]
#             if info[prop]['type'] in ['property', 'railroad', 'utility']:
#                 if isFree(prop) == 'non' and p_bals["p2"] >= int(info[prop]['cost']):
#                     Buy(prop)
#         elif BOT_DIFFICULTY == "Normal":
#             prop = cur_pos["p2"]
#             if info[prop]['type'] in ['property', 'railroad', 'utility']:
#                 if isFree(prop) == 'non' and p_bals["p2"] >= int(info[prop]['cost']):
#                     if random.random() < 0.7:
#                         Buy(prop)
#         elif BOT_DIFFICULTY == "Hard":
#             prop = cur_pos["p2"]
#             if info[prop]['type'] in ['property', 'railroad', 'utility']:
#                 if isFree(prop) == 'non' and p_bals["p2"] >= int(info[prop]['cost']):
#                     color = info[prop]['colour']
#                     count = sum(1 for p in po_props["p2"] if info[p]['colour'] == color)
#                     if (color in ['brown', 'blue'] and count == 1) or \
#                             (color not in ['brown', 'blue'] and count == 2) or \
#                             info[prop]['type'] in ['railroad', 'utility']:
#                         Buy(prop)
#                     elif random.random() < 0.5:
#                         Buy(prop)
#         info['turn_label'].setText(f"Player {mc.cur_player[1]}'s turn")