#!/usr/bin/python3
import tkinter as tk
import tkinter.font as tkFont
import time
import os
import ctypes
from PIL import Image
from PIL import ImageTk
import threading
import imutils
import numpy as np
from enum import Enum
from optionMenu import optionMenu
from language import Language
from arduino import Arduino
import copy
import picamera
import picamera.array
import cv2


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

# PiCamera Resolution
# V1
PiCam_V1 = (2592, 1944)

# V2
PiCam_V2 = (3280, 2464)

# HQ
PiCam_HQ = (4056, 3040)

# Autofind
PiCam_auto = (0, 0)

# need to flip image
PiFlip= True

# save Raw_images
saveRawImages = False

class App():

    def __init__(self, camDevice="/dev/video0",
                 camResolution=PiCam_auto,
                 serialPort="/dev/ttyACM0"):
        # Language Class currently only French and English
        self.lg = Language()

        self.videoFlag=False
        self.videoOut=None
        # if resolution is 0 then auto check
        if camResolution[0] == 0:
            cam = picamera.camera.PiCamera()
            self.camWidth = cam.MAX_RESOLUTION[0]
            self.camHeight = cam.MAX_RESOLUTION[1]
            cam.close()
        else:
            self.camWidth = camResolution[0]
            self.camHeight = camResolution[1]
        self.camDevice = camDevice

        # camera  settings
        self.cameraBrightness = 50
        self.cameraContrast = 0

        # film rate per second
        self.filmRate = 24
        self.filmResolution = 1080

        # actual frame inside picture to store

        self.viewWidth = 640
        self.viewHeight = 480
        self.settingConfiguration = "settings.conf"
        self.imageTop = 0
        self.imageLeft = 0
        self.imageRight = self.camWidth-1
        self.imageBottom = self.camHeight-1
        self.loadConfig()

        # default image path
        self.imagePath = "/home/pi/images/"
        self.imagePrefix = "img_"
        self.videoPath = "/mnt/video/"
        self.videoPrefix = "video_"
        self.videoCount= 0
        # arduino object
        self.arduino = Arduino(port=serialPort)
        # turn light on
        self.arduino.light(True)
        # just to be sure
        self.arduino.light(True)

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.resizable(0, 0)

        # set default language
        self.languageID = tk.IntVar(value=self.lg.languageID)
        self.root.wm_title(self.lg.getText("Title"))

        # ask thread to capture one image
        self.requestImage = False
        self.storedImage = None
        self.camThread = None

        #  CAPTURE RUN FLAG
        self.captureFlag = False

        # image frame
        self.imageFrame = tk.Frame(self.root,
                                   width=600,
                                   height=480,
                                   bg='black')
        self.imageFrame.pack_propagate(0)
        self.imageFrame.pack(side=tk.LEFT,
                             ipadx=0,
                             ipady=0,
                             fill="both")
        self.imagePanel = None

        # cam streaming thread
        self.stopEvent = threading.Event()
        self.camThread = threading.Thread(target=self.videoLoop, args=())
        self.camThread.start()

        # create right panel
        self.rightPanel = tk.Frame(self.root)
        self.rightPanel.pack(side=tk.RIGHT, fill="both", anchor="e")

        # create top info
        self.topInfo = tk.Frame(self.rightPanel)
        self.topInfo.pack(side=tk.TOP)

        # no text=""
        # all text are made using the refreshLanguage() function

        self.photoLabelFrame = tk.LabelFrame(self.topInfo,
                                             width="25")
        self.photoLabel = tk.Label(self.photoLabelFrame,
                                   text=str(self.arduino.frameCount),
                                   width="18")
        self.photoLabelFrame.pack(pady=10)
        self.photoLabel.pack()

        self.captureFlagFrame = tk.Frame(self.rightPanel)
        self.captureFlagFrame.pack(side=tk.TOP)

        self.captureFlagLabel = tk.Label(self.captureFlagFrame,
                                         width="20",
                                         height="2",
                                         borderwidth=2,
                                         relief="solid",
                                         bg=self.captureFlagFrame[
                                            "background"])

        self.captureFlagLabel.pack(side=tk.RIGHT, ipadx=1, padx=2,pady=15)
        self.refreshCaptureFlagLabel()

        # create command frame
        self.commandFrame = tk.Frame(self.rightPanel)
        self.commandFrame.pack(side=tk.TOP)

        sFont = tkFont.Font(root=self.commandFrame, family="Courier", size=14)

        self.forwardButton = tk.Button(self.commandFrame,
                                       bg="gray80",
                                       command=self.OnFwdCallBack,
                                       font=sFont,
                                       width="14")
        self.forwardButton.pack(padx=2, ipady=5,pady=5)

        self.stopButton = tk.Button(self.commandFrame,
                                    command=self.OnStopCallBack,
                                    bg="red", activebackground="tomato",
                                    font=sFont,
                                    width="14")

        self.stopButton.pack(padx=2, ipady=10, pady=5)

        self.recordButton = tk.Button(self.commandFrame,
                                      command=self.OnStartCallBack,
                                      font=sFont,
                                      bg="green",
                                      activebackground="pale green",
                                      width="14")
        self.recordButton.pack(padx=2, pady=3, ipady=5)

        self.clearButton = tk.Button(self.commandFrame,
                                     command=self.OnClearAllCallBack,
                                     font=sFont,
                                     bg="yellow",
                                     activebackground="light yellow",
                                     width="14")
        self.clearButton.pack(padx=2, ipady=5,pady=5)

        self.optionButton = tk.Button(self.commandFrame,
                                      bg="gray80",
                                      command=self.OnOptionCallBack,
                                      font=sFont,
                                      width="14")
        self.optionButton.pack(padx=2, ipady=5,pady=5)

        self.blanktext = tk.Text(self.commandFrame,
                                 width=25,
                                 height=4,
                                 highlightthickness=0,
                                 borderwidth=0,
                                 bg=self.commandFrame["background"])
        self.blanktext.pack()
        self.refreshLanguage()

    def openCameraStream(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.viewWidth)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.viewHeight)
        self.camera.set(cv2.CAP_PROP_FPS, 10)
        self.camera.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
        self.camera.set(cv2.CAP_PROP_CONTRAST, 0.5)

        #print("original Brightness", self.camera.get(cv2.CAP_PROP_BRIGHTNESS))
        #print("original Contrast", self.camera.get(cv2.CAP_PROP_CONTRAST))
        #print("set Brightness", self.camera.get(cv2.CAP_PROP_BRIGHTNESS))
        #print("set Contrast", self.camera.get(cv2.CAP_PROP_CONTRAST))


    def closeCameraStream(self):
        self.camera.release()
        self.camera = None

    def refreshCaptureFlagLabel(self):
        if self.captureFlag:
            self.captureFlagLabel["text"] = self.lg.getText("Running")
            self.captureFlagLabel["bg"] = "pale green"
        else:
            self.captureFlagLabel["text"] = self.lg.getText("Ready")
            self.captureFlagLabel["bg"] = self.rightPanel["background"]

    def enableButtons(self, flag):
        if flag:
            value = "normal"
        else:
            value = "disabled"
        self.forwardButton["state"] = value
        self.recordButton["state"] = value
        self.clearButton["state"] = value
        self.optionButton["state"] = value

    def refreshLanguage(self):
        self.root.wm_title(self.lg.getText("Title"))
        self.photoLabelFrame["text"] = self.lg.getText("Label Frame")
        self.stopButton["text"] = self.lg.getText("STOP BUTTON")
        self.forwardButton["text"] = self.lg.getText("FWD BUTTON")
        self.recordButton["text"] = self.lg.getText("START BUTTON")
        self.clearButton["text"] = self.lg.getText("CLR BUTTON")
        self.optionButton["text"] = self.lg.getText("OPTION BUTTON")
        self.refreshCaptureFlagLabel()

    def OnStopCallBack(self):
        if self.captureFlag:
            self.captureFlag = False
        else:
            self.arduino.stop()
            self.refreshCaptureFlagLabel()
            self.enableButtons(True)

    def OnFwdCallBack(self):
        self.enableButtons(False)
        self.arduino.next()
        self.photoLabel["text"] = str(self.arduino.frameCount)
        self.enableButtons(True)
        pass

    def OnStartCallBack(self):
        self.captureFlag = True
        self.enableButtons(False)
        self.refreshCaptureFlagLabel()
        self.root.after(100, self.captureImage)
        pass

    def OnClearAllCallBack(self):
        self.arduino.clrFrame()
        self.photoLabel["text"] = str(self.arduino.frameCount)
        string = "rm {}*".format(self.imagePath)
        os.system(string)

    def OnOptionCallBack(self):
        optionDialog = optionMenu(self)
        self.stopEvent.set()
        time.sleep(0.05)
        self.root.wait_window(optionDialog.top)
        if optionDialog.ExitFlag:
            self.arduino.light(False)
            self.arduino.light(False)
            self.arduino.close()
            self.root.quit()
        else:
            self.refreshLanguage()
            self.stopEvent.clear()
            self.camThread = threading.Thread(target=self.videoLoop, args=())
            self.camThread.start()

    def moveToNextFrame(self):
        print("move next frame")
        self.arduino.next()
        self.photoLabel["text"] = str(self.arduino.frameCount)
        if self.captureFlag:
            self.root.after(100, self.captureImage)
        else:
            self.enableButtons(True)
        self.refreshCaptureFlagLabel()

    def captureImage(self):
        # send a request
        # the video thread loop should
        # grabbed the image  and
        # execute the storeImageThread
        self.requestImage = True

    def resizeImageToHD(self, image):
        # ok from 4:3 ratio to 16:9 ratio
        # frame will always get
        # some horizontal border

        # First extract only needed parts

        print("resize ", image.shape)
        print("top", self.imageTop,
              "left", self.imageLeft,
              "bottom", self.imageBottom,
              "right", self.imageRight)
        cut_image = image[self.imageTop:self.imageBottom,
                          self.imageLeft:self.imageRight]
        print("cutimage", cut_image.shape)
        cut_dy, cut_dx, depth = cut_image.shape

        H = 1920
        V = 1080
        if self.filmResolution == 720:
            H = 1280
            V = 720
        elif self.filmResolution == 480:
            H = 640
            V = 480
        ratio = V/H
        # where is the border
        if (cut_dy/cut_dx) > ratio:
            HD_Frame = imutils.resize(cut_image, height=V)
        else:
            HD_Frame = imutils.resize(cut_image, width=H)
        dy, dx, depth = HD_Frame.shape
        borderV = (V - dy)//2
        borderH = (H - dx)//2
        print("HD_Frame", HD_Frame.shape)

        blank_HDimage = np.zeros((V, H, 3), np.uint8)
        # change border color if you want by filling image first
        # blank_HDimage[0:1080,0:1920] = (255,255,255)
        # blank_HDimage[borderV:1080-borderV,borderH:1920-borderH]=HD_Frame
        blank_HDimage[borderV:borderV+dy, borderH:borderH+dx] = HD_Frame
        print("resize Done")
        return blank_HDimage

    def storeImage(self):
        if saveRawImages:
            fileName = self.imagePath + "raw_"
            fileName = fileName + self.imagePrefix
            fileName = fileName + "{:05d}".format(self.arduino.frameCount)
            fileName = fileName + ".jpg"
            cv2.imwrite(fileName, self.storedImage)

        # resize image to HD
        HD_image = self.resizeImageToHD(self.storedImage)

        # let's save image
        fileName = self.imagePath + self.imagePrefix+"{:05d}".format(
                   self.arduino.frameCount) + ".jpg"
        print("filename->", fileName)

        cv2.imwrite(fileName, HD_image)

        height, width, layers = HD_image.shape
        print("H",height,"W", width)

        if not self.videoFlag:
            self.videoFlag=True
            self.videoCount= self.videoCount + 1
            videoName= self.videoPath+self.videoPrefix+str(self.videoCount)
            videoName= videoName + ".mp4"
            print("create",videoName)
            self.videoOut = cv2.VideoWriter(videoName,
                                            cv2.VideoWriter_fourcc(*'MP4V'),
                                            self.filmRate, (width,height))
            self.videoOut.set(cv2.VIDEOWRITER_PROP_QUALITY, 100)
        print("write video Frame:",self.arduino.frameCount)
        self.videoOut.write(HD_image)

        if self.captureFlag:
            self.root.after(100, self.moveToNextFrame)
        else:
            self.enableButtons(True)
        self.refreshCaptureFlagLabel()

    def videoLoop(self):
        self.openCameraStream()
        try:
            while not self.stopEvent.is_set():
                # is the image has beend requested
                if self.requestImage:
                    if self.camera is not None:
                        self.closeCameraStream()
                    frame = None
                    with picamera.PiCamera() as piCam:
                        piCam.resolution = (self.camWidth, self.camHeight)
                        piCam.framerate =  10
                        piCam.brightness = self.cameraBrightness
                        piCam.contrast = self.cameraContrast

                        with picamera.array.PiRGBArray(piCam) as output:
                            piCam.capture(output, 'rgb')
                            frame = output.array
                        piCam.close()
                    if frame is None:
                        continue

                    if PiFlip:
                        frame = cv2.rotate(frame, cv2.ROTATE_180)
                    self.storedImage = copy.deepcopy(frame)
                    self.storedImage = cv2.cvtColor(self.storedImage,
                                                    cv2.COLOR_BGR2RGB)
                    self.requestImage = False
                    self.root.after(1, self.storeImage)
                    #continue
                else:
                    if not self.captureFlag:
                        if self.camera is None:
                            self.openCameraStream()
                        # ok not capturing anymore
                        # close  video
                        if self.videoFlag:
                            self.videoFlag=False
                            self.videoOut.release()
                            print("close video1")

                        valid, frame = self.camera.read()
                        if valid is False:
                            continue
                        # put capture frame rectangle
                        # convert from view to capture size
                        if PiFlip:
                            frame = cv2.rotate(frame, cv2.ROTATE_180)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    else:
                        time.sleep(0.05)
                        continue

                xratio = (600 / 640) * self.viewWidth / self.camWidth
                yratio = (600 / 640) * self.viewHeight / self.camHeight
                P1 = (int(self.imageLeft * xratio + 0.5),
                      int(self.imageTop * yratio + 0.5))
                P2 = (int(self.imageRight * xratio + 0.5),
                      int(self.imageBottom * yratio + 0.5))
                smallFrame = imutils.resize(frame, width=600)

                cv2.rectangle(smallFrame, P1, P2,
                              (0, 0, 255),
                              thickness=2)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = Image.fromarray(smallFrame)
                image = ImageTk.PhotoImage(image)

                if self.imagePanel is None:
                    self.imagePanel = tk.Label(self.imageFrame, image=image)
                    self.imagePanel.image = image
                    self.imagePanel.pack(side="left", padx=0)

                # otherwise, simply update the panel
                else:
                    self.imagePanel.configure(image=image)
                    self.imagePanel.image = image
        except (RuntimeError, TypeError, NameError):
            print("[INFO] caught a RuntimeError")
        if self.camera is not None:
            self.closeCameraStream()

    def loadConfig(self):
        file = open(self.settingConfiguration, "rt")
        data = file.read()
        rows = data.split("\n")
        for row in rows:
            info = row.split("=")
            if len(info) == 2:
                if info[0] == "top":
                    self.imageTop = int(info[1])
                elif info[0] == "left":
                    self.imageLeft = int(info[1])
                elif info[0] == "bottom":
                    self.imageBottom = int(info[1])
                    if self.imageBottom >= self.camHeight:
                        self.imageBottom = self.camHeight-1
                elif info[0] == "right":
                    self.imageRight = int(info[1])
                    if self.imageRight >= self.camWidth:
                        self.imageRight = self.camWidth-1
                elif info[0] == "language":
                    self.lg.setLanguage(info[1])
                elif info[0] == "rate":
                    self.filmRate = int(info[1])
                elif info[0] == "resolution":
                    self.filmResolution = int(info[1])
                elif info[0] == "contrast":
                    self.cameraContrast = int(info[1])
                elif info[0] == "brightness":
                    self.cameraBrightness = int(info[1])

        file.close()

    def saveConfig(self):
        file = open(self.settingConfiguration, "wt")
        file.write("[CaptureFrame]\n")
        file.write("top={}\n".format(self.imageTop))
        file.write("left={}\n".format(self.imageLeft))
        file.write("bottom={}\n".format(self.imageBottom))
        file.write("right={}\n".format(self.imageRight))
        file.write("rate={}\n".format(self.filmRate))
        file.write("resolution={}\n".format(self.filmResolution))
        file.write("[Config]\n")
        file.write("language={}\n".format(self.lg.getLanguage()))
        file.write("[Camera]\n")
        file.write("brightness={}\n".format(self.cameraBrightness))
        file.write("contrast={}\n".format(self.cameraContrast))
        file.close()

    def mainloop(self):
        self.root.mainloop()

app = App()
app.mainloop()

