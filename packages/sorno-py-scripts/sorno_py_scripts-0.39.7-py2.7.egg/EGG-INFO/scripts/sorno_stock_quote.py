#!/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
"""Gets stock quotes and other information for stock symbols.

The script can print real-time or close to real-time stock quotes, historical
quotes, and also fundamental ratios for the stock (company).

TODO:
Use google api instead, e.g. http://www.google.com/finance/info?q=nasdaq:appl


    Copyright 2014 Heung Ming Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse

from cStringIO import StringIO

import csv
import datetime
import logging
import sys
import subprocess

from bs4 import BeautifulSoup
import requests
from sorno import loggingutil
from sorno import consoleutil

_LOG = logging.getLogger(__name__)
_PLAIN_LOGGER = None  # will be created in main()
_PLAIN_ERROR_LOGGER = None  # will be created in main()


class StockApp(object):
    # https://code.google.com/p/yahoo-finance-managed/wiki/enumQuoteProperty
    FIELD_HEADERS = [
        ("name", "s"),
        ("price", "l1"),
        ("date", "d1"),
        ("time", "t1"),
        ("change", "c1"),
        ("changeInPercent", "c"),
        ("lastTradeRealtime", "k1"),
        ("changeRealtime", "c6"),
        ("changePercentRealtime", "k2"),
        ("open", "o"),
        ("high", "h"),
        ("low", "g"),
        ("volume", "v"),
        ("AverageDailyVolume", "a2"),
        # ("SharesOutstanding", "j2"), shares outstanding returns non-standard
        # csv value
        ("bidRealtime", "b3"),
        ("askRealtime", "b2"),
        ("YearLow", "j"),
        ("YearHigh", "k"),
        ("DilutedEPS", "e"),
        ("EPSEstimateCurrentYear", "e7"),
        ("EPSEstimateNextYear", "e8"),
        ("PERatio", "r"),
        ("PERatioRealtime", "r2"),
        ("ShortRatio", "s7"),
        ("DividendPayDate", "r1"),
        ("ExDividendDate", "q"),
    ]

    YAHOO_STOCK_QUOTE_CSV_API = "http://download.finance.yahoo.com/d/quotes.csv"
    YAHOO_STOCK_HISTORICAL_QUOTES_API = "http://ichart.yahoo.com/table.csv"
    YAHOO_STOCK_INSIDER_PURCHASES_PAGE_TEMPLATE = (
        "http://finance.yahoo.com/q/it?s=%s+Insider+Transactions"
    )

    QUANDL_STOCK_FUNDAMENTAL_API = "http://www.quandl.com/api/v1/datasets/OFDP/DMDRN_%s_ALLFINANCIALRATIOS.csv"

    def __init__(
        self,
        stock_symbol,
        print_fundamentals=False,
        print_history=False,
        print_kd=False,
        print_price_quote=True,
        num_of_days_for_history=30,
        print_insider_purchases=False,
    ):
        self.stock_symbol = stock_symbol

        self.print_fundamentals = print_fundamentals
        self.print_history = print_history
        self.print_kd = print_kd
        self.print_price_quote = print_price_quote

        self.num_of_days_for_history = num_of_days_for_history
        self.print_insider_purchases = print_insider_purchases
        self.day_low = None
        self.day_high = None
        self.current_quote = None

    def run(self):
        if self.print_price_quote:
            resp = requests.get(
                self.YAHOO_STOCK_QUOTE_CSV_API,
                params={
                    's': self.stock_symbol,
                    'f': "".join([h[1] for h in self.FIELD_HEADERS]),
                    'e': ".csv",
                },
            )
            _LOG.debug("URL: %s", resp.url)

            text = resp.text.strip()
            headers = [h[0] for h in self.FIELD_HEADERS]

            lines = [",".join(headers), text]
            reader = csv.DictReader(lines)
            # there is only one row in the result
            d = list(reader)[0]

            for header in headers:
                _PLAIN_LOGGER.info("%s:\t%s", header, d[header])

            self.day_high = float(d['high'])
            self.day_low = float(d['low'])
            self.current_quote = float(d['price'])

        if self.print_fundamentals:
            resp = requests.get(
                self.QUANDL_STOCK_FUNDAMENTAL_API % self.stock_symbol.upper()
            )

            text = resp.text

            reader = csv.DictReader(text.split("\n"))

            rows = list(reader)
            rows.sort(key=lambda r: r['Date'])

            consoleutil.DataPrinter(rows).print_result(
                consoleutil.DataPrinter.PRINT_STYLE_VERBOSE
            )

        if self.print_history:
            _PLAIN_LOGGER.info("")
            self.print_historical_stock_quotes()

        if self.print_insider_purchases:
            _PLAIN_LOGGER.info("")
            self.print_insider_purchase_entries()

    def print_historical_stock_quotes(self):
        today = datetime.datetime.today()
        from_date = today - datetime.timedelta(self.num_of_days_for_history)

        params = {
            's': self.stock_symbol,
            'a': from_date.month - 1,
            'b': from_date.day,
            'c': from_date.year,
            'd': today.month-1,
            'e': today.day,
            'f': today.year,
            'g': "d",  # daily quotes
            'ignore': ".csv",
        }

        resp = requests.get(
            self.YAHOO_STOCK_HISTORICAL_QUOTES_API,
            params=params,
        )

        _LOG.info("URL: %s", resp.url)

        if self.print_kd:
            # The csv data came in reverse chronlogical order and with the
            # following fields:
            # Date Open High Low Close Volume Adj Close

            # First, reverse the data so that we store it in chronological
            # order.
            data = []
            first = True
            for line in resp.text.split("\n"):
                if line:
                    data.append(line.split(','))
            data.reverse()

            if not data:
                return

            # Second, take out the headers
            headers = data[-1] + ["%k", "%d"]
            del data[-1]

            all_ks = []
            # Third, calculate the %k and %d
            lowest = None
            highest = None
            for i, row in enumerate(data):
                if i >= 13:
                    data_in_period = data[i - 13:i + 1]
                    lowest = min([float(r[3]) for r in data_in_period])
                    highest = max([float(r[2]) for r in data_in_period])
                    current_close = float(row[4])
                    k = self.calculate_k(current_close, lowest, highest)
                    row.append(str(k))
                    all_ks.append(k)
                    if len(all_ks) >= 3:
                        # calculate %d
                        row.append(str(int(round(sum(all_ks[-3:]) / 3.0))))

            # Fourth, calculate current %k and %d
            if all_ks:
                current_row = [
                    "Current",
                    "N/A",
                    str(self.day_high),
                    str(self.day_low),
                    str(self.current_quote),
                    "N/A",
                    "N/A",
                ]
                lowest = min(lowest, self.day_low)
                highest = max(highest, self.day_high)
                k = self.calculate_k(self.current_quote, lowest, highest)
                current_row.append(str(k))
                all_ks.append(k)
                if len(all_ks) >= 3:
                    # calculate %d
                    current_row.append(str(int(round(sum(all_ks[-3:]) / 3.0))))
                data.append(current_row)

            # change it back to reverse chronlogical order
            data.reverse()

            # Finally, format the headers and data, then print them out
            out = []
            for row in data:
                out.append(self.format_data_row(row))

            consoleutil.DataPrinter(
                out,
                headers=headers,
                print_func=_PLAIN_LOGGER.info
            ).print_result()
        else:
            out = []
            first = True
            headers = None
            for line in resp.text.split("\n"):
                if line:
                    linedata = line.split(',')
                    if first:
                        headers = linedata
                        first = False
                        continue

                    out.append(self.format_data_row(linedata))
            consoleutil.DataPrinter(
                out,
                headers=headers,
                print_func=_PLAIN_LOGGER.info
            ).print_result()

    @staticmethod
    def format_data_row(row):
        return [
            "{0:.2f}".format(float(c)) if "." in c else c
            for c in row
        ]

    def historical_data_row_for_printing(self, row):
        return "\t".join(
            [
                "{0:.2f}".format(float(c)) if "." in c else c
                for c in row
            ]
        )

    @staticmethod
    def calculate_k(current, lowest, highest):
        return int(
            round(
                (current - lowest) / (highest - lowest) * 100
            )
        )

    def print_insider_purchase_entries(self):
        resp = requests.get(
            self.YAHOO_STOCK_INSIDER_PURCHASES_PAGE_TEMPLATE % self.stock_symbol,
        )
        soup = BeautifulSoup(resp.text, "lxml")
        tables = soup.select("table.yfnc_tableout1")
        if len(tables) < 3:
            _PLAIN_ERROR_LOGGER.error("No insider purchases available")
            return 1

        insider_history_table = tables[2]

        headers = []
        rows = []
        for i, tr in enumerate(insider_history_table.select("tr table tr")):
            if i == 0:
                # process headers
                for th in tr.select("th"):
                    headers.append(th.get_text())
            else:
                # process data
                rows.append([td.get_text() for td in tr.select("td")])
        consoleutil.DataPrinter(
            rows,
            headers=headers,
            print_func=_PLAIN_LOGGER.info,
        ).print_result(consoleutil.DataPrinter.PRINT_STYLE_NICETABLE)


def parse_args(cmd_args):
    description = __doc__.split("Copyright 2014")[0].strip()

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )

    parser.add_argument(
        "--fundamentals",
        action="store_true",
        help="Print fundamentals data",
    )

    parser.add_argument(
        "--insider-purchases",
        action="store_true",
        help="Print insider purchases",
    )

    parser.add_argument(
        "--history",
        help="Print historical stock quotes",
        action="store_true",
    )

    parser.add_argument(
        "--no-price-quote",
        action="store_true",
        help="Not printing price quote of the stock",
    )

    parser.add_argument(
        "-n",
        "--num-of-days",
        help="Number of days to print for historical stock quotes",
        type=int,
        default=30,
    )

    parser.add_argument(
        "-k",
        "--kd-line",
        help="Print values for fast stochastic oscillators along with"
            " historical stock quotes. This option can only be used with"
            " --num-of-days and there are at least 14 historical stock quotes."
            " The period used for %%k is 14, and %%d is 3-period"
            " moving average of %%k.",
        action="store_true",
    )

    parser.add_argument("stock_symbol", nargs="+")

    args = parser.parse_args(cmd_args)
    return args


def main():
    global _PLAIN_LOGGER, _PLAIN_ERROR_LOGGER

    args = parse_args(sys.argv[1:])

    loggingutil.setup_logger(_LOG, debug=args.debug)
    _PLAIN_LOGGER = loggingutil.create_plain_logger("PLAIN")
    _PLAIN_ERROR_LOGGER = loggingutil.create_plain_logger("PLAIN_ERROR", stdout=False)

    for stock_symbol in args.stock_symbol:
        app = StockApp(
            stock_symbol,
            print_history=args.history,
            print_kd=args.kd_line,
            print_price_quote=not args.no_price_quote,
            print_fundamentals=args.fundamentals,
            num_of_days_for_history=args.num_of_days,
            print_insider_purchases=args.insider_purchases,
        )
        app.run()


if __name__ == '__main__':
    main()
