import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load data
(X_tr, y_tr), (X_tst, y_tst) = mnist.load_data()
# reshape to be [samples][pixels][width][height]
X_tr = X_tr.reshape(X_tr.shape[0], 1, 28, 28).astype('float32')
X_tst = X_tst.reshape(X_tst.shape[0], 1, 28, 28).astype('float32')
# normalize inputs from 0-255 to 0-1
X_tr = X_tr / 255
X_tst = X_tst / 255
# one hot encode outputs
y_tr = np_utils.to_categorical(y_tr)
y_tst = np_utils.to_categorical(y_tst)
num_classes = y_tst.shape[1]

# define the larger model
def create_model():
	# create model
	m = Sequential()
	m.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
	m.add(MaxPooling2D(pool_size=(2, 2)))
	m.add(Conv2D(15, (3, 3), activation='relu'))
	m.add(MaxPooling2D(pool_size=(2, 2)))
	m.add(Dropout(0.2))
	m.add(Flatten())
	m.add(Dense(128, activation='relu'))
	m.add(Dense(50, activation='relu'))
	m.add(Dense(num_classes, activation='softmax'))
	# Compile model
	m.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return m
# build the model
modelConvBig = create_model()
# Fit the model
modelConvBig.fit(X_tr, y_tr, validation_data=(X_tst, y_tst), epochs=10, batch_size=200,verbose=2)
# Final evaluation of the model
scores = modelConvBig.evaluate(X_tst, y_tst, verbose=0)
print("Large CNN Error: %.2f%%" % (100-scores[1]*100))
