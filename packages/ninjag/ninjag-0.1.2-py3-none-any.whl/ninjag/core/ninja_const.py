def ninja_const(inputDict, indent=""):
    """Return a list of user defined constants

    Args:
        inputDict (dict): a dictionary of constant definitions
        indent (str): indentation for each definition
    Returns:
        a string
    """
    output = []
    for k, v in inputDict.items():
        output.append(
                "{}{} = {}".format(indent, k, v)
            )
    return "\n\n".join(output)
