import operator
import math

# Useful operator declarations that may be included.
factorial    = lambda a : math.gamma(a + 1)
square       = lambda a : a * a
cube         = lambda a : a * a * a
subfactorial = lambda a : round(factorial(a) / math.e)
NOT          = lambda a : ~int(a) if a.is_integer() else math.nan
AND          = lambda a, b : int(a) & int(b) if a.is_integer() and b.is_integer() else math.nan
OR           = lambda a, b : int(a) | int(b) if a.is_integer() and b.is_integer() else math.nan
XOR          = lambda a, b : int(a) ^ int(b) if a.is_integer() and b.is_integer() else math.nan


# Defines all allowed operators for the problem. To add a new operator, simply add a new entry to the list.
BINARY_OPERS = [
    ('{}+{}',  operator.add),
    ('{}-{}',  operator.sub),
    ('{}*{}',  operator.mul),
    ('{}/{}',  operator.truediv),
    ('{}**{}', operator.pow),
    # ('{}&{}',  AND),
    # ('{}|{}',  OR),
    # ('{}^{}',  XOR),
]

UNARY_OPERS = [
    ('sqrt({})',  math.sqrt),
    ('{}!',       factorial),
    # ('-{}',       operator.neg),
    # ('cbrt({})',  math.cbrt),
    # ('gamma({})', math.gamma),
    # ('sqr({})',   square),
    # ('cube({})',  cube),
    # ('!{}',       subfactorial),
    # ('⌈{}⌉',       math.ceil),
    # ('⌊{}⌋',       math.floor),
    # ('~{}',       NOT),
]

# Computational bounds in order to prevent overflow errors.
# Must be 0 <= MIN_BOUND < MAX_BOUND.
# Going below 0 is usually pointless, as any negative number can 
# simply be it's positive version negated
MAX_BOUND = 1000
MIN_BOUND = 0
