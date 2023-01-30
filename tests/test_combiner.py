import io
import unittest
from textwrap import dedent

from pmg_csv_combiner.combiner import combine


class CSVFile:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value


class NamedStringIO(io.StringIO):
    def __init__(self, name: str, initial_value: str = "") -> None:
        super().__init__(initial_value)
        self.name = name


class TestCombiner(unittest.TestCase):

    csv1 = CSVFile(
        "csv1.csv",
        dedent(
            """\
            "a","b","c"
            "a1","b1","c1"
            """
        ),
    )

    csv2 = CSVFile(
        "path/to/csv2.csv",
        dedent(
            """\
            "a","b","d","e","f"
            "a2","b2","d2","e2","f2"
            """
        ),
    )

    csv3 = CSVFile(
        "csv3.csv",
        dedent(
            """\
            "a","b","c"
            """
        )
    )

    csv4 = CSVFile(
        "csv4.csv",
        dedent(
            """\
            "a","b","d","e","f"
            "a4","b4","d4","e4","f4"
            """
        )
    )

    csv5 = CSVFile(
        "csv5.csv",
        dedent(
            """\
            """
        )
    )

    csv6 = CSVFile(
        "csv6.csv",
        dedent(
            """\
            "a","b","c","d","e"
            "a6","b6","c6","d6","e6"
            """
        )
    )

    csv7 = CSVFile(
        "csv7.csv",
        dedent(
            """\
            """
        )
    )

    csv8 = CSVFile(
        "csv8.csv",
        dedent(
            """\
            """
        )
    )

    csv9 = CSVFile(
        "csv9.csv",
        dedent(
            """\
            "a","b","c"
            "a9","b9","c9"
            """
        ),
    )

    csv10 = CSVFile(
        "csv10.csv",
        dedent(
            """\
            "c","b","a"
            "c10","b10","a10"
            """
        ),
    )

    expected_csv1_csv2 = dedent(
        """\
        "a","b","c","d","e","f","filename"
        "a1","b1","c1","","","","csv1.csv"
        "a2","b2","","d2","e2","f2","csv2.csv"
        """
    )

    expected_csv3_csv4 = dedent(
        """\
        "a","b","c","d","e","f","filename"
        "a4","b4","","d4","e4","f4","csv4.csv"
        """
    )

    expected_csv5_csv6 = dedent(
        """\
        "a","b","c","d","e","filename"
        "a6","b6","c6","d6","e6","csv6.csv"
        """
    )

    expected_csv7_csv8 = dedent(
        """\
        """
    )

    expected_csv9_csv10 = dedent(
        """\
        "a","b","c","filename"
        "a9","b9","c9","csv9.csv"
        "a10","b10","c10","csv10.csv"
        """
    )

    expected_csv2_csv3_csv4 = dedent(
        """\
        "a","b","d","e","f","c","filename"
        "a2","b2","d2","e2","f2","","csv2.csv"
        "a4","b4","d4","e4","f4","","csv4.csv"
        """
    )

    cases = [
        ((csv1, csv2), expected_csv1_csv2),
        ((csv3, csv4), expected_csv3_csv4),
        ((csv5, csv6), expected_csv5_csv6),
        ((csv7, csv8), expected_csv7_csv8),
        ((csv9, csv10), expected_csv9_csv10),
        ((csv2, csv3, csv4), expected_csv2_csv3_csv4)
    ]

    def run_case(self, case: tuple[list[CSVFile], str]):
        fds = [NamedStringIO(f.name, f.value) for f in case[0]]
        e = case[1].split()
        for line, expected_line in zip(combine(*fds), e):
            self.assertEqual(line, expected_line)

    def test_combiner_different_columns(self):
        self.run_case(self.cases[0])

    def test_combiner_no_row_file(self):
        self.run_case(self.cases[1])

    def test_combiner_exist_empty_files(self):
        self.run_case(self.cases[2])

    def test_combiner_all_empty_files(self):
        self.run_case(self.cases[3])

    def test_combiner_colums_in_different_order(self):
        self.run_case(self.cases[4])

    def test_combiner_more_than_2_files(self):
        self.run_case(self.cases[5])


if __name__ == "__main__":
    unittest.main()