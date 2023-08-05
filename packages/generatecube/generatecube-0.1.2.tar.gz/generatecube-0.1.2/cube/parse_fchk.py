def alpha_electrons_number(path):
    return _electrons_n(path, 'Number of alpha electrons')


def beta_electrons_number(path):
    return _electrons_n(path, 'Number of beta electrons')


def _electrons_n(path, identifier):
    """Returns int for the number of electrons when the line starts with identifier"""
    with open(path, 'rt') as f:
        # the iterator reads the file line by line, therefore reading big files is not a problem
        for line in f:
            if line.startswith(identifier):
                return int(line.split()[-1])