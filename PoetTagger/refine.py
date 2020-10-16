#형태소 분류기에 넣기 전, 문서에 포함된 특수문자나 줄바꿈 문자를 지워 텍스트를 정제하는 코드.


import os
import re
import pandas as pd

poets = pd.read_csv("poets.csv",index_col = False)

texts = poets['text']
rtexts = []

for text in texts:
    #글에 일반적으로 사용되는 느낌표, 따옴표, 마침표, 쉼표 등을 제외한 다른 잡스러운 특수문자와 한자를 지움.
    rtext = re.sub("[^\uac00-\ud7af\u0020\u0030-\u0039\u0021\u0022\u0027\u002c\u002e\n]","",text)
    #줄바꿈 문자가 여러번 반복된 경우 하나로 바꿈.
    rtext = re.sub("\n\n+","\n",rtext)
    #스페이스 문자가 여러번 반복되어 있는 경우 스페이스 문자 하나로 바꾼다.
    rtext = re.sub("\u0020\u0020+","\u0020",rtext)
    #줄바꿈 스페이스을 줄바꿈으로.
    rtext = re.sub("\n\u0020","\n",rtext)
    #다시 줄바꿈 반복 제거.
    rtext = re.sub("\n\n+","\n",rtext)
    #태깅하는 사람 보기 편하게 줄을 좀 띄워서 준다.
    rtext = re.sub("\n","\n\n",rtext)

    rtexts.append(rtext)

rtext_series = pd.Series(rtexts)
poets = poets.assign(text = rtext_series)
poets.to_csv("./refined.csv",index=False)
