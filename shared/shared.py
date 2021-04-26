def clipValue(value, lower=0, upper=255):
    """
    Limits input 'value' between minimum and maximum (inclusive) limits.
    :param value: input
    :param lower: lower bound
    :param upper: upper bound
    :return: value clipped to be within range.
    """
    return max(min(value, upper), lower)


def fillOutList(input, length, default=None):
    """
    Input sanitisation.  Make sure that the input is a tuple of the correct length.

    :param input: Input, could be an iterable, or a single value
    :param length: length of the output tuple.
    :param default: Default values for absent values.  If None, duplicate input values.
    :return: A tuple of the correct length.
    """
    retVal = []
    if type(input) is int or type(input) is float:
        retVal.append(input)
    elif input is None:
        retVal.append(0)  # I guess... arbitrary decision that None = 0, maybe better to make a tuple of Nones
    else:
        retVal.extend(input)
        retVal = retVal[:length]

    while len(retVal) < length:
        if default is None:
            retVal.extend(retVal)
        else:
            retVal.append(default)
    return retVal[:length]


def fillOutTuple(input, length, default=None):
    return tuple(fillOutList(input, length, default))


def normaliseProportions(proportions, count=2):
    props = fillOutTuple(proportions, count)

    total = sum(props)
    if count > icount:
        remainder = max(0, (1 - total) / (count - icount))
        props = tuple(props) + (remainder,) * (count - icount)
        total = sum(props)  # recalculate total, should be >= 1

    return [p / total for p in props]
