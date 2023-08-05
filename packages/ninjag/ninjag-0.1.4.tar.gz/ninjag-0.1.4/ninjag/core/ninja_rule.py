def ninja_rule(ruleDict):
    """Return a list of Ninja rules

    Args:
        ruleDict (dict): a dictionary of rules
    Returns:
        a list, each item is a string like
        rule <rule name>
            command = ...
    """
    output = []
    for k in sorted(ruleDict.keys()):
        v = ruleDict[k]
        output.append(
            "rule {}\n  command = {}".format(k, v)
        )
    return "\n\n".join(output)
