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
    required = ['rules', 'tasks']
    for k in required:
        if k not in argd:
            print(
                "Error hint: missing required field: \"{}\"".format(k))
            exit()
        else:
            pass

    check_definitions(argd['rules'], 'rules')
    check_tasks(argd['tasks'])
    check_definitions(argd['const'], 'const')

    return argd
