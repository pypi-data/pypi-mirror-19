from xlsx_to_handontable import count_col


def values_row_to_lable_counts(values_row):
    labels = [label_or_none for label_or_none in values_row if label_or_none]
    counts = count_col.count_col(values_row)
    return zip(labels, counts)


def line_to_label_counts(s):
    values_row = [i if len(i) else None for i in s.split('\t')]
    return values_row_to_lable_counts(values_row)


def label_counts_s_to_js_nested_headers(label_counts_s):
    return [[dict(label=label, colspan=col) for label, col in label_cols]
            for label_cols in label_counts_s]


def values_rows_to_lable_counts_s(values_rows):
    return [values_row_to_lable_counts(values_row) for values_row in values_rows]


def values_rows_to_js_nested_headers(values_rows):
    label_counts_s = values_rows_to_lable_counts_s(values_rows)
    return label_counts_s_to_js_nested_headers(label_counts_s)


if __name__ == '__main__':
    s = '''\
    1	2	3
    2_1	2_2			2_3
    3_1	3_2	3_3	3_4	3_5	3_6
    '''

    s = '''\
    기본		알람						시스템
    이름	URL	미디어 정보 확인	버퍼링 감지	정지화면	블랙화면 	무음	고음	보유기간	재시작 지연 시간(초)
    '''

    s = '''
    0\t1\t\t2
    a\tb\tc\td
    '''

    l = [i.strip() for i in s.split('\n')]
    l = [i for i in l if len(i)]
    print(l)
    label_counts_s = list([line_to_label_counts(i) for i in l])
    print("label_counts_s=", label_counts_s)
    print(label_counts_s_to_js_nested_headers(label_counts_s=label_counts_s))
