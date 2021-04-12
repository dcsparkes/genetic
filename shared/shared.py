def clipValue(value, lower=0, upper=255):
    """
    Limits input 'value' between minimum and maximum (inclusive) limits.
    :param value: input
    :param lower: lower bound
    :param upper: upper bound
    :return: value clipped to be within range.
    """
    return max(min(value, upper), lower)