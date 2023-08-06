def ninja_rule(rules):
    """Return a list of Ninja rules

    Args:
        rules (list): a list of dictionaries of rules
    Returns:
        a list, each item is a string like
        rule <rule name>
            command = ...
    """
    output = []
    for d in rules:
        for k in sorted(d.keys()):
            v = d[k]
            output.append(
                "rule {}\n  command = {}".format(k, v)
            )
    return "\n\n".join(output)
