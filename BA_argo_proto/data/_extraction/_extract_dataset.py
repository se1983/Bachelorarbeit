import numpy as np


def extract_variable(dataset, field_name):
    """
    Extractor for Variables of a netCDF.

    :param dataset: Opened netCDF Dataset
    :param field_name: The Name of the Variable.
    :return: Extracted Data
    """
    if field_name not in dataset.variables:
        return np.nan

    var = dataset.variables[field_name]
    val = var[::] if var.size > 1 else var[0]
    return np.ma.getdata(val) if np.ma.is_masked(val) else val


def string_from_bytearray(arr):
    """
    Formats bytearrays to string.
    :param arr: bytearray
    :return: string representation of the bytearray.
    """
    if type(arr) == np.ndarray:
        return "".join([c.decode('utf-8') if type(c) in (np.bytes_, bytes) else c for c in arr])
    else:
        return arr
