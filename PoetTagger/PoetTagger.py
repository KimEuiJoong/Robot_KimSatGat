import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic

PTagger_form = uic.loadUiType("PoetTagger.ui")[0]
tags = []

class PTaggerWindow(QMainWindow,PTagger_form):
    tags = []
    tag_flags = {}
    tag_cbs = {} 
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
                self.tag_flags[tag] = False
                self.tag_cbs[tag] = QCheckBox(tag,self)
        except Exception as e:
            print(e)
            pass
        #initialize ui
        self.setupUi(self)
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
        for tag in self.tags:
            self.tag_cbs[tag].clicked.connect(self.checkTag)


    def openCSV(self):
        path = QFileDialog.getOpenFileName(self,"파일 찾기","./")
        if path[0] == "":
            return
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

        self.textEdit.setText(poet_text)
        self.tagsEdit.setText(poet_tags_txt)
        chkd_tags = poet_tags_txt.split('#')
        for tag in self.tags:
            self.tag_flags[tag] = False
        for tag in chkd_tags:
            if tag != '':
                self.tag_flags[tag] = True
        for tag in self.tags:
            if self.tag_flags[tag] == True:
                if self.tag_cbs[tag].isChecked() == False:
                    self.tag_cbs[tag].setChecked(True)
            else:
                if self.tag_cbs[tag].isChecked() == True:
                    self.tag_cbs[tag].setChecked(False)

    def checkTag(self):
        chkd_tags = []
        for tag in self.tags:
            if self.tag_cbs[tag].isChecked():
                self.tag_flags[tag] = True
                chkd_tags.append(tag)
            else:
                self.tag_flags[tag] = False
        tags_text = '#'.join(chkd_tags) 
        self.tagsEdit.setText(tags_text)
        index = self.comboBox.currentIndex()
        self.poet_df.iat[index,4] = tags_text
    def saveCSV(self):
        if self.file_name == "":
            path = QFileDialog.getSaveFileName(self,"파일 저장","./")[0]
            if path == "":
                return
            else:
                self.file_name = path
            self.poet_df.to_csv(self.file_name,index=False)
        else:
            self.poet_df.to_csv(self.file_name,index=False)
        self.setWindowTitle("PoetTagger - " + self.file_name)
    def saveAsCSV(self):
        path = QFileDialog.getSaveFileName(self,"파일 저장","./")[0]
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

#main 실행부
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ptaggerWindow = PTaggerWindow()
    ptaggerWindow.show()
    app.exec_()