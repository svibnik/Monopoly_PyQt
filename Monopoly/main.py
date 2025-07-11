
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                             QListWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QMessageBox, QDialog, QMenuBar, QMenu)
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush, QFont, QAction, QPixmap
import random
import time

import MonopolyConstants as mc
import MonopolyFunctions as mf
from MonopolyConstants import *
from MonopolyFunctions import *

class PropertyWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.info = info[name]                 # Получаем данные по клетки из славаря
        self.initUI()

    def initUI(self):
        pos = self.info['position']            # Позиция каждой клетки

                                               # Определяем форму клетки в зависимости от ее положения
        if pos[0] in [0, 10] and pos[1] in [0, 10]:  # Угловые клетки
            self.setFixedSize(80, 80)  # Квадратные
        elif pos[0] in [0, 10]:  # Боковые клетки (лево/право)
            self.setFixedSize(80, 48)  # Широкие
        elif pos[1] in [0, 10]:  # Верхние/нижние клетки
            self.setFixedSize(48, 80)  # Высокие
        else:  # Все остальные (не должны быть в классической монополии)
            self.setFixedSize(64, 64)

        # Убираем закругления
        self.setStyleSheet(f"""
            background-color: {self.info['colour']};
            border: 1px solid black;
            border-radius: 0px;
        """)

        # Название свойства
        self.name_label = QLabel(self.info.get('name', self.name), self)

        # На клетках пишем названия
        if pos[0] in [0, 10] and pos[1] in [0, 10]:  # Угловые
            self.name_label.setGeometry(0, 0, 80, 80)
        elif pos[0] in [0, 10]:  # Боковые
            self.name_label.setGeometry(0, 0, 80, 48)
        elif pos[1] in [0, 10]:  # Верхние/нижние
            self.name_label.setGeometry(0, 0, 48, 80)
        else:
            self.name_label.setGeometry(0, 0, 64, 64)

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)   # Выравнивание текста по центру
        self.name_label.setWordWrap(True)                            # Перенос слов разрешить
        self.name_label.setStyleSheet("""
            background-color: darkgrey;
            font-size: 9px;
            font-weight: bold;
            padding: 2px;
        """)

                                                                      # Цветная полоса (верхняя часть клетки)
        self.color_frame = QFrame(self)
        if self.info['colour'] == 'lightgrey':
            self.color_frame.setGeometry(0, 0, 0, 0)
        else:
            if pos[0] in [0, 10] and pos[1] in [0, 10]:  # Угловые
                self.color_frame.setGeometry(0, 0, 0, 0)
            elif pos[0] == 0:  # Боковые левые
                self.color_frame.setGeometry(68, 0, 12, 48)
            elif pos[0] == 10: # правые
                self.color_frame.setGeometry(0, 0, 12, 48)
            elif pos[1] == 0:  # Верхние
                self.color_frame.setGeometry(0, 68, 48, 12)
            elif pos[1] == 10:  # нижние
                self.color_frame.setGeometry(0, 0, 48, 12)
            else:
                self.color_frame.setGeometry(0, 0, 64, 64)
        self.color_frame.setStyleSheet(f"""
            background-color: {self.info['colour']};
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border: 1px solid black;
        """)


        # Позиции игроков                                     Доделать, если времени
        self.player1 = QFrame(self)
        self.player1.setGeometry(16, 24, 12, 12)
        self.player1.setStyleSheet("""
            background-color: red; 
            border: 1px solid white;
        """)
        self.player1.hide()

        self.player2 = QFrame(self)
        self.player2.setGeometry(32, 24, 12, 12)
        self.player2.setStyleSheet("""
            background-color: blue; 
            border: 1px solid white;
        """)
        self.player2.hide()



class DiceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(54, 54)
        self.value = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw dice background
        painter.setBrush(QBrush(QColor("lightgrey")))
        painter.drawRoundedRect(0, 0, 54, 54, 5, 5)

        # Draw dots based on value
        painter.setBrush(QBrush(QColor("black")))

        dot_positions = {
            1: [(27, 27)],
            2: [(13, 13), (41, 41)],
            3: [(13, 13), (27, 27), (41, 41)],
            4: [(13, 13), (13, 41), (41, 13), (41, 41)],
            5: [(13, 13), (13, 41), (27, 27), (41, 13), (41, 41)],
            6: [(13, 13), (13, 27), (13, 41), (41, 13), (41, 27), (41, 41)]
        }

        for pos in dot_positions[self.value]:
            painter.drawEllipse(pos[0] - 4, pos[1] - 4, 8, 8)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monopoly")
        self.setFixedSize(960, 640)  # Увеличена ширина окна         # Настроить изменяющ размер если время

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.initUI()
        self.initMenu()

    def initUI(self):
        #self.setStyleSheet("background-color: lightgreen;")

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы, чтобы поле было в углу

        # Game board
        self.board_widget = QWidget()
        self.board_widget.setFixedSize(596, 596)  # Увеличена ширина доски      Нужно если есть время умненьшить ширину!

        # Создаем QLabel для фонового изображения внутри board_widget
        board_background = QLabel(self.board_widget)
        pixmap = QPixmap("Monopoly/img/background.jpg")

        #self.board_widget.setStyleSheet("background-color: transparent;")  # Прозрачный фон что бы он не перекрывал главное акно
        self.board_layout = QGridLayout(self.board_widget)
        self.board_layout.setSpacing(0)
        self.board_layout.setContentsMargins(0, 0, 0, 0)

        # Масштабируем изображение под размер виджета
        board_background.setPixmap(pixmap.scaled(
            self.board_widget.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        board_background.setGeometry(80, 80, 510, 510)
        board_background.lower()  # Отправляем на задний план

        # Заполнение доски(её сетки) клетками недвижимости
        self.property_widgets = {}
        for name, data in info.items():
            row = data['position'][1]
            col = data['position'][0]

            prop = PropertyWidget(name)
            self.property_widgets[name] = prop
            self.board_layout.addWidget(prop, row, col)

        # Side panel
        side_panel = QWidget()
        side_panel.setFixedWidth(320)
        side_layout = QVBoxLayout(side_panel)

        # Player info
        self.player1_list = QListWidget()
        self.player2_list = QListWidget()

        # # Добавляем в глобальный словарь
        # info['p1_prop_box'] = self.player1_list
        # info['p2_prop_box'] = self.player2_list


        player_info_layout = QHBoxLayout()
        player_info_layout.addWidget(self.player1_list)
        player_info_layout.addWidget(self.player2_list)

        # Property enlarge view
        self.prop_enlarge = QFrame()
        self.prop_enlarge.setFixedSize(175, 280)
        self.prop_enlarge.setStyleSheet("background-color: white; border: 1px solid black;")
        self.prop_enlarge.hide()

        self.prop_enlarge_c = QFrame(self.prop_enlarge)
        self.prop_enlarge_c.setFixedSize(175, 48)
        self.prop_enlarge_c.move(0, 0)

        self.prop_enlarge_name = QLabel(self.prop_enlarge)
        self.prop_enlarge_name.setFixedSize(175, 24)
        self.prop_enlarge_name.move(0, 48)
        self.prop_enlarge_name.setFont(QFont("Helvetica", 14))
        self.prop_enlarge_name.setStyleSheet("text-decoration: underline;")

        self.prop_enlarge_cost = QLabel(self.prop_enlarge)
        self.prop_enlarge_cost.setFixedSize(175, 16)
        self.prop_enlarge_cost.move(0, 72)

        self.prop_enlarge_rent = QLabel(self.prop_enlarge)
        self.prop_enlarge_rent.setFixedSize(175, 16)
        self.prop_enlarge_rent.move(0, 88)

        # Dice and controls
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)

        self.dice1 = DiceWidget()
        self.dice2 = DiceWidget()

        dice_layout = QHBoxLayout()
        dice_layout.addWidget(self.dice1)
        dice_layout.addWidget(self.dice2)

        self.roll_button = QPushButton("Roll")
        self.roll_button.clicked.connect(self.roll_dice)

        self.end_turn_button = QPushButton("End Turn")
        self.end_turn_button.clicked.connect(self.change_turn)

        self.buy_button = QPushButton("Buy")
        self.buy_button.clicked.connect(self.buy_property)

        self.build_button = QPushButton("Build")
        self.build_button.clicked.connect(self.build_house)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.build_button)

        control_layout.addLayout(dice_layout)
        control_layout.addWidget(self.roll_button)
        control_layout.addWidget(self.end_turn_button)
        control_layout.addLayout(button_layout)

        # Status message
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Helvetica", 14))

        # Add widgets to side layout
        side_layout.addLayout(player_info_layout)
        side_layout.addWidget(self.prop_enlarge)
        side_layout.addWidget(control_widget)
        side_layout.addWidget(self.status_label)

        # Add board and side panel to main layout
        main_layout.addWidget(self.board_widget)
        main_layout.addWidget(side_panel)

        # В initUI():
        self.prop_enlarge = QFrame()
        self.prop_enlarge.setFixedSize(200, 320)
        self.prop_enlarge.setStyleSheet("""
            background-color: #f5f5f5;
            border: 2px solid #8B4513;
            border-radius: 5px;
            padding: 10px;
        """)

        # Заголовок
        self.prop_enlarge_name = QLabel(self.prop_enlarge)
        self.prop_enlarge_name.setGeometry(8, 8, 184, 45)
        self.prop_enlarge_name.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            border-bottom: 1px solid gray;
        """)

        # Основная информация
        self.prop_enlarge_info = QTextEdit(self.prop_enlarge)
        self.prop_enlarge_info.setGeometry(8, 48, 184, 264)
        self.prop_enlarge_info.setReadOnly(True)

        # Initialize game state
        self.init_game()

    def initMenu(self):
        menubar = self.menuBar()

        # Game menu
        game_menu = menubar.addMenu('Game')

        help_action = QAction('Help', self)
        help_action.triggered.connect(self.show_help)
        game_menu.addAction(help_action)

        players_action = QAction('Player Key', self)
        players_action.triggered.connect(self.show_player_key)
        game_menu.addAction(players_action)

    def init_game(self):
        # Initialize player positions and balances
        for i in range(1, 3):
            cur_pos['p' + str(i)] = 'Go'
            p_bals['p' + str(i)] = 1500
            p_worths['p' + str(i)] = 1500
            p_debts['p' + str(i)] = {'p1': 0, 'p2': 0}
            po_props['p' + str(i)] = []

        change_ps(2)
        for i in info:
            names.append(i)

        # Show initial player positions
        for player in cur_pos:
            self.show_player(cur_pos[player], player)

        # Update player info boxes
        self.update_player_info()

        # Set initial turn
        self.turn_label = QLabel("Player 1's turn")                                     # Разместить с верху по середине квадрата если есть время
        self.turn_label.setFont(QFont("Helvetica", 10, QFont.Weight.Bold))
        self.statusBar().addWidget(self.turn_label)

        self.last_player = 'p0'

    def show_player(self, prop, player):
        if prop in self.property_widgets:                                               # Добавить показ играков если есть время
            if player == 'p1':
                self.property_widgets[prop].player1.show()
            else:
                self.property_widgets[prop].player2.show()

    def hide_player(self, prop, player):
        if prop in self.property_widgets:
            if player == 'p1':
                self.property_widgets[prop].player1.hide()
            else:
                self.property_widgets[prop].player2.hide()

    def update_player_info(self):
        # Очищаем оба списка
        self.player1_list.clear()
        self.player2_list.clear()

        # Заполняем список только для Player 1
        self.player1_list.addItem(f'Player 1')
        self.player1_list.addItem(f'Balance: £{p_bals["p1"]}')
        self.player1_list.addItem(f'Worth: £{p_worths["p1"]}')
        self.player1_list.addItem(f'Debt: £{sum(p_debts["p1"].values())}')
        self.player1_list.addItem('─── Owned Properties ───')
        for prop in po_props["p1"]:
            item = QListWidgetItem(prop)
            item.setBackground(QColor(info[prop]['colour']))
            self.player1_list.addItem(item)

        # Заполняем список только для Player 2                              # Для двух играков
        self.player2_list.addItem(f'Player 2')
        self.player2_list.addItem(f'Balance: £{p_bals["p2"]}')
        self.player2_list.addItem(f'Worth: £{p_worths["p2"]}')
        self.player2_list.addItem(f'Debt: £{sum(p_debts["p2"].values())}')
        self.player2_list.addItem('─── Owned Properties ───')
        for prop in po_props["p2"]:
            item = QListWidgetItem(prop)
            item.setBackground(QColor(info[prop]['colour']))
            self.player2_list.addItem(item)

    def roll_dice(self):
        if self.last_player == mc.cur_player:
            self.status_label.setText('End Turn to roll.')
        else:
            self.do_roll()

    def do_roll(self):
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        total = num1 + num2

        self.dice1.value = num1
        self.dice2.value = num2
        self.dice1.update()
        self.dice2.update()

        self.move_player(mc.cur_player, total)

        if self.last_player != 'p1':
            self.last_player = 'p1'
            mf.change_last_player('p1')
        else:
            self.last_player = 'p2'
            mf.change_last_player('p2')


    def move_player(self, player, am):
        current = cur_pos[player]

        c = names.index(current)

        for i in range(am):
            self.hide_player(cur_pos[player], player)
            c += 1
            if c > 39:
                c -= 40
            cur_pos[player] = names[c]
            self.show_player(cur_pos[player], player)
            QApplication.processEvents()
            time.sleep(0.3)

        self.status_label.setText(f'You landed on {cur_pos[player]}.')
        self.check_events(am, current)

    def check_events(self, am, current):
        prop = cur_pos[mc.cur_player]
        self.enlarge_update()

        if info[prop]['type'] in ['property', 'railroad', 'utility']:
            other = isFree(prop)
            if other != "non" and other != "buy player":
                rent(mc.cur_player, other, am)
            else:
                self.show_enlarge()
        else:
            self.hide_enlarge()

        lb = names.index(current)
        ub = names.index(current) + am

        for i in range(lb + 1, ub + 1):
            if i >= len(names):
                i -= 40
            if names[i] == 'Go':
                transaction(mc.cur_player, 200)
                self.status_label.setText('You passed Go collect £200')
                break

        if prop == 'Go To Jail':
            self.move_to_jail()
        elif prop == 'Super Tax':
            transaction(mc.cur_player, -100)
            self.status_label.setText('Pay £100 in Super Tax!')
        elif prop == 'Income Tax':
            transaction(mc.cur_player, -200)
            self.status_label.setText('Pay £200 in Income Tax!')

    def enlarge_update(self):
        prop = cur_pos[mc.cur_player]
        self.prop_enlarge_name.setText(prop)

        info_text = ""
        if info[prop]['type'] == 'property':
            info_text = f"""
            <b>Cost:</b> £{info[prop]['cost']}<br>
            <b>Rent:</b> £{info[prop]['rent']}<br>
            <b>With 1 House:</b> £{info[prop]['rent1']}<br>
            <b>With 2 Houses:</b> £{info[prop]['rent2']}<br>
            <b>With 3 Houses:</b> £{info[prop]['rent3']}<br>
            <b>With 4 Houses:</b> £{info[prop]['rent4']}<br>
            <b>With Hotel:</b> £{info[prop]['rent5']}<br>
            <b>House Cost:</b> £{info[prop]['HCost']}<br>
            <b>Mortgage Value:</b> £{info[prop]['mortgage']}
            """
        elif info[prop]['type'] == 'railroad':
            info_text = f"""
            <b>Cost:</b> £{info[prop]['cost']}<br>
            <b>Rent:</b> £{info[prop]['rent']}<br>
            <b>If 2 Railroads:</b> £{info[prop]['rent1']}<br>
            <b>If 3 Railroads:</b> £{info[prop]['rent2']}<br>
            <b>If 4 Railroads:</b> £{info[prop]['rent3']}<br>
            <b>Mortgage Value:</b> £{info[prop]['mortgage']}
            """

        self.prop_enlarge_info.setHtml(info_text)
        self.prop_enlarge.show()

    def show_enlarge(self):
        self.prop_enlarge.show()

    def hide_enlarge(self):
        self.prop_enlarge.hide()

    def change_turn(self):
        mc.change_cur_player()

        self.turn_label.setText(f"Player {mc.cur_player[1]}'s turn")
        self.update_player_info()

        if mc.cur_player == 'p2':
            self.bot_turn()

    def buy_property(self):
        prop = cur_pos[mc.cur_player]

        if info[prop]['type'] in ['property', 'railroad', 'utility']:
            if prop not in po_props[mc.cur_player]:
                if isFree(prop) == 'non':
                    if p_bals[mc.cur_player] >= int(info[prop]['cost']):
                        Buy(prop)
                        self.update_player_info()
                    else:
                        self.status_label.setText('Not Enough Money!')
                else:
                    self.status_label.setText('Already Owned By You!')
        else:
            self.status_label.setText("You can't buy this.")

    def build_house(self):
        prop = cur_pos[mc.cur_player]
        col = info[prop]['colour']

        if info[prop]['type'] == 'property':
            if p_bals[mc.cur_player] >= int(info[prop]['HCost']):
                if check_group(col, prop):
                    add_house(prop)
                    transaction(mc.cur_player, int(info[prop]['HCost']) * -1)
                    self.update_player_info()
                else:
                    self.status_label.setText(
                        'You need to own all the\nproperties in the\ncolour group to buy a house.')
            else:
                self.status_label.setText('Not enough money.')
        else:
            self.status_label.setText("You can't build here.")

    def move_to_jail(self):
        self.hide_player(cur_pos[mc.cur_player], mc.cur_player)
        self.show_player('Just Vsitng', mc.cur_player)
        cur_pos[mc.cur_player] = 'Just Vsitng'

    def bot_turn(self):
        if mc.cur_player == "p2":
            self.roll_dice()
            if BOT_DIFFICULTY == "Easy":
                prop = cur_pos["p2"]
                if info[prop]['type'] in ['property', 'railroad', 'utility']:
                    if isFree(prop) == 'non' and p_bals["p2"] >= int(info[prop]['cost']):
                        Buy(prop)
            elif BOT_DIFFICULTY == "Normal":
                prop = cur_pos["p2"]
                if info[prop]['type'] in ['property', 'railroad', 'utility']:
                    if isFree(prop) == 'non' and p_bals["p2"] >= int(info[prop]['cost']):
                        if random.random() < 0.7:
                            Buy(prop)
            elif BOT_DIFFICULTY == "Hard":
                prop = cur_pos["p2"]
                if info[prop]['type'] in ['property', 'railroad', 'utility']:
                    if isFree(prop) == 'non' and p_bals["p2"] >= int(info[prop]['cost']):
                        color = info[prop]['colour']
                        count = sum(1 for p in po_props["p2"] if info[p]['colour'] == color)
                        if (color in ['brown', 'blue'] and count == 1) or \
                                (color not in ['brown', 'blue'] and count == 2) or \
                                info[prop]['type'] in ['railroad', 'utility']:
                            Buy(prop)
                        elif random.random() < 0.5:
                            Buy(prop)

            self.update_player_info()
            self.turn_label.setText(f"Player {mc.cur_player[1]}'s turn")

        self.change_turn()

    def show_help(self):
        QMessageBox.information(self, "Help",
                                "Monopoly Game Help\n\nRoll the dice to move around the board.\nBuy properties to collect rent from other players.")

    def show_player_key(self):
        QMessageBox.information(self, "Player Key", "Player 1: Red\nPlayer 2 (Bot): Green")

class MainMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monopoly - Main Menu")
        self.setFixedSize(400, 300)

        background = QLabel(self)
        pixmap = QPixmap("Monopoly/img/background.jpg")
        background.setPixmap(pixmap.scaled(self.size(),
                                        Qt.AspectRatioMode.IgnoreAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()  # Отправляем на задний план

        layout = QVBoxLayout()

        title_label = QLabel("MONOPOLY")
        title_label.setFont(QFont("Helvetica", 26, QFont.Weight.Bold))
        title_label.setStyleSheet(f"""
            color: white;
            background-color: black;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_button = QPushButton("Start Game")
        start_button.setFont(QFont("Helvetica", 20))
        start_button.setStyleSheet(f"""
            color: green;
            background-color: lightblue;
            border-radius: 15px;
            border: 1px solid black;
        """)
        start_button.clicked.connect(self.show_difficulty_menu)

        exit_button = QPushButton("Exit")
        exit_button.setFont(QFont("Helvetica", 20))
        exit_button.setStyleSheet(f"""
            color: red;
            background-color: lightblue;
            border-radius: 15px;
            border: 1px solid black;
        """)
        exit_button.clicked.connect(self.exit_app)  # Изменено здесь

        layout.addWidget(title_label)
        layout.addWidget(start_button)
        layout.addWidget(exit_button)
        layout.addStretch()

        self.setLayout(layout)

    def show_difficulty_menu(self):
        self.difficulty_menu = DifficultyMenu()
        self.difficulty_menu.exec()
        self.close()

    def exit_app(self):
        QApplication.exit()  # Корректное завершение приложения


class DifficultyMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monopoly - Select Difficulty")
        self.setFixedSize(400, 300)
        self.setStyleSheet(f"""
            background-color: lightblue;
        """)

        layout = QVBoxLayout()

        title_label = QLabel("Select Bot Difficulty")
        title_label.setFont(QFont("Helvetica", 26, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        easy_button = QPushButton("Easy")
        easy_button.setFont(QFont("Helvetica", 20))
        easy_button.setStyleSheet(f"""
            background-color: green;
            border-radius: 15px;
            border: 1px solid black;
        """)
        easy_button.clicked.connect(lambda: self.set_difficulty("Easy"))

        normal_button = QPushButton("Normal")
        normal_button.setFont(QFont("Helvetica", 20))
        normal_button.setStyleSheet(f"""
            background-color: orange;
            border-radius: 15px;
            border: 1px solid black;
        """)
        normal_button.clicked.connect(lambda: self.set_difficulty("Normal"))

        hard_button = QPushButton("Hard")
        hard_button.setFont(QFont("Helvetica", 20))
        hard_button.setStyleSheet(f"""
            background-color: red;
            border-radius: 15px;
            border: 1px solid black;
        """)
        hard_button.clicked.connect(lambda: self.set_difficulty("Hard"))

        layout.addWidget(title_label)
        layout.addWidget(easy_button)
        layout.addWidget(normal_button)
        layout.addWidget(hard_button)
        layout.addStretch()

        self.setLayout(layout)

    def set_difficulty(self, diff):
        global BOT_DIFFICULTY
        BOT_DIFFICULTY = diff
        self.accept()
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_menu = MainMenu()
    main_menu.exec()

    sys.exit(app.exec())