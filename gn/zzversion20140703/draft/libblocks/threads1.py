import threading
MY_LOCK = threading.Lock()
TOTAL = 0

class CountThread(threading.Thread):
    def run(self):
        global TOTAL
        for i in range(100000):
            MY_LOCK.acquire()
            TOTAL = TOTAL + 1
            MY_LOCK.release()
        print('%s\n' % (TOTAL))

        
a = CountThread()
b = CountThread()
a.start()
b.start()
