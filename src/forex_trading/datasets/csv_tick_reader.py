import csv
import logging
from pathlib import Path
from typing import Iterator, Dict
from datetime import datetime

import forex_trading


class CSVTickReader:
    """
    Attribute Information:
        1. Date
        2. Time
        3. Price
        4. Volumne
    """

    def __init__(self, source: Path) -> None:
        self.source = source
        self.bar = {}
        self.resolution = 60

    def data_iter(self) -> Iterator[Dict[str, str]]:
        with self.source.open() as source_file:
            reader = csv.reader(source_file)
            next(reader)
            for row in reader:
                timestamp_string = row[0] + " " + row[1]
                last_sample_ts = datetime.strptime(
                    timestamp_string, "%m/%d/%Y %H:%M:%S.%f"
                )
                break
            for row in reader:
                try:
                    timestamp_string = row[0] + " " + row[1]
                    ts = datetime.strptime(
                        timestamp_string, "%m/%d/%Y %H:%M:%S.%f"
                    )
                    delta = ts - last_sample_ts
                    if delta.seconds >= self.resolution:
                        yield {ts: self.bar}
                        self.bar["open"] = float(row[2])
                        self.bar["high"] = float(row[2])
                        self.bar["low"] = float(row[2])
                        last_sample_ts = ts
                    else:
                        try:
                            self.bar["high"] = max(
                                self.bar["high"], float(row[2])
                            )
                            self.bar["low"] = min(
                                self.bar["low"], float(row[2])
                            )
                            self.bar["close"] = float(row[2])
                        except KeyError:
                            logging.debug("first bar forming...")
                except IndexError:
                    logging.error(row)


# PACKAGE_ROOT = Path(forex_trading.__file__).resolve().parent
#
# DATAPATH = PACKAGE_ROOT / "datasets"
# tickRdr = CSVTickReader(source=DATAPATH / "EURUSD_1_TICK.csv").data_iter()
# next(tickRdr)
# for i, value in enumerate(tickRdr):
#     if i < 2:
#         print(value)
