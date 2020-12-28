#!/usr/bin/python3
from enum import Enum


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


class Languages(Enum):
    French = 0
    chinese = 1
    English = 2


class Language:

        def __init__(self,  currentLanguage="Français"):
            # language definition
            self.FrenchLanguage = {
                "Language": "Français",
                "Language label": "Langue",
                "Title": "Projecteur",
                "Label Frame": "Image #",
                "STOP BUTTON": "STOP",
                "FWD BUTTON": "AVANCER",
                "START BUTTON": "DÉMARRER",
                "CLR BUTTON": "EFFACE TOUT",
                "OPTION BUTTON": "OPTION",
                "EXIT BUTTON": "QUITTER",
                "PREVIOUS BUTTON": "RETOUR",
                "LIGHT BUTTON": "LUMIÈRE ON/OFF",
                "Ready": "PRÊT",
                "Running": "EN MARCHE",
                "Top": "HAUT",
                "Left": "GAUCHE",
                "Bottom": "BAS",
                "Right": "DROIT",
                "Config frame": "AJUSTEMENT DU CADRE",
                "Config load": "RECHARGER",
                "Config save": "SAUVER",
                "CamSize": "CAMERA",
                "film Rate": "Cadence (Image/sec)",
                "Resolution": "Résolution",
                "Brightness": "Brillance",
                "Contrast": "Contraste"
                }

            self.EnglishLanguage = {
                "Language": "English",
                "Language label": "Language",
                "Title": "Projector",
                "Label Frame": "Image #",
                "STOP BUTTON": "STOP",
                "FWD BUTTON": "FWD",
                "START BUTTON": "START",
                "CLR BUTTON": "CLEAR ALL",
                "OPTION BUTTON": "OPTION",
                "EXIT BUTTON": "EXIT",
                "PREVIOUS BUTTON": "RETURN",
                "LIGHT BUTTON": "TOGGLE LIGHT",
                "Ready": "READY",
                "Running": "RUNNING",
                "Top": "TOP",
                "Left": "LEFT",
                "Bottom": "BOTTOM",
                "Right": "RIGHT",
                "Config frame": "FRAME SIZE SETTINGS",
                "Config load": "RELOAD",
                "Config save": "SAVE",
                "CamSize": "CAMERA",
                "film Rate": "Rate (Frame/sec)",
                "Resolution": "Resolution",
                "Brightness": "Brightness",
                "Contrast": "Contrast"
                }
            self.language = {
                Languages.French.value: self.FrenchLanguage,
                Languages.English.value: self.EnglishLanguage}
            self.languageID = self.getLanguageID(currentLanguage)

        def getLanguageID(self, languageName):
            for idx in self.language.keys():
                LG_Text = self.language[idx]['Language']
                if LG_Text == languageName:
                    return idx
            # ok no language Found set French by default
            return Languages.French.value

        def list(self):
            languageList = []
            for idx in self.language.keys():
                languageList.append(self.language[idx]['Language'])
            return languageList

        def getLanguage(self):
            return self.getText('Language')

        def setLanguage(self, newLanguage):
            self.languageID = self.getLanguageID(newLanguage)

        def getText(self, txt):
            try:
                value = self.language[self.languageID][txt]
            except KeyError:
                return "???"
            return value

