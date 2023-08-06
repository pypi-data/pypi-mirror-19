from .ninja_def import ninja_def
from .ninja_io import ninja_io
from .ninja_build_dep import ninja_build_dep


def ninja_build(tasks):
    """Return the Ninja build section

    Args:
        tasks (list): a list of task dictionaries
    Returns:
        a string
    """
    output = []
    for t in tasks:
        item = "build {0}: {1} {2}{3}{4}".format(
                    ninja_io(t['out']),
                    t['rule'],
                    ninja_io(t['in']),
                    ninja_build_dep(t, "dep|"),
                    ninja_build_dep(t, "dep||")
                )
        if 'def' in t:
            output.append("{}\n{}".format(
                    item,
                    ninja_def(t['def'], "  "))
                )
        else:
            output.append(item)
    return "\n\n".join(output)
