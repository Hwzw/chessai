import chess as chess
import math
import numpy as np
import pandas as pd
import pygame as pg
import tensorflow as tf
from tensorflow import keras
from scipy.special import expit
import cnn_model
from cnn_model import board_to_list
from cnn_model import AiEval
import minmax
from minmax import alpha_beta
from minmax import get_best_move
from minmax import get_worst_move
from minmax import evaluate
import game

game.ai_vs_ai(chess.Board(), get_best_move,True,get_worst_move,4)