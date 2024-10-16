import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PySide6.QtCore import Qt

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.player = 'X'
        self.board = [[''] * 3 for _ in range(3)]

    def init_ui(self):
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(300, 300, 300, 300)

        grid = QGridLayout()
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = QPushButton('')
                button.setFixedSize(80, 80)
                button.clicked.connect(self.make_move)
                grid.addWidget(button, i, j)
                self.buttons.append(button)
        
        self.setLayout(grid)

    def make_move(self):
        button = self.sender()
        row, col = divmod(self.buttons.index(button), 3)
        
        if self.board[row][col] == '' and not self.check_winner():
            button.setText(self.player)
            self.board[row][col] = self.player
            
            if self.check_winner():
                QMessageBox.information(self, 'Gewinner', f'Spieler {self.player} hat gewonnen!')
                self.reset_game()
            elif all(self.board[i][j] != '' for i in range(3) for j in range(3)):
                QMessageBox.information(self, 'Unentschieden', 'Das Spiel endet unentschieden!')
                self.reset_game()
            else:
                self.player = 'O' if self.player == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def reset_game(self):
        self.player = 'X'
        self.board = [[''] * 3 for _ in range(3)]
        for button in self.buttons:
            button.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec())