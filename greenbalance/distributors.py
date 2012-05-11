try:
    from itertools import cycle
except ImportError:
    def cycle(iterable):
        # cycle('ABCD') --> A B C D A B C D A B C D ...
        saved = []
        for element in iterable:
            yield element
            saved.append(element)
        while saved:
            for element in saved:
                  yield element

import wr


def weighted_random(data):
    return wr.choice(data)

def round_robin(data):
    return cycle(data)
