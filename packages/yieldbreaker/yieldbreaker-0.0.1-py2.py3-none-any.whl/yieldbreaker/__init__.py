"""
Simplify some use of generator/coroutine by splitting the yield/send flow into
two different steps

Example:

Assuming you have the following generator:

    def gen():
        for i in range(50):
            res = yield i
            print(i, res)

And you want to to print "FizzBuzz", you need somethign like::

    sg = gen()
    g = sg.send(None)
    try:
        while True:
            if (g % 5) == 0 and (g%7 == 0):
                g = sg.send('fizzbuzz')
            elif g%5 == 0:
                g = sg.send('fizz')
            elif (g % 7 == 0):
                g = sg.send('buzz')
            else :
                g = sg.send(g)
    except StopIteration:
        pass

Which can be cumbersome to write and hard to understand... you could rewrite
your initial gennerator and "split" the yield::

    def gen2():
        for i in range(50):
            yield i
            res = yield
            print(i, res)




"""

__version__ = '0.0.1'

class YieldBreaker:
    
    def __init__(self, generator):
        self._gen = generator
        self._should = 'send'
        self._exausted = False
        self.send(None)
        
    def __iter__(self):
        return self
        
    def send(self, value):
        if self._should == 'send':
            try:
                self._next = self._gen.send(value)
            except StopIteration:
                self._exausted = True
            self._should = 'yield'
        else:
            raise ValueError('attempt to send before yielding')
        
    def __next__(self):
        if self._should == 'yield':
            if self._exausted:
                raise StopIteration
            self._should = 'send'
            return self._next
        else:
            raise ValueError('attempt to yield next instead of send')
