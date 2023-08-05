from .ninja_const import ninja_const
from .ninja_io import ninja_io


def ninja_build(tasks):
    """Return the Ninja build section

    Args:
        tasks (list): a list of task dictionaries
    Returns:
        a string
    """
    output = []
    for t in tasks:
        item = "build {}: {} {}".format(
                    ninja_io(t['out']),
                    t['rule'],
                    ninja_io(t['in'])
                )
        if 'const' in t:
            output.append("{}\n{}".format(
                    item,
                    ninja_const(t['const'], "  "))
                )
        else:
            output.append(item)
    return "\n\n".join(output)
