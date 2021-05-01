from vector import vector

import random

from PIL import ImageColor


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
        if default is None:
            retVal.append(0)  # I guess... arbitrary decision that None = 0, maybe better to make a tuple of Nones
        else:
            retVal.append(default)
    else:
        retVal.extend(input)
        if default:
            retVal.extend([default] * length)
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


def randomRGBContrasting(count=2):
    hue1 = random.randint(0, 359)
    hues = [(hue1 + i * 360 // count) % 360 for i in range(count)]
    random.shuffle(hues)
    sats = [s * 100 // (count + 2) for s in range(1, count + 2)]
    random.shuffle(sats)
    values = [random.randint(0, 100) for i in range(count)]
    return [ImageColor.getrgb("hsv({},{}%,{}%)".format(h, s, v)) for h, s, v in zip(hues, sats, values)]


def randomRGBPair():
    colour1 = []
    colour2 = []

    for i in range(3):
        channel1 = random.randint(0, 255)
        channel2 = (channel1 + random.randint(16, 240)) % 256
        colour1.append(channel1)
        colour2.append(channel2)

    return [tuple(colour1), tuple(colour2)]


def rgbBlend(c1, c2, proportion):
    """
    Blend with proportion: 0.0 = pure colour1, 1.0 = pure colour2
    :param c1: colour1
    :param c2: colour2
    :return: blended colour
    """
    prop = clipValue(proportion, lower=0.0, upper=1.0)
    return tuple([round(a * (1 - prop) + b * prop) for a, b in zip(c1, c2)])


def rgbBlendPerChannel(cA, cB, proportions):
    """
    Blend with proportions: 0.0 = pure cA for that channel, 1.0 = pure cB

    :param cA: base colour
    :param cB: mix colour
    :param proportions: list/tuple containing the proportion per channel
    :return:
    """
    # print("cA: {}, cB: {}, proportions: {}".format(cA, cB, proportions))
    return tuple([round(a * (1 - p) + b * p) for a, b, p in zip(cA, cB, proportions)])


def _diamondVectors(angleInfo):
    """
    Calculate the unit vectors for the tessellated parallelogram pattern.  Default to orthogonal if second angle is not
    provided.

    :param angleInfo: angle information
    :return: tuple pair of 2D Vectors.
    """
    angs = []

    if type(angleInfo) is int or type(angleInfo) is float:
        angs.append(angleInfo)
    elif angleInfo is not None:
        angs = angleInfo[:2]

    if not len(angs):
        angs.append(0)
    if len(angs) == 1:
        angs.append(angs[0] + 90)
    return [vector.Vector2D.unit(a) for a in angs]


def reorient(list2d, orientation):
    """Flip and rotate list such that each of the 8 unique orientations can be returned.  Orientation """
    if orientation & 1:
        list2d = list(zip(*list2d))
    if orientation & 2:
        list2d = reversed(list2d)
    if orientation & 4:
        return [list(reversed(row)) for row in list2d]
    else:
        return [list(row) for row in list2d]
