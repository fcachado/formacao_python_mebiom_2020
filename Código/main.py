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


def criar_individuo(p, c, var, t_delta):
    if p.comprimento() == 0:
        cmin = c.custo()
    elif c.custo() < p.custominimo():
        cmin = c.custo()
    else:
        cmin = p.custominimo()

    tm = (1 - math.log(c.conforto(var.get("w"), cmin))) * var.get("b")

    tr = (
        (1 - math.log(c.conforto(var.get("w"), cmin)))
        * (p.comprimento() / var.get("v_max"))
        * var.get("p")
    )

    td = (1 - math.log(1 - c.conforto(var.get("w"), cmin))) * var.get("u")
    return Individuo(c, tm + t_delta, tr + t_delta, td + t_delta)


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
    for n_ind in range(var.get("v")):
        lista_cidades = gerador_cidades(x, y, var.get("n"))
        c = caminho()
        for cidade in lista_cidades:
            c.add(cidade)
