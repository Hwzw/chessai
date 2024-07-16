import pandas as pd
import numpy as np
import chess as chess
import tensorflow as tf
from tensorflow import keras
from scipy.special import expit
class AiEval:
    model = keras.Sequential([
    keras.Input(shape=(8, 8, 6, 1)),
    keras.layers.Conv3D(64, (3, 3, 6), activation='relu', padding='same'),
    keras.layers.MaxPooling3D((2, 2, 2)),
    keras.layers.Conv3D(32, (3, 3, 6), activation='relu', padding='same'),
    keras.layers.MaxPooling3D((2, 2, 2)),
    keras.layers.Conv3D(16, (2, 2, 1), activation='relu', padding='same'),
    keras.layers.Dropout(0.1),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    #keras.layers.Dropout(0.5),
    keras.layers.Dense(2, activation='softmax')
    ])
    optimizer = keras.optimizers.SGD()
    epsilon = np.finfo(float).eps
    epochs=1
    def __init__(self) -> None:
        boards_csv = pd.read_csv('chessData.csv')
        boards_csv = boards_csv[:int(len(boards_csv)/10000)]
        boards_csv['Evaluation'] = pd.to_numeric(boards_csv['Evaluation'].str.replace('[^0-9.-]', '', regex=True))
        boards_csv['Evaluation'] = boards_csv['FEN'].apply(lambda fen: np.where(chess.Board(fen).turn, 1, -1)) * boards_csv['Evaluation']

        X = boards_csv['FEN']
        board_list = []
        batch_size = 100  # Adjust based on your available memory
        X_batches = [X[i:i + batch_size] for i in range(0, len(X), batch_size)]
        X_processed = []
        for batch in X_batches:
            X_processed.extend([board_to_list(chess.Board(x)) for x in batch])
        X = np.array(X_processed)


        y = boards_csv['Evaluation']
        y = np.column_stack([expit(y+ self.epsilon), 1-expit(y+self.epsilon)])

        # Training Set:
        X_train = X[:int(0.8 * len(X))]
        X_train = X_train.reshape(-1, 8, 8, 6, 1)
        y_train = y[:int(0.8 * len(y))]


        # Test Set:
        X_test = X[int(0.8 * len(X)):]
        X_test = X_test.reshape(-1, 8, 8, 6, 1)
        y_test = y[int(0.8 * len(y)):]

        self.model.compile(optimizer=self.optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(X_train, y_train, epochs=self.epochs)
    def predict(board, self):
        board_list = board_to_list(board)
        board_list = np.array(board_list)
        board_list = board_list.reshape(-1, 8, 8, 6, 1)
        return self.model.predict(board_list)

def board_to_list(board):
    piece_map = {
        chess.PAWN: [1,0,0,0,0,0],
        chess.KNIGHT: [0,1,0,0,0,0],
        chess.BISHOP: [0,0,1,0,0,0],
        chess.ROOK: [0,0,0,1,0,0],
        chess.QUEEN: [0,0,0,0,1,0],
        chess.KING: [0,0,0,0,0,1]
    }

    board_list = [[[0]*6 for _ in range(8)] for _ in range(8)]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = chess.square_rank(square)
            col = chess.square_file(square)
            piece_value = piece_map[piece.piece_type]
            if piece.color != board.turn:
                piece_value = [-x for x in piece_value]
            board_list[7 - row][col] = piece_value

    #turn_layer = [[1 if board.turn == chess.WHITE else -1]*6 for _ in range(8)]
    #turn_layer = [[1 if board.turn == chess.WHITE else -1 for _ in range(6)] for _ in range(8)]
    #board_list.append(turn_layer)
    return board_list