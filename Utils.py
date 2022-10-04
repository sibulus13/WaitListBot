priorityConvert = {'Student': 1, 'Alumni': 2, 'Non-SFU': 3}


def get_priority(roles):
    maxPriority = 99
    for role in roles:
        if role in priorityConvert:
            maxPriority = min(priorityConvert[role], maxPriority)
    return maxPriority
