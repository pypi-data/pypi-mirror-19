from collections import deque,defaultdict
from functools   import partial
import time
import pythymio


class EventQueue:
    def __init__(self):
        self.d = defaultdict( partial(deque,maxlen=1) )

    def _parse_sleep_request(self,s):
        """ if str = "sleep 1.5", it returns 1.5
            if not a sleep request, returns False
        """
        try:
            s1,s2 = s.split(' ')
            assert s1 == 'sleep'
            return float(s2)
        except:
            return False
    
    
    def push(self,name,arg):
        """ push event on eventqueue
        """
        # traitement sur le format des arguments
        arg = list(map(float,arg))
        if name == "fwd.button.center" and arg == []:
            arg = True
        self.d[name].append( arg )


    def isEmpty(self,name):
        """ returns True if eventqueue named "name" is empty
        """
        return len(self.d[name])==0


    def pop(self,name):
        return self.d[name].popleft()


    def queueLoop(self,user_fun):
        userAgent        = user_fun()
        answerSentToUser = None  # initially, nothing sent to user
        try:
            while True:
                # send answer to previous request and get new request
                userRequest = userAgent.send( answerSentToUser )

                # is it a sleep request of the form sleep x ?
                sleepReq = self._parse_sleep_request(userRequest)    

                if sleepReq:
                    t0 = time.time()
                    while time.time() < t0+sleepReq:
                        # ask thymio for event, and push in queue
                        n,a = yield
                        n=n.replace('fwd.','')
                        self.push(n,a)
                    answerSentToUser = None
                else:
                    # while no event in queue matches the user's request, or while the sleep request has not ended           
                    while self.isEmpty(userRequest):
                        # ask thymio for event, and push in queue
                        n,a = yield
                        n=n.replace('fwd.','')
                        self.push(n,a)

                    # send the requested event to user and get next request
                    answerSentToUser = self.pop(userRequest)


        except StopIteration:
            pass





def runThymioControl(userFun,eventlist=None):
    eq = EventQueue()

    if eventlist is None:
        eventlist = ["prox","buttons"]

    with pythymio.thymio(eventlist,[]) as Thym:

        runThymioControl.Thym=Thym
        queueLoopGenerator = eq.queueLoop(userFun)
        queueLoopGenerator.next()

        def dispatch(evtid, evt_name, evt_args):
            try:
                queueLoopGenerator.send((evt_name,evt_args))
            except StopIteration:
                Thym.stop()

        Thym.loop(dispatch)


#### Moteurs ####

def av(l=500,r=500):
    runThymioControl.Thym.set('motor.left.target', [l])
    runThymioControl.Thym.set('motor.right.target', [r])

def td():
    av(500,-500)
    
def tg():
    av(-500,500)

def arrete():
    av(0,0)
    

