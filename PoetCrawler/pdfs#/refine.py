#형태소 분류기에 넣기 전, 문서에 포함된 특수문자나 줄바꿈 문자를 지워 텍스트를 정제하는 코드.


import os
import re
import pandas as pd

poets = pd.read_csv("poets.csv",names=['name','writer','text','cc'])

texts = poets['text']
rtexts = []

for text in texts:
    #줄바꿈 문자의 경우 스페이스로 바꾼다. 
    rtext = re.sub("\n","\u0020",text)
    #글에 일반적으로 사용되는 느낌표, 따옴표, 마침표, 쉼표 등을 제외한 다른 잡스러운 특수문자를 지움.
    rtext = re.sub("[^\uac00-\ud7af\u0020\u0030-\u0039\u0021\u0022\u0027\u002c\u002e]","",rtext)
    #스페이스 문자가 여러번 반복되어 있는 경우 스페이스 문자 하나로 바꾼다.('            '같이 쓸데없이 반복된 경우 ' '로 바꾼다는 뜻.) 
    rtext = re.sub("\u0020\u0020+","\u0020",rtext)

    rtexts.append(rtext)

rtext_series = pd.Series(rtexts)
rtext_series.to_csv("./refined.csv",index=False)
