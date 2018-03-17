import numpy as np


def extract_variable(dataset, field_name):
    if field_name not in dataset.variables:
        return np.nan

    var = dataset.variables[field_name]
    val = var[::] if var.size > 1 else var[0]
    return np.ma.getdata(val) if np.ma.is_masked(val) else val


def string_from_bytearray(arr):
    if type(arr) == np.ndarray:
        return "".join([c.decode('utf-8') if type(c) in (np.bytes_, bytes) else c for c in arr])
    else:
        return arr
