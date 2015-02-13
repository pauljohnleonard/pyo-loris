
import wx
import model
from pyolib._wxwidgets import ControlSlider, VuMeter, BACKGROUND_COLOUR,SndViewTable,SndViewTablePanel
from pyolib._widgets import wxShowWindow

import os,sys




class WaveDisplay(wx.Panel):

    """
    Decided to use the pyo table view  so this is on the back burner
    """


    def __init__(self,parent):
        wx.Panel.__init__(self, parent, -1, (0,0), (400,100))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.sndBitmap=None
        self.backgroundcolor="#3F3F44"
        self.outlinecolor = "#FFFFBF"
        self.Bind(wx.EVT_MOUSE_EVENTS,self.onMouse)
        self.Bind(wx.EVT_SIZE,self.resize)
        self.channel=None

    def resize(self,evt):
        print "resize"
        self.create_bitmap()

    def onMouse(self,evt):
        if evt.LeftIsDown():
            x,y=evt.GetPosition()
            size = self.GetSizeTuple()
            xx=float(x)/size[0]
            yy=float(y)/size[1]



    def set_channel(self,channel):
        self.channel=channel
        self.create_bitmap()

    def create_bitmap(self):
        if not self.channel:
            return

        size = self.GetSizeTuple()
        self.sndBitmap = wx.EmptyBitmap(size[0], size[1])
        self.memory = wx.MemoryDC()
        self.memory.SelectObject(self.sndBitmap)
        gc = wx.GraphicsContext_Create(self.memory)
        gc.SetPen(wx.Pen("#00FF00"))
        gc.SetBrush(wx.Brush("#FF0000", style=wx.TRANSPARENT))
        self.memory.SetBrush(wx.Brush(self.backgroundcolor))
        self.memory.DrawRectangle(0,0,size[0],size[1])

        list=self.channel.table.getViewTable(self.GetSizeTuple())

        for samples in list:
                if len(samples):
                    gc.DrawLines(samples)

        self.memory.SelectObject(wx.NullBitmap)
        self.needBitmap = True
        self.Refresh()


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext_Create(dc)
        dc.BeginDrawing()
        self.draw(dc)
        dc.EndDrawing()


    def draw(self, dc):
        gc = wx.GraphicsContext_Create(dc)
        dc.BeginDrawing()
        # dc.SetTextForeground("#000000")
        # dc.SetFont(self.font)
        if not self.sndBitmap:
            w,h = self.GetSizeTuple()
            dc.SetBrush(wx.Brush(self.backgroundcolor, wx.SOLID))
            dc.Clear()
            dc.SetPen(wx.Pen(self.outlinecolor, width=1, style=wx.SOLID))
            dc.DrawRectangle(0, 0, w, h)
        else:
            dc.DrawBitmap(self.sndBitmap,0,0)


        dc.EndDrawing()

            
class MyFrame(wx.Frame):
   
    def __init__(self,parent, title, pos, size=(600, 600)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.make_panels()
        self.Bind(wx.EVT_IDLE,self.monit)
       # self.facade=facade.Facade()
        self.def_dir=os.getcwd()+"/samples"
        self.model=model.Model()
        self.model.server._server.setAmpCallable(self.vu_meter)

        self.Layout()

    def synth(self,evt):
       self.model.synth()
       
        
  
    def analyze(self,evt):
        
        
        # fd=wx.FileDialog(self, " File name",defaultDir=self.def_dir)
        #
        # fd.ShowModal()
        # name=fd.GetFilenames()[0]
        # self.def_dir=fd.GetDirectory()

        
        drift=float(self.drift_ctrl.GetValue())
        resolution=float(self.resolution_ctrl.GetValue())
        lobe=float(self.lobe_ctrl.GetValue())
        floor=float(self.floor_ctrl.GetValue())

        # fname=str(self.def_dir+"/"+name)
        # print fname
        fname = "samples/clarinet.aiff"
        self.model.add_channel(name=fname,drift=drift,resolution=resolution,lobe=lobe,floor=floor)

        self.wave.set_channel(self.model.channels[0])



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


        self.wave=WaveDisplay(self)

        box = wx.BoxSizer(wx.VERTICAL)


        box.Add(spin,0,flag=wx.EXPAND|wx.ALL)
        box.Add(but, 0, flag=wx.EXPAND|wx.ALL)
        box.Add(self.cmdbox,0,flag=wx.EXPAND|wx.ALL)
        box.Add(self.console,0,flag=wx.EXPAND|wx.ALL)
        box.Add(self.wave,2,flag=wx.EXPAND|wx.ALL)

        
        self.cmdbox.Bind(wx.EVT_TEXT_ENTER,self.cmd_func)
        
        #self.SetAutoLayout(True)
        self.SetSizer(box)

        self.widgets_box=box

#        self.Layout()
        
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

        #box.SetItemMinSize((150,250))

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
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER,size=(0,50))
        
        sizer=wx.BoxSizer(wx.HORIZONTAL)

      
        self.resolution_ctrl,pan=self.add_number(panel,20.0,1000,300,"Resolution")
        sizer.Add(pan)
   
        self.drift_ctrl,pan=self.add_number(panel,20.0,1000,30,"Drift")
        sizer.Add(pan)
 
        self.lobe_ctrl,pan=self.add_number(panel,20.0,1000,120,"Lobe")
        sizer.Add(pan)
 
        self.floor_ctrl,pan=self.add_number(panel,20.0,1000,120,"Floor")
        sizer.Add(pan)


        sizer2=wx.BoxSizer(wx.VERTICAL)
        #sizer2.AddSpacer((1,30),wx.EXPAND)
        self.vu_meter=VuMeter(panel, size=(50,10))
        self.vu_meter.setNumSliders(2)

        sizer2.Add(self.vu_meter)
        #sizer2.AddSpacer((1,30),wx.EXPAND)

        sizer.Add(sizer2)

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
    # print random.getstate()

     
    app =  wx.App(False)     #  wx.PySimpleApp()
    mainFrame = MyFrame(None, title='PYO-GA', pos=(50,50))
    mainFrame.Show()
    app.MainLoop()
