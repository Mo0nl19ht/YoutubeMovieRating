import pandas as pd
import numpy as np
from tensorflow.keras.layers import Embedding, Dense, LSTM,Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.python.client import device_lib


device_lib.list_local_devices()


X=pd.read_csv("data_0_all_finish_del.csv")
X['comment']=X['comment'].map(eval)
x_train=np.array(X['comment'])
x=[]
for i in x_train:
    x.append(np.asarray(i).astype('float32'))
x=np.asarray(x)
y=np.asarray(X['rate'])
y=y.reshape(-1,1)

model = Sequential()
model.add(Embedding(118798,1000))
model.add(Bidirectional(LSTM(32, return_sequences=True),input_shape=(30,1)))
model.add(Bidirectional(LSTM(32, return_sequences=True)))
model.add(Bidirectional(LSTM(32)))
model.add(Dense(1, activation='relu'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('test0726.h5', monitor='val_loss', mode='min', verbose=1, save_best_only=True)

model.compile(optimizer='Adam', loss='mse', metrics=["mae"])
history = model.fit(x, y, epochs=10, callbacks=[es, mc], batch_size=8000, validation_split=0.2,verbose=1)

# loaded_model = load_model('best_model.h5')
# loaded_model.evaluate(x, y)

# def sentiment_predict(new_sentence):
#     stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
#     new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
#     new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
#     encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩 위에서 fit 해야함
#     pad_new = pad_sequences(encoded, maxlen = max_len)
#     score = float(loaded_model.predict(pad_new))
#     return score