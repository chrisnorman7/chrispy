import wx, os
from sys import argv

app = wx.App(False)

class MyTextField(wx.TextCtrl):
 def __init__(self, window, style):
  self.window = window
  wx.TextCtrl.__init__(self, window, style = style)
 def SetValue(self, text):
  self.window.SetTitle(self.window.getFileName())
  wx.TextCtrl.SetValue(self, text)

class Frame(wx.Frame):
 filename = ''
 def SetTitle(self, title):
  title = title if title else 'Untitled Document'
  title = 'Chrispy - ' + title
  return wx.Frame.SetTitle(self, title)
 def setFilePath(self, *args):
  self.filename = os.path.join(*args)
 def getFilePath(self):
  return os.path.join(self.filename)
 def getFileName(self):
  return os.path.split(self.getFilePath())[1]
 def getFileDir(self):
  return os.path.split(self.getFilePath())[0]
 def selectFile(self, title = 'Choose a file'):
  dlg = wx.FileDialog(self, title, self.getFileDir(), self.getFileName())
  ret = True
  if dlg.ShowModal() == wx.ID_OK:
   self.setFilePath(dlg.GetPath())
  else:
   ret = False
  dlg.Destroy()
  return ret
 def OnOpen(self, event = None):
  if self.selectFile('Open'):
   if not os.path.exists(self.getFilePath()):
    wx.MessageBox('The file ' + self.getFilePath() + ' does not exist.', 'File does not exist')
   else:
    try:
     with open(self.getFilePath(), 'r') as f:
      self.entryField.SetValue(f.read().replace('\n', os.linesep))
      self.SetTitle(self.getFileName())
    except IOError:
     wx.MessageBox('Error opening file ' + self.getFilename() + '.', 'Error')
 def OnSaveAs(self, event = None):
  if self.selectFile('Save As'):
   self.OnSave()
 def OnSave(self, event = None):
  if not self.getFilePath():
   self.OnSaveAs()
  else:
   try:
    with open(self.getFilePath(), 'w') as f:
     f.write(self.entryField.GetValue())
   except IOError:
    wx.MessageBox('Error writing to file ' + self.getFilePath() + '.', 'Error saving file')
 def OnExit(self, event = None):
  self.Close(True)
 def __init__(self, parent = None, title = 'Untitled Document', size = (200, 100)):
  wx.Frame.__init__(self, parent = parent, title = title, size = size)
  self.SetTitle(title)
  self.entryField = MyTextField(self, wx.TE_MULTILINE)
  fileMenu = wx.Menu()
  self.Bind(wx.EVT_MENU, self.OnOpen, fileMenu.Append(wx.ID_OPEN, '&open...', 'Open a file for editing'))
  fileMenu.AppendSeparator()
  self.Bind(wx.EVT_MENU, self.OnSave, fileMenu.Append(wx.ID_SAVE, '&Save', 'Save the file'))
  self.Bind(wx.EVT_MENU, self.OnSaveAs, fileMenu.Append(wx.ID_SAVEAS, 'S&ave As...', 'Duplicate the file'))
  fileMenu.AppendSeparator()
  self.Bind(wx.EVT_MENU, self.OnExit, fileMenu.Append(wx.ID_EXIT, '&Quit', 'Exit the program'))
  menuBar = wx.MenuBar()
  menuBar.Append(fileMenu, '&File')
  self.SetMenuBar(menuBar)
  self.CreateStatusBar()
  self.Show(True)

if len(argv) == 2:
 if os.path.exists(argv[1]):
  mainFrame.setFilename(argv[1])
 else:
  wx.MessageBox('Cannot open ' + argv[1], 'Error finding file')
  quit()

mainFrame = Frame()
app.MainLoop()
