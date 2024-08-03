"""
probabilistic

a module to make probabilistic calculus
"""
from statistics import mean

class BinomialCoef:
    
    """
    the abstraction for rhe binomial coeficent
    """
    
    def __init__(self,n,k):
        if n < k: raise Exception('n most be greather or equal to k')
        if k == 0 or k == n:
            self._value = 1
            pass
        else:
            self._n = n
            self._k = k
            self._num = list([i for i in range(1,n + 1) if i > max(k,n - k)])
            self._den = list([i for i in range(1,min(k + 1,n - k + 1))])
            if len(self._den) == 0:
                self._den = [1]
                pass
            self._value = None
            pass
        pass
    
    @property
    def value(self):
        if self._value:
            return self._value
        N = self._num.pop(0)
        D = self._den.pop(0)
        while len(self._den) > 0:
            N *= self._num.pop(0)
            D = self._den.pop(0)
            N //= D
            pass
        while len(self._num) > 0:
            N *= self._num.pop(0)
            pass
        self._value = N // D
        return self._value
    
    pass

def binomial(p,n,k):
    coef = BinomialCoef(n,k)
    return coef.value * (p**k) * ((1 - p)**(n - k))

def geometrical(p,k):
    return p*((1 - p)**(k - 1))

def nbinomial(p,r,k):
    coef = BinomialCoef(k - 1, r - 1)
    return coef.value * (p**r) * ((1 - p)**(k - r))
