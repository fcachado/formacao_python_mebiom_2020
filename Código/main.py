import random
from Caminho import caminho
from Individuo import Individuo
from População import Populacao
import math
import copy
import matplotlib.pyplot as plt


def gerador_cidades(x, y, num):
    lista = []
    for i in range(num):
        while True:
            cidade = [random.randint(x[0], x[1]), random.randint(y[0], y[1])]
            if cidade not in lista:
                break
        lista.append(cidade)
    return lista


if __name__ == "__main__":
    var = {
        "x_max": 20,
        "y_max": 20,
        "n": 15,
        "t_final": 300,
        "w": 1 / 1000,
        "v": 25,
        "v_max": 50,
        "u": 300,
        "b": 1,
        "p": 5,
        "p2": 0.5,
        "p3": 0.5,
        "intervalo_dados": 1000,
        "intervalo_print": 5,
    }
    x = [0, var.get("x_max")]
    y = [0, var.get("y_max")]
    p = Populacao()
