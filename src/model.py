__author__ = 'eespjl'

import atexit

import pyo
import loris

import synth


class Thing:

    def __init__(self,name,size,sr,parts):
        self.size=size
        self.sr=sr
        self.name=name
        self.parts=parts


class Model:

    def __init__(self):
        self.thing=None
        self.server = pyo.Server().boot()
        atexit.register(self.quit)
        self.chan=None
        self.a=pyo.Sig(0.0)
        self.index=pyo.SigTo(self.a,time=2.0)
        self.a.ctrl()



    def synth(self):

        if not self.chan:
            return

        self.server.stop()


        self.synth = synth.Synth(self.chan.freqs, self.chan.tones, self.chan.noises)

        self.server.start()

    def analyze(self,name,resolution=270,drift=30,lobe=270,floor=80):


        #         name="clarinet.aiff"


        if True:
            file=loris.AiffFile(name)

            samps  = file.samples()
            samplerate=file.sampleRate()

            table=pyo.SndTable(name)
            table.normalize()

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



        self.chan=synth.Channel(self.index,parts)
        self.chan.table=table


    def set_pos(self,mpos):
        pass

    def quit(self):
        self.server.stop()



if __name__ == "__main__":
    model=Model()


    model.analyze(name='samples/clarinet.aiff',drift=30,resolution=270)    # ,lobe=120,floor=80)
    model.synth()


    model.server.gui(locals())