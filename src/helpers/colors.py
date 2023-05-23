def rgb_to_hex(rgb: tuple):
    """
    Function to convert rgb to hex

    :return: str Hex-code
    """
    red, green, blue = rgb
    return '#{:02x}{:02x}{:02x}'.format(red, green, blue)
