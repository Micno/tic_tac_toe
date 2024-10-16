import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout,
    QMessageBox, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie, QIcon



class AnimatedButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.movie = None

    def set_movie(self, movie):
        if self.movie:
            self.movie.stop()
        self.movie = movie
        if self.movie:
            self.movie.setScaledSize(self.size())
            self.movie.frameChanged.connect(self.update_icon_from_movie)
            self.movie.finished.connect(self.on_movie_finished)
            self.movie.start()

    def update_icon_from_movie(self):
        self.setIcon(QIcon(self.movie.currentPixmap()))
        self.setIconSize(self.size())

    def on_movie_finished(self):
        self.setIcon(QIcon(self.movie.currentPixmap()))
        self.setIconSize(self.size())
        self.movie.stop()


class AnimatedLabel(QLabel):
    def __init__(self, movie, size=QSize(30, 30), parent=None):
        super().__init__(parent)
        self.setMovie(movie)
        self.movie().setScaledSize(size)
        self.setFixedSize(size)
        self.movie().start()


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.x_movie = QMovie(r"C:\Users\Arthur\OneDrive\Projekte\tic_tac_toe\XinTTT.gif")
        self.o_movie = QMovie(r"C:\Users\Arthur\OneDrive\Projekte\tic_tac_toe\OinTTT.gif")
        self.init_ui()
        self.player = 'X'
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.win_count = {'X': 0, 'O': 0}
        
        self.update_player_label()
        self.update_win_counter()

    def init_ui(self):
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(300, 300, 350, 500)

        main_layout = QGridLayout()

        self.win_counter_x = QLabel()
        self.win_counter_o = QLabel()
        self.win_preview_x = AnimatedLabel(self.x_movie)
        self.win_preview_o = AnimatedLabel(self.o_movie)
        win_counter_layout = QHBoxLayout()
        win_counter_layout.addWidget(self.win_preview_x)
        win_counter_layout.addWidget(self.win_counter_x)
        win_counter_layout.addWidget(self.win_preview_o)
        win_counter_layout.addWidget(self.win_counter_o)
        main_layout.addLayout(win_counter_layout,0, 0, 1, 3)

        game_layout = QGridLayout()

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = AnimatedButton()
                button.setFixedSize(100, 100)
                button.clicked.connect(self.make_move)
                game_layout.addWidget(button, i, j)
                self.buttons.append(button)
        
        main_layout.addLayout(game_layout, 1, 0, 1, 3)
        
        self.player_preview = AnimatedLabel(self.x_movie)
        self.player_label = QLabel("ist an der Reihe")
        player_layout = QHBoxLayout()
        player_layout.addWidget(self.player_preview)
        player_layout.addWidget(self.player_label)
        main_layout.addLayout(player_layout, 2, 0, 1, 3)

        self.setLayout(main_layout)

    def update_player_label(self):
        current_movie = self.x_movie if self.player == 'X' else self.o_movie
        self.player_preview.setMovie(current_movie)

    def update_win_counter(self):
        self.win_counter_x.setText(f": {self.win_count['X']}")
        self.win_counter_o.setText(f": {self.win_count['O']}")

    def make_move(self):
        button = self.sender()
        row, col = divmod(self.buttons.index(button), 3)
        
        if self.board[row][col] is None and not self.check_winner():
            current_movie = QMovie(
                self.x_movie.fileName() if self.player == 'X' else self.o_movie.fileName()
            )
            button.set_movie(current_movie)
            self.board[row][col] = self.player
            
            if self.check_winner():
                self.win_count[self.player] += 1
                QMessageBox.information(
                    self, 'Gewinner', f'Spieler {self.player} hat gewonnen!'
                )
                self.update_win_counter()
                self.reset_game()
            elif all(self.board[i][j] is not None for i in range(3) for j in range(3)):
                QMessageBox.information(
                    self, 'Unentschieden', 'Das Spiel endet unentschieden!'
                )
                self.reset_game()
            else:
                self.player = 'O' if self.player == 'X' else 'X'
                self.update_player_label()

    def check_winner(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] is not None or
                self.board[0][i] == self.board[1][i] == self.board[2][i] is not None):
                return True
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] is not None or
            self.board[0][2] == self.board[1][1] == self.board[2][0] is not None):
            return True
        return False

    def reset_game(self):
        self.player = 'X'
        self.board = [[None for _ in range(3)] for _ in range(3)]
        for button in self.buttons:
            button.set_movie(None)
            button.setIcon(QIcon())
        self.update_player_label()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec())