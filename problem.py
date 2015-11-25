try:
    import numpy as np
except ImportError:
    import numpypy as np


class Problem(object):
    """
    Opis problemu do rozwiazania
    """

    def __init__(self, elementy, belka):
        self.elementy = np.array(elementy)
        self.belka = belka      #: rozmiar belki


    @staticmethod
    def laduj_z_pliku(plik):
        with open(plik, 'rb') as f:
            lines = f.readlines()

        _san = lambda l: int(l.strip())

        rozmiar_belki = _san(lines[0])

        elementy = []
        for i in xrange(0, _san(lines[1])):
            elementy.append(_san(lines[2+i]))

        return Problem(elementy, rozmiar_belki)


