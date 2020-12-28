class node:
    def __init__(self, ind):
        super().__init__()
        self.frente = None
        self.atras = None
        self.__ind = ind

    def get_ind(self):
        return self.__ind


class Populacao:
    def __init__(self):
        super().__init__()
        self.__inicio = None
        self.__melhor = None
        self.__qt = 0
        self.__custo_minimo = 0

    def comprimento(self):
        return self.__qt

    def apagar_all(self):
        self.__inicio = None
        self.__melhor = None
        self.__qt = 0

    def __det_melhor(self):
        if self.__qt > 0:
            aux = self.__inicio
            min = aux.get_ind().get_caminho().custo()
            melhor = aux
            aux = aux.atras
            while aux is not None:
                if aux.get_ind().get_caminho().custo() < min:
                    min = aux.get_ind().get_caminho().custo()
                    melhor = aux
                aux = aux.atras
            self.__melhor = melhor
            self.__custo_minimo = min
        else:
            self.__melhor = None
            self.__custo_minimo = 0

    def custominimo(self):
        return self.__custo_minimo

    def melhor(self):
        return self.__melhor

    def proximo(self):
        return self.__inicio.get_ind()

    def apaga(self):
        self.__inicio = self.__inicio.atras
        self.__qt -= 1
        self.__det_melhor()

    def apaga_melhor(self):
        # print("----")
        # print(self.__melhor)
        # print(self.__inicio)
        if self.__melhor == self.__inicio:
            # print("primeiro")
            self.__inicio = self.__melhor.atras
        elif self.__melhor.atras is None:
            # print("último")
            aux = self.__melhor.frente
            aux.atras = None
            self.__melhor.frente = None
        else:
            # print("meio")
            aux_atras = self.__melhor.atras
            aux_frente = self.__melhor.frente
            aux_atras.frente = aux_frente
            aux_frente.atras = aux_atras
            self.__melhor.atras = None
            self.__melhor.frente = None
        self.__det_melhor()
        self.__qt -= 1

    def add(self, ind):
        nova = node(ind)
        if self.__inicio is None:
            # print("inicio")
            self.__inicio = nova
            self.__melhor = nova
        else:
            aux = self.__inicio
            n = 1
            while aux is not None:
                aux_ind = aux.get_ind()
                if ind.prox_evento_tempo() < aux_ind.prox_evento_tempo():
                    # print("menos tempo")
                    break
                else:
                    n += 1
                if aux.atras is None:
                    # print("break proximo null")
                    break
                else:
                    aux = aux.atras

            if n == 1:
                # print("primeiro")
                nova.atras = self.__inicio
                self.__inicio.frente = nova
                self.__inicio = nova
            elif n > self.__qt:
                # print("fim")
                nova.frente = aux
                aux.atras = nova
            else:
                # print("meio")
                nova.frente = aux.frente
                aux_frente = aux.frente
                aux_frente.atras = nova
                aux.frente = nova
                nova.atras = aux

        self.__qt += 1
        self.__det_melhor()

    def mostrar_pop(self):
        print("------------")
        n = 1
        aux = self.__inicio
        while aux is not None:
            print(n)
            aux_ind = aux.get_ind()
            aux_ind.print()
            aux = aux.atras
            n += 1
