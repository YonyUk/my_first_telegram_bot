"""
data structs

here is defined a set of datastructures utils for store data
"""

from heapq import heappush,heappop

class HeapMax:
    
    """
    a heap of max
    """
    
    class HeapResult:
        
        def __init__(self,value,probability):
            self._value = value
            self._prob = probability
            pass
        
        @property
        def value(self):
            return self._value
        
        @property
        def probability(self):
            return self._prob
        
        def __str__(self):
            return f'Value: {self._value}, Probability: {self._prob}'
        
        def __repr__(self):
            return str(self)
        
        pass
    
    def __init__(self):
        self._items = []
        pass
    
    @property
    def count(self):
        return len(self._items)
    
    def push(self,value,prob):
        heappush(self._items,(-1*prob,value))
        pass
    
    def pop(self):
        prob,value = heappop(self._items)
        return self.HeapResult(value,-1*prob)
    
    def clear(self):
        self._items.clear()
    
    pass