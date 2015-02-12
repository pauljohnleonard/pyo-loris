import loris, os, time
from pyo import *
import math, numpy


class Synth:
    """
    LOris synthesizer that can be controlled in real time.

    """

    def __init__(self, freqs, ampTone, ampNoise):
        # Mix all the partials   (TODO do I really need this ?)   Hmm yes if you want stereo ?
        self.mixer = Mixer(outs=2, chnls=1).out()


        # Creat an array of oscillators (one per partial)

        # self.parts = PartialOsc(freq=freqs, ampTone=ampTone, ampNoise=ampNoise)

        init_phase = 0

        self.white = Noise()

        # low pass filter the noise
        # loris uses 4 forward and back coeffecients but pyo only has a bi quad.
        # TODO implement general digital filter in pyo

        self.mod = Biquad(self.white, freq=500, q=1, type=0, mul=ampNoise, add=ampTone)

        self.osc = Sine(freq=freqs, mul=self.mod, phase=init_phase)



        for key in range(len(self.osc)):
            self.mixer.addInput(key, self.osc[key])
            self.mixer.setAmp(key, 0, 1.0)
            self.mixer.setAmp(key, 1, 1.0)

        self.mixer.out()




class Channel:
    def __init__(self, index,parts):


        self.parts=parts
        self.noises = []
        self.tones = []
        self.freqs = []



        for i,part in enumerate(self.parts):
            print i,part.label()

            ampNoiseList = [(0, 0)]
            ampToneList = [(0, 0)]
            freqList = [(0, 0)]
            fade = 0.001
            sr = 44100

            cnt = 0


            for bp in part:
                t_sec = bp.time()
                f = bp.frequency()
                a = bp.amplitude()
                bw = bp.bandwidth()

                if cnt == 0:
                    if t_sec > fade:
                        t = int((t_sec - fade) * sr)
                    else:
                        t = 1

                    ampToneList.append((t, 0))
                    ampNoiseList.append((t, 0))
                    freqList.append((t, f))

                t = int(t_sec * sr)
                ampTone = a * math.sqrt(1. - bw)
                ampNoise = a * math.sqrt(2. * bw);

                ampToneList.append((t, ampTone))
                ampNoiseList.append((t, ampNoise))
                freqList.append((t, f))

                cnt = cnt + 1


            # terminate the modulation lists
            t = int((t_sec + fade) * sr)

            size = int((t_sec + 2 * fade) * sr)
            ampToneList.append((t, 0))
            ampNoiseList.append((t, 0))
            freqList.append((t, f))

            # print t , size

            dur = float(size) / sr

            ampNoiseList.append((size - 1, 0))
            ampToneList.append((size - 1, 0))
            freqList.append((size - 1, f))

            ampToneTab = LinTable(ampToneList, size)
            ampNoiseTab = LinTable(ampNoiseList, size)
            freqTab = LinTable(freqList, size)

            c = 2
            if c == 0:
                ampTone = Osc(table=ampToneTab, freq=1.0 / dur)
                ampNoise = Osc(table=ampNoiseTab, freq=1.0 / dur)
                freq = Osc(table=freqTab, freq=1.0 / dur)
            elif c == 1:
                mode = 3
                start = dur * .3
                loop_dur = 0.0
                xfade = 0
                interp = 2
                smooth = False
                ampTone = Looper(table=ampToneTab, start=start, dur=loop_dur, pitch=1.0 / dur, xfade=xfade,
                                 mode=mode, interp=interp, autosmooth=smooth)
                ampNoise = Looper(table=ampNoiseTab, start=start, dur=loop_dur, pitch=1.0 / dur, xfade=xfade,
                                  mode=mode, interp=interp, autosmooth=smooth)
                freq = Looper(table=freqTab, start=start, dur=loop_dur, pitch=1.0 / dur, xfade=xfade, mode=mode,
                              interp=interp, autosmooth=smooth)
            else:
                smooth=False
                ampTone = Pointer2(table=ampToneTab,index=index, interp=2, autosmooth=smooth)
                ampNoise = Pointer2(table=ampNoiseTab,index=index,interp=2, autosmooth=smooth)
                freq = Pointer2(table=freqTab,index=index,interp=2, autosmooth=smooth)



            self.freqs.append(freq)
            self.tones.append(ampTone)
            self.noises.append(ampNoise)



def setmix(chanA,chanB,fact):

    N_CHAN_A = len(chanA.parts)  # ,len(parts_flute))
    N_CHAN_B = len(chanB.parts)  # ,len(parts_flute))
    N_SYNTH = max(N_CHAN_A, N_CHAN_B)

    freqs = [None for _ in range(N_SYNTH)]
    tones = [None for _ in range(N_SYNTH)]
    noises = [None for _ in range(N_SYNTH)]

    fact_A=fact
    fact_B=1.0-fact

    for i in range(N_SYNTH):
        if i < N_CHAN_A:

            if i < N_CHAN_B:
                freqs[i] = chanA.freqs[i]*fact_A+chanB.freqs[i]*fact_B
                tones[i] = chanA.tones[i]*fact_A+chanB.tones[i]*fact_B
                noises[i] = chanA.noises[i]*fact_A+chanB.noises[i]*fact_B
            else:
                freqs[i] = chanA.freqs[i]
                tones[i] = chanA.tones[i]*fact_A
                noises[i] = chanA.noises[i]*fact_A


        else:
            if i < N_CHAN_B:
                freqs[i] = chanB.freqs[i]
                tones[i] = chanB.tones[i]*fact_B
                noises[i] = chanB.noises[i]*fact_B

    return freqs,tones,noises

if __name__ == "__main__":


    s = Server().boot()
    a=Sig(0.0)
    index=SigTo(a,time=2.0)
    a.ctrl()


    spc_file="samples/clarinetM.spc"
    if not  os.path.isfile(spc_file):
            print spc_file, " Does not exist"
            sys.exit(0)


    parts= loris.importSpc(spc_file)

    chan_clar = Channel( index,parts)

    spc_file = "samples/fluteM.spc"
    if not  os.path.isfile(spc_file):
            print spc_file, " Does not exist"
            sys.exit(0)


    parts= loris.importSpc(spc_file)

    chan_flute = Channel( index,parts)


    fact=Sig(0.0)

    fact.ctrl()
    freqs,tones,noises=setmix(chan_clar,chan_flute,fact)
    synth = Synth(freqs, tones, noises)

    s.gui('locals()')

