import loris, os, time
from pyo import *
import math, numpy


class Synth:
    """
    LOris synthesizer that can be controlled in real time.

    synt.setTarget(feature,time)

    """

    def __init__(self, freqs, ampTone, ampNoise):
        # Mix all the partials   (TODO do I really need this ?)   Hmm yes if you want stereo ?
        self.mixer = Mixer(outs=2, chnls=1).out()


        # Creat an array of oscillators (one per partial)
        self.parts = PartialOsc(freq=freqs, ampTone=ampTone, ampNoise=ampNoise)

        osc = self.parts.osc

        for key in range(len(osc)):
            self.mixer.addInput(key, osc[key])
            self.mixer.setAmp(key, 0, 1.0)
            self.mixer.setAmp(key, 1, 1.0)

        self.mixer.out()


class PartialOsc:
    """
    Oscillator for a single Partial
    
    part is a loris Partial list.
    
    output(t)=(ampTone+ampNoise*LPF(whiteNoise)))*sin(freq*2*pi*t+phase)
 
    """

    def __init__(self, freq, ampTone, ampNoise):
        init_phase = 0

        self.white = Noise()

        # low pass filter the noise 
        # loris uses 4 forward and back coeffecients but pyo only has a bi quad.
        # TODO implement general digital filter in pyo
        self.mod = Biquad(self.white, freq=500, q=1, type=0, mul=ampNoise, add=ampTone)

        self.osc = Sine(freq=freq, mul=self.mod, phase=init_phase)


    def out(self):
        self.osc.out()


class Channel:
    def __init__(self, parts):


        self.noises = []
        self.tones = []
        self.freqs = []

        for part in parts:
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

            if True:
                ampTone = Osc(table=ampToneTab, freq=1.0 / dur)
                ampNoise = Osc(table=ampNoiseTab, freq=1.0 / dur)
                freq = Osc(table=freqTab, freq=1.0 / dur)
            else:
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
            self.freqs.append(freq)
            self.tones.append(ampTone)
            self.noises.append(ampNoise)


if __name__ == "__main__":
    s = Server().boot()

    spc_clar = "spc/clarinet.spc"
    parts_clar = loris.importSpc(spc_clar)
    chan_clar = Channel(parts_clar)

    spc_flute = "spc/flute.spc"
    parts_flute = loris.importSpc(spc_flute)
    chan_flute = Channel(parts_flute)

    N_CHAN_C = len(parts_clar)  # ,len(parts_flute))
    N_CHAN_F = len(parts_flute)  # ,len(parts_flute))
    N_SYNTH = max(N_CHAN_C, N_CHAN_F)


    if True:
        freqs = [None for _ in range(N_SYNTH)]
        tones = [None for _ in range(N_SYNTH)]
        noises = [None for _ in range(N_SYNTH)]

        fact_c=Sig(1.0)
        fact_f=1.0-fact_c
        fact_c.ctrl()

        for i in range(N_SYNTH):
            if i < N_CHAN_C:
                freqs[i] = chan_clar.freqs[i]*fact_c
                tones[i] = chan_clar.tones[i]*fact_c
                noises[i] = chan_clar.noises[i]*fact_c

                if i < N_CHAN_F:
                    freqs[i] += chan_flute.freqs[i]*fact_f
                    tones[i] += chan_flute.tones[i]*fact_f
                    noises[i] += chan_flute.noises[i]*fact_f

            else:
                if i < N_CHAN_F:
                    freqs[i] = chan_flute.freqs[i]*fact_f
                    tones[i] = chan_flute.tones[i]*fact_f
                    noises[i] = chan_flute.noises[i]*fact_f


    else:
        freqs = chan_flute.freqs
        tones = chan_flute.tones
        noises = chan_flute.noises

    synth = Synth(freqs, tones, noises)

    s.gui('locals()')

