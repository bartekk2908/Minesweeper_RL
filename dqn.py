from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
from keras.optimizers import Adam


def dqn(learning_rate, input_shape, output_size, conv_units, dense_units):
    model = Sequential([
        Conv2D(conv_units, (3, 3), activation='relu', padding='same', input_shape=(input_shape[0], input_shape[1], 1)),
        Conv2D(conv_units, (3, 3), activation='relu', padding='same'),
        Conv2D(conv_units, (3, 3), activation='relu', padding='same'),
        Conv2D(conv_units, (3, 3), activation='relu', padding='same'),
        Flatten(),
        Dense(dense_units, activation='relu'),
        Dense(dense_units, activation='relu'),
        Dense(output_size, activation='linear')])

    model.compile(optimizer=Adam(learning_rate=learning_rate, epsilon=1e-4), loss='mse')

    return model
