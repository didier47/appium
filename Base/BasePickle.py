import pickle


def write(data, path="data.pickle"):
    with open(path, 'wb') as f:
        pickle.dump(data, f, 0)


def read(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}

    return data


def readInfo(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            print(data)
        except EOFError:
            data = []

    return data


def writeInfo(data="", path="data.pickle"):
    """
    :type data: dict
    """
    _read = readInfo(path)
    result = []
    if _read:
        _read.append(data)
        result = _read
    else:
        result.append(data)
    with open(path, 'wb') as f:

        pickle.dump(result, f)


if __name__ == "__main__":
    pass
