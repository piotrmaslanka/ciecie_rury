import numpy as np
from collections import deque

def policz_mozliwe_skroje(dlugosc_substratu, dlugosci_produktow):
    """
    Wypisuje wszystkie mozliwe sposoby ciecia dluznicy o dlugosci dlugosc_substratu
    Wynik jest tablica tablic z ilosciami ciecia na dany sposob.
    """

    def _zawiera(sc1, sc2):
        """Czy sc1 jest supersposobem dla sc2?"""
        for a, b in zip(sc1, sc2):
            if a < b:
                return False
        return True

    theta = set()
    to_remove = []

    things_to_derive = deque()
    things_to_derive.append((0, ) * len(dlugosci_produktow))

    while len(things_to_derive) > 0:
        ox = things_to_derive.popleft()

        try:
            for oy in list(theta):
                if _zawiera(oy, ox): raise RuntimeError
                if np.sum(dlugosci_produktow * ox) > dlugosc_substratu: raise RuntimeError
                if _zawiera(ox, oy):
                    theta.remove(oy)
        except RuntimeError:
            continue

        theta.add(ox)

        for i in xrange(0, len(ox)):
            op = list(ox)
            op[i] += 1
            things_to_derive.append(tuple(op))

    return map(lambda x: np.array(x, dtype=np.int32), list(theta))
