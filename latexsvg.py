#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class ScriptBox(QtGui.QPlainTextEdit):

    reDraw = pyqtSignal()
    
    def __init__(self, parent):
        
        super(ScriptBox,self).__init__(parent)
        self.move(20,20)
        self.resize(580,200)
        self.multilines = 1
        
    @pyqtSlot()
    def export(self):
        mathstr = str(self.toPlainText())
        print mathstr

        if self.multilines == 0:

            prefile = open("./template/pre.tex","r");
            texstrpre = prefile.read();
            prefile.close()
    
            postfile = open("./template/post.tex","r");
            texstrpost = postfile.read();
            postfile.close()
            
        else:

            prefile = open("./template/prelong.tex","r");
            texstrpre = prefile.read();
            prefile.close()
    
            postfile = open("./template/postlong.tex","r");
            texstrpost = postfile.read();
            postfile.close()
            
        
        texstr = texstrpre + mathstr + texstrpost

        texfile = open("standalone.tex","w")
        texfile.write(texstr)
        texfile.close()
        
        cmd1 = "pdflatex " + "standalone.tex"        
        os.system(cmd1)
        
        cmd10 = "latex " + "standalone.tex"
        os.system(cmd10)

        if self.multilines == 1:

            cmd11 = "pdfcrop standalone.pdf standalone.pdf"
            os.system(cmd11)
        
        cmd2 = "convert -density 800 standalone.pdf standalone.png"
        os.system(cmd2)

  #      cmd3 = "pdf2svg standalone.pdf standalone.svg"
        cmd3 = "dvisvgm --no-fonts standalone.dvi"
        os.system(cmd3)
        print 'emit'
        self.reDraw.emit()
        
class CompileButton(QtGui.QPushButton):

    
    def __init__(self, parent):
        
        super(CompileButton,self).__init__(parent)
        self.move(180,250)
        self.resize(100,30)
        self.setText("Compile it!")
        self.clicked.connect(self.on_click)
        
    def on_click(self):

        pass


    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return

        # write the relative cursor position to mime data
        mimeData = QtCore.QMimeData()

        curdir = os.getcwd()
        print curdir
        filedir = curdir + "/standalone.svg"
        mimeData.setUrls([QUrl.fromLocalFile(filedir)])
        mimeData.setData("text/plain",filedir)

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = QtGui.QPixmap.grabWidget(self)

        # below makes the pixmap half transparent
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()

        # make a QDrag
        drag = QtGui.QDrag(self)
        # put our MimeData
        drag.setMimeData(mimeData)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())

        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) 


    def mousePressEvent(self, e):
        QtGui.QPushButton.mousePressEvent(self, e)
  
class DragButton(QtGui.QPushButton):

    
    def __init__(self, parent):
        
        super(DragButton,self).__init__(parent)
        self.move(320,250)
        self.resize(100,30)
        self.setText("Drag me!")
        self.clicked.connect(self.on_click)
        
    def on_click(self):

        pass

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return

        # write the relative cursor position to mime data
        mimeData = QtCore.QMimeData()

        curdir = os.getcwd()
        filedir = curdir + "/standalone.svg"
        mimeData.setUrls([QUrl.fromLocalFile(filedir)])
        mimeData.setData("text/plain",filedir)

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        pixmap = QtGui.QPixmap.grabWidget(self)

        # below makes the pixmap half transparent
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()

        # make a QDrag
        drag = QtGui.QDrag(self)
        # put our MimeData
        drag.setMimeData(mimeData)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())

        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) 

    def mousePressEvent(self, e):
        QtGui.QPushButton.mousePressEvent(self, e)
            
class Display(QtGui.QWidget):

    def __init__(self,parent):
        
        super(Display, self).__init__(parent)
        self.initUI()
        self.initStatus = 0;
        os.system("rm standalone.png")

    def initUI(self):
 
        self.setGeometry(20,300,580,250)      
        
    def paintEvent(self,e):

        p = QPainter(self)
        
        p.begin(self)

        p.fillRect(1,1,578,250, Qt.white)

        if self.initStatus != 0:
            
            img1 = QPixmap("standalone.png")

            width = img1.size().width()
            height = img1.size().height()
            print width

            if (width < 570) &(height < 200):

                img2 = img1
                
            else:                 
                img2 = img1.scaled(500,200,Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            p.drawPixmap(10,20,img2)
            
        else:
            self.initStatus = 1

        p.end()
        

#        os.system("rm standalone.png")
        
    @pyqtSlot()
    def reDraw(self):
        print 'reDraw'
        self.update()

def main():
    app = QtGui.QApplication(sys.argv)
    
    w = QMainWindow()
    w.resize(620,600)
    w.setWindowTitle("Latex svg!")

    textbox = ScriptBox(w)
    compbtn = CompileButton(w)
    dragbtn = DragButton(w)
    dispbox = Display(w)

    w.connect(compbtn, SIGNAL("clicked()"), textbox, SLOT("export()"))
    w.connect(textbox, SIGNAL("reDraw()"), dispbox, SLOT("reDraw()"))
       
    # Show window
    w.show()

    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
