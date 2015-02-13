__author__ = 'eespjl'

import atexit

import pyo
import loris

import synth




class Model:

    def __init__(self):
        self.server = pyo.Server().boot()
        atexit.register(self.quit)
        self.channels=[None]
        self.a=pyo.Sig(0.0)
        self.index=pyo.SigTo(self.a,time=.1)

        # only works if server.gui() is called
        self.a.ctrl()


    def synth_channel(self):

        if not self.chan:
            return


    def add_channel(self,name,resolution=270,drift=30,lobe=270,floor=80):


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



        chan=synth.Channel(self.index,parts)
        chan.table=table
        self.channels[0]=chan
        self.server.stop()

        self.synth = synth.Synth(chan.freqs, chan.tones, chan.noises)

        self.server.start()



    def set_pos(self,x):
        """
        x  is 0 - 1
        :param x:
        :return:
        """

        print "set pos" , x
        self.a.setValue(x)


    def quit(self):
        self.server.stop()



if __name__ == "__main__":
    model=Model()


    model.add_channel(name='samples/clarinet.aiff',drift=30,resolution=270)    # ,lobe=120,floor=80)
    model.synth()


    model.server.gui(locals())