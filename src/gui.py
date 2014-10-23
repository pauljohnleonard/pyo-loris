
import wx
import random
import loris
from  pyoLorisSynth import *

class Thing:
    
    def __init__(self,name,size,sr,parts):
        self.size=size
        self.sr=44100
        self.name=name
        self.parts=parts
            
class MyFrame(wx.Frame):
   
    def __init__(self,parent, title, pos, size=(300, 250)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.make_panels()
        self.Bind(wx.EVT_IDLE,self.monit)
        self.thing=None
                   
        self.server = Server().boot().start()


    def analyze(self,evt):
        
        
        name="clarinet.aiff"
        file=loris.AiffFile(name)
        samps  = file.samples()
        samplerate=file.sampleRate()
     


        df=float(self.drift_ctrl.GetValue())
        reso=float(self.freq_ctrl.GetValue())
        lobe=float(self.lobe_ctrl.GetValue())
        floor=float(self.floor_ctrl.GetValue())
        
        print "analyse",reso,df,lobe
      
        anal=loris.Analyzer(270)    #  reso,lobe)       # reconfigure Analyzer
        anal.setFreqDrift(30)       #  df )
     
        samplerate=44100
        parts = anal.analyze( samps, samplerate )
            
        
        # loris.channelize( flut, loris.createFreqReference( flut, 291*.8, 291*1.2, 50 ), 1 )
        
        refenv = anal.fundamentalEnv()
        loris.channelize( parts, refenv, 1 )
        loris.distill( parts )
        
        
        self.thing=Thing(name,len(samps),samplerate,parts)

     
     
    def synth(self,evt):   
        
        if self.thing == None:
            return
        thing=self.thing
        
        # self.server.stop()
        synth=LorisSynth(thing.parts,thing.sr,thing.size)
        synth.out()
 
         
        time.sleep(500)
        
        print "SYNTH" 
    
    def quit(self,evt):
        
        print "Quit"
        sys.exit(0)
        
    def monit(self,evt):
        
        pass
    
    def make_panels(self):
        
        
        spin=self.make_spin_panel(self)
        
        but=self.make_button_panel(self)
        self.cmdbox = wx.TextCtrl (self, -1, style=wx.TE_PROCESS_ENTER )
        self.console = wx.TextCtrl(self, -1, " server console ", style=wx.TE_MULTILINE)
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        box.Add(spin, 2, wx.EXPAND)
        box.Add(but, 1, wx.EXPAND)
        box.Add(self.cmdbox,0,wx.EXPAND)
        box.Add(self.console,4,wx.EXPAND)
        
        self.cmdbox.Bind(wx.EVT_TEXT_ENTER,self.cmd_func)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
    def cmd_func(self):
        pass
        
    def add_spinner(self,parent,minV,maxV,val,tit):
        
        panel=wx.Panel(parent,-1,style=wx.SUNKEN_BORDER)
     
        
        box = wx.BoxSizer(wx.VERTICAL)
      
        tit=wx.StaticText(panel, -1, tit)
      
        ctrl=wx.SpinCtrl(panel, -1, '')
        ctrl.SetRange(minV, maxV)
        ctrl.SetValue(val)
        
        box.Add(tit)
        box.Add(ctrl)
        
        panel.SetSizer(box)
        
        
        return ctrl,panel
    
    def add_number(self,parent,minV,maxV,val,tit):
        
        panel=wx.Panel(parent,-1,style=wx.SUNKEN_BORDER)
        
        box = wx.BoxSizer(wx.VERTICAL)
      
        tit=wx.StaticText(panel, -1, tit)
      
        ctrl=wx.TextCtrl(panel,-1, 'xxxx')
        ctrl.SetValue(str(val))
        
        box.Add(tit)
        box.Add(ctrl)
        
        panel.SetSizer(box)
        
        return ctrl,panel
        
        
        
    def  make_spin_panel(self,parent):
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER)
        
        sizer=wx.BoxSizer(wx.HORIZONTAL)
      
      
        self.freq_ctrl,pan=self.add_number(panel,20.0,1000,300,"Resolution")
        sizer.Add(pan)
   
        self.drift_ctrl,pan=self.add_number(panel,20.0,1000,30,"Drift")
        sizer.Add(pan)
 
        self.lobe_ctrl,pan=self.add_number(panel,20.0,1000,120,"Lobe")
        sizer.Add(pan)
 
        self.floor_ctrl,pan=self.add_number(panel,20.0,1000,120,"Floor")
        sizer.Add(pan)
 

        panel.SetSizer(sizer)
        
        return panel
           
    def  make_button_panel(self,parent):
        
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER)
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        
        analyze=wx.Button(panel, 1, 'Analyze')    
        box.Add(analyze,1,wx.EXPAND)
        
        synth=wx.Button(panel, 1, 'Synth')    
        box.Add(synth,1,wx.EXPAND)
 
        
        quit=wx.Button(panel, 1, 'Quit')    
        box.Add(quit,1,wx.EXPAND)
        
        
        analyze.Bind(wx.EVT_BUTTON, self.analyze)
        quit.Bind(wx.EVT_BUTTON, self.quit)
        synth.Bind(wx.EVT_BUTTON,self.synth)
        
        
        
#         kill.Bind(wx.EVT_BUTTON, self.kill_pheno)
#         
#         creat.Bind(wx.EVT_BUTTON, self.create_pheno)   
#         edit.Bind(wx.EVT_BUTTON, self.edit_pheno)     
#         breed.Bind(wx.EVT_BUTTON,self.breed_pheno)
#         save.Bind(wx.EVT_BUTTON,self.save_pheno)
#         load.Bind(wx.EVT_BUTTON,self.load_pheno)
#                          
        #panel.SetAutoLayout(True)

        panel.SetSizer(box)
        #panel.Layout()
        return panel
        
        
 
  
if __name__ == "__main__":
    
    
  
      
    #random.seed(0)
    print random.getstate()

     
    app =  wx.App(False)     #  wx.PySimpleApp()
    mainFrame = MyFrame(None, title='PYO-GA', pos=(50,50), size=(800,300))
    mainFrame.Show()
    app.MainLoop()
