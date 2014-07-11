#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

http://www.tutorialspoint.com/python/python_multithreading.htm
'''

import threading
import Queue

import time

#import sys
#sys.path +=sys.path + ['..']

#constants
queueLock = threading.Lock()


class Block(threading.Thread):
    def __init__(self, blkid, blkname, blkqueue):
        threading.Thread.__init__(self)
        self.blkid = blkid
        self.blkname = blkname
        self.blkqueue = blkqueue
        self.exitFlag = 0

    def stop(self):
        self.exitFlag = 1

    def run(self):
        print "Starting " + self.blkname
        self.process_data() #self.blkname, self.blkqueue)
        print "Exiting " + self.blkname


    def process_data(self):   #blkname, blkqueue):
        while not self.exitFlag:
            #queueLock.acquire()
            if not self.blkqueue.empty():
                data = self.blkqueue.get()
                #queueLock.release()
                print "%s processing %s" % (self.blkname, data)
            else:
                print "    %s idle" % (self.blkname,)
                #queueLock.release()
            time.sleep(1)
        return


def test():
    blk1 = Block(1, 'Block One', Queue.Queue(10))
    blk1.start()

    blk2 = Block(2, 'Block Two', Queue.Queue(10))
    blk2.start()

    blk1.blkqueue.put('1')
    blk1.blkqueue.put('2')

    blk2.blkqueue.put('A')
    blk2.blkqueue.put('B')

    time.sleep(5)

    blk1.blkqueue.put('3')
    blk2.blkqueue.put('C')

    time.sleep(5)

    blk1.blkqueue.put('4')
    time.sleep(2)    # required not to loose '4' on block 1 if sleeping
    blk1.stop()
    blk2.stop()
    blk1.join()
    blk2.join()
    return






if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        pass
