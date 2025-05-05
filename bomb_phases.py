#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: Lama A., Janpolad G., Kaleb M., Teya S.
#################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys
from random import randint,choice
from PIL import ImageTk, Image
import pygame

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window)
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # initialize diff selection var
        self._selected = False
        # start pygame mixer for sounds
        pygame.mixer.init()
        
    # create a difficulty selection screen
    def diff_screen(self):
        # bg image
        self._dsPath = Image.open('graphics/images/background.jpg').resize((800, 480))
        self._dsImg = ImageTk.PhotoImage(self._dsPath)
        self._dsBase = Label(self, image=self._dsImg)
        self._dsBase.pack()
        # title box
        self._boxTitle = Canvas(self._dsBase, bg='#E03040', width=700, height=75)
        self._boxTitle.create_text(350, 38, text='Select a Difficulty', font=('Consolas', 36, 'bold', 'italic'), fill='#FFFFFF')
        self._boxTitle.place(x=50, y=40)
        # easy button
        self._canvas1 = Canvas(self._dsBase, width=200, height=300)
        self._btnE = tkinter.Button(self._canvas1, width=100, height=100, bg='#F0F0FF', fg='#30C040', text='Easy', font=('Consolas', 22), command=lambda: self.set_difficulty('e'))
        self._btnEWin = self._canvas1.create_window(100, 150, anchor=CENTER, window=self._btnE)
        self._canvas1.place(x=50, y=140)
        # medium button
        self._canvas2 = Canvas(self._dsBase, width=200, height=300)
        self._btnN = tkinter.Button(self._canvas2, width=100, height=20, bg='#F0F0FF', fg='#E0C040', text='Normal', font=('Consolas', 22), command=lambda: self.set_difficulty('n'))
        self._btnNWin = self._canvas2.create_window(100, 150, anchor=CENTER, window=self._btnN)
        self._canvas2.place(x=300, y=140)
        # hard button
        self._canvas3 = Canvas(self._dsBase, width=200, height=300)
        self._btnH = tkinter.Button(self._canvas3, width=100, height=20, bg='#F0F0FF', fg='#C03040', text='Hard', font=('Consolas', 22), command=lambda: self.set_difficulty('h'))
        self._btnHWin = self._canvas3.create_window(100, 150, anchor=CENTER, window=self._btnH)
        self._canvas3.place(x=550, y=140)
        # put it all in
        self.pack(fill=BOTH, expand=True)
    
    # set the difficulty and boot the actual game
    def set_difficulty(self, d):
        # make difficulty global for other components to use
        global difficulty
        difficulty = d
        self._diff = d
        # destroy diff screen
        self._dsBase.pack_forget()
        self._dsBase.destroy()
        # mark diff as selected
        self._selected = True
        # startup the actual bomb
        self.setup()
        

    # sets up the LCD GUI
    def setup(self):
        # bg image
        self._bgImage = Image.open('graphics/images/background.jpg').resize((800, 480))
        self._bg = ImageTk.PhotoImage(self._bgImage)
        self._base = Label(self, image=self._bg)
        self._base.pack()
        # title box
        self._boxTitle = Canvas(self._base, bg='#E03040', width=700, height=75)
        self._boxTitle.create_text(350, 38, text='The UTampa Trivia Bomb', font=('Consolas', 36, 'bold', 'italic'), fill='#FFFFFF')
        self._boxTitle.place(x=50, y=40)
        # keypad button
        self._canvas1 = Canvas(self._base, width=200, height=75)
        self._btnK = tkinter.Button(self._canvas1, width=100, height=10, bg='#E0F0FF', text='Click to View\nKeypad Question', font=('Consolas', 14), command=lambda: self.open_question("Keypad Question", keypadQuestion, [keypadVL], keypadImg))
        self._btnKWin = self._canvas1.create_window(100, 38, anchor=CENTER, window=self._btnK)
        self._canvas1.place(x=50, y=140)
        # toggle button
        self._canvas2 = Canvas(self._base, width=200, height=75)
        self._btnT = tkinter.Button(self._canvas2, width=100, height=10, bg='#E0F0FF', text='Click to View\nToggles Question', font=('Consolas', 14), command=lambda: self.open_question('Toggles Question', togglesQuestion, [togglesVL], togglesImg))
        self._btnTWin = self._canvas2.create_window(100, 38, anchor=CENTER, window=self._btnT)
        self._canvas2.place(x=300, y=140)
        # wire button
        self._canvas3 = Canvas(self._base, width=200, height=75)
        self._btnW = tkinter.Button(self._canvas3, width=100, height=10, bg='#E0F0FF', text='Click to View\nWires Questions', font=('Consolas', 14), command=lambda: self.open_question('Wires Statements', wiresQuestions, wiresVLs))
        self._btnWWin = self._canvas3.create_window(100, 38, anchor=CENTER, window=self._btnW)
        self._canvas3.place(x=550, y=140)
        # bottom left info display
        self._boxDisplay = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText1 = self._boxDisplay.create_text(5, 5, text='keypad display\n...\ntoggles display\n...\nwires display\n...', font=('Consolas', 14), fill='#FFFFFF', anchor=NW)
        self._boxDisplay.place(x=50, y=240)
        # exit image
        self._exitImage = Image.open('graphics/images/exit.png').resize((32,32))
        self._exitImg = ImageTk.PhotoImage(self._exitImage)
        # bottom right info display
        self._boxExtra = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText2 = self._boxExtra.create_text(320, 5, text='button display\n...\ntimer display\n...\nexit button', font=('Consolas', 14), fill='#FFFFFF', anchor=NE, justify=RIGHT)
        self._exit = tkinter.Button(self._boxExtra, width=32, height=32, image=self._exitImg, command=self.quit)
        self._exitWin = self._boxExtra.create_window(325, 200, anchor=SE, window=self._exit)
        self._boxExtra.place(x=425, y=240)
        # put it all together
        self.pack(fill=BOTH, expand=True)
    
    # open up the given question screen
    def open_question(self, title, question, sList, image=None):
        # create the canvas
        self._qBase = Canvas(self._base, bg='#101018', width=700, height=400)
        # add title
        self._qBase.create_text(5, 5, text=f'{title}', font=('Consolas', 24, 'bold'), fill='#FFFFFF', anchor=NW)
        # add question(s)
        self._qBase.create_text(5, 395, text=f'{question}', font=('Consolas', 14, 'italic'), fill='#FFFFFF', anchor=SW)
        # add image
        if image:
            self._qImage = Image.open(f'graphics/images/{image}').resize((300,300))
            self._qImg = ImageTk.PhotoImage(self._qImage)
            self._qImgLabel = Label(self._qBase, image=self._qImg)
            self._qImgLabel.place(x=200, y=45)
        # add dictate button
        self._qDictateImage = Image.open('graphics/images/dictate.png').resize((32,32))
        self._qDictateImg = ImageTk.PhotoImage(self._qDictateImage)
        self._qDictate = tkinter.Button(self._qBase, width=32, height=32, image=self._qDictateImg, command=lambda: self.playsound(sList))
        self._qBase.create_window(652, 5, anchor=NE, window=self._qDictate)
        # add close button
        self._qClose = tkinter.Button(self._qBase, width=32, height=32, image=self._exitImg, command=lambda: self.close_question())
        self._qBase.create_window(700, 5, anchor=NE, window=self._qClose)
        # place it
        self._qBase.place(x=50, y=40)
    
    # close the question screen
    def close_question(self):
        try:
            self._qBase.pack_forget()
            self._qBase.destroy()
        except:
            pass
        pygame.mixer.music.set_volume(0)
        # make absolutely sure the sounds stop
        for i in range (20):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unload()
                sleep(0.1)
        pygame.mixer.music.set_volume(1)
    
    # play a given sound
    def playsound(self, sounds):
        global playsound
        playsound = sounds
            
    # play a hint
    def show_hint(self, component, hint, voice):
        #avoids sound overlapping
        self.close_question()
        
        # showhint = hints
        self._hBase = Canvas(self._base, bg='#F0F0FF', width=400, height=240)
        self._hBase.create_text(5, 5, text=f'{component} Hint', font=('Consolas', 16, 'bold'), anchor=NW)
        self._hBase.create_text(5, 30, text=f'{hint}', font=('Consolas', 12), anchor=NW)
        
        # exit image
        self._closeImage = Image.open('graphics/images/exit.png').resize((16,16))
        self._closeImg = ImageTk.PhotoImage(self._closeImage)
        
        # adds exit button
        self._hClose = tkinter.Button(self._hBase, width=16, height=16, image=self._closeImg, command=lambda: self.close_hint())
        self._hBase.create_window(395, 5, anchor=NE, window=self._hClose)
        
        # place it
        self._hBase.place(x=200, y=120)
        
        #play voiceline
        self.playsound(voice)
        
    #closes a hint  
    def close_hint(self):
        self._hBase.pack_forget()
        self._hBase.destroy()
        pygame.mixer.music.unload()
        
    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # get rid of existing screen
        self._base.pack_forget()
        self._base.destroy()
        # put a background in again
        self._esPath = Image.open('graphics/images/background.jpg').resize((800, 480))
        self._esImg = ImageTk.PhotoImage(self._esPath)
        self._esBase = Label(self, image=self._esImg)
        self._esBase.pack()
        # title
        self._boxTitle = Canvas(self._esBase, bg='#E0F0FF', width=700, height=75)
        # if you win, say its defused and hooray sound
        if success:
            self._boxTitle.create_text(350, 38, text='The bomb was defused!', font=('Consolas', 28, 'bold', 'italic'), fill='#30C040')
            pygame.mixer.music.load('graphics/sounds/bomb_defused.wav')
            pygame.mixer.music.play()
        # if you lose, say it exploded and boom sound
        else:
            self._boxTitle.create_text(350, 38, text='The bomb exploded!', font=('Consolas', 28, 'bold', 'italic'), fill='#C03040')
            pygame.mixer.music.load('graphics/sounds/bomb_detonated.mp3')
            pygame.mixer.music.play()
        self._boxTitle.place(x=50, y=40)
        # retry btn
        self._canvas1 = Canvas(self._esBase, width=600, height=300)
        self._btnR = tkinter.Button(self._canvas1, width=100, height=20, bg='#F0F0FF', text='Retry...', font=('Consolas', 48, 'bold', 'italic'), command=self.retry)
        self._btnRWin = self._canvas1.create_window(300, 150, anchor=CENTER, window=self._btnR)
        self._canvas1.place(x=100, y=140)
        # exit btn
        self._exit = tkinter.Button(self._esBase, width=32, height=32, image=self._exitImg, command=self.quit)
        self._exit.place(x=750, y=430)
        # put the end screen together
        self.pack(fill=BOTH, expand=True)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

