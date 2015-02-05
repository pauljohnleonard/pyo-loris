import loris, os, time
from pyo import *
import math,numpy
   
CTRLS=False

class PartTable:


    def __init__(self,parts):
        self.parts=parts
        dt=None
        tmax=0.0
        cnt=0
        for part in parts:
            # print "***************************************************"
            it=part.iterator()
            tlast=None

            while not it.atEnd():
                bp=it.next()
                if tlast:
                    dtt=bp.time()-tlast
                    if not dt:
                        dt=dtt
                    else:
                        assert abs(dt- dtt) < 0.00000001

                tlast=bp.time()
                tmax=max(tlast,tmax)

            cnt+=1

        print " There are ",cnt," Partials "

        self.nSeg=int(tmax/dt)+1
        self.nBin=cnt

        self.lookup_freq= numpy.zeros((self.nSeg,self.nBin))
        self.lookup_amp = numpy.zeros((self.nSeg,self.nBin))
        self.lookup_bw  = numpy.zeros((self.nSeg,self.nBin))
        self.dt=dt

        row=0
        for part in parts:
            # print "***************************************************"
            it=part.iterator()
            tlast=None

            while not it.atEnd():
                bp=it.next()
                col=round(bp.time()/dt)
                self.lookup_freq[col][row]=  bp.frequency()
                self.lookup_amp[col][row] =  bp.amplitude()
                self.lookup_bw[col][row]  =  bp.bandwidth()

            row += 1


    def at_index(self,col):
            return self.lookup_freq[col],self.lookup_amp[col],self.lookup_bw[col]

class Synth:
    
    
    def __init__(self,feat):
        
        self.mixer=Mixer(outs=2, chnls=1).out()

        # these are arrays
        self.freqs=SigTo(value=feat.freq,time=.0)
        self.ampsNoise=SigTo(value=feat.noise,time=.0)
        self.ampsTone=SigTo(value=feat.tone,time=.0)
        
        
        if CTRLS:
            self.freqs.ctrl([SLMap(20., 2000., 'log', 'value',feat.freq)])
            self.ampsNoise.ctrl([SLMap(0.,1., 'lin', 'value',feat.noise)])
            self.ampsTone.ctrl([SLMap(0.,1., 'lin', 'value',feat.tone)])
        
        self.parts=PartialOsc(freq=self.freqs,ampTone=self.ampsTone,ampNoise=self.ampsNoise,scale=1.0/len(feat.freq))
       
        
        scale=1.0/len(feat.freq)
        osc=self.parts.osc
        
        for key in range(len(osc)):

            self.mixer.addInput(key,osc[key])
            self.mixer.setAmp(key,0,scale)
            self.mixer.setAmp(key,1,scale)          
       
        self.mixer.out()

       
    def setTarget(self,feat,dtime=None):
        """
        set the target for all the oscillators in terms of noise tone and freq.
        """
        if time != None:
            self.freqs.setTime(dtime)
            self.ampsNoise.setTime(dtime)
            self.ampsTone.setTime(dtime)
            
        self.freqs.setValue(feat.freq)
        self.ampsNoise.setValue(feat.noise)
        self.ampsTone.setValue(feat.tone)
        

class Feature:

    def __init__(self,n):
        self.freq=[0]*n
        self.noise=[0]*n
        self.tone=[0]*n


    def set(self,freq,amp,bw):
        self.freq[:]=freq
        self.tone[:] = amp*numpy.sqrt( 1. - bw )
        self.noise[:] = amp*numpy.sqrt( 2. * bw )

        
class FeatureX:
    
    def __init__(self,fund):
        self.freq=[]
        self.noise=[]
        self.tone=[]
        
        self.freq=Feature.factory.harmonics(fund)
        
        for i in range(Feature.factory.n):
            self.noise.append(0.0)
            self.tone.append(1.0)

        
class FactoryX:
    
    def __init__(self,n):
        self.n=n
        
    def harmonics(self,fund):
        freqs=[]
        for i in range(self.n):
            freqs.append((i+1)*fund)
            
        return freqs
    
    def random_values(self,min=0,max=1.0):
        vals=[]
        for i in range(self.n):
            fact1=random.random()
            fact2=1.0-fact1
            
            vals.append(max*fact1+min*fact2)
            
        return vals
        
        
class PartialOsc:

    """
    Oscillator for a single Partial
    
    part is a loris Partial list.
    
    output(t)=(ampTone+ampNoise*LPF(whiteNoise)))*sin(freq*2*pi*t+phase)
 
    """

    def __init__(self,freq,ampTone,ampNoise,scale):
            
        init_phase=0
        
           
        self.white = Noise()
        
        # low pass filter the noise 
        # loris uses 4 forward and back coeffecients but pyo only has a bi quad.
        # TODO implement general digital filter in pyo
        self.mod=Biquad(self.white, freq=500, q=1, type=0, mul=ampNoise, add=ampTone)
                                
        
        self.osc=Sine(freq=freq,mul=self.mod,phase=init_phase)
        
     
    def out(self):
        self.osc.out()
    


class Player:

    def __init__(self,parts):
        self.table=PartTable(parts)
        self.feat=Feature(len(parts))
        self.synth=Synth(self.feat)
        self.time=0
        self.cnt=0

    def doit(self):
        f,amp,bw=self.table.at_index(self.cnt)
        self.feat.set(f,amp,bw)
        self.synth.setTarget(self.feat,self.table.dt)
        self.cnt=(self.cnt+1)%self.table.nSeg




if __name__ == "__main__":
    s = Server().boot()

    spc_file="samples/clarinet.spc"
    parts=loris.importSpc(spc_file)

    player=Player(parts)

    seq=Pattern(player.doit,player.table.dt)

    seq.play()
    n = len(parts)

    s.gui('locals()')

