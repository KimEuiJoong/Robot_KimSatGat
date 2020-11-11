import random
import pickle

#사용자 상태(feeling) 받아오기
feeling = '사랑'

#상태-태그 불러오기
import pandas as pd

fts = pd.read_csv('./feeling_tag_score.csv', names=['feeling', 'tag', 'score'])

#점수에 기반한 랜덤 방식으로 태그 고르기
tags = fts['tag'][fts['feeling']==feeling].tolist()
scores = fts['score'][fts['feeling']==feeling].tolist()
score_sum = 0
for score in scores:
    score_sum += score

randomTag = random.choices(tags, weights=scores)[0]

#시 데이터 불러오기
with open('./poems_tagging', 'rb') as fr:
    poems = pickle.load(fr)

#태그에 해당하는 시 인덱스 목록 생성
randomPoems_intLocation = []
pi = 0 #루프 내에서 시 인덱스를 가리키는 인덱스(dataframe.iloc)

for tagList in poems['tag']:
    if any(randomTag in tag for tag in tagList):
        randomPoems_intLocation.append(pi)
    pi += 1

#시 목록에서 랜덤으로 시 추출
poemIntLocation = random.choices(randomPoems_intLocation)[0]
randomPoem = poems.iloc[poemIntLocation]

print("feeling: " + feeling)
print("randomTag: " + randomTag)
print("randomPoemTag: " + ''.join(randomPoem['tag']))
print("randomPoemName: " + randomPoem['name'])
print("randomPoemWriter: " + randomPoem['writer'])
print("randomPoemText: " + randomPoem['text'])
