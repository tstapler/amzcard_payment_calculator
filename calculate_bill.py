from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import csv
import re
from typing import Tuple

from dateutil.relativedelta import relativedelta

cents = Decimal('.01')

NEW_STATEMENT_BALANCE = "New Statement Balance"
PREV_BALANCE = "Previous  Balance"
PREV_PAYMENTS = "Payments & Other Credits (-)"
BALANCE_TYPE = "Balance Type"
DATE_AND_AMOUNT = "Purchase Date/Amount"
DAY_MONTH_YEAR_FORMAT = "%m/%d/%Y"


def to_dollars(amount: str) -> Decimal:
    return Decimal(amount.strip("$").replace(',', ''))


def read_payment_plan(row: dict) -> Tuple[datetime, Decimal]:
    purchase_date, purchase_amount = row[DATE_AND_AMOUNT].split()
    return datetime.strptime(purchase_date, DAY_MONTH_YEAR_FORMAT), to_dollars(purchase_amount)


def payment_months_left(statement_date: datetime, purchase_date: datetime, num_payments: int) -> int:
    """The number of payments left for a purchase.

    The number of months left for a payment should be starting month plus the number of
    payments plus 1. This is because you don't have to make a payment until the month
    after you make a purchase.
    """
    due_date = purchase_date + relativedelta(months=num_payments)
    months_to_go = (due_date - statement_date).days // 30
    return months_to_go + 1


def main(csv_file, statement_date=datetime.now()):
    with open(csv_file) as f:
        payment = Decimal(0)
        for row in csv.DictReader(f):
            row_balance = to_dollars(row[NEW_STATEMENT_BALANCE])
            balance_type = row[BALANCE_TYPE]
            months_to_go = None
            if 'EQUAL MONTHLY' in balance_type:
                purchase_date, purchase_amount = read_payment_plan(row)
                if match := re.match(r"(\d+) EQUAL MONTHLY", balance_type):
                    num_payments = int(match[1])
                    row_balance = purchase_amount / num_payments
                    months_to_go = payment_months_left(statement_date, purchase_date, num_payments)
                    if months_to_go > 0:
                        payment += row_balance
            if balance_type == "Regular":
                payment += row_balance
            if balance_type == "Total":
                continue
            print(
                f"{balance_type} balance is {row_balance.quantize(cents, rounding=ROUND_HALF_UP)}"
                    .title())
            if months_to_go:
                print(f"You started this plan on {purchase_date.strftime(DAY_MONTH_YEAR_FORMAT)} and have {months_to_go} months to go before you have "
                      f"paid it off")
            print()
        print(
            f"Your amazon payment for this month is {payment.quantize(cents, rounding=ROUND_HALF_UP)}"
                .title())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest="file")

    args = parser.parse_args()
    main(args.file)
