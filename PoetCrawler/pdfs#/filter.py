#pdf 파일의 내용을 읽고, 한글 비율에 따라 분류하는 코드. 

import os
import shutil
import re
import pdfminer
import pdfminer.high_level

def isKor(c):
    #이 문자가 한글인가?
    code = ord(c)
    #한글의 유니코드 범위
    if code >= 0xAC00 and code <= 0xD7AF:
        return True
    else:
        return False


def perKorPoet(file_name):
    text = pdfminer.high_level.extract_text(file_name)
    #정규 표현식을 이용해 text에서 특수문자, 줄바꿈 문자, 폼피드를 제거.
    text = re.sub(pattern='[^\w]',repl='',string=text)
    text = re.sub(pattern='[\n\f]',repl='',string=text)
    kor_n = 0
    non_kor_n = 0
    for char in text:
        if isKor(char):
            kor_n += 1
        else:
            non_kor_n += 1
    n = kor_n + non_kor_n
    if n!=0:
        p = kor_n/n
    else:
        p=0
    #텍스트에서 한글의 비율을 반환
    return p


filelist = os.listdir('.')
for path in filelist:
    _,extension = os.path.splitext(path)
    if extension == '.pdf':
        p = perKorPoet(path) *100
        if p>=0 and p<10:
            shutil.move(path,'./0~10/'+ path)
        elif p>=10 and p<20:
            shutil.move(path,'./10~20/'+ path)
        elif p>=20 and p<30:
            shutil.move(path,'./20~30/'+ path)
        elif p>=30 and p<40:
            shutil.move(path,'./30~40/'+ path)
        elif p>=40 and p<50:
            shutil.move(path,'./40~50/'+ path)
        elif p == 50:
            #한자 시의 경우 한글과 한자의 비율이 반반인 경우가 많기에 따로 분류.
            shutil.move(path,'./50/'+ path)
        else:
            shutil.move(path,'./ex50/'+ path)
