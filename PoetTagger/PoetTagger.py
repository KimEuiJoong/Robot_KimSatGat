import sys
import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5 import uic

PTagger_form = uic.loadUiType("PoetTagger.ui")[0]
tags = []

class PTaggerWindow(QMainWindow,PTagger_form):
    tags = []
    tag_cbs = {} 
    tagsEdit = None
    poet_df = None
    file_name = ""
    def __init__(self):
        super().__init__()
        #read tags
        try:
            with open("tags.txt","r",encoding="utf-8") as f:
                for l in f.readlines():
                    rl = l.replace("\n","")
                    self.tags.append(rl)
            for tag in self.tags:
                self.tag_cbs[tag] = QCheckBox(tag,self)
        except Exception as e:
            print(e)
        #initialize ui
        self.setupUi(self)
        self.tagsEdit = foutEdit(self)    
        self.tagsEdit.move(520,80)
        self.tagsEdit.resize(391,121)
        for i in range(0,len(self.tags)):
            self.gridLayout.addWidget(self.tag_cbs[self.tags[i]],i//4,i%4)
        self.actionOpen.triggered.connect(self.openCSV)
        self.actionSave.triggered.connect(self.saveCSV)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSaveAs.triggered.connect(self.saveAsCSV)
        self.actionSaveAs.setShortcut("Ctrl+A")
        self.comboBox.currentIndexChanged.connect(self.choosePoet)
        self.saveButton.clicked.connect(self.saveCSV)
        self.nextButton.clicked.connect(self.nextPoet)
        self.nextButton.setShortcut("right")
        self.prevButton.clicked.connect(self.prevPoet)
        self.prevButton.setShortcut("left")
        #self.tagsEdit.textChanged.connect(self.tagsWrite)
        self.tagsEdit.foutEvent.connect(self.tagsWrite)
        self.textEdit.textChanged.connect(self.textWrite)
        self.deltagButton.clicked.connect(self.tagsDelete)
        self.savetagButton.clicked.connect(self.saveTagFile)
        for tag in self.tags:
            self.tag_cbs[tag].clicked.connect(self.checkTag)
        self.disableUi()
    def saveTagFile(self):
        
        try:
            with open("tags.txt","w",encoding="utf-8") as f:
                for tag in self.tags:
                    f.write(tag+"\n")
        except Exception as e:
            print(e)

    def disableUi(self):
        self.textEdit.setEnabled(False)
        self.tagsEdit.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.prevButton.setEnabled(False)
        self.deltagButton.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.savetagButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        for tag in self.tags:
            self.tag_cbs[tag].setEnabled(False)

    def enableUi(self):
        self.textEdit.setEnabled(True)
        self.tagsEdit.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.prevButton.setEnabled(True)
        self.deltagButton.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.savetagButton.setEnabled(True)
        self.saveButton.setEnabled(True)
        for tag in self.tags:
            self.tag_cbs[tag].setEnabled(True)

    def textWrite(self):
        poet_text = self.textEdit.toPlainText()
        poet_index = self.comboBox.currentIndex()
        self.poet_df.iat[poet_index,2] = poet_text
        

    def openCSV(self):
        path = QFileDialog.getOpenFileName(self,"파일 찾기","./","csv format (*.csv)")
        if path[0] == "":
            return
        self.enableUi()
        self.poet_df = None
        self.poet_df = pd.read_csv(path[0],index_col = False)
        if len(self.poet_df.columns) <= 4:
            self.poet_df[4] = "#" 
            self.file_name = ""
        else:
            self.file_name = path[0]
        self.setWindowTitle("PoetTagger - " + self.file_name)
        self.poet_df.columns = ['name','writer','text','cc','tags']
        self.comboBox.clear()
        for name in self.poet_df['name']:
            self.comboBox.addItem(name)

    def choosePoet(self): 
 
        poet_index = self.comboBox.currentIndex()
        poet = self.poet_df.iloc[poet_index]
        poet_text = poet['text']
        poet_tags_txt = poet['tags']
        if poet_tags_txt == '#' or pd.isna(poet_tags_txt):
            poet_tags_txt = ''
        self.textEdit.setText(poet_text)
        self.tagsEdit.setText(poet_tags_txt)
        chkd_tags = poet_tags_txt.split('#')

        for tag in self.tags:
            self.tag_cbs[tag].setChecked(False)

        for tag in chkd_tags:
            if tag not in self.tags and tag != '':
                self.tags.append(tag)
                self.tag_cbs[tag] = QCheckBox(tag,self)
                self.tag_cbs[tag].clicked.connect(self.checkTag)
                tag_cbs_n = len(self.tag_cbs)-1
                self.gridLayout.addWidget(self.tag_cbs[tag],tag_cbs_n//4,tag_cbs_n%4)
                self.tag_cbs[tag].setChecked(True)
            if tag != '':
                self.tag_cbs[tag].setChecked(True)

    def checkTag(self):

        chkd_tags = []
        for tag in self.tags:
            if self.tag_cbs[tag].isChecked():
                chkd_tags.append(tag)
        
        tags_text = '#'.join(chkd_tags) 
        self.tagsEdit.setText(tags_text)
        index = self.comboBox.currentIndex()
        self.poet_df.iat[index,4] = tags_text

    def saveCSV(self):
        if self.file_name == "":
            path = QFileDialog.getSaveFileName(self,"파일 저장","./","csv format (*.csv)")[0]
            if path == "":
                return
            else:
                self.file_name = path
            self.poet_df.to_csv(self.file_name,index=False)
        else:
            self.poet_df.to_csv(self.file_name,index=False)
        self.setWindowTitle("PoetTagger - " + self.file_name)
    def saveAsCSV(self):
        path = QFileDialog.getSaveFileName(self,"파일 저장","./","csv format (*.csv)")[0]
        if path == "":
            return
        else:
            self.file_name = path
        self.poet_df.to_csv(self.file_name,index=False)
        self.setWindowTitle("PoetTagger - " + self.file_name)
    def nextPoet(self):
        poet_index = self.comboBox.currentIndex()
        if poet_index != len(self.poet_df['name']):
            self.comboBox.setCurrentIndex(poet_index+1)
    def prevPoet(self):
        poet_index = self.comboBox.currentIndex()
        if poet_index != 0:
            self.comboBox.setCurrentIndex(poet_index-1)

    def tagsWrite(self):

        poet_index = self.comboBox.currentIndex()
        tags_text = self.tagsEdit.toPlainText()
        chkd_tags = tags_text.split('#')

        #init checkboxes
        for tag in self.tags:
            self.tag_cbs[tag].setChecked(False)

        #getting non repeated tag text
        n_rep_chkd = []
        for tag in chkd_tags:
            if tag not in n_rep_chkd:
                n_rep_chkd.append(tag)
        tags_text = '#'.join(n_rep_chkd)

        for tag in n_rep_chkd:
            #if it is not in taglist, add tag & checkbox to the list
            if tag not in self.tags and tag != '':
                self.tags.append(tag)
                self.tag_cbs[tag] = QCheckBox(tag,self)
                self.tag_cbs[tag].clicked.connect(self.checkTag)
                tag_cbs_n = len(self.tag_cbs)-1
                self.gridLayout.addWidget(self.tag_cbs[tag],tag_cbs_n//4,tag_cbs_n%4)
            if tag != '':
                self.tag_cbs[tag].setChecked(True)

        self.poet_df.iat[poet_index,4] = tags_text
        self.tagsEdit.setText(tags_text)

    def tagsDelete(self):

        del_text = self.delEdit.text()
        if del_text == '':
            return
        del_tags = del_text.split('#')

        #delete tags from edit_text
        edit_text = self.tagsEdit.toPlainText() 
        if edit_text != '':
            edit_tags = edit_text.split('#')
            for tag in del_tags:
                if tag in edit_tags:
                    edit_tags.remove(tag)
            edit_text = '#'.join(edit_tags)
            self.tagsEdit.setText(edit_text)

        #delete tags from lists
        for tag in del_tags:
            if tag in self.tags:
                self.tags.remove(tag)
                del self.tag_cbs[tag]

        #make checkboxes from scratch
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().deleteLater()

        for tag in self.tags:
            self.tag_cbs[tag] = QCheckBox(tag,self)
            self.tag_cbs[tag].clicked.connect(self.checkTag)

        for i in range(0,len(self.tags)):
            self.gridLayout.addWidget(self.tag_cbs[self.tags[i]],i//4,i%4)
        
        #recheck
        for tag in edit_tags:
            self.tag_cbs[tag].setChecked(True)


class foutEdit(QTextEdit):
    foutEvent = pyqtSignal()
    def focusOutEvent(self,event):
        self.foutEvent.emit()
        super(foutEdit,self).focusOutEvent(event)



#main 실행부
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ptaggerWindow = PTaggerWindow()
    ptaggerWindow.show()
    app.exec_()