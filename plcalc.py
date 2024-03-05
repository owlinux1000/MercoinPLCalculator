#!/usr/bin/env python

from pathlib import Path
import csv
import argparse


class ProfitAndLossCalculator:
    def __init__(self, path: str) -> None:
        self.__total_purchase_quanity = 0
        self.__total_purchase_amount = 0
        self.__total_sell_quanity = 0
        self.__total_sell_amount = 0
        self.__calculate(path)
        pass

    def __calculate(self, path: str) -> None:
        files = list(Path(path).glob("*.csv"))

        if len(list(files)) == 0:
            raise FileNotFoundError("No csv files found in the given path")

        for file in files:
            with open(file, "r") as fin:
                reader = csv.DictReader(fin)
                for row in reader:
                    if (row["取引種別"] == "受取" and row["通貨ペア"] == "BTC/JPY") or \
                        (row["取引種別"] == "購入" and row["通貨ペア"] == "BTC/POINT") or \
                            (row["取引種別"] == "購入" and row["通貨ペア"] == "BTC/JPY"):
                        self.__total_purchase_quanity += float(row["増加数量"])
                        self.__total_purchase_amount += float(row["約定金額"])
                        continue
                    if (row["取引種別"] == "売却" and row["通貨ペア"] == "BTC/JPY") or \
                        (row["取引種別"] == "売却" and row["通貨ペア"] == "BTC/POINT") or \
                            (row["取引種別"] == "送付" and row["通貨ペア"] == "BTC/JPY"):
                        self.__total_sell_quanity += float(row["減少数量"])
                        self.__total_sell_amount += float(row["約定金額"])
                        continue

    def get_total_purchase_quanity(self):
        return self.__total_purchase_quanity

    def get_total_purchase_amount(self):
        return self.__total_purchase_amount

    def get_total_sell_quanity(self):
        return self.__total_sell_quanity

    def get_total_sell_amount(self):
        return self.__total_sell_amount


def main():
    parser = argparse.ArgumentParser(
        description="Calculate Mercoin profit and loss from their csv files",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="path to a directory containing csv files",
        required=True
    )
    args = parser.parse_args()

    calculator = ProfitAndLossCalculator(args.path)
    print(f"購入数量の合計: {calculator.get_total_purchase_quanity()}")
    print(f"購入金額の合計: {calculator.get_total_purchase_amount()}")
    print(f"売却数量の合計: {calculator.get_total_purchase_quanity()}")
    print(f"売却金額の合計: {calculator.get_total_sell_amount()}")
    diff = calculator.get_total_sell_amount() - calculator.get_total_purchase_amount()
    print(f"所得金額: {diff}")


if __name__ == "__main__":
    main()
