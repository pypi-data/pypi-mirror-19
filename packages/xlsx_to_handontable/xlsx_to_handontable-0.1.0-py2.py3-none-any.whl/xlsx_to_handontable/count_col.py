def _go(l):
    n = 0
    for i in l:
        if i is not None and n:
            yield n
            n = 0
        n += 1
    if n:
        yield n


def count_col(l):
    return list(_go(l))


def test_count_col():
    col_expects = [
        [
            [1, None, 1], [2, 1]
        ],
        [
            [1, 1, None, None, 1], [1, 3, 1]
        ],
        [
            [1, 1, None, None, 1, 1, None], [1, 3, 1, 2]
        ],
        [
            [1, 1, None, None, None], [1, 4]
        ],
        [
            [], []
        ],
    ]

    for col, expect in col_expects:
        print("{} => {}".format(col, expect))
        assert count_col(col) == expect


if __name__ == '__main__':
    test_count_col()
