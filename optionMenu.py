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

        self.spacing_8mm = 3.81
        self.spacing_super8 = 4.23

        # this specify on root that we want exit
        self.ExitFlag = False
        self.top = tk.Toplevel(parent.root, width=800, height=480)
        self.top.wm_overrideredirect(True)
        self.top.geometry("800x480+0+0")
        # Picture frame config
        self.configFrame = tk.Frame(self.top)
        self.configFrame.pack(side=tk.LEFT, padx=5, ipadx=5)

        configFont = tkFont.Font(root=self.configFrame,
                                 family="Courier", size=14)

        sFont = tkFont.Font(root=self.configFrame, family="Courier", size=16)

        # film frame size widget
        self.myWidgetFrameSize(self.configFrame, configFont)
        # Camera Brightness widget
        self.myWidgetBrightness(self.configFrame, configFont)
        # Camera Contrast widget
        self.myWidgetContrast(self.configFrame, configFont)
        # Camera Save Load settings
        self.myWidgetLoadSave(self.configFrame, sFont)
        # film frame widget
        self.myWidgetFrameRate(self.top, configFont)
        # film Total Images stop
        self.myWidgetTotalImages(self.filmFrame, configFont)
        # skip image too dark
        # this appends when camera start
        self.myWidgetSkipImage(self.filmFrame, configFont)

        # option Frame
        self.optionFrame = tk.Frame(self.top)
        self.optionFrame.pack(side=tk.RIGHT, padx=2)
        # language Widget
        self.myWidgetLanguage(self.optionFrame, configFont)
        # output MP$ resolution widget
        self.myWidgetResolution(self.optionFrame, configFont)
        # save images
        self.myWidgetSaveImages(self.optionFrame, configFont)
        # buttons
        self.toggleLightButton = tk.Button(self.optionFrame,
                                           command=self.OnLightCallBack,
                                           font=sFont,
                                           width=20)

        self.previousButton = tk.Button(self.optionFrame,
                                        command=self.OnPreviousCallBack,
                                        font=sFont,
                                        width=20)

        self.exitButton = tk.Button(self.optionFrame,
                                    command=self.OnExitCallBack,
                                    font=sFont,
                                    width=20)

        self.toggleLightButton.pack(pady=3, padx=15)
        self.previousButton.pack(pady=3, padx=15)
        self.exitButton.pack(pady=3, padx=15)
        self.refreshLanguage()

    def myWidgetLanguage(self, parentFrame, currentFont):
        # language box
        self.languageLabelFrame = tk.LabelFrame(parentFrame,
                                                font=currentFont)
        self.languageLabelFrame.pack(side=tk.TOP, pady=8)
        allLanguages = self.lg.list()
        self.languageLabelFrame.option_add("*TCombobox*Listbox*Font",
                                           currentFont)
        self.languageBox = ttk.Combobox(self.languageLabelFrame,
                                        values=allLanguages,
                                        font=currentFont,
                                        width=17,
                                        state="readonly"
                                        )
        self.languageBox.bind("<<ComboboxSelected>>", self.languageBoxEvent)
        self.languageBox.set(self.lg.getLanguage())
        self.languageBox.pack(side=tk.BOTTOM, padx=12, pady=10)

    def myWidgetFrameSize(self, parentFrame, currentFont):
        self.configLabelFrame = tk.LabelFrame(parentFrame,
                                              font=currentFont,
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
                                              font=currentFont,
                                              width="20")
        self.configCameraSizeLabel.pack(side=tk.TOP)

        self.configTopLabel = tk.Label(configTopFrame,
                                       text=self.lg.getText("Top")+":",
                                       font=currentFont,
                                       anchor="e",
                                       width="10")
        self.configTopLabel.pack(side=tk.LEFT)

        self.TopVar = tk.IntVar(value=int(self.parent.imageTop))
        configTopEntry = tk.Entry(configTopFrame,
                                  font=currentFont,
                                  textvariable=self.TopVar,
                                  width="10")
        configTopEntry.pack(side=tk.LEFT)

        configLeftFrame.pack()
        self.configLeftLabel = tk.Label(configLeftFrame,
                                        font=currentFont,
                                        anchor="e",
                                        width="10")
        self.configLeftLabel.pack(side=tk.LEFT)
        self.LeftVar = tk.IntVar(value=int(self.parent.imageLeft))
        configLeftEntry = tk.Entry(configLeftFrame,
                                   font=currentFont,
                                   textvariable=self.LeftVar,
                                   width="10")
        configLeftEntry.pack(side=tk.LEFT)

        configBottomFrame.pack()
        self.configBottomLabel = tk.Label(configBottomFrame,
                                          font=currentFont,
                                          anchor="e",
                                          width="10")
        self.configBottomLabel.pack(side=tk.LEFT)
        self.BottomVar = tk.IntVar(value=int(self.parent.imageBottom))
        configBottomEntry = tk.Entry(configBottomFrame,
                                     font=currentFont,
                                     textvariable=self.BottomVar,
                                     width="10")
        configBottomEntry.pack(side=tk.LEFT)

        configRightFrame.pack()
        self.configRightLabel = tk.Label(configRightFrame,
                                         font=currentFont,
                                         anchor="e",
                                         width="10")
        self.configRightLabel.pack(side=tk.LEFT)
        self.RightVar = tk.IntVar(value=int(self.parent.imageRight))
        configRightEntry = tk.Entry(configRightFrame,
                                    font=currentFont,
                                    textvariable=self.RightVar,
                                    width="10")
        configRightEntry.pack(side=tk.LEFT)

    def myWidgetLoadSave(self, parentFrame, currentFont):
        configButtonFrame = tk.Frame(self.configFrame)
        self.configButtonLoad = tk.Button(configButtonFrame,
                                          command=self.OnLoadConfig,
                                          width="8",
                                          height="1",
                                          font=currentFont)

        self.configButtonSave = tk.Button(configButtonFrame,
                                          command=self.OnSaveConfig,
                                          width="8",
                                          height="1",
                                          font=currentFont)
        self.configButtonLoad.pack(side=tk.LEFT, padx=2)
        self.configButtonSave.pack(side=tk.RIGHT, padx=2)
        configButtonFrame.pack(ipady=2)

    def myWidgetFrameRate(self, parentFrame, currentFont):
        self.filmFrame = tk.Frame(parentFrame)
        self.filmFrame.pack(side=tk.LEFT, padx=10)

        self.filmRateLabelFrame = tk.LabelFrame(self.filmFrame,
                                                font=currentFont)
        self.filmRateLabelFrame.pack(side=tk.TOP, pady=5, ipady=10)
        self.filmRateLabelFrame.option_add("*TCombobox*Listbox*Font",
                                           currentFont)
        self.ratePerSecond = tk.IntVar(value=int(self.parent.filmRate))

        self.rateEntry = tk.Entry(self.filmRateLabelFrame,
                                  font=currentFont,
                                  textvariable=self.ratePerSecond,
                                  justify=tk.CENTER,
                                  width="10")
        self.rateEntry.pack(side=tk.TOP)

        R12 = tk.Radiobutton(self.filmRateLabelFrame, text="12",
                             variable=self.ratePerSecond, value=12)
        R17 = tk.Radiobutton(self.filmRateLabelFrame, text="17",
                             variable=self.ratePerSecond, value=17)
        R18 = tk.Radiobutton(self.filmRateLabelFrame, text="18",
                             variable=self.ratePerSecond, value=18)
        R24 = tk.Radiobutton(self.filmRateLabelFrame, text="24",
                             variable=self.ratePerSecond, value=24)

        R12.pack(side=tk.LEFT, padx=5)
        R17.pack(side=tk.LEFT, padx=5)
        R18.pack(side=tk.LEFT, padx=5)
        R24.pack(side=tk.LEFT, padx=5)

    def myWidgetTotalImages(self, parentFrame, currentFont):
        self.totalImagesFrame = tk.Frame(parentFrame)
        self.totalImagesFrame.pack(side=tk.TOP, pady=10)

        self.totalImagesLabelFrame = tk.LabelFrame(self.totalImagesFrame,
                                                   font=currentFont)
        self.totalImagesLabelFrame.pack(side=tk.TOP)
        self.totalImagesLabelFrame.option_add("*TCombobox*Listbox*Font",
                                              currentFont)

        self.totalLength = tk.IntVar(value=int(0))
        self.totalImages = tk.IntVar(value=int(self.parent.totalImages))
        self.filmType = tk.IntVar(value=int(self.parent.filmType))

        self.calcFilmLength()

        lengthFrame = tk.Frame(self.totalImagesLabelFrame)
        lengthFrame.pack(side=tk.TOP)

        radioFrame = tk.Frame(lengthFrame)
        radioFrame.pack(side=tk.LEFT)
        tFont = tkFont.Font(root=parentFrame, family="Courier", size=12)

        F50 = tk.Radiobutton(radioFrame, text="50'  (15m)",
                             variable=self.totalLength,
                             value=50,
                             command=self.calcNbImages,
                             font=tFont)
        F100 = tk.Radiobutton(radioFrame, text="100' (30m)",
                              variable=self.totalLength,
                              value=100,
                              command=self.calcNbImages,
                              font=tFont)
        F200 = tk.Radiobutton(radioFrame, text="200' (60m)",
                              variable=self.totalLength,
                              value=200,
                              command=self.calcNbImages,
                              font=tFont)
        F50.pack(side=tk.TOP)
        F100.pack(side=tk.TOP)
        F200.pack(side=tk.TOP)

        infoFrame = tk.Frame(lengthFrame)
        infoFrame.pack(side=tk.LEFT, ipady=2)

        self.totalImagesLabel = tk.Label(infoFrame,
                                         font=currentFont,
                                         width="6")
        self.totalImagesLabel.pack(side=tk.TOP)

        self.totalImagesEntry = tk.Entry(infoFrame,
                                         font=currentFont,
                                         textvariable=self.totalImages,
                                         justify=tk.CENTER,
                                         width="6")
        self.totalImagesEntry.pack(side=tk.LEFT, padx=10)

        typeFrame = tk.Frame(self.totalImagesLabelFrame)
        typeFrame.pack(side=tk.TOP)
        S8 = tk.Radiobutton(typeFrame, text="super 8",
                            variable=self.filmType,
                            value=self.parent.film_super8,
                            command=self.calcNbImages,
                            font=tFont)

        N8 = tk.Radiobutton(typeFrame, text="8mm",
                            variable=self.filmType,
                            value=self.parent.film_8mm,
                            command=self.calcNbImages,
                            font=tFont)
        S8.pack(side=tk.LEFT)
        N8.pack(side=tk.LEFT)

    def myWidgetSkipImage(self, parentFrame, currentFont):
        self.skipImageLabelFrame = tk.LabelFrame(parentFrame,
                                                 font=currentFont)
        self.skipImageLabelFrame.pack(side=tk.TOP, pady=10)
        self.skipImageLabelFrame.option_add("*TCombobox*Listbox*Font",
                                            currentFont)

        self.skipImageText = tk.Label(self.skipImageLabelFrame,
                                      text="% threshold",
                                      font=currentFont)
        self.skipImageText.pack(side=tk.TOP)

        self.skipThreshold = tk.IntVar(value=int(self.parent.skipThreshold))
        self.skipThresholdSlider = tk.Scale(self.skipImageLabelFrame,
                                            from_=0, to=100,
                                            variable=self.skipThreshold,
                                            length=220,
                                            font=currentFont,
                                            orient=tk.HORIZONTAL)
        self.skipThresholdSlider.pack(side=tk.TOP)

    def myWidgetResolution(self, parentFrame, currentFont):
        self.filmResolutionLabelFrame = tk.LabelFrame(parentFrame,
                                                      font=currentFont)
        self.filmResolutionLabelFrame.pack(side=tk.TOP, pady=1, ipady=1)
        self.filmResolutionLabelFrame.option_add("*TCombobox*Listbox*Font",
                                                 currentFont)
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

    def myWidgetBrightness(self, parentFrame, currentFont):
        self.brightnessLabelFrame = tk.LabelFrame(parentFrame,
                                                  font=currentFont)
        self.brightnessLabelFrame.pack(side=tk.TOP, pady=3)
        self.brightnessLabelFrame.option_add("*TCombobox*Listbox*Font",
                                             currentFont)
        self.brightness = tk.IntVar(value=int(self.parent.cameraBrightness))
        self.brightnessSlider = tk.Scale(self.brightnessLabelFrame,
                                         from_=0, to=100,
                                         variable=self.brightness,
                                         length=250,
                                         font=currentFont,
                                         orient=tk.HORIZONTAL)
        self.brightnessSlider.pack(side=tk.TOP)

    def myWidgetContrast(self, parentFrame, currentFont):
        self.contrastLabelFrame = tk.LabelFrame(parentFrame,
                                                font=currentFont)
        self.contrastLabelFrame.pack(side=tk.TOP, pady=3)
        self.contrastLabelFrame.option_add("*TCombobox*Listbox*Font",
                                           currentFont)
        self.contrast = tk.IntVar(value=int(self.parent.cameraContrast))
        self.contrastSlider = tk.Scale(self.contrastLabelFrame,
                                       from_=-100, to=100,
                                       length=250,
                                       variable=self.contrast,
                                       font=currentFont,
                                       orient=tk.HORIZONTAL)
        self.contrastSlider.pack(side=tk.TOP)

    def myWidgetSaveImages(self, parentFrame, currentFont):
        self.saveLabel = tk.LabelFrame(parentFrame,
                                       width=230, height=85,
                                       font=currentFont)
        self.saveImages = tk.IntVar(value=self.parent.saveImages)
        self.saveImagesCheck = tk.Checkbutton(self.saveLabel,
                                              variable=self.saveImages,
                                              font=currentFont)
        self.saveImagesCheck.pack(side=tk.TOP, anchor="nw")
        self.saveRawImages = tk.IntVar(value=self.parent.saveRawImages)
        self.saveRawImagesCheck = tk.Checkbutton(self.saveLabel,
                                                 variable=self.saveRawImages,
                                                 font=currentFont)
        self.saveRawImagesCheck.pack(side=tk.TOP, anchor="nw")

        self.saveLabel.pack(side=tk.TOP, anchor="n")
        self.saveLabel.pack_propagate(0)

        blanktext = tk.Text(parentFrame,
                            height=1,
                            highlightthickness=0,
                            borderwidth=0,
                            bg=self.top["background"])
        blanktext.pack(side=tk.TOP)

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
        self.saveRawImagesCheck['text'] = self.lg.getText("save raw images")
        self.saveImagesCheck['text'] = self.lg.getText("save images")
        self.totalImagesLabelFrame['text'] = self.lg.getText("film length")
        self.totalImagesLabel['text'] = self.lg.getText("images length")
        self.skipImageLabelFrame['text'] = self.lg.getText("skip image")
        self.skipImageText['text'] = self.lg.getText("threshold percent")

    def OnLoadConfig(self):
        self.parent.loadConfig()
        self.TopVar.set(int(self.parent.imageTop))
        self.LeftVar.set(int(self.parent.imageLeft))
        self.BottomVar.set(int(self.parent.imageBottom))
        self.RightVar.set(int(self.parent.imageRight))
        self.ratePerSecond.set(int(self.parent.filmRate))
        self.totalImages.set(int(self.parent.totalImages))
        self.skipThreshold.set(int(self.parent.skipThreshold))
        self.resolution.set(int(self.parent.filmResolution))
        self.brightness.set(int(self.parent.cameraBrightness))
        self.contrast.set(int(self.parent.cameraContrast))
        self.saveRawImages.set(int(self.parent.saveRawImages))
        self.saveImages.set(int(self.parent.saveImages))
        self.filmType.set(int(self.parent.filmType))

    def OnSaveConfig(self):
        self.parent.imageTop = self.TopVar.get()
        self.parent.imageLeft = self.LeftVar.get()
        self.parent.imageBottom = self.BottomVar.get()
        self.parent.imageRight = self.RightVar.get()
        self.parent.filmRate = self.ratePerSecond.get()
        self.parent.totalImages = self.totalImages.get()
        self.parent.skipThreshold = self.skipThreshold.get()
        self.parent.filmResolution = self.resolution.get()
        self.parent.cameraBrightness = self.brightness.get()
        self.parent.cameraContrast = self.contrast.get()
        self.parent.saveImages = self.saveImages.get() == 1
        self.parent.saveRawImages = self.saveRawImages.get() == 1
        self.parent.filmType = self.filmType.get()
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
        self.parent.totalImages = self.totalImages.get()
        self.parent.skipThreshold = self.skipThreshold.get()
        self.parent.filmResolution = self.resolution.get()
        self.parent.cameraBrightness = self.brightness.get()
        self.parent.cameraContrast = self.contrast.get()
        self.parent.saveImages = self.saveImages.get() == 1
        self.parent.saveRawImages = self.saveRawImages.get() == 1
        self.parent.filmType = self.filmType.get()
        self.top.destroy()

    def calcImagePerFeet(self):
        ImgPerFt = (12.0 * 25.4) / self.spacing_super8
        if self.filmType.get() == self.parent.film_8mm:
            ImgPerFt = (12.0 * 25.4) / self.spacing_8mm
        return ImgPerFt

    def calcFilmLength(self):
        ratio = self.calcImagePerFeet()
        self.totalLength.set(int(0.5 + (self.totalImages.get() / ratio)))

    def calcNbImages(self):
        ratio = self.calcImagePerFeet()
        filmLength = self.totalLength.get()
        if filmLength > 0:
                self.totalImages.set(int(0.5 + (filmLength * ratio)))
        self.calcFilmLength()
