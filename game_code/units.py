PIXELS_IN_ONE_UNIT = 10.0
UNITS_IN_ONE_PIXEL = 1 / PIXELS_IN_ONE_UNIT


def screen_to_world(k):
    if isinstance(k, tuple) or isinstance(k, list):
        return k[0] * UNITS_IN_ONE_PIXEL, k[1] * UNITS_IN_ONE_PIXEL
    else:
        return k * UNITS_IN_ONE_PIXEL


def world_to_screen(k):
    if isinstance(k, tuple) or isinstance(k, list):
        return k[0] * PIXELS_IN_ONE_UNIT, k[1] * PIXELS_IN_ONE_UNIT
    else:
        return k * PIXELS_IN_ONE_UNIT
