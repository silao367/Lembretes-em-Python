from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class Browser():

    def __init__(self):
          
          self.window = QWidget()
          self.window.setWindowTitle('Navegador Browser.py')
          self.window.maximumSize()

          self.layout = QVBoxLayout()
          self.horizontal = QHBoxLayout()

          self.url_bar = QTextEdit()
          self.url_bar.setMaximumHeight(30)

          self.go_bnt = QPushButton('GO')
          self.go_bnt.setMinimumHeight(30)

          self.back_bnt = QPushButton('<')
          self.back_bnt.setMinimumHeight(30)

          self.forward_btn = QPushButton('>')
          self.forward_btn.setMinimumHeight(30)

          self.horizontal.addWidget(self.url_bar)
          self.horizontal.addWidget(self.go_bnt)
          self.horizontal.addWidget(self.back_bnt)
          self.horizontal.addWidget(self.forward_btn)

          self.browser = QWebEngineView()

          #Botao click
          self.go_bnt.clicked.connect(lambda: self.navigation(self.url_bar.toPlainText()))

          #Botao back
          self.back_bnt.clicked.connect(self.browser.back)

          #Botao forward
          self.forward_btn.clicked.connect(self.browser.forward)


          self.layout.addLayout(self.horizontal)
          self.layout.addWidget(self.browser)

          #Url padrao para navegador
          self.browser.setUrl(QUrl('http://google.com'))

          #Mostrando layout
          self.window.setLayout(self.layout)
          self.window.show()

#Funcao para adicionar http no comeco da URL
def navigation(self, url):
     if not url.startswith('http'):
          url = 'http://'+url
          self.url_bar.setText(url)
          self.browser.setUrl(QUrl(url))

app = QApplication([])
window = Browser()
app.exec_()                 