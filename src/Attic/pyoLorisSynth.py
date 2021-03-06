import loris
from pyo import *
import math
    
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
        #  TypeError: "input" argument must be a PyoObject.
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
            ampNoise = a*math.sqrt( 2. * bw )
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
        
        if False:
            self.ampTone=Osc(table=self.ampToneTab,freq=1.0/dur)
            self.ampNoise=Osc(table=self.ampNoiseTab,freq=1.0/dur)
            self.freq=Osc(table=self.freqTab,freq=1.0/dur)
        else:
            mode=3
            start=dur*.3
            loop_dur=0.0
            xfade=0
            interp=2
            smooth=False
            self.ampTone=Looper(table=self.ampToneTab,start=start,dur=loop_dur,pitch=1.0/dur,xfade=xfade,mode=mode,interp=interp,autosmooth=smooth)
            self.ampNoise=Looper(table=self.ampNoiseTab,start=start,dur=loop_dur,pitch=1.0/dur,xfade=xfade,mode=mode,interp=interp,autosmooth=smooth)
            self.freq=Looper(table=self.freqTab,start=start,dur=loop_dur,pitch=1.0/dur,xfade=xfade,mode=mode,interp=interp,autosmooth=smooth)



        self.white = Noise() 
        
        # low pass filter the noise 
        # loris uses 4 forward and back coeffecients but pyo only has a bi quad.
        # TODO implement general digital filter in pyo
        self.mod=Biquad(self.white, freq=500, q=1, type=interp, mul=self.ampNoise, add=self.ampTone)
                                
        
        self.osc=Sine(freq=self.freq,mul=self.mod,phase=init_phase)
        
        # MIx the oscillator outputs
          # Mix all the partials   (TODO do I really need this ?
        self.mixer=Mixer(outs=2, chnls=1)
        scale=1.0   # /len(feat.freq)
        osc=self.osc

        for key in range(len(osc)):

            self.mixer.addInput(key,osc[key])
            self.mixer.setAmp(key,0,scale)
            self.mixer.setAmp(key,1,scale)

        self.mixer.out()




class LorisSynth:
    """
    A set of OScillators one for each Partial.
    
    """
    
    
    def __init__(self,parts,sr,size,fade=0.001):
        
        self.oscs=[]
        
        for part in parts:
            osc=PartialOsc(part,sr,size,fade)
            self.oscs.append(osc)


    def out(self):
        for osc in self.oscs:
            osc.out()
            
if __name__ == "__main__":            
    parts=loris.importSpc("../samples/clarinet.aiff.spc")
    
    
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
           
           
    s = Server().boot()

    print " t max = ",t
    fade=0.001
    samplerate=44100
    size=int(samplerate*(t+2*fade))
    
    synth=LorisSynth(parts,samplerate,size)
    # synth.out()
    
    s.gui(locals())
        
