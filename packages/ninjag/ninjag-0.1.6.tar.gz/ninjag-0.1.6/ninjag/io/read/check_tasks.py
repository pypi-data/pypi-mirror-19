from .check_definitions import check_definitions


def check_tasks(tasks):
    """Check tasks section"""
    if not isinstance(tasks, list):
        print("Error hint: \"tasks\" section must be a list")
        exit()

    for i, d in enumerate(tasks):
        for k in ["rule", "in", "out"]:
            if k not in d:
                msg = "Error hint:  task[{}] ".format(i+1)
                msg += "is missing required field: \"{}\"".format(k)
                print(msg)
                exit()
            else:
                pass

        if "const" in d:
            check_definitions(d['const'], "tasks/const")
        else:
            pass

    return True
