# PMG CSV Combiner

Project from [PMG Programming Challenge](https://github.com/AgencyPMG/ProgrammingChallenges/tree/master/csv-combiner).

# How to use

This project uses [Poetry](https://python-poetry.org/). Check the official page for how to install it.

You can run it as follows:

```
$ poetry install
$ poetry run python pmg_csv_combiner/main.py tests/fixtures/clothing.csv tests/fixtures/accessories.csv > combined.csv
```

# Features

- Supports CSV files with different set of columns.
- Supports combining multiple files together.
- Can handle large files smoothly.
