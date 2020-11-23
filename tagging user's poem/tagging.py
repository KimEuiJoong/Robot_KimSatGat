# -*-coding: utf-8-*-
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from ckonlpy.tag import Twitter
from ckonlpy.tag import Postprocessor
from ckonlpy.utils import load_wordset
from tensorflow.keras.models import load_model
import pickle

#input : poem-시 본문(string), model-모델 경로(string)
#output : tags-태그 3개(list)
def tagging(poem, model):
    with open('tokenizerS3', 'rb') as fr: #model 학습에 사용한 Tokenizer
        tokenizer = pickle.load(fr)

    Xi = tokenizer.texts_to_sequences(poem) #interger encoding
    X = []
    for word in Xi:
        for w in word:
            X.append(word)
    X = [X]
    X = pad_sequences(X, maxlen = 200, padding='post')[0] #padding
    X = X.reshape(1, 200)

    model = load_model(model)

    y = model.predict(X, batch_size = 1)

    mainTags = ['기쁨','즐거움','사랑1','사랑2','희망','활기','순수','잔잔','슬픔','의지','그리움1','그리움2','무심','고독','불안','성찰']

    tagIndexs = []
    y_copy = y[0].copy()
    for i in range(3):
        tagIndexs.append(y_copy.argmax())
        y_copy[y_copy.argmax()] = 0

    tags = [mainTags[i] for i in tagIndexs]

    return tags

'''test
poem = '5월 아침\n비 개인 5월 아침\n혼란스런 꾀꼬리 소리\n찬엄한 햇살 퍼져 오릅내다\n이슬비 새벽을 적시울 즈음\n두견의 가슴 찢는 소리 피어린 흐느낌\n한 그릇 옛날 향훈이 어찌\n이 맘 홍근 안 젖었으리오마는\n이 아침 새 빛에 하늘대는 어린 속잎들\n저리 부드러웁고\n발목은 포실거리어\n꾀꼬리는 다시 창공을 흔드오\n자랑찬 새 하늘을 사치스레 만드오\n사향 냄새도 잊어버렸대서야\n불혹이 자랑이 아니 되오\n아침 꾀꼬리에 안 불리는 혼이야\n새벽 두견이 못 잡는 마음이야\n한낮이 정밀하단들 또 무얼하오\n저 꾀꼬리 무던히 소년인가 보오\n새벽 두견이야 오랜 중년이고\n내사 불혹을 자랑턴 사람.\n접힌 마음 구긴 생각 이제 다 어루만져졌나보오\n'
model = 'model_v0.4.h5'

tags = tagging(poem, model)

print(tags)
'''
