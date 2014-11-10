
import wx
import random
import loris

import facade,os,sys

            
class MyFrame(wx.Frame):
   
    def __init__(self,parent, title, pos, size=(300, 250)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.make_panels()
        self.Bind(wx.EVT_IDLE,self.monit)
        self.facade=facade.Facade()
        self.def_dir=os.getcwd()
        
    def synth(self,evt):   
        
       self.facade.send("model.synth()") 
       
        
  
    def analyze(self,evt):
        
        
        fd=wx.FileDialog(self, " File name",defaultDir=self.def_dir)
        
        fd.ShowModal()
        name=fd.GetFilenames()[0]   #     "clarinet.aiff"
 
        
        drift=self.drift_ctrl.GetValue()
        resolution=self.resolution_ctrl.GetValue()
        lobe=self.lobe_ctrl.GetValue()
        floor=self.floor_ctrl.GetValue()
    
        self.facade.send("model.analyze(name='"+name+"',drift="+drift+",resolution="+resolution+",lobe="+lobe+",floor="+floor+")")
            
     
   
    def quit(self,evt):
        
        self.facade.quit()
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
      
      
        self.resolution_ctrl,pan=self.add_number(panel,20.0,1000,300,"Resolution")
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
