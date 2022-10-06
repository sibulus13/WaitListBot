class PriorityItem():

    def __init__(self, priority: int, value: str) -> None:
        self.priority = priority
        self.value = value


class WaitList():
    # sort queue from low to high priority key, items poppable from middle
    # untested
    def __init__(self, wait_priority=2, max_priority=5, max_capacity=20):
        self.lst = []
        self.wait_list = []
        self.wait_priority = wait_priority
        self.max_priority = max_priority
        self.max_capacity = max_capacity

    def add(self, item):
        if item.priority > self.wait_priority:
            self.wait_list.append(item)
            return
        if len(self.lst) < self.max_capacity:
            self.lst.append(item)
            return
        self.wait_list.append(item)

    def remove(self, item):
        for i, v in enumerate(self.lst):
            if v.value == item.value:
                self.lst.pop(i)
                return
        for i, v in enumerate(self.wait_list):
            if v.value == item.value:
                self.wait_list.pop(i)
                return
        print(f'Error: {item.value} not found and cannot be removed')

    def show(self):
        print('List')
        for entry in self.lst:
            print(entry.value)
        for entry in self.wait_list:
            print('waitlisted: ', entry.value)
        print()

    def show_absolute(self):
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