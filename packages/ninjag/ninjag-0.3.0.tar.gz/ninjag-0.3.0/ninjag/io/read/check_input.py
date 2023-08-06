from .check_definitions import check_definitions
from .check_tasks import check_tasks
from .check_types import check_types


def check_input(argd):
    """Check whether the user input is valid

    Args:
        argd (dict): user input dict
    Returns:
        same as input if no errors found
        otherwise exit with a message.
    """
    # check whether the required fields exist
    required = []
    for k in required:
        if k not in argd:
            print(
                "Error hint: missing required field: \"{}\"".format(k))
            exit()
        else:
            pass

    # check whether the formats are correct
    check_definitions(argd['rule'], 'rule')
    check_tasks(argd['task'])
    check_definitions(argd['def'], 'def')
    check_types(argd['include'], 'include', [list, str])
    check_types(argd['subninja'], 'subninja', [list, str])
    check_types(argd['phony'], 'phony', [list, dict])
    check_types(argd['default'], 'default', [list, str])

    return argd
