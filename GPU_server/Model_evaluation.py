import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

#시, 태그 불러오기(X1,X2,y1,y2)
with open('poems_token_ckonlpy', 'rb') as fr:
    poems_token = pickle.load(fr) #series-list
with open('poems_str', 'rb') as fr:
    poems_str = pickle.load(fr) #list
with open ('poems_tag_16', 'rb') as fr:
    poems_tag_16 = pickle.load(fr) #series
with open ('poems_tag_11', 'rb') as fr:
    poems_tag_11 = pickle.load(fr) #series

poems_tag_16 = poems_tag_16.drop(poems_tag_16[poems_tag_16=='불용'].index) #불용 태그 제거
poems_tag_16 = poems_tag_16.str.split('#') #태그 여러개 분리(str->list)

poems_tag_11 = poems_tag_11.drop(poems_tag_11[poems_tag_11=='불용'].index)
poems_tag_11 = poems_tag_11.str.split('#')

#태그 2개 이상 데이터 삭제
for i in range(len(poems_tag_16)):
    if len(poems_tag_16.iloc[i]) != 1:
        poems_tag_16[poems_tag_16.index[i]] = np.nan
poems_tag_16.dropna(inplace=True)
for i in range(len(poems_tag_16)): #list->str
    poems_tag_16.iloc[i] = ''.join(poems_tag_16.iloc[i])

for i in range(len(poems_tag_11)):
    if len(poems_tag_11.iloc[i]) != 1:
        poems_tag_11[poems_tag_11.index[i]] = np.nan
poems_tag_11.dropna(inplace=True)
for i in range(len(poems_tag_11)): #list->str
    poems_tag_11.iloc[i] = ''.join(poems_tag_11.iloc[i])

# 태그 한 시만 DataFrame으로 변환
poem_tag = pd.DataFrame()
poem_tag['poemToken'] = poems_token
poem_tag['poemStr'] = poems_str
poem_tag['tag16'] = poems_tag_16
poem_tag['tag11'] = poems_tag_11
poem_tag.dropna(inplace=True)

#훈련/테스트 데이터 분류(4종류) 후 X 데이터 정수 인코딩
sep_len = (int)(len(poem_tag)*8/10)

#token, str, tag16, tag11
poem_train_t = poem_tag['poemToken'].iloc[0:sep_len+1] #훈련할 시
poem_test_t = poem_tag['poemToken'].iloc[sep_len+1:len(poem_tag)+1]
tag_train_16 = poem_tag['tag16'].iloc[0:sep_len+1] #맞춰볼 태그
tag_test_16 = poem_tag['tag16'].iloc[sep_len+1:len(poem_tag)+1]
poem_train_s = poem_tag['poemStr'].iloc[0:sep_len+1]
poem_test_s = poem_tag['poemStr'].iloc[sep_len+1:len(poem_tag)+1]
tag_train_11 = poem_tag['tag11'].iloc[0:sep_len+1]
tag_test_11 = poem_tag['tag11'].iloc[sep_len+1:len(poem_tag)+1]

vocab_size_token = 4247 #미리 계산
vocab_size_str = 2013 #미리 계산

tokenizerT = Tokenizer(vocab_size_token, oov_token='OOV')
tokenizerT.fit_on_texts(poem_train_t) #Tokenizer에 단어-정수 집합 생성
X_train_int_t = tokenizerT.texts_to_sequences(poem_train_t) #정수 인코딩
X_test_int_t = tokenizerT.texts_to_sequences(poem_test_t)

tokenizerS = Tokenizer(vocab_size_str, oov_token='OOV')
tokenizerS.fit_on_texts(poem_train_s)
X_train_int_s = tokenizerS.texts_to_sequences(poem_train_s)
X_test_int_s = tokenizerS.texts_to_sequences(poem_test_s)

#X 데이터 패딩
max_len = 200 #미리 계산

X_train_t = pad_sequences(X_train_int_t, maxlen = max_len, padding='post')
X_test_t = pad_sequences(X_test_int_t, maxlen = max_len,  padding='post')

X_train_s = pad_sequences(X_train_int_s, maxlen = max_len, padding='post')
X_test_s = pad_sequences(X_test_int_s, maxlen = max_len,  padding='post')

#태그 데이터 정수 인코딩 -> 원-핫 인코딩
tags16 = ['기쁨','즐거움','사랑1','사랑2','희망','활기','순수','잔잔','슬픔','의지',
        '그리움1','그리움2','무심','고독','불안','성찰']
tags11 = ['기쁨','사랑1','순수','잔잔','슬픔','의지','그리움1','그리움2','무심','고독',
        '성찰']

#정수 인코딩
y_train_int_16 = tag_train_16.copy()
for i in range(len(y_train_int_16)):
    if tags16.index(y_train_int_16.iloc[i]) >= 0:
        y_train_int_16.iloc[i] = tags16.index(y_train_int_16.iloc[i])
y_test_int_16 = tag_test_16.copy()
for i in range(len(y_test_int_16)):
    if tags16.index(y_test_int_16.iloc[i]) >= 0:
        y_test_int_16.iloc[i] = tags16.index(y_test_int_16.iloc[i])

y_train_int_11 = tag_train_11.copy()
for i in range(len(y_train_int_11)):
    if tags11.index(y_train_int_11.iloc[i]) >= 0:
        y_train_int_11.iloc[i] = tags11.index(y_train_int_11.iloc[i])
