'''
custom utils library by Franz Ludwig Kostelezky
'''

def flatten(ls: list) -> list:
    """This function returns a flattend list from an inputed nested list.

    Args:
        ls (list): The nested list, which should be converted to a flattend list.

    Returns:
        list

    """
    result = []
    if ls is not None:
        for element in ls:
            if type(element) is list:
                for subelement in flatten(element):
                    result.append(subelement)
            else:
                result.append(element)
    else:
        result = False
    return result