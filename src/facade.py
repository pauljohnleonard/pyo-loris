import subprocess,inspect
import atexit,time,Queue,threading

class Facade:
    """
    
    Usage
    
    c=gaclient.Clinet(debug=False,srate=44100.0)
    c.send(" stuff ")
    
    
    """
    
    def __init__(self,debug=False,srate=44100.0,dolog=True):
        self.debug=debug
        self.proc=None
        if  not debug:
            self.proc=subprocess.Popen(["python -i loris_server.py"], shell=True,
                                       stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
#            ,
#                                       stderr=subprocess.STDOUT,
#                                       stdout=subprocess.PIPE)
            
            self.pipe   = self.proc.stdin
            self.stdout = self.proc.stdout
            #print self.proc.pid
        if dolog:
            self.log=open("loris.log","w")
        else:
            self.log =None

     
        self.err_t=threading.Thread(target=self.pipe_reader)
        self.daemon=False
        self.q=Queue.Queue()
        self.err_t.start()
        atexit.register(quit)
        
    def pipe_reader(self):
        while True:
           
            text=self.stdout.readline()
            if len(text) == 0:
                print " end of file "
                return
            #print ":",text
            if self.err_t == None:
                return 
            self.q.put(text)
               

    def send(self,cmd):
        
        if self.debug:
            print cmd
        else:
            if self.log != None:
                self.log.write(cmd+"\n")
                self.log.flush()
            self.pipe.write(cmd+"\n")


           #self.send("build.play()")
         
    def quit(self):
        print "quitting  .... "
        if self.proc == None:
            return
        self.send("model.quit()")
        self.send("time.sleep(0.5)")
        
        self.pipe.close()
        print " waiting for client to die"
        self.proc.wait()
        print " dead"
        self.proc = None
        print " . . . . . quitted "
        
     
 
if __name__ == "__main__":
   
   
    
    c=Facade(debug=False)
    
    c.send("model.analyse(clarinet.aiff)")
    model.analyze(name='clarinet.aiff',drift=30,resolution=270,lobe=120,floor=120)
    model.synth()
    