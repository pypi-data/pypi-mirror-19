from .ninja_const import ninja_const


def ninja_build(tasks):
    """Return the Ninja build section

    Args:
        tasks (list): a list of task dictionaries
    Returns:
        a list, each is a string like
        build my.out: cc in.c
            cflags = -Wall
    """
    output = []
    for t in tasks:
        output.append(
                "build {}: {} {}".format(
                    " ".join(t['out']),
                    t['rule'],
                    " ".join(t['in'])
                )
            )
        if 'const' in t:
            output = output + ninja_const(t['const'], "  ")
    return output
