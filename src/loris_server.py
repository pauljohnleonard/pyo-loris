from model import *



model=Model()
model.server.start()
if True:
     model.analyze(name='clarinet.aiff',drift=30,resolution=270)    # ,lobe=120,floor=80)
     model.synth()



time.sleep(20)
#gui(locals())
