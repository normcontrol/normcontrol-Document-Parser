def pt_to_sm(value):
    """

    Converts topographical points to centimeters

    :param value: Conventional value

    :return: The resulting value in centimeters

    """
    return value / 28.346

def dm_to_sm(value):
    """

    Converts inches to centimeters

    :param value: Conventional value

    :return: The resulting value in centimeters

    """
    return value * 2.54