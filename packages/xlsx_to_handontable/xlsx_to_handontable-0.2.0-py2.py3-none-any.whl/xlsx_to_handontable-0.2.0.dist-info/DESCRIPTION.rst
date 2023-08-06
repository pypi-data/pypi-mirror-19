# xlsx_to_handontable

- xlsx to handontable `configuration` + `sample`

# INSTALL

    pip install xlsx_to_handontable

# USAGE

    from xlsx_to_handontable import xlsx_to_configs_samples
    from yaml_dump import yaml_dump
    p = '0.xlsx'
    configs, samples = xlsx_to_configs_samples(p)
    print(yaml_dump(configs))
    print('-' * 20)
    print(yaml_dump(samples))    



# History

## 0.1.0 (2017-01-13)
- First release on PyPI.