class Sounds(PhaseThread):
    # create thread
    def __init__(self):
        super().__init__("sound")
        
    # runs the thread
    def run(self):
        # init global playsound activator
        global playsound
        playsound = None
        #loop
        self._running = True
        while (self._running):
            # if playsound called
            if (playsound != None):
                sounds = playsound
                playsound = None
                # play the sounds
                for sound in sounds:
                    pygame.mixer.music.load(f"graphics/sounds/{sound}")
                    pygame.mixer.music.play()
                    # wait for sound to finish before playing next one
                    while pygame.mixer.music.get_busy():
                        sleep(0.1)
            sleep(0.1)
            
# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value <= 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)
    
    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

    
# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                # the combination is correct -> phase defused
                if (self._value in self._target):
                    self._defused = True
                # if the combination doesn't match any target, fail
                else:
                    self._failed = True
                    for tar in self._target:
                        if (self._value == tar[0:len(self._value)]):
                            self._failed = False
            sleep(0.1)

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        self._running = True
        self._temp =  None
        while (self._running):
            self._value = ''.join([str(int(pin.value)) for pin in self._component])
            # check each wire
            for i in range (5):
                # if the wire is diconnected and shouldnt have been, fail
                if (self._value[i] == '0') and (self._target[i] == '1') and not (self._value == self._temp):
                    self._failed = True
                    self._temp = self._value
                # if the wires are all done, defuse
                elif self._value == self._target:
                    self._defused = True
            sleep(0.1)

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return f'{self._value}/{int(self._value, 2)}'

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target=None, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        self._color = None
        self._runColor = None
        self._activated = False
        self._interval = 20 if difficulty == 'e' else 10 if difficulty == 'n' else 5
        self._chance = 8 if difficulty == 'e' else 15 if difficulty == 'n' else 30
    # runs the thread
    def run(self):
        self._running = True
        # initialize
        i = 0
        self._pressed = False
        
        while (self._running):
            # get the pushbutton's state
            self._value = self._component.value
            # every second
            if i == 0:
                # if its on
                if self._color != None:
                    # if it was pressed, set the color to run and activated to true
                    if self._pressed:
                        self._runColor = self._color
                        self._activated = True
                        self._pressed = False
                    self._rgb[self._color].value = True
                    self._color = None
                # if its off
                elif randint(1,15) == 15:
                    self._color = randint(0,2)
                    self._rgb[self._color].value = False
            # check for press  
            if self._value and self._color != None:
                self._pressed = True
            # iterate
            i += 1
            if i>=10:
                i = 0
            sleep(0.1)
    
    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        self._running = True
        self._temp = None
        while (self._running):
            self._value = ''.join([str(int(pin.value)) for pin in self._component])
            # check each toggle
            for i in range (4):
                # if a toggle was switched when it shouldnt have been, fail
                if (self._value[i] == '1') and (self._target[i] == '0') and not (self._value == self._temp):
                    self._failed = True
                    self._temp = self._value
                # if the toggles are correct, defuse
                elif self._value == self._target:
                    self._defused = True
            sleep(0.1)

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return f'{self._value}/{int(self._value, 2)}'