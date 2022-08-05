import displaylib
import ledLib
from machine import Pin
from time import sleep
from machine import PWM

#Steuert die Anzeige der Symbole auf dem Display
class AmiAuto:
    
    class symbol:
        def __init__(self, display, data):
            self.data = data
            self.display = display
                        
        def show(self, invert = None):
            self.display.clearAll()
            #skip ist eine variable, die bestimmt, ob beim befehl setColumnn das Bild tatsächlich angezeigt
            #werden soll oder die daten nur in den Buffer geladen werden sollen
            self.skip = False
            #prüft ob das bild invertiert werden soll
            if invert == 'invert':
                #bei der invertierung sollen die daten nur in den buffer geladen werden
                self.skip = True
                #buffer wird gestartet, d.h. er kann nun daten annehmen
                self.display.startBuffer()
                #der buffer wird geleert
                self.display.clearBuffer()
            for i in range(8):   
                self.display.setColumn(i+1,self.data[i], self.skip)
            if invert == 'invert':
                #buffer wird gesperrt
                self.display.stopBuffer()
                #alle daten werden invertiert, d.h. 1--> 0; 0--> 1
                self.display.invertBuffer()
                #buffer wird auf das display ausgegeben
                self.display.printBuffer()
    
    #nimmt die Pin IDs an
    def __init__(self, block, clk, din, cs, LEDL, LEDR):
        #sonstige
        self.block = block
        self.clk = clk
        self.din = din
        self.cs = cs
        #LEDs
        self.pinLEDLinks = LEDL
        self.pinLEDRechts = LEDR
    
    #initiiert das Display und die LEDs
    def Zündung(self):
        #global display
        self.display = displaylib.Display(self.block, self.clk, self.din, self.cs)
        #erzeugt ein neues Objekt namens display der Klasse Display aus der Bibliothek displaylib
        
        self.display.startup()
        #ruft die startup Methode aus dem display Objekt auf

        self.display.setBrightness(7)
        brightness = 7
        #ruft die setBrightness Methode aus dem display Objekt auf und übergibt den Wert 7
        
        #erzeugt beide notwendigen LED Objekte für die LEDs
        self.LEDLinks = ledLib.Led(self.pinLEDLinks)
        self.LEDRechts = ledLib.Led(self.pinLEDRechts)
        
        self.dreißig = self.symbol(self.display,[[2,7],
                               [1,8],
                               [2,3,5,6,7],
                               [3,5,7],
                               [2,3,5,7],
                               [3,5,7],
                               [2,3,5,6,7],
                               [1,8]])
        
        self.funfzig = self.symbol(self.display,[[2,7],
                               [1,8],
                               [2,3,5,6,7],
                               [2,5,7],
                               [2,3,5,7],
                               [3,5,7],
                               [2,3,5,6,7],
                               [1,8]])
        
        self.vorfahrt = self.symbol(self.display,[[2,3,4,5,6,7],
                               [1,2,3,4,5,6,7,8],
                               [1,2,7,8],
                               [2,7],
                               [2,3,6,7],
                               [3,6],
                               [3,4,5,6],
                               [4,5]])
        
        self.links = self.symbol(self.display,[[],
                               [4],
                               [3,4],
                               [2,3,4,5,6,7],
                               [2,3,4,5,6,7],
                               [3,4],
                               [4],
                               []])
        
        self.rechts = self.symbol(self.display,[[],
                               [5],
                               [5,6],
                               [2,3,4,5,6,7],
                               [2,3,4,5,6,7],
                               [5,6],
                               [5],
                               []])