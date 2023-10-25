import csv
from pathlib import Path
from typing import Iterator, List
from datetime import datetime

import forex_trading

PACKAGE_ROOT = Path(forex_trading.__file__).resolve().parent
DATAPATH = PACKAGE_ROOT / "datasets"


class TxtTickReader:
    """
    Attribute Information
    1. Date
    2. Time
    3. Open
    4. High
    5. Low
    6. Close
    7. UpVolume
    8. TotalVolume
    9. UpTicks
    10. DownTicks
    11. TotalTicks
    """

    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[List[str]]:
        with self.source.open() as source_file:
            reader = csv.reader(source_file)
            next(reader)
            for row in reader:
                timestamp_string = row[0] + " " + row[1]
                ts = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S")
                yield dict(
                    open=float(row[2]),
                    high=float(row[3]),
                    low=float(row[4]),
                    close=float(row[5]),
                    UpVolume=float(row[6]),
                    DownVolume=float(row[7]),
                    Datetime=ts,
                )


if __name__ == "__main__":
    tickRdr = TxtTickReader(
        source=DATAPATH / "LMAX EUR_USD 1 Minute.txt"
    ).data_iter()
    print(next(tickRdr))
    print(next(tickRdr))
