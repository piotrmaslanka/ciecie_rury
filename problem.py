class Problem(object):
    """Description of problem to solve"""

    def __init__(self, stock_size, elements):
        self.stock_size = stock_size        # size of the stock to cut
        self.elements = elements              # a list of elements to cut out (order doesn't matter)
        self.elements_size = len(elements)

    @staticmethod
    def load_from_file(plik):
        with open(plik, 'rb') as f:
            lines = f.readlines()

        _san = lambda l: int(l.strip())

        stock_size = _san(lines[0])

        elements = []
        for i in xrange(0, _san(lines[1])):
            elements.append(_san(lines[2+i]))

        return Problem(stock_size, elements)


