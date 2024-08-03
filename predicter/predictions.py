"""
predicions

this module is to make probabilistics predictions about data
"""
from predicter.sqlite_db import PredicterDB
from predicter.probabilistic import binomial,nbinomial,geometrical
from statistics import mean
from predicter.data_structs import HeapMax
import re

class Predictor:
    
    def __init__(self,database_name,database_path=None):
        self._database = PredicterDB(database_name,database_path)
        self._history_size = None
        self._result_limit = 1
        self._heap = HeapMax()
        pass
    
    @property
    def prediction(self):
        heap = HeapMax()
        _,x100pred = self.x100interval()
        for key in x100pred.keys():
            heap.push(key,x100pred[key])
            pass
        temp_intervals = []
        while heap.count > 0:
            temp = heap.pop()
            limits = re.findall('\d+',temp.value)
            _,x10pred = self.x10interval(int(limits[0]),int(limits[1]))
            for key in x10pred.keys():
                temp_intervals.append((key,x10pred[key]))
                pass
            pass
        for v,prob in temp_intervals:
            heap.push(v,prob)
            pass
        temp_intervals.clear()
        while heap.count > 0:
            temp = heap.pop()
            limits = re.findall('\d+',temp.value)
            _,atpred = self.atinterval(int(limits[0]),int(limits[1]))
            for key in atpred.keys():
                temp_intervals.append((key,atpred[key]))
                pass
            pass
        for v,prob in temp_intervals:
            heap.push(v,prob)
            pass
        temp_intervals.clear()
        while heap.count > 0:
            temp = heap.pop()
            limits = re.findall('\d+',temp.value)
            _,dpred = self.dinterval(int(limits[0]),int(limits[1]))
            for key in dpred.keys():
                temp_intervals.append((key,dpred[key]))
                pass
            pass
        for v,prob in temp_intervals:
            heap.push(v,prob)
            pass
        result = {}
        for i in range(min(self._result_limit,heap.count)):
            temp = heap.pop()
            result[temp.value] = temp.probability
            pass
        return result
    
    def _x100_binomial_prob(self,history):
        # assuming a uniform distribution and top limit of 6500
        counts = [history[k] for k in history.keys()]
        n = sum(counts)
        result = {}
        for i in range(self._database.x100classes):
            if not i in history.keys():
                result[i] = binomial(1 / self._database.x100classes,n + 1,1)
                pass
            else:
                result[i] = binomial(1 / self._database.x100classes,n + 1,history[i] + 1)
                pass
            pass
        return result

    def _x10_binomial_prob(self,history):
        # assuming a uniform distribution and top limit of 6500
        counts = [history[k] for k in history.keys()]
        n = sum(counts)
        result = {}
        for i in range(self._database.x10classes):
            if not i in history.keys():
                result[i] = binomial(1 / self._database.x10classes,n + 1,1)
                pass
            else:
                result[i] = binomial(1 / self._database.x10classes,n + 1,history[i] + 1)
                pass
            pass
        return result
    
    def _atomic_binomial_prob(self,history):
        # assuming a uniform distribution and top limit of 6500
        counts = [history[k] for k in history.keys()]
        n = sum(counts)
        result = {}
        for i in range(self._database.aclasses):
            if not i in history.keys():
                result[i] = binomial(1 / self._database.aclasses,n + 1,1)
                pass
            else:
                result[i] = binomial(1 / self._database.aclasses,n + 1,history[i] + 1)
                pass
            pass
        return result
    
    def _decimal_binomial_prob(self,history):
        # assuming a uniform distribution and top limit of 6500
        counts = [history[k] for k in history.keys()]
        n = sum(counts)
        result = {}
        for i in range(self._database.dclasses):
            val = None
            if len(str(i)) < 2:
                val = float(f'0.0{i}')
                pass
            else:
                val = float(f'0.{i}')
                pass
            if not val in history.keys():
                result[val] = binomial(1 / self._database.dclasses,n + 1,1)
                pass
            else:
                result[val] = binomial(1 / self._database.dclasses,n + 1,history[val] + 1)
                pass
            pass
        return result
   
    def _get_result_sorted(self,result):
        for key in result.keys():
            self._heap.push(key,result[key])
            pass
        r = {}
        for i in range(min(self._result_limit,self._heap.count)):
            temp = self._heap.pop()
            r[temp.value] = temp.probability
            pass
        self._heap.clear()
        return r
    
    def x100interval(self):
        tag,history = self._database.intervals_history(limit=self._history_size,interval=100)
        temp = self._x100_binomial_prob(history)
        result = {}
        for key in temp.keys():
            result[f'{key * 100} <= x < {(key + 1) * 100}'] = temp[key]
            pass
        return tag,self._get_result_sorted(result)
    
    def x10interval(self,bottom,top):
        tag,history = self._database.intervals_history(bottom,top,limit=self._history_size,interval=10)
        temp = self._x10_binomial_prob(history)
        result = {}
        for key in temp.keys():
            result[f'{key * 10 + bottom} <= x < {(key + 1) * 10 + bottom}'] = temp[key]
            pass
        return tag,self._get_result_sorted(result)
    
    def atinterval(self,bottom,top):
        tag,history = self._database.intervals_history(bottom,top,limit=self._history_size,interval=1)
        temp = self._atomic_binomial_prob(history)
        result = {}
        for key in temp.keys():
            result[f'{key + bottom} <= x < {key + 1 + bottom}'] = temp[key]
            pass
        return tag,self._get_result_sorted(result)
    
    def dinterval(self,bottom,top):
        tag,history = self._database.intervals_history(bottom,top,limit=self._history_size)
        temp = self._decimal_binomial_prob(history)
        result = {}
        for key in temp.keys():
            result[f'{key  + bottom}x'] = temp[key]
            pass
        return tag,self._get_result_sorted(result)
    
    def set_history_size(self,size):
        if not type(size) == int and not size == None:
            raise Exception('size most be integer')
        self._history_size = size
        pass

    def set_result_limit(self,limit):
        if not type(limit) == int:
            raise Exception('limit most be of type integer')
        self._result_limit = limit
        pass

    def update(self,value):
        self._database.update(value)
        pass
    
    pass