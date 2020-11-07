import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
#tf.debugging.set_log_device_placement(True)

with tf.device('/device:GPU:0'):
    with open('poems_token_ckonlpy', 'rb') as fr:
        poems_token = pickle.load(fr) #series-list
    with open ('poems_tag_16', 'rb') as fr:
        poems_tag = pickle.load(fr) #series

    poems_tag = poems_tag.drop(poems_tag[poems_tag=='불용'].index)
    poems_tag = poems_tag.str.split('#')

    #태그 2개 이상 데이터 삭제
    for i in range(len(poems_tag)):
        if len(poems_tag.iloc[i]) != 1:
            poems_tag[poems_tag.index[i]] = np.nan
    poems_tag.dropna(inplace=True)
    for i in range(len(poems_tag)):
        poems_tag.iloc[i] = ''.join(poems_tag.iloc[i])

    # 태그 한 시만 DataFrame으로 변환
    poem_tag = pd.DataFrame()
    poem_tag['poem'] = poems_token
    poem_tag['tag'] = poems_tag
    poem_tag.dropna(inplace=True)

    #훈련/테스트 데이터 분류
    poem_tag['poem'] = poem_tag['poem'].str.split(" ")

    sep_len = (int)(len(poem_tag)*8/10)
    poem_train = poem_tag['poem'].iloc[0:sep_len+1]
    tag_train = poem_tag['tag'].iloc[0:sep_len+1]
    poem_test = poem_tag['poem'].iloc[sep_len+1:len(poem_tag)+1]
    tag_test = poem_tag['tag'].iloc[sep_len+1:len(poem_tag)+1]

    #단어 집합 크기 결정
    t = Tokenizer()
    t.fit_on_texts(poem_train)

    threshold = 2
    total_cnt = len(t.word_index)
    rare_cnt = 0
    total_freq = 0
    rare_freq = 0

    for key, value in t.word_counts.items():
        total_freq += value
        if(value < threshold):
            rare_cnt += 1
            rare_freq += value

    vocab_size = total_cnt - rare_cnt + 2

    #시 데이터 정수 인코딩
    tokenizer = Tokenizer(vocab_size, oov_token='OOV')
    tokenizer.fit_on_texts(poem_train) #Tokenizer에 단어-정수 집합 생성
    X_train_int = tokenizer.texts_to_sequences(poem_train) #정수 인코딩
    X_test_int = tokenizer.texts_to_sequences(poem_test)

    #시 데이터 패딩
    max_len = 200
    X_train = pad_sequences(X_train_int, maxlen = max_len, padding='post')
    X_test = pad_sequences(X_test_int, maxlen = max_len,  padding='post')

    X_train[0]

    #태그 데이터 정수 인코딩 -> 원-핫 인코딩
    tags = ['기쁨','즐거움','사랑1','사랑2','희망','활기','순수','잔잔','슬픔','의지',
            '그리움1','그리움2','무심','고독','불안','성찰']

    #정수 인코딩
    y_train_int = tag_train.copy()
    for i in range(len(y_train_int)):
        if tags.index(y_train_int.iloc[i]) >= 0:
            y_train_int.iloc[i] = tags.index(y_train_int.iloc[i])
    y_test_int = tag_test.copy()
    for i in range(len(y_test_int)):
        if tags.index(y_test_int.iloc[i]) >= 0:
            y_test_int.iloc[i] = tags.index(y_test_int.iloc[i])

    #정수->one-hot Vector
    y_train = to_categorical(y_train_int, len(tags))
    y_test = to_categorical(y_test_int, len(tags))

    #모델 설계 + 학습 + 평가 +저장
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout
    from tensorflow.keras import initializers
    from tensorflow.keras.callbacks import TerminateOnNaN, EarlyStopping

    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=max_len)) #2: embedding layer
    model.add(LSTM(128, activation='softsign', return_sequences=True,
                   kernel_initializer='he_normal')) #3~9: LSTM layer
    model.add(Dropout(0.5))
    model.add(LSTM(128, return_sequences=True, activation='softsign')) #4
    model.add(Dropout(0.5))
    model.add(LSTM(128, return_sequences=True, activation='relu')) #5
    model.add(Dropout(0.5))
    model.add(LSTM(128, return_sequences=True, activation='relu')) #6
    model.add(Dropout(0.5))
    model.add(LSTM(128, return_sequences=True, activation='relu')) #7
    model.add(Dropout(0.5))
    model.add(LSTM(128, return_sequences=True, activation='relu')) #8
    model.add(Dropout(0.5))
    model.add(LSTM(128, activation='softsign', kernel_initializer='he_normal')) #9
    model.add(Dropout(0.5))
    model.add(Dense(len(tags), activation='softmax', kernel_initializer='he_normal')) #10: output layer

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.summary()

    tnan = TerminateOnNaN()
    #es = EarlyStopping(monitor='val_loss', mode='min', min_delta=0,  verbose=1, patience=50)

    model.fit(X_train, y_train, batch_size=32, epochs=200, verbose=1, callbacks=[tnan], validation_split=0.3)

    absoluteScore = model.evaluate(X_test, y_test, batch_size=32, verbose=0)[1]
    def predict_tag(arr, n):
        arr_temp = arr.copy()
        tag = []
        for i in range(n):
            tag.append(arr_temp.argmax())
            arr_temp[arr_temp.argmax()] = 0
        return tag

    y_pred = model.predict(X_test, batch_size=32)

    cnt = 0
    for i in range(len(y_pred)):
        for j in predict_tag(y_pred[i], 3):
            if tags[y_test[i].argmax()] == tags[j]:
                cnt += 1
    testScore = cnt/len(y_pred)

    print("테스트 절대 정확도:", absoluteScore)
    print('테스트 정확도: ', testScore)

    model.save('./LSTM_gpu_test_' + str(absoluteScore) + '_' + str(testScore) + '.h5')
