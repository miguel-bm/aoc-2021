def parse_list(string: str, type: type = str, splitter: str = None) -> list:
    """
    Convert a string to a list or arbitrary type
    """
    if splitter is None:
        splitter = "," if "," in string else ("\n" if "\n" in string else " ")

    return [type(element) for element in string.strip().split(splitter)]


def parse_int_list(string: str, splitter: str = None) -> list[int]:
    """
    Convert a string to a list of integers
    """
    return parse_list(string=string, type=int, splitter=splitter)


def parse_tuple_list(
    string: str, types: list[type], splitter: str = None
) -> list[tuple]:
    """
    Convert a string to a list of tuples
    """

    if splitter is None:
        splitter = "," if "," in string else " "

    return [
        tuple(t(e) for t, e in zip(types, line.strip().split(splitter)))
        for line in string.strip().split("\n")
    ]


def parse_dict(
    string: str, types: tuple[type] = (str, str), splitter: str = None
) -> dict:
    """
    Convert a string to a dictionary
    """

    key_type = types[0]
    value_type = types[1]
    if splitter is None:
        splitter = "," if "," in string else " "

    return {
        key_type(key): value_type(value)
        for line in string.strip().split("\n")
        for key, value in line.strip().split(splitter)
    }
