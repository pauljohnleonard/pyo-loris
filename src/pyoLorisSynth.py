import loris, os, time
from pyo import *
import math

s = Server().boot()
    
class PartialOsc:
    
    """
    Oscillator for a single Partial
    
    part is a loris Partial list.
    
    output(t)=(ampTone+ampNoise*LPF(whiteNoise)))*sin(freq*2*pi*t+phase)
 
    """
    
    def __init__(self,part,sr,size,fade):
            
        init_phase=part.initialPhase()
        
        # pyo wants phase as a number between 0 - 1
        init_phase=init_phase/math.pi/2.0
        
        if init_phase < 0.0:
            init_phase+=1.0
            
        assert init_phase >= 0.0 and init_phase < 1.0
            
    
        # make 3 envelopes to control the 
        #   amplitude of the tone
        #     "       of the noise
        #    frequency of the oscillator
        #  We add points before and after the end of the list because the list does not contain zeros at these points
        #  
        ampNoiseList=[(0,0)]
        ampToneList=[(0,0)]
        freqList=[(0,0)]
        
        cnt=0

        for bp in part:
            t_sec=bp.time()
        
            f=bp.frequency()    
            a=bp.amplitude()
            bw=bp.bandwidth()
        
            if cnt == 0:
                if t_sec > fade:
                    t=int((t_sec-fade)*sr)
                else:
                    t=1
                          
                ampToneList.append((t,0))
                ampNoiseList.append((t,0))
                freqList.append((t,f))
        
            t=int(t_sec *sr)
            ampTone = a*math.sqrt( 1. - bw )
            ampNoise = a*math.sqrt( 2. * bw ) ;  
            ampToneList.append((t,ampTone))
            ampNoiseList.append((t,ampNoise))   
            freqList.append((t,f))
            cnt=cnt+1
        
        
        t=int((t_sec+fade)*sr)
                          
        ampToneList.append((t,0))
        ampNoiseList.append((t,0))
        freqList.append((t,f))
        
        if t >=size :
            print t , size
        
        dur=float(size)/sr

        ampNoiseList.append((size-1,0))
        ampToneList.append((size-1,0))
        freqList.append((size-1,f))

        
        self.ampToneTab=LinTable(ampToneList,size)
        self.ampNoiseTab=LinTable(ampNoiseList,size)
        self.freqTab=LinTable(freqList,size)
        
        
        self.ampTone=Osc(table=self.ampToneTab,freq=1.0/dur)
        self.ampNoise=Osc(table=self.ampNoiseTab,freq=1.0/dur)
        self.freq=Osc(table=self.freqTab,freq=1.0/dur)
        
        self.white = Noise() 
        
        # low pass filter the noise 
        # loris uses 4 forward and back coeffecients but pyo only has a bi quad.
        # TODO implement general digital filter in pyo
        self.mod=Biquad(self.white, freq=500, q=1, type=0, mul=self.ampNoise, add=self.ampTone)
                                
        
        self.osc=Sine(freq=self.freq,mul=self.mod,phase=init_phase)
        
        
    def out(self):
        self.osc.out()



class LorisSynth:
    """
    A set of OScillators one for each Partial.
    
    """
    
    
    def __init__(self,parts,sr,size,fade):
        
        self.oscs=[]
        
        for part in parts:
            osc=PartialOsc(part,sr,size,fade)
            self.oscs.append(osc)


    def out(self):
        for osc in self.oscs:
            osc.out()
            
            
parts=loris.importSpc("clarinet.spc")


if True:
    cnt=0
    for part in parts:
        #print "*****************************************"
        #it=part.iterator()
        #while not it.atEnd():
        #    bp=it.next()
        #    print "t:",bp.time(), " a:",bp.amplitude()," bw:",bp.bandwidth()," f:",bp.frequency()," p:",bp.phase()
        cnt+=1
    print " There are ",cnt," Partials "
    
t=0
for part in parts:
   for bp in part:
       t=max(t,bp.time()) 
       
       

print " t max = ",t
fade=0.001
samplerate=44100
size=int(samplerate*(t+2*fade))

synth=LorisSynth(parts,samplerate,size,fade)
synth.out()

s.gui(locals())
        