y_test_int_11 = tag_test_11.copy()
for i in range(len(y_test_int_11)):
    if tags11.index(y_test_int_11.iloc[i]) >= 0:
        y_test_int_11.iloc[i] = tags11.index(y_test_int_11.iloc[i])

#정수->one-hot Vector
y_train_16 = to_categorical(y_train_int_16, len(tags16))
y_test_16 = to_categorical(y_test_int_16, len(tags16))

y_train_11 = to_categorical(y_train_int_11, len(tags11))
y_test_11 = to_categorical(y_test_int_11, len(tags11))


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout
from tensorflow.keras import initializers
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import TerminateOnNaN, EarlyStopping

#평가함수 정의
def predict_tag(arr, n): #레이블(확률 배열)에서 상위값 n(태그 개수)개의 인덱스 반환
    arr_temp = arr.copy()
    tag = []
    for i in range(n):
        tag.append(arr_temp.argmax())
        arr_temp[arr_temp.argmax()] = 0
    return tag

#모델 생성+학습+저장하는 함수 정의
def model_control(l, o, e, a, d, x, y):
    #l,o,e,a,d,y: 정수(각 배열의 인덱스), x: 't' / 's'(문자)

    #파라미터 정의
    momentum = SGD(lr=0.01, momentum=0.9)
    def swish(x):
        return x * tf.nn.sigmoid(x)

    layers = [5, 10] #1
    optimizers = ['adam', 'sgd', 'Adadelta', momentum] #2
    embedding_sizes = [100, 10, 200] #1
    activations = ['relu', 'softsign', swish, 'elu', 'tanh'] #3
    dropouts = [0.5, 0.2] #1
    vocab_sizes = {'t':4247, 's':2013} #2
    tag_numbers = [16, 11] #2
    #max_len = 200
    X_trains = {'t':X_train_t, 's':X_train_s}
    y_trains = [y_train_16, y_train_11]
    X_tests = {'t':X_test_t, 's':X_test_s}
    y_tests = [y_test_16, y_test_11]
    tagss = [tags16, tags11]

    #함수 입력값에 따라 파라미터 결정
    layer = layers[l]
    opt = optimizers[o]
    emb = embedding_sizes[e]
    act = activations[a]
    drop = dropouts[d]
    vocab_size = vocab_sizes[x]
    tag_num = tag_numbers[y]
    X_train = X_trains[x]
    y_train = y_trains[y]
    X_test = X_tests[x]
    y_test = y_tests[y]
    tags = tagss[y]

    #모델 생성
    model = Sequential()
    model.add(Embedding(vocab_size, emb, input_length=max_len)) #2
    model.add(LSTM(128, activation=act, return_sequences=True, kernel_initializer='he_normal')) #3
    model.add(Dropout(drop))
    if(layer==10):
        model.add(LSTM(128, activation=act, return_sequences=True, kernel_initializer='he_normal'))
        model.add(Dropout(drop))
        model.add(LSTM(128, activation=act, return_sequences=True, kernel_initializer='he_normal'))
        model.add(Dropout(drop))
        model.add(LSTM(128, activation=act, return_sequences=True, kernel_initializer='he_normal'))
        model.add(Dropout(drop))
        model.add(LSTM(128, activation=act, return_sequences=True, kernel_initializer='he_normal'))
        model.add(Dropout(drop))
        model.add(LSTM(128, activation=act, return_sequences=True, kernel_initializer='he_normal'))
        model.add(Dropout(drop))
    model.add(LSTM(128, activation=act, kernel_initializer='he_normal')) #4
    model.add(Dropout(drop))
    model.add(Dense(tag_num, activation='softmax', kernel_initializer='he_normal')) #5

    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    model.summary() #화면에 출력

    tnan = TerminateOnNaN()
    es = EarlyStopping(monitor='val_loss', mode='min', min_delta=0,  verbose=1, patience=100) #과적합방지

    #학습
    model.fit(X_train, y_train, batch_size=32, epochs=200, verbose=1,
          callbacks=[es, tnan], validation_split=0.3)

    #평가지표 생성
    absScore = model.evaluate(X_test, y_test, batch_size=32, verbose=0)[1]

    y_pred = model.predict(X_test, batch_size=32)
    cnt = 0 #정답 count
    for i in range(len(y_pred)): #i: y_pred, y_test의 인덱스
        for j in predict_tag(y_pred[i], 3): #j: y_pred의 태그 인덱스
            if tags[y_test[i].argmax()] == tags[j]:
                cnt += 1
    score = cnt/len(y_pred)

    #저장
    if opt == momentum:
        opt = 'momentum'
    if act == swish:
        act == 'swish'
    modelname = ('_l_' + str(layer) + '_o_' + opt + '_e_' + str(emb)
                 + '_a_' + act + '_d_' + str(drop) + '_x_' + x + '_y_' + str(tag_num)
                 + '_s_' + str(absScore) + '_' + str(score) +'.h5')
    model.save(".\model\\" + modelname)

    print("절대 정확도 : " absScore)
    print("테스트 정확도 : " score)


#모델 학습 진행
for l in range(1):
    for o in range(2):
        for e in range(1):
            for a in range(3):
                for d in range(1):
                    for x in ['t', 's']:
                        for y in range(2):
                            model_control(l,o,e,a,d,x,y)
