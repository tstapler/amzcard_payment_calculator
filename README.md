# Amazon Card Payment Calculator

**DISCLAMER**: These scripts are for personal usage only, they are not affilited with Amazon or Syncrony Bank. Always validate the script's output and use them at your own risk.

A collection of scripts to help calculate how much to pay for an Amazon Credit card statement.

## Usage
Download your statement from the Amazon Card website.

Next, convert your PDF statement into a csv
```shell
❯ python read_statement.py --statement statements/feb-march-statement.pdf
Saving to statements/feb-march-statement.csv
```

Finally, calculate your bill from the current month's statement.
```shell
❯ python calculate_bill.py --file statements/feb-march-statement.csv
Regular Balance Is 173.83

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

```
