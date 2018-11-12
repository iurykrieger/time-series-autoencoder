from pandas import read_csv, Series
from datetime import datetime
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

def get_train_test_dataset(apikey_normalized_data_file, client):
    dataset = read_csv(apikey_normalized_data_file, header=0, index_col=0, parse_dates=True)
    train = dataset[client["train"]["start"]:client["train"]["end"]]
    test = dataset[:client["train"]["start"]]
    test.append(dataset[client["train"]["end"]:])
    return train, test

def get_autoencoder(data, layer_range = 3000, step = 250):
    data = Input(shape=(data.shape[1], ))
    encoded = Dense(layer_range, activation="relu")(data)
    
    # Encoded layers
    for value in range((layer_range - step), 0, -step):
        encoded = Dense(value, activation="relu")(encoded)

    decoded = encoded

    # Decoded layers
    for value in range(step, (layer_range), step):
        decoded = Dense(value, activation="relu")(decoded)
    
    autoencoder = Model(inputs=data, outputs=Dense(data.shape[1], activation="sigmoid")(decoded))
    autoencoder.compile(optimizer="adadelta", loss="binary_crossentropy")
    autoencoder.summary()

    return autoencoder