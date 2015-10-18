import numpy as np
from mozliwe_skroje import policz_mozliwe_skroje


class Problem(object):
    """
    Opis problemu do rozwiazania
    """

    def __init__(self, typy_elementow, ilosc_elementow, rozmiar_belki):
                # i-ty typ jaka ma dlugosc
        self.typy_elementow = np.array(typy_elementow)

                # ile musi byc elementow i-tego typu
        self.ilosc_elementow = np.array(ilosc_elementow)
        self.rozmiar_belki = rozmiar_belki

        self.mozliwe_sposoby_ciecia = policz_mozliwe_skroje(rozmiar_belki, self.typy_elementow)

        self.resztka_z_ntego_sposobu_ciecia = [
            rozmiar_belki - np.sum(self.typy_elementow * sposob_ciecia)
            for sposob_ciecia
            in self.mozliwe_sposoby_ciecia
        ]


        self.dl_rek = len(self.mozliwe_sposoby_ciecia)  # dlugosc rekordow

    def print_(self):
        print 'Problem do rozwiazania:\n  Przy nieskonczonej ilosci dluznic dlugosci %s okresl sposoby ciecia tak by uzyskac:' % (self.rozmiar_belki, )
        for typ, ilosc in zip(self.typy_elementow, self.ilosc_elementow):
            print '   %s elementow o dlugosci %s' % (ilosc, typ)
        print '  minimalizujac resztki z ciecia'

    @staticmethod
    def laduj_z_pliku(plik):
        with open(plik, 'rb') as f:
            lines = f.readlines()

        _san = lambda l: int(l.strip())

        rozmiar_belki = _san(lines[0])

        elementy = []
        for i in xrange(0, _san(lines[1])):
            elementy.append(_san(lines[2+i]))

        typy_elementow = list(set(elementy))

        ilosc_elementow = [elementy.count(x) for x in typy_elementow]

        return Problem(typy_elementow, ilosc_elementow, rozmiar_belki)


