# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:22:47 2014

@author: belza
"""

import threading,Queue,time
import sys
sys.path +=sys.path + ['..']

class Port_in(threading.Thread):
    def __init__(self,lock,function):
 
        threading.Thread.__init__(self)
        self.connector = None
        self.lock = lock
        self.function = function
        self.finished = False
    def run(self):
        while not self.finished :
            ev=self.connector.get()
            print "llegó evento ", ev
            self.lock.acquire()
            self.function(ev)
            self.lock.release()
    def connect(self,connector):
            self.connector = connector
            
    def stop(self):
        self.finished = True
        self._Thread__stop()

    

class BlockPrueba(threading.Thread):
   
    def __init__(self, number_in=0,number_out=0):
          
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.ports_in=[]
        self.ports_in.append(Port_in(self.lock,self.process))
        self.ports_in.append(Port_in(self.lock,self.process))
        self.ports_out =None
        self.finished = False
    def run(self):
         self.ports_in[0].start()
         self.ports_in[1].start()
         self.ports_in[0].join()
         self.ports_in[1].join()
         
    def connect(self,index, connector):
        self.ports_in[index].connect(connector)    

    def process(self,ev):
        print "enter, ",ev
        time.sleep(5)
        print "out,  ",ev
        
    
    def stop(self):
            self.finished = True
            self.ports_in[0].stop()
            self.ports_in[1].stop()
            self._Thread__stop()


def test():
    '''A test function.
    '''
    myQueue1=Queue.Queue(10)
    myQueue2 = Queue.Queue(10)
    block = BlockPrueba()
    block.connect(0,myQueue1)
    block.connect(1,myQueue2)
    block.start()
    myQueue1.put(1)
    myQueue2.put(2)
    
    time.sleep(20)
    block.stop()
    
if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
