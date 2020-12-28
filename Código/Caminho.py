import math


class cidade:
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        self.next = None

    def get_position(self):
        return [self.__x, self.__y]

    def change_coords(self, c):
        self.__x = c[0]
        self.__y = c[1]


class caminho:
    def __init__(self):
        super().__init__()
        self.__inicio = None
        self.__fim = None
        self.__qt = 0
        self.__custo = 0

    def custo(self):
        return self.__custo

    def quantas(self):
        return self.__qt

    def conforto(self, w, c_min):
        v = (w + math.pow((c_min / self.__custo), 2)) / (1 + (2 * w))
        return v

    def __calc_distancia(self, coord_fim, coords):
        v = abs(coord_fim[0] - coords[0]) + abs(coord_fim[1] - coords[1])
        return v

    def substituir(self, coords, i):
        aux = self.__inicio
        n = 1
        while aux is not None:
            if n == i:
                break
            n += 1
            aux = aux.next
        aux.change_coords(coords)
        self.__custo = 0
        aux = self.__inicio
        while aux is not None:
            if aux.next is None:
                break
            else:
                self.__custo += self.__calc_distancia(
                    aux.get_position(), aux.next.get_position()
                )
            aux = aux.next

    def add(self, coords):
        nova = cidade(coords[0], coords[1])
        if self.__inicio is None:
            self.__inicio = nova
        if self.__fim is None:
            self.__fim = nova
        else:
            self.__custo += self.__calc_distancia(self.__fim.get_position(), coords)
            self.__fim.next = nova
            self.__fim = nova
        self.__qt += 1

    def print_list(self):
        aux = self.__inicio
        while aux is not None:
            print(aux.get_position(), end="")
            aux = aux.next
            if aux is not None:
                print("->", end="")
        print("\tCusto: {:02d}".format(self.__custo), end="")
        print()

    def get_city(self, i):
        aux = self.__inicio
        n = 1
        while aux is not None:
            if n == i:
                break
            n += 1
            aux = aux.next
        return aux.get_position()

    def pertence(self, coords):
        aux = self.__inicio
        while aux is not None:
            aux_coords = aux.get_position()
            if aux_coords[0] == coords[0] and aux_coords[1] == coords[1]:
                return True
            aux = aux.next
        return False
