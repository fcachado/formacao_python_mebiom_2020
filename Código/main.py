import random
from Caminho import caminho
from Individuo import Individuo
from População import Populacao
import math
import copy
import matplotlib.pyplot as plt


def troca_cidades(c_old):
    c = copy.deepcopy(c_old)
    i = random.randint(1, c.quantas())
    j = -1
    while True:
        j = random.randint(1, c.quantas())
        if j != i:
            break
    i_c = c.get_city(i)
    j_c = c.get_city(j)
    c.substituir(i_c, j)
    c.substituir(j_c, i)
    return c


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
        "x_max": 40,
        "y_max": 40,
        "n": 15,
        "t_final": 600,
        "w": 1 / 1000,
        "v": 25,
        "v_max": 50,
        "u": 300,
        "b": 1,
        "p": 5,
        "p2": 0.5,
        "p3": 0.5,
        "intervalo_dados": 5000,
        "intervalo_print": 6,
    }
    x = [0, var.get("x_max")]
    y = [0, var.get("y_max")]
    p = Populacao()
    for n_ind in range(var.get("v")):
        lista_cidades = gerador_cidades(x, y, var.get("n"))
        c = caminho()
        for cidade in lista_cidades:
            c.add(cidade)
        ind = criar_individuo(p, c, var, 0)
        p.add(ind)
    t = 0
    intervalo_print = 1
    intervalo_dados = 1

    n_mortes = 0
    n_reproducao = 0
    n_mutacao = 0
    n_epidemias = 0

    array_cmin = []
    array_t = []

    while True:
        indv = p.proximo()
        tipo = indv.prox_evento_tipo()
        t = indv.prox_evento_tempo()

        # mutação
        if tipo == 1:
            c_novo = indv.get_caminho()
            prob = 1 - math.pow(
                indv.get_caminho().conforto(var.get("w"), p.custominimo()), 2
            )
            if random.random() < prob:
                n_mutacao += 1
                c_novo = troca_cidades(c_novo)
                if random.random() < var.get("p2"):
                    n_mutacao += 1
                    c_novo = troca_cidades(c_novo)
                    if random.random() < var.get("p3"):
                        n_mutacao += 1
                        c_novo = troca_cidades(c_novo)
            p.apaga()
            indv.muda_mutacao(
                (1 - math.log(c.conforto(var.get("w"), p.custominimo()))) * var.get("b")
                + t
            )
            indv.muda_caminho(c_novo)
            p.add(indv)

        # reprodução
        elif tipo == 2:
            n_reproducao += 1
            p.apaga()
            c_novo = troca_cidades(indv.get_caminho())
            ind = criar_individuo(p, c_novo, var, t)
            p.add(ind)
            indv.muda_reproducao(
                (
                    (1 - math.log(c.conforto(var.get("w"), p.custominimo())))
                    * (p.comprimento() / var.get("v_max"))
                    * var.get("p")
                )
                + t
            )
            p.add(indv)
        # morte
        elif tipo == 3:
            prob = 1 - math.pow(
                indv.get_caminho().conforto(var.get("w"), p.custominimo()), 2
            )
            if random.random() < prob:
                n_mortes += 1
                p.apaga()
            else:
                p.apaga()
                indv.muda_morte(
                    (
                        (1 - math.log(1 - c.conforto(var.get("w"), p.custominimo())))
                        * var.get("u")
                    )
                    + t
                )
                p.add(indv)
        # epidemia
        if p.comprimento() > var.get("v_max"):
            p_novo = Populacao()
            cmin = p.custominimo()
            for n_it in range(5):
                p_novo.add(p.melhor().get_ind())
                p.apaga_melhor()
            while p.comprimento() > 0:
                ind_test = p.proximo()
                if random.random() < ind_test.get_caminho().conforto(
                    var.get("w"), cmin
                ):
                    p_novo.add(ind_test)
                p.apaga()
            p = p_novo
            n_epidemias += 1

        if t > (var.get("t_final") / var.get("intervalo_print")) * intervalo_print:
            print(
                "T: {:05f} ({:>4d}/{:>4d})".format(
                    t, intervalo_print, var.get("intervalo_print")
                )
            )
            print("\t{:>14s}: {:7d}".format("Nº epidemias", n_epidemias))
            print("\t{:>14s}: {:7d}".format("Nº mortes", n_mortes))
            print("\t{:>14s}: {:7d}".format("Nº reproducões", n_reproducao))
            print("\t{:>14s}: {:7d}".format("Nº mutacões", n_mutacao))
            print("\t{:>14s}: {:7d}".format("Dimensão", p.comprimento()))
            print("\t{:>14s}: {:7d}".format("Custo mínimo", p.custominimo()))
            intervalo_print += 1

        if t > (var.get("t_final") / var.get("intervalo_dados")) * intervalo_dados:
            array_cmin.append(p.custominimo())
            array_t.append(t)
            intervalo_dados += 1

        if t > var.get("t_final"):
            print("Terminou o tempo de simulação!")
            break
        elif p.comprimento() == 1:
            print("População vazia")
            break

    fig = plt.figure()
    plt.plot(array_t, array_cmin)
    plt.xlabel("Tempo")
    plt.ylabel("Custo")
    plt.title("Evolução do custo ao longo do tempo de simulação")
    plt.show()

