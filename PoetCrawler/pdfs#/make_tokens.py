#pandas를 이용해 정제된 csv파일을 읽고, 
#konlpy에 포함된 형태소 분류기들로 분류하는 코드.
#mecab은 윈도우에서 설치가 까다롭기에 따로 작성했음. 다른 분류기와 사용법은 동일!

from konlpy.tag import Hannanum,Kkma,Komoran
import pandas as pd

hannanum = Hannanum()
kkma = Kkma()
komoran = Komoran()

r = pd.read_csv("refined.csv",names=['rtext'])

rtexts = r['rtext']
tokens = []

for rtext in rtexts:
    token_table = {}
    token_table['Hannanum'] = hannanum.morphs(rtext)
    token_table['Kkma'] = kkma.morphs(rtext)
    token_table['Komoran'] = komoran.morphs(rtext)
    tokens.append(token_table)

tokens_df = pd.DataFrame(tokens)
tokens_df.to_csv("tokens.csv")