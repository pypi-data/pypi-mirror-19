
def size(n):
    """Return data unit"""
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def pprint_ntuple(nt):
    """Return field name """
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = size(value)
        print('%-10s : %7s' % (name.capitalize(), value))
