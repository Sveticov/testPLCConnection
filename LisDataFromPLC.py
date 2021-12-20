import time

from snap7.exceptions import Snap7Exception

from DataFromPLC import DataFromPLC
from real_convert import real_convert


def listDataFromPLC(connection, *data_plc: DataFromPLC):
    list_plc = []

    if connection:
        for data in data_plc:
            list_plc.append(real_convert(data.info))

            time.sleep(0.2)
        return list_plc
