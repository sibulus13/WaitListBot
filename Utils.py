priorityConvert = {'Student': 1, 'Alumni': 2, 'Non-SFU': 3}


def get_priority(roles):
    '''
        Takes in user roles and return the min priority of all roles
    '''
    maxPriority = 99
    for role in roles:
        if role in priorityConvert:
            maxPriority = min(priorityConvert[role], maxPriority)
    return maxPriority
