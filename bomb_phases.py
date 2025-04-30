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
#         # open difficulty select screen
#         self.diff_screen()
        self.setDifficulty('e')

    def diff_screen(self):
        # FOR LAMA/JOHNY, CREATE DIFFICULTY SCREEN
        # run setupBoot with ('e', 'n', 'h') for difficulty var
        pass
    
    # sets up the LCD "boot" GUI
    def setDifficulty(self, d):
        # make difficulty global for other components to use
        global difficulty
        difficulty = d
        self._diff = d
        

    # sets up the LCD GUI
    def setup(self):
        # bg image
        self._bgImage = Image.open('graphics/images/background.jpg').resize((800, 480))
        self._bg = ImageTk.PhotoImage(self._bgImage)
        self._base = Label(self, image=self._bg)
        self._base.pack()
        
        self._boxTitle = Canvas(self._base, bg='#E03040', width=700, height=75)
        self._boxTitle.create_text(350, 38, text='The UTampa Trivia Bomb', font=('Consolas', 36, 'bold', 'italic'), fill='#FFFFFF')
        self._boxTitle.place(x=50, y=40)
        
        self._canvas1 = Canvas(self._base, width=200, height=75)
        self._btnK = tkinter.Button(self._canvas1, width=100, height=10, bg='#E0F0FF', text='Click to View\nKeypad Question', font=('Consolas', 16))
        self._btnKWin = self._canvas1.create_window(100, 38, anchor=CENTER, window=self._btnK)
        self._canvas1.place(x=50, y=140)
        
        self._canvas2 = Canvas(self._base, width=200, height=75)
        self._btnT = tkinter.Button(self._canvas2, width=100, height=10, bg='#E0F0FF', text='Click to View\nToggles Question', font=('Consolas', 16))
        self._btnTWin = self._canvas2.create_window(100, 38, anchor=CENTER, window=self._btnT)
        self._canvas2.place(x=300, y=140)
        
        self._canvas3 = Canvas(self._base, width=200, height=75)
        self._btnW = tkinter.Button(self._canvas3, width=100, height=10, bg='#E0F0FF', text='Click to View\nWires Questions', font=('Consolas', 16))
        self._btnWWin = self._canvas3.create_window(100, 38, anchor=CENTER, window=self._btnW)
        self._canvas3.place(x=550, y=140)
        
        self._boxDisplay = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText1 = self._boxDisplay.create_text(5, 5, text='keypad display\n...\ntoggles display\n...\nwires display\n...', font=('Consolas', 18), fill='#FFFFFF', anchor=NW)
        self._boxDisplay.place(x=50, y=240)
        
        self._exitImage = Image.open('graphics/images/exit.png').resize((48,48))
        self._exitImg = ImageTk.PhotoImage(self._exitImage)
        
        self._boxExtra = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText2 = self._boxExtra.create_text(320, 5, text='button display\n...\ntimer display\n...\nexit button', font=('Consolas', 18), fill='#FFFFFF', anchor=NE, justify=RIGHT)
        self._exit = tkinter.Button(self._boxExtra, width=32, height=32, image=self._exitImg, command=self.quit)
        self._exitWin = self._boxExtra.create_window(325, 200, anchor=SE, window=self._exit)
        self._boxExtra.place(x=425, y=240)
        
        self.pack(fill=BOTH, expand=True)
    
    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

#     # pauses the timer
#     def pause(self):
#         if (RPi):
#             self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

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
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

#     # pauses and unpauses the timer
#     def pause(self):
#         # toggle the paused state
#         self._paused = not self._paused
#         # blink the 7-segment display when paused
#         self._component.blink_rate = (2 if self._paused else 0)
    
    #This is what happens when the button is pressed
    def process(self, color):
        if color == 0: #Red
            self._value -= 15
            
        elif color == 1: #Green
            self._value += 10
            
        else: #Blue
            print(choice([keypadHint,togglesHint]))
    
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

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return f'{self._value}/{int(self._value, 2)}'