import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('filedialog.ui',self)
        
        self.buttons = [self.trns]
        self.fin, self.out = '', ''
        self.end.hide()
        
        self.btn.clicked.connect(self.getFiles)
        self.trns.clicked.connect(self.transliteration)
        
    def getFiles(self):
        i, okBtnPressed = QInputDialog.getText(
            self, "Файлы", "Введите имена файлов ввода\nи вывода через пробел"
        )
        if okBtnPressed:
            try:
                assert len(i.split()) == 2
                self.fin = open(i.split()[0].strip(), 'r')
                self.fout = open(i.split()[1].strip(), 'w')
                for button in self.buttons:
                    button.setEnabled(True)
            except AssertionError as a:
                msg = QMessageBox.critical(self, "Предупреждение",
                                           "Проверьте, что вы ввели два файла!",
                                           QMessageBox.Close)
            except FileNotFoundError as f:
                msg = QMessageBox.critical(self, "Предупреждение",
                                           "Не найден такой файл!  ",
                                           QMessageBox.Close)
            
                
            
    def transliteration(self):
        alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
                    'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i',
                    'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
                    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
                    'х': 'kh', 'ц': 'tc', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                    'ы': 'y', 'э': 'e', 'ю': 'iu', 'я': 'ia', 'ь': '', 'ъ': ''}    
        word = ''
        for letter in self.fin.read():
            if letter.lower() in alphabet:
                if letter in 'ЖХЦЧШЩЮЯ':
                    word += alphabet[letter.lower()][0].upper() +\
                        alphabet[letter.lower()][1:]
                elif letter == letter.upper():
                    word += alphabet[letter.lower()].upper()
                else:
                    word += alphabet[letter]
            else:
                word += letter 
        self.fout.write(word)
        self.fout.close()
        self.end.show()
        

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())