import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication
import string


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('filedialog.ui', self)
        
        self.buttons = [self.trns, self.cphr, self.chw, self.keys, self.rev,
                        self.stata]
        self.fin, self.out = '', ''
        self.end.hide()
        
        self.btn.clicked.connect(self.getFiles)
        self.trns.clicked.connect(self.transliteration)
        self.cphr.clicked.connect(self.cipher)
        self.chw.clicked.connect(self.change_word)
        self.keys.clicked.connect(self.qwerty)
        self.rev.clicked.connect(self.rtext)
        self.stata.clicked.connect(self.statistics)
        
    def getFiles(self):
        i, okBtnPressed = QInputDialog.getText(
            self, "Файлы", "Введите имена файлов ввода\nи вывода через пробел")
        if okBtnPressed:
            try:
                assert len(i.split()) == 2
                self.fin = open(i.split()[0].strip(), 'r')
                self.fout = open(i.split()[1].strip(), 'w')
                for button in self.buttons:
                    button.setEnabled(True)
                self.end.hide()
            except AssertionError as a:
                msg = QMessageBox.critical(self, "Предупреждение",
                                           "Введите два файла!",
                                           QMessageBox.Close)
            except FileNotFoundError as f:
                msg = QMessageBox.critical(self, "Предупреждение",
                                           "Не найден файл ввода!  ",
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
        for button in self.buttons:
            button.setEnabled(False)  
            
    def cipher(self):
        shift, okBtnPressed = QInputDialog.getInt(
            self, "Смещение", "Выберите сдвиг", 0, -25, 25, 1)
        if okBtnPressed:        
            msg = self.fin.read()
            message = ''
            for i in range(len(msg)):
                if 1072 <= ord(msg[i].lower()) <= 1103:
                    if msg[i] == msg[i].lower():
                        message += chr((ord(msg[i]) - 1072 + shift) % 33 +
                                       1072)
                    else:
                        message += chr((ord(msg[i].lower()) - 1072 + shift) %
                                       33 + 1072).upper()
                elif 97 <= ord(msg[i].lower()) <= 122:
                    if msg[i] == msg[i].lower():
                        message += chr((ord(msg[i]) - 97 + shift) % 26 + 97)
                    else:
                        message += chr((ord(msg[i].lower()) - 97 + shift) %
                                       26 + 97).upper()            
                else:
                    message += msg[i]
            self.fout.write(message)
            self.fout.close()
            self.end.show()
            for button in self.buttons:
                button.setEnabled(False)
    
    def change_word(self):
        try:
            i, okBtnPressed = QInputDialog.getText(
                self, "Cлова",
                "Введите два слова через пробел:\nкоторое хотите \
заменить и на которое хотите заменить") 
            if okBtnPressed:
                assert len(i.split()) == 2
                word1 = i.split()[0]
                word2 = i.split()[1]
                text = self.fin.read().split()
                n_text = []
                sample = ''
                for word in text:
                    sample = word
                    if word.lower().strip(string.punctuation) == word1:
                        sample = word2
                        if (word[0] == word[0].upper() or
                            word[0] in string.punctuation):
                            sample = sample[0].upper() + sample[1::]
                        if word[-1] in string.punctuation:
                            sample = sample + word[-1]
                    n_text.append(sample)
            self.fout.write(' '.join(n_text))
            self.fout.close()
            self.end.show()
            for button in self.buttons:
                button.setEnabled(False)              
        except AssertionError as a:
            msg = QMessageBox.critical(self, "Предупреждение",
                                       "Введите два слова!",
                                       QMessageBox.Close)
            
    def qwerty(self):
        ru_en = {'а': 'f', 'б': ',', 'в': 'd', 'г': 'u', 'д': 'l', 'е': 't',
                    'ё': '`', 'ж': ';', 'з': 'p', 'и': 'b', 'й': 'q',
                    'к': 'r', 'л': 'k', 'м': 'v', 'н': 'y', 'о': 'j', 'п': 'g',
                    'р': 'h', 'с': 'c', 'т': 'n', 'у': 'e', 'ф': 'a',
                    'х': '[', 'ц': 'w', 'ч': 'x', 'ш': 'i', 'щ': 'o',
                    'ы': 's', 'э': '\'', 'ю': '.', 'я': 'z', 'ь': 'm',
                    'ъ': ']', 'Э': '"', 'Ж': ':', 'Ъ': '}', 'Х': '{', 'Б': '<',
                    'Ю': '>', '.': '/', ',': '?'}
        en_ru = dict([(v, k) for k, v in ru_en.items()])
        print(en_ru)
        i, okBtnPressed = QInputDialog.getItem(
            self, "Раскладка", "Из какой раскладки вы хотите перевод?",
            ('русская', 'английская'), 1, False) 
        if okBtnPressed:
            text = self.fin.read()
            n_text = ''
            if i == 'русская':
                for letter in text:
                    if letter in ru_en:
                        n_text += ru_en[letter]
                    elif letter.lower() in ru_en:
                        n_text += ru_en[letter.lower()].upper()
                    else:
                        n_text += letter
            else:
                for letter in text:
                    if letter in en_ru:
                        n_text += en_ru[letter]
                    elif letter.lower() in en_ru:
                        n_text += en_ru[letter.lower()].upper()
                    else:
                        n_text += letter
            self.fout.write(n_text)
            self.fout.close()
            self.end.show()
            for button in self.buttons:
                button.setEnabled(False) 
    
    def rtext(self):
        text = self.fin.read()
        n_text = []
        for word in text.split()[::-1]:
            if word[0] == word[0].upper():
                n_text.append(word[-1].upper() + word[-2::-1])
            else:
                n_text.append(word[::-1])
        self.fout.write(' '.join(n_text))
        self.fout.close()
        self.end.show()
        for button in self.buttons:
            button.setEnabled(False)
            
    def statistics(self):
        text = self.fin.read().split()
        words = dict()
        letters = dict()
        for word in text:
            word = word.lower().strip(string.punctuation)
            words[word] = words.get(word, 0) + 1
            for letter in word:
                letters[letter] = letters.get(letter, 0) + 1
        words = sorted([(v, k) for k, v in words.items()],
                       key=lambda x: (-x[0], x[1]))
        letters = sorted([(v, k) for k, v in letters.items()],
                         key=lambda x: (-x[0], x[1]))
        if len(words) < 10:
            n_w = len(words) + 1
        else:
            n_w = 11
        if len(letters) < 10:
            n_l = len(letters) + 1
        else:
            n_l = 11
        self.fout.write('{} самых использованных слов:\n'.format(n_w - 1))
        for i in range(1, n_w):
            self.fout.write('{}. {} - {} раз\n'.format(i, words[i-1][1],
                                                          words[i-1][0]))
        self.fout.write('{} самых использованных символов:\n'.format(n_l - 1))
        for i in range(1, n_l):
            self.fout.write('{}. {} - {} раз\n'.format(i, letters[i-1][1],
                                                          letters[i-1][0]))
        self.fout.close()
        self.end.show()
        for button in self.buttons:
            button.setEnabled(False)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
