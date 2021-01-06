#!/usr/bin/python3
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

'''
Copyright <2020> <Daniel Perron>

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files (the "Software"),
to deal in the Software without restriction,
including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software,and to permit persons
to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE
'''


class optionMenu:

    def __init__(self, parent):

        self.parent = parent

        # use parent language file
        self.lg = parent.lg

        # this specify on root that we want exit
        self.ExitFlag = False

        self.top = tk.Toplevel(parent.root)
        self.top.attributes("-fullscreen", True)

        # defective touch screen keep top clear
        self.blanktext = tk.Text(self.top,
                                 width=20, height=3,
                                 highlightthickness=0,
                                 borderwidth=0,
                                 bg=self.top["background"])
        self.blanktext.pack()

        # Picture frame config
        self.configFrame = tk.Frame(self.top)
        self.configFrame.pack(side=tk.LEFT, padx=5, ipadx=5)

        configFont = tkFont.Font(root=self.configFrame,
                                 family="Courier", size=14)

        sFont = tkFont.Font(root=self.configFrame, family="Courier", size=18)

        # language box
        self.languageLabelFrame = tk.LabelFrame(self.configFrame,
                                                font=configFont)
        self.languageLabelFrame.pack(side=tk.TOP, pady=10)

        allLanguages = self.lg.list()

        self.languageLabelFrame.option_add("*TCombobox*Listbox*Font",
                                           configFont)

        self.languageBox = ttk.Combobox(self.languageLabelFrame,
                                        values=allLanguages,
                                        font=configFont,
                                        width=19,
                                        state="readonly"
                                        )
        self.languageBox.bind("<<ComboboxSelected>>", self.languageBoxEvent)

        self.languageBox.set(self.lg.getLanguage())
        self.languageBox.pack(side=tk.BOTTOM, padx=12, pady=10)

        self.configLabelFrame = tk.LabelFrame(self.configFrame,
                                              font=configFont,
                                              text=self.lg.getText(
                                                   "Config frame"),
                                              width="40")
        self.configLabelFrame.pack(ipadx=10)
        configTopFrame = tk.Frame(self.configLabelFrame)
        configLeftFrame = tk.Frame(self.configLabelFrame)
        configBottomFrame = tk.Frame(self.configLabelFrame)
        configRightFrame = tk.Frame(self.configLabelFrame)
        configTopFrame.pack()

        # P.S. all text are written using the refreshLanguage function

        self.configCameraSizeLabel = tk.Label(configTopFrame,
                                              font=configFont,
                                              width="20")
        self.configCameraSizeLabel.pack(side=tk.TOP)

        self.configTopLabel = tk.Label(configTopFrame,
                                       text=self.lg.getText("Top")+":",
                                       font=configFont,
                                       anchor="e",
                                       width="10")
        self.configTopLabel.pack(side=tk.LEFT)

        self.TopVar = tk.IntVar(value=int(self.parent.imageTop))
        configTopEntry = tk.Entry(configTopFrame,
                                  font=configFont,
                                  textvariable=self.TopVar,
                                  width="10")
        configTopEntry.pack(side=tk.LEFT)

        configLeftFrame.pack()
        self.configLeftLabel = tk.Label(configLeftFrame,
                                        font=configFont,
                                        anchor="e",
                                        width="10")
        self.configLeftLabel.pack(side=tk.LEFT)
        self.LeftVar = tk.IntVar(value=int(self.parent.imageLeft))
        configLeftEntry = tk.Entry(configLeftFrame,
                                   font=configFont,
                                   textvariable=self.LeftVar,
                                   width="10")
        configLeftEntry.pack(side=tk.LEFT)

        configBottomFrame.pack()
        self.configBottomLabel = tk.Label(configBottomFrame,
                                          font=configFont,
                                          anchor="e",
                                          width="10")
        self.configBottomLabel.pack(side=tk.LEFT)
        self.BottomVar = tk.IntVar(value=int(self.parent.imageBottom))
        configBottomEntry = tk.Entry(configBottomFrame,
                                     font=configFont,
                                     textvariable=self.BottomVar,
                                     width="10")
        configBottomEntry.pack(side=tk.LEFT)

        configRightFrame.pack()
        self.configRightLabel = tk.Label(configRightFrame,
                                         font=configFont,
                                         anchor="e",
                                         width="10")
        self.configRightLabel.pack(side=tk.LEFT)
        self.RightVar = tk.IntVar(value=int(self.parent.imageRight))
        configRightEntry = tk.Entry(configRightFrame,
                                    font=configFont,
                                    textvariable=self.RightVar,
                                    width="10")
        configRightEntry.pack(side=tk.LEFT)
        configButtonFrame = tk.Frame(self.configFrame)
        self.configButtonLoad = tk.Button(configButtonFrame,
                                          command=self.OnLoadConfig,
                                          width="9",
                                          height="1",
                                          font=sFont)

        self.configButtonSave = tk.Button(configButtonFrame,
                                          command=self.OnSaveConfig,
                                          width="9",
                                          height="1",
                                          font=sFont)

        self.configButtonLoad.pack(side=tk.LEFT, padx=2)
        self.configButtonSave.pack(side=tk.RIGHT, padx=2)
        configButtonFrame.pack(ipady=10)

        # film frame
        self.filmFrame = tk.Frame(self.top)
        self.filmFrame.pack(side=tk.LEFT)

        self.filmRateLabelFrame = tk.LabelFrame(self.filmFrame,
                                                font=configFont)
        self.filmRateLabelFrame.pack(side=tk.TOP)
        self.filmRateLabelFrame.option_add("*TCombobox*Listbox*Font",
                                           configFont)
        self.ratePerSecond = tk.IntVar(value=int(self.parent.filmRate))

        self.rateEntry = tk.Entry(self.filmRateLabelFrame,
                                  font=configFont,
                                  textvariable=self.ratePerSecond,
                                  justify=tk.CENTER,
                                  width="10")
        self.rateEntry.pack(side=tk.TOP)

        R9 = tk.Radiobutton(self.filmRateLabelFrame, text="9",
                            variable=self.ratePerSecond, value=9)
        R12 = tk.Radiobutton(self.filmRateLabelFrame, text="12",
                             variable=self.ratePerSecond, value=12)
        R18 = tk.Radiobutton(self.filmRateLabelFrame, text="18",
                             variable=self.ratePerSecond, value=18)
        R24 = tk.Radiobutton(self.filmRateLabelFrame, text="24",
                             variable=self.ratePerSecond, value=24)

        R9.pack(side=tk.LEFT, padx=5)
        R12.pack(side=tk.LEFT, padx=5)
        R18.pack(side=tk.LEFT, padx=5)
        R24.pack(side=tk.LEFT, padx=5)

        # resolution
        self.filmResolutionLabelFrame = tk.LabelFrame(self.filmFrame,
                                                      font=configFont)
        self.filmResolutionLabelFrame.pack(side=tk.TOP, pady=5)
        self.filmResolutionLabelFrame.option_add("*TCombobox*Listbox*Font",
                                                 configFont)
        self.resolution = tk.IntVar(value=int(self.parent.filmResolution))

        R480P = tk.Radiobutton(self.filmResolutionLabelFrame,
                               text="480P",
                               variable=self.resolution,
                               value=480)
        R720P = tk.Radiobutton(self.filmResolutionLabelFrame,
                               text="720P",
                               variable=self.resolution,
                               value=720)
        R1080P = tk.Radiobutton(self.filmResolutionLabelFrame,
                                text="1080P",
                                variable=self.resolution,
                                value=1080)

        R480P.pack(side=tk.LEFT, padx=4)
        R720P.pack(side=tk.LEFT, padx=4)
        R1080P.pack(side=tk.LEFT, padx=4)

        # Camera Brightness
        self.brightnessLabelFrame = tk.LabelFrame(self.filmFrame,
                                                  font=configFont)
        self.brightnessLabelFrame.pack(side=tk.TOP, pady=8)
        self.brightnessLabelFrame.option_add("*TCombobox*Listbox*Font",
                                             configFont)
        self.brightness = tk.IntVar(value=int(self.parent.cameraBrightness))

