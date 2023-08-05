from .check_definitions import check_definitions
from .check_tasks import check_tasks


def check_input(argd):
    """Check whether the user input is valid

    Args:
        argd (dict): user input dict
    Returns:
        same as input if no errors found
        otherwise exit with a message.
    """
    for k in ['const', 'rules', 'tasks']:
        if k not in argd:
            print(
                "Error hint: missing required field: \"{}\"".format(k))
            exit()
        else:
            pass

        if k == "const" or k == "rules":
            check_definitions(argd[k], k)
        else:
            check_tasks(argd[k])

    return argd
