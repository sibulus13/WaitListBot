class WaitList():
    # sort queue from low to high priority key, items poppable from middle
    # untested
    def __init__(self):
        self.waitList = []

    def add(self, item):
        for i in range(len(self.waitList)):
            if item['priority'] < self.waitList['priority']:
                self.waitList.insert(i, item)
                return
        self.waitList.append(item)

    def remove(self, item):
        self.waitList.remove(item)

    def show(self):
        for entry in self.waitList:
            print(entry)

    def get(self):
        return self.waitList
