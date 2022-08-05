import displaylib
import AmiAuto
from time import sleep
from machine import Pin

#hier werden alle tasten definiert
dreißigtaste = Pin(18,Pin.IN)
funfzigtaste = Pin(19,Pin.IN)
vorfahrttaste = Pin(20,Pin.IN)

linkstaste = Pin(17,Pin.IN, Pin.PULL_DOWN)
rechtstaste = Pin(16,Pin.IN, Pin.PULL_DOWN)

lichttaste = Pin(21,Pin.IN)
stoptaste = Pin(0, Pin.IN)

aktivlicht = Pin(25, Pin.OUT)

#speichert alle notwendigen statusvariablen geschützt ab
class status:
    
    #klasse als prototyp für die zu speicherenden variablen, mit getter und setter methoden
    #um nicht für jede variable diese einzeln zu definieren, ausserdem für beliebig viele
    #variablen einsetzbar
    class var:
        
        #erzeugt die variable und speichert den startwert ab
        def __init__(self, value):
            self.__var = value
        
        #speichert einen übergebenen wert ab
        def setto(self, value):
            self.__var = value
         
        #liest den wert aus und gibt ihn ab 
        def get(self):
            return self.__var
    
    #erzeugt alle variablen, die genau genommen nun objekte des typs var sind, und übergibt einen startwert
    def __init__(self):
        self.__licht = self.var(False)
        self.__lichtupdate = self.var(False)
        self.__timer = self.var(0)
        self.__c = self.var(1)
        self.__blinkerrechts = self.var(False)
        self.__blinkerlinks = self.var(False)
        self.__dreißig = self.var(False)
        self.__funfzig = self.var(False)
        self.__vorfahrt = self.var(False)

#erzeugt ein neues AmiAutoobjekt für die Displaysteuerung und ein statusobjekt für die statusvariablen
auto = AmiAuto.AmiAuto(1, 10, 11, 13, 14, 15)
auto.Zündung()
auto.display.setAnimation(0)
status = status()

#regelt den kontinuierlichen blinkvorgang
def blinken():
    #überprüft ob ein blinker gesetzt ist
    if (status.__blinkerlinks.get() == True) or (status.__blinkerrechts.get() == True):
        #überprüft ob die 5 sekunden abgelaufen sind
        if status.__timer.get() == 5000:
            #timer wird resettet
            status.__timer.setto(0)
            #überprüft ob das licht eingeschaltet ist
            if status.__licht.get() == False:
                #schaltet die jeweilige LED des Blinkers ab
                if status.__blinkerlinks.get() == True:
                    auto.LEDLinks.ledOff()
                else:
                    auto.LEDRechts.ledOff()
            else:
                #bei eingeschaltetem Licht werden die LEDs nur beide auf den gedimmten Zustand gesetzt
                auto.LEDLinks.ledBrightness(10000)
                auto.LEDRechts.ledBrightness(10000)
            #hier wird der jeweilige blinker durch das setzten der Variable abgeschaltet
            if status.__blinkerlinks.get() == True:
                status.__blinkerlinks.setto(False)
            else:
                status.__blinkerrechts.setto(False)
            auto.display.clearAll()
        
        #zählt pro Druchlauf, der alle 100ms geschieht, 100ms hoch
        status.__timer.setto(status.__timer.get() + 100)
        
        #überprüft ob der timerwert restlos durch 500 teilbar ist (dieser block wird alle 500ms ausgeführt)
        if status.__timer.get() % 500 == 0:
            #überprüft die variable c, die speichert, in welchem zyklus der blinker sich befindet
            if status.__c.get() == 1:
                #schaltet die jeweilige led und den pfeil ein
                if status.__blinkerlinks.get() == True:
                    auto.LEDLinks.ledOn()
                    auto.links.show()
                    auto.LEDLinks.ledBrightness(65000)
                else:
                    auto.LEDRechts.ledOn()
                    auto.rechts.show()
                    auto.LEDRechts.ledBrightness(65000)
                auto.display.setBrightness(7)
                #ändert die c status variable, um den zykluswechsel einzuleiten
                status.__c.setto(0)
            else:
                #überprüft ob das licht eingeschaltet ist
                if status.__licht.get() == True:
                    auto.display.setBrightness(1)
                    #steuert die LED und das display an
                    if status.__blinkerlinks.get() == True:
                        auto.links.show('invert')
                        auto.LEDLinks.ledBrightness(10000)
                    else:
                        auto.rechts.show('invert')
                        auto.LEDRechts.ledBrightness(10000)
                else:
                    #steuert die LED und das display an
                    if status.__blinkerlinks.get() == True:
                        auto.LEDLinks.ledBrightness(0)
                    else:
                        auto.LEDRechts.ledBrightness(0)
                    auto.display.clearAll()
                #ändert die c status variable, um den zykluswechsel einzuleiten
                status.__c.setto(1)
        #prüft, ob bei laufendem blinker die blinker taste gedrückt wird      
        if linkstaste.value() == 1:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while linkstaste.value() == 1:
                sleep(0.1)
            #setzt den blinker auf 5000, um von dem bereits existierenden reset gebrauch zu machen
            status.__timer.setto(5000)
        #prüft, ob bei laufendem blinker die blinker taste gedrückt wird
        if rechtstaste.value() == 1:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while rechtstaste.value() == 1:
                sleep(0.1)
            #setzt den blinker auf 5000, um von dem bereits existierenden reset gebrauch zu machen
            status.__timer.setto(5000)
    
