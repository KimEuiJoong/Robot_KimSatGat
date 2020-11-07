import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import sys
sys.setrecursionlimit(10000)
import tensorflow as tf
tf.debugging.set_log_device_placement(True)

with tf.device('/device:GPU:0'):
    #시, 태그 데이터 불러오기
    with open('./poems_token_MLP_v2', 'rb') as fr:
        poems_token = pickle.load(fr)
    with open('./poems_tag', 'rb') as fr:
        poems_tag = pickle.load(fr)

    #멀티 레이블 정제(#이용해 리스트로 변환)
    poems_tag = poems_tag.drop(poems_tag[poems_tag=='불용'].index)
    poems_tag = poems_tag.str.split('#')

    #레이블 이진화(벡터화)
    mlb = MultiLabelBinarizer()
    poems_tagVector = mlb.fit_transform(poems_tag)

    #시 인덱스에 맞게 데이터 합치고 정제
    poems_tokens = []
    for poem in poems_token:
        poems_tokens.append(str(poem).replace("[","").replace("]","").replace("'",""))
    poem_tag = pd.DataFrame(poems_tokens, columns = ['poem'])
    poem_tag['tag'] = pd.Series(poems_tag)
    poem_tag.dropna(axis=0, inplace=True)
    for index in range(len(poems_tag.index)):
        poem_tag.loc[poems_tag.index[index], "tag"] = poems_tagVector[index]

    #훈련 데이터 / 테스트 데이터 분류
    sep_len = (int)(len(poem_tag)*8/10)
    train_poem = poem_tag['poem'].iloc[0:sep_len+1]
    train_tag = poem_tag['tag'].iloc[0:sep_len+1]
    test_poem = poem_tag['poem'].iloc[sep_len+1:len(poem_tag)+1]
    test_tag = poem_tag['tag'].iloc[sep_len+1:len(poem_tag)+1]

    max_words = 7000
    num_tag = 16

    #Keras Tokenizer로 DTM 생성(4가지 모드 사용 가능)
    def prepare_data(train_data, test_data, mode):
        t = Tokenizer(num_words = max_words)
        t.fit_on_texts(train_data)
        X_train = t.texts_to_matrix(train_data, mode=mode)
        X_test = t.texts_to_matrix(test_data, mode=mode)
        return X_train, X_test, t.index_word, mode

    modes = ['binary', 'count', 'tfidf', 'freq']
    X_train, X_test, index_to_word, mode = prepare_data(train_poem, test_poem, modes[0])

    Y_train = np.array([np.asarray(np.zeros(16,)).astype(np.float32)])
    for y in train_tag.to_numpy():
        Y_train = np.append(Y_train, np.array([np.asarray(y).astype(np.float32)]), axis=0)
    Y_train = np.delete(Y_train, 0, axis=0)
    Y_test = np.array([np.asarray(np.zeros(16,)).astype(np.float32)])
    for y in test_tag.to_numpy():
        Y_test = np.append(Y_test, np.array([np.asarray(y).astype(np.float32)]), axis=0)
    Y_test = np.delete(Y_test, 0, axis=0)

    #DeepLearning 모델 설계 + 학습 + 저장
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras.models import load_model

    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units=16, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, batch_size=128, epochs=100, verbose=0, validation_split=0.1)

    model.save('./model/' + 'MLP_model_v0.1.h5')
