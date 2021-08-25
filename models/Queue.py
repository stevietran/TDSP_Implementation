import heapq
import itertools

class PriorityQueue:
    def __init__(self):
        self.__pq = []                         # list of entries arranged in a heap
        self.__entry_finder = {}               # mapping of tasks to entries
        self.__REMOVED = '<removed-task>'      # placeholder for a removed task
        self.__counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0.0):
        'Add a new task or update the priority of an existing task'
        if task in self.__entry_finder:
            self.remove_task(task)
        count = next(self.__counter)
        entry = [priority, count, task]
        self.__entry_finder[task] = entry
        heapq.heappush(self.__pq, entry)

    def remove_task(self,task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.__entry_finder.pop(task)
        entry[-1] = self.__REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.__pq:
            priority, count, task = heapq.heappop(self.__pq)
            if task is not self.__REMOVED:
                del self.__entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    #An extra method to determine whether pq is empty
    def isEmpty(self):
        return len(self.__pq) == 0
