__author__ = 'eespjl'

import atexit

from  pyoLorisSynth import *
import pyo


class Thing:

    def __init__(self,name,size,sr,parts):
        self.size=size
        self.sr=sr
        self.name=name
        self.parts=parts


class Model:

    def __init__(self):
        self.thing=None

        self.server = Server().boot()
        atexit.register(self.quit)


    def synth(self):

        self.server.stop()

        if self.thing == None:
            return
        thing=self.thing

        self.synth=LorisSynth(thing.parts,thing.sr,thing.size)
        self.synth.out()
        self.server.start()

    def analyze(self,name,resolution=270,drift=30,lobe=270,floor=80):


#         name="clarinet.aiff"


        if True:
            file=loris.AiffFile(name)

            samps  = file.samples()
            samplerate=file.sampleRate()

            self.table=pyo.SndTable(name)
            self.table.normalize()

            print "analyse",resolution,drift,lobe

            anal=loris.Analyzer(resolution)    #  reso,lobe)       # reconfigure Analyzer
            anal.setFreqDrift(drift)       #  df )


            parts = anal.analyze( samps, samplerate )


            # loris.channelize( flut, loris.createFreqReference( flut, 291*.8, 291*1.2, 50 ), 1 )

            refenv = anal.fundamentalEnv()
            loris.channelize( parts, refenv, 1 )
            loris.distill( parts )

            loris.exportSpc(name+".spc",parts,60)
        else:
            parts=loris.importSpc(name+".spc")

        t=0
        for part in parts:
            for bp in part:
                t=max(t,bp.time())

        fade=0.001
        samplerate=44100
        size=int(samplerate*(t+2*fade))
        self.thing=Thing(name,size,samplerate,parts)

    def quit(self):
        self.server.stop()




if __name__ == "__main__":
    model=Model()


    model.analyze(name='clarinet.aiff',drift=30,resolution=270)    # ,lobe=120,floor=80)
    model.synth()


    model.server.gui(locals())