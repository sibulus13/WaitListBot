import datetime

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


def create_same_weekday_arr(startDate, occurences=100):
    '''
        Gets same time of the week for x occurences
    '''
    date_arr = [startDate]
    for i in range(occurences):
        aWeek = datetime.timedelta(days=7)
        startDate += aWeek
        date_arr.append(startDate)
    return date_arr

def priority_not_in_effect(weekday):
    '''
        Checker for if priority is in effect
    '''

    if weekday == 0 or weekday == 1:
        return True
    return False


if __name__ == '__main__':
    # Some quality manual testing
    monday = datetime.datetime(
        2022,
        10,
        11,
    )

    print(create_same_weekday_arr(monday))
    for day in create_same_weekday_arr(monday):
        print(day.weekday())
