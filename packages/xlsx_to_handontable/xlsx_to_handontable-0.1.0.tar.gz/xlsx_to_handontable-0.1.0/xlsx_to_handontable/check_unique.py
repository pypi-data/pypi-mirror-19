from collections import Counter
from pprint import pprint


def check_unique(about, l):
    c = Counter(l)
    vs = [(k,v) for k,v in c.items() if v>1]
    errors = ["@{about} : {k} is not unique (count : {v})".format(about=about,k=k,v=v) for k,v in vs]
    return errors




if __name__ == '__main__':
    l = [1, 1, 2, 3]
    pprint(check_unique('mylist', l))