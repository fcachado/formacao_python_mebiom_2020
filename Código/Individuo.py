class Individuo:
    def __init__(self, c, tm, tr, td):
        super().__init__()
        self.__caminho = c
        self.__tr = tr
        self.__tm = tm
        self.__td = td

    def get_caminho(self):
        return self.__caminho

    def prox_evento_tipo(self):
        if self.__tm < self.__tr and self.__tm < self.__td:
            return 1
        elif self.__tr < self.__td and self.__tr < self.__tm:
            return 2
        else:
            return 3

    def prox_evento_tempo(self):
        if self.__tm < self.__tr and self.__tm < self.__td:
            return self.__tm
        elif self.__tr < self.__td and self.__tr < self.__tm:
            return self.__tr
        else:
            return self.__td

    def tempo_mutacao(self):
        return self.__tm

    def tempo_morte(self):
        return self.__td

    def tempo_reproducao(self):
        return self.__tr

    def muda_caminho(self, c):
        self.__caminho = c

    def muda_mutacao(self, t):
        self.__tm = t

    def muda_morte(self, t):
        self.__td = t

    def muda_reproducao(self, t):
        self.__tr = t

    def print(self):
        print("\tTm: {:0.6f}".format(self.__tm))
        print("\tTd: {:0.6f}".format(self.__td))
        print("\tTr: {:0.6f}".format(self.__tr))
        print("\tCaminho:")
        print("\t\t", end="")
        self.__caminho.print_list()
