class PriorityItem():

    def __init__(self, priority: int, value: str) -> None:
        self.priority = priority
        self.value = value


class WaitList():
    '''
        Distinguishes between roled (SFU, non-SFU) members for waitlist sign ups 
        Once deadline passes:
            all role sign ups become the same priority,
            any free spots on the main list is filled with waitlisted members
    '''

    def __init__(self, wait_priority=2, max_priority=5, max_capacity=20):
        self.lst = []
        self.wait_list = []
        self.wait_priority = wait_priority
        self.max_priority = max_priority
        self.max_capacity = max_capacity
        self.deadline_passed = False

    def is_in(self, item):
        '''
            Checks if item is in state lists
        '''
        for i, v in enumerate(self.lst):
            if v.value == item.value:
                return True

        for i, v in enumerate(self.wait_list):
            if v.value == item.value:
                return True
        return False

    def add(self, item):
        '''
            adds member to sign up list depending on member priority:
                if member is already signed up, return msg
                if member is low priority > add to waitlist
                if member is high priority > add to list if not full, else waitlist
        '''
        if self.is_in(item):
            msg = f'You, {item.value} have already signed up'
            print(msg)
            return msg
        if item.priority > self.wait_priority:
            self.wait_list.append(item)
            msg = f'You, {item.value} have been waitlisted'
            return msg
        if len(self.lst) < self.max_capacity:
            self.lst.append(item)
            msg = f'You, {item.value} are on the list'
            return msg
        self.wait_list.append(item)
        msg = f'You, {item.value} have been waitlisted'
        return msg

    def remove(self, item):
        '''
            remove item from list
            prints error if item not found
        '''
        for i, v in enumerate(self.lst):
            if v.value == item.value:
                self.lst.pop(i)
                msg = f'You have been un-signed up from the sign up list'
                print(msg)
                return msg

        for i, v in enumerate(self.wait_list):
            if v.value == item.value:
                self.wait_list.pop(i)
                msg = f'You have been un-signed up from the waitlist'
                print(msg)
                return msg
        msg = f'Error: {item.value} not found and cannot be removed'
        print(msg)
        return msg

    def show(self):
        '''
            shows list state
        '''
        print('List')
        for entry in self.lst:
            print(entry.value)
        for entry in self.wait_list:
            print('waitlisted: ', entry.value)
        print()

    def show_absolute(self):
        '''
            shows list state
        '''
        print('Absolute List')
        for entry in self.lst:
            print(entry.value)
        free_spots = self.max_capacity - len(self.lst)
        if free_spots <= 0:
            print()
            return
        for entry in self.wait_list:
            print(entry.value)
            free_spots -= 1
            if free_spots <= 0:
                print()
                return
        print()

    def get(self):
        wait_list = ''
        for entry in self.lst:
            wait_list += entry.value + '\n'
        for entry in self.wait_list:
            wait_list += 'waitlisted: ' + entry.value + '\n'
        return wait_list

    def get_counts(self):
        '''
            Return msg of the numbers of people on list and waitlist
        '''
        msg = f'list: {len(self.lst)}/{self.max_capacity} \t waitlist: {len(self.wait_list)}'
        print(msg)
        return msg

    def get_absolute(self):
        wait_list = ''
        for entry in self.lst:
            wait_list += entry.value + '\n'
        free_spots = self.max_capacity - len(self.lst)
        if free_spots <= 0:
            return wait_list
        for entry in self.wait_list:
            wait_list += entry.value + '\n'
            free_spots -= 1
            if free_spots <= 0:
                return wait_list
        return wait_list


if __name__ == '__main__':
    waitlist = WaitList()
    waitlist.add(PriorityItem(0, 'Michael'))
    waitlist.add(PriorityItem(0, 'Johnny'))
    waitlist.add(PriorityItem(1, 'Karen'))
    waitlist.add(PriorityItem(2, 'Andy'))
    waitlist.add(PriorityItem(3, 'Brandon'))
    waitlist.add(PriorityItem(3, 'Clark'))
    waitlist.show()
    waitlist.show_absolute()
    waitlist.remove(PriorityItem(0, 'Michael'))
    waitlist.remove(PriorityItem(0, 'Brandon'))
    waitlist.show()
    waitlist.show_absolute()
    pass