#        self.brightnessEntry = tk.Entry(self.brightnessLabelFrame,
#                                  font=configFont,
#                                  textvariable=self.brightness,
#                                  justify=tk.CENTER,
#                                  width="10")
#        self.brightnessEntry.pack(side=tk.TOP)
        self.brightnessSlider = tk.Scale(self.brightnessLabelFrame,
                                         from_=0, to=100,
                                         variable=self.brightness,
                                         length=220,
                                         font=configFont,
                                         orient=tk.HORIZONTAL)
        self.brightnessSlider.pack(side=tk.TOP)

        # Camera Contrast
        self.contrastLabelFrame = tk.LabelFrame(self.filmFrame,
                                                font=configFont)
        self.contrastLabelFrame.pack(side=tk.TOP, pady=8)
        self.contrastLabelFrame.option_add("*TCombobox*Listbox*Font",
                                           configFont)
        self.contrast = tk.IntVar(value=int(self.parent.cameraContrast))

#        self.contrastEntry = tk.Entry(self.contrastLabelFrame,
#                                  font=configFont,
#                                  textvariable=self.contrast,
#                                 justify=tk.CENTER,
#                                 width="10")
#       self.contrastEntry.pack(side=tk.TOP)
        self.contrastSlider = tk.Scale(self.contrastLabelFrame,
                                       from_=-100, to=100,
                                       length=220,
                                       variable=self.contrast,
                                       font=configFont,
                                       orient=tk.HORIZONTAL)

        self.contrastSlider.pack(side=tk.TOP)

        # option Frame
        self.optionFrame = tk.Frame(self.top)
        self.optionFrame.pack(side=tk.RIGHT, padx=10)

        #sFont = tkFont.Font(root=self.optionFrame, family="Courier", size=18)

        # save images

        self.saveLabel =  tk.LabelFrame(self.optionFrame,
                          width=230, height= 100,
                          font=configFont)
        self.saveImages = tk.IntVar(value=self.parent.saveImages)
        self.saveImagesCheck = tk.Checkbutton(self.saveLabel,
                                              variable=self.saveImages,
                                              font=configFont)
        self.saveImagesCheck.pack(side=tk.TOP,anchor = "nw")
        self.saveRawImages = tk.IntVar(value=self.parent.saveRawImages)
        self.saveRawImagesCheck = tk.Checkbutton(self.saveLabel,
                                              variable=self.saveRawImages,
                                              font=configFont)
        self.saveRawImagesCheck.pack(side=tk.TOP,anchor = "nw")

        self.saveLabel.pack(side=tk.TOP, anchor ="n")
        self.saveLabel.pack_propagate(0)

        blanktext = tk.Text(self.optionFrame,
                                 height=1,
                                 highlightthickness=0,
                                 borderwidth=0,
                                 bg=self.top["background"])
        blanktext.pack(side=tk.TOP)


        # buttons



        self.toggleLightButton = tk.Button(self.optionFrame,
                                           command=self.OnLightCallBack,
                                           font=sFont,
                                           width=22)

        self.exitButton = tk.Button(self.optionFrame,
                                    command=self.OnExitCallBack,
                                    font=sFont,
                                    width=22)

        self.previousButton = tk.Button(self.optionFrame,
                                        command=self.OnPreviousCallBack,
                                        font=sFont,
                                        width=22)

        self.toggleLightButton.pack(pady=12, padx=2)
        self.exitButton.pack(pady=12,padx=2)
        self.previousButton.pack(pady=12, padx=2)
        self.refreshLanguage()

    def languageBoxEvent(self, event):
        self.lg.setLanguage(self.languageBox.get())
        self.refreshLanguage()

    def refreshLanguage(self):
        self.configLabelFrame['text'] = self.lg.getText("Config frame")
        camSizeString = self.lg.getText("CamSize") + ": {} x {}".format(
                                        self.parent.camWidth,
                                        self.parent.camHeight)
        self.configCameraSizeLabel['text'] = camSizeString
        self.configTopLabel['text'] = self.lg.getText("Top") + ":"
        self.configLeftLabel['text'] = self.lg.getText("Left") + ":"
        self.configBottomLabel['text'] = self.lg.getText("Bottom") + ":"
        self.configRightLabel['text'] = self.lg.getText("Right") + ":"
        self.configButtonLoad['text'] = self.lg.getText("Config load")
        self.configButtonSave['text'] = self.lg.getText("Config save")
        self.languageLabelFrame['text'] = self.lg.getText("Language label")
        self.filmRateLabelFrame['text'] = self.lg.getText("film Rate")
        self.filmResolutionLabelFrame['text'] = self.lg.getText("Resolution")
        self.toggleLightButton['text'] = self.lg.getText("LIGHT BUTTON")
        self.exitButton['text'] = self.lg.getText("EXIT BUTTON")
        self.previousButton['text'] = self.lg.getText("PREVIOUS BUTTON")
        self.brightnessLabelFrame['text'] = self.lg.getText("Brightness")
        self.contrastLabelFrame['text'] = self.lg.getText("Contrast")
        self.saveLabel['text'] = self.lg.getText("save label")
        self.saveRawImagesCheck['text'] = self.lg.getText("save images")
        self.saveImagesCheck['text'] = self.lg.getText("save raw images")

    def OnLoadConfig(self):
        self.parent.loadConfig()
        self.TopVar.set(int(self.parent.imageTop))
        self.LeftVar.set(int(self.parent.imageLeft))
        self.BottomVar.set(int(self.parent.imageBottom))
        self.RightVar.set(int(self.parent.imageRight))
        self.ratePerSecond.set(int(self.parent.filmRate))
        self.resolution.set(int(self.parent.filmResolution))
        self.brightness.set(int(self.parent.cameraBrightness))
        self.contrast.set(int(self.parent.cameraContrast))
        self.saveRawImages.set(int(self.parent.saveRawImages))
        self.saveImages.set(int(self.parent.saveImages))

    def OnSaveConfig(self):
        self.parent.imageTop = self.TopVar.get()
        self.parent.imageLeft = self.LeftVar.get()
        self.parent.imageBottom = self.BottomVar.get()
        self.parent.imageRight = self.RightVar.get()
        self.parent.filmRate = self.ratePerSecond.get()
        self.parent.filmResolution = self.resolution.get()
        self.parent.cameraBrightness = self.brightness.get()
        self.parent.cameraContrast = self.contrast.get()
        self.parent.saveImages = self.saveImages.get()==1
        self.parent.saveRawImages = self.saveRawImages.get()==1
        self.parent.saveConfig()

    def OnLightCallBack(self):
        self.parent.arduino.toggleLight()

    def OnExitCallBack(self):
        self.ExitFlag = True
        self.top.destroy()

    def OnPreviousCallBack(self):
        self.parent.imageTop = self.TopVar.get()
        self.parent.imageLeft = self.LeftVar.get()
        self.parent.imageBottom = self.BottomVar.get()
        self.parent.imageRight = self.RightVar.get()
        self.parent.filmRate = self.ratePerSecond.get()
        self.parent.filmResolution = self.resolution.get()
        self.parent.cameraBrightness = self.brightness.get()
        self.parent.cameraContrast = self.contrast.get()
        self.parent.saveImages = self.saveImages.get()==1
        self.parent.saveRawImages = self.saveRawImages.get()==1
        self.top.destroy()

    def center(self, toplevel):
        toplevel.update_idletasks()

        # Tkinter way to find the screen resolution
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()

        geo1 = toplevel.geometry().split('+')[0].split('x')
        size = tuple(int(_) for _ in geo1)
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2

        toplevel.geometry("+%d+%d" % (x, y))

