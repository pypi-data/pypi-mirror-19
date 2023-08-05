from .ninja_io import ninja_io


def ninja_const(inputDict, indent=""):
    """Return a list of user defined constants

    If the value of the const definition is a list,
    then it will be concatenated.

    Args:
        inputDict (dict): a dictionary of constant definitions
        indent (str): indentation for each definition

    Returns:
        a string
    """
    output = []
    for k in sorted(inputDict.keys()):
        v = inputDict[k]
        output.append(
                "{}{} = {}".format(indent, k, ninja_io(v))
            )
    return "\n".join(output)
