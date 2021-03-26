import inspect
from datetime import datetime

from calculate_bill import main


def trim_leading_spaces(text):
    """ Trim all of the leading whitespace from a string leaving a newline at the end.

    This function should be used to assert shell output via multiline strings. It
    handles removing the leading whitespace from the multiline string, but leaving
    the trailing newline most shell output should end with.

    :param text: The text to be trimmed
    :return: input with leading newlines and spaces removed
    """
    return inspect.cleandoc(text) + "\n"


def test_main(capsys):
    statement_date = datetime.fromisoformat("2021-03-26 11:39:09.288853")
    main("fixtures/sample-feb-march-statement.csv", statement_date=statement_date)
    captured = capsys.readouterr()
    assert captured.out == trim_leading_spaces(
        """Regular Balance Is 173.83

           12 Equal Monthly Payments 0% Apr Balance Is 74.18
           You started this plan on 11/26/2020 and have 9 months to go before you have paid it off

           6 Equal Monthly Payments 0% Apr Balance Is 28.17
           You started this plan on 01/09/2021 and have 4 months to go before you have paid it off

           6 Equal Monthly Payments 0% Apr Balance Is 46.11
           You started this plan on 02/21/2021 and have 5 months to go before you have paid it off

           6 Equal Monthly Payments 0% Apr Balance Is 1.84
           You started this plan on 02/21/2021 and have 5 months to go before you have paid it off

           6 Equal Monthly Payments 0% Apr Balance Is 1.10
           You started this plan on 02/21/2021 and have 5 months to go before you have paid it off

           Your Amazon Payment For This Month Is 325.22
    """)

# TODO: test for a payment at the end date
# TODO: test for a payment after the end date