#setzt alle status variablen zurück, um einen reibungslosen betrieb ohne doppelbelegungen zu gewährleisten
def inputreset():
    status.__blinkerrechts.setto(False)
    status.__blinkerlinks.setto(False)
    status.__dreißig.setto(False)
    status.__funfzig.setto(False)
    status.__vorfahrt.setto(False)
    status.__timer.setto(0)
    status.__c.setto(1)
    
    if status.__licht.get() == False:
        auto.LEDLinks.ledOff()
        auto.LEDRechts.ledOff()
    else:
        auto.LEDLinks.ledBrightness(10000)
        auto.LEDRechts.ledBrightness(10000)
    auto.display.setBrightness(7)

#schaltet die onboard led ein, um zu signalisieren, das das programm läuft
aktivlicht.value(1)

#HAUPTSCHLEIFE
#Die Hauptschleife läuft alle 100ms durch und fängt alle Tastendrücke ab
while 1==1:
    
    #prüft ob die Taste für das Licht gedrüct wird
    if lichttaste.value() == 1:
        #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
        while lichttaste.value() == 1:
            sleep(0.1)
        #setzt die Statusvariable lichtupdate auf True, um zu signalisieren, das sich der Lichtzustand
        #geändert hat
        status.__lichtupdate.setto(True)
        if status.__licht.get() == False:
            status.__licht.setto(True)
            auto.LEDRechts.ledOn()
            auto.LEDRechts.ledBrightness(10000)
            auto.LEDLinks.ledOn()
            auto.LEDLinks.ledBrightness(10000)
        else:
            status.__licht.setto(False)
            auto.LEDLinks.ledOff()
            auto.LEDRechts.ledOff()
    
    #prüft ob die stoptaste gedrückt wurde
    if stoptaste.value() == 1:
        aktivlicht.value(0)
        #verlässt die Hauptschleife
        break
    
    #prüft ob der blinker links gedrückt wurde
    if linkstaste.value() == 1:
        #da dieser block nur ausgefürt werden soll, wenn der blinker aus ist, wird dies hier abgefragt
        if status.__blinkerlinks.get() == False:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while linkstaste.value() == 1:
                sleep(0.1)
            inputreset()
            #schaltet den blinker ein
            status.__blinkerlinks.setto(True)
    
    #prüft ob der blinker rechts gedrückt wurde
    if rechtstaste.value() == 1:
        #da dieser block nur ausgefürt werden soll, wenn der blinker aus ist, wird dies hier abgefragt
        if status.__blinkerrechts.get() == False:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while rechtstaste.value() == 1:
                sleep(0.1)
            inputreset()
            #schlaltet den blinker ein
            status.__blinkerrechts.setto(True)
    
    #berarbeitet einen eventuell gesetzten blinker
    blinken()
    
    #prüft ob das dreißig schild eingeschaltet werden soll
    if dreißigtaste.value() == 1:
        #da dieser block nur ausgefürt werden soll, wenn der blinker aus ist, wird dies hier abgefragt
        if status.__dreißig.get() == False:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while dreißigtaste.value() == 1:
                sleep(0.1)
            inputreset()
            #schild wird eingeschaltet
            status.__dreißig.setto(True)
            #prüft, ob der lichtzustand sich geändert hat
            if status.__lichtupdate.get() == False:
                #prüft den neuen lichtzustand
                if status.__licht.get() == True:
                    #zeigt das dreißig schild invertiert an
                    auto.dreißig.show('invert')
                else:
                    auto.dreißig.show()
    #prüft, ob das 30 schild aktiv ist, um den timer zu bearbeiten und lichtänderungen zu realisieren    
    if status.__dreißig.get() == True:
        
        #zählt den timer um 100ms hoch
        status.__timer.setto(status.__timer.get() + 100)
        
        #prüft, ob der lichtzustand geändert wurde
        if status.__lichtupdate.get() == True:
            #prüft den neuen lichtzustand
            if status.__licht.get() == True:
                #zeigt das 30 schild invertiert an
                auto.dreißig.show('invert')
            else:
                auto.dreißig.show()
            #ändert die lichtupdate variable, um zu signalisieren, das das lichtupdate erfolgreich
            #bearbeitet wurde
            status.__lichtupdate.setto(False)
        
        #prüft, ob während des leuchtens des 30 zeichens der 30 knopf erneut gedrück wird
        if dreißigtaste.value() == 1:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while dreißigtaste.value() == 1:
                sleep(0.1)
            #setzt den timer auf 5000, um das zeichen auszuschalten
            status.__timer.setto(5000)
            print('aus')
        
        #falls der timer entweder durch den befehl oben oder nach 5s auf 5000 springt, schaltet dieser
        #block das display aus
        if status.__timer.get() == 5000:
            inputreset()
            print('reset')
            auto.display.clearAll()
        
    #DIE NÄCHSTEN BLÖCKE SIND ANALOG ZU DEN BLÖCKEN DES 30 SCHILDS GESTALTET   
    
    if funfzigtaste.value() == 1:
        if status.__funfzig.get() == False:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while funfzigtaste.value() == 1:
                sleep(0.1)
            inputreset()
            status.__funfzig.setto(True)
            if status.__lichtupdate.get() == False:
                if status.__licht.get() == True:
                    auto.funfzig.show('invert')
                else:
                    auto.funfzig.show()
        
    if status.__funfzig.get() == True:
        
        status.__timer.setto(status.__timer.get() + 100)
        
        if status.__lichtupdate.get() == True:
            if status.__licht.get() == True:
                auto.funfzig.show('invert')
            else:
                auto.funfzig.show()
            status.__lichtupdate.setto(False)
        
        if funfzigtaste.value() == 1:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while funfzigtaste.value() == 1:
                sleep(0.1)
            status.__timer.setto(5000)
            
        if status.__timer.get() == 5000:
            inputreset()
            auto.display.clearAll()
            
            
    if vorfahrttaste.value() == 1:
        if status.__vorfahrt.get() == False:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while vorfahrttaste.value() == 1:
                sleep(0.1)
            inputreset()
            status.__vorfahrt.setto(True)
            if status.__lichtupdate.get() == False:
                if status.__licht.get() == True:
                    auto.vorfahrt.show('invert')
                else:
                    auto.vorfahrt.show()
        
    if status.__vorfahrt.get() == True:
        status.__timer.setto(status.__timer.get() + 100)
        if status.__lichtupdate.get() == True:
            if status.__licht.get() == True:
                auto.vorfahrt.show('invert')
            else:
                auto.vorfahrt.show()
            status.__lichtupdate.setto(False)
        if vorfahrttaste.value() == 1:
            #hält das programm solange an, wie die taste gedrückt wird, um doppeleingaben zu vermeiden
            while vorfahrttaste.value() == 1:
                sleep(0.1)
            status.__timer.setto(5000)
        if status.__timer.get() == 5000:
            inputreset()
            auto.display.clearAll()
            
    sleep(0.1)
