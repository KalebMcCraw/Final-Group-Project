#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: Lama A, Janpolad G, Kaleb M, Teya S.
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

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.after(500, self.diff_screen)
        self.setupBoot()

    def diff_screen(self):
        win = Toplevel(self)
        win.title("Choose Your Destiny")
        win.geometry("800x480")
        win.configure(bg='black')

        Label(win, text="How do you launch this game?", font=('Consolas', 22, 'bold'),
              fg='white', bg='black').pack(pady=(40, 20))

        Button(win, text="💤 Casual Player", font=('Consolas', 18), bg='gray', fg='white',
               width=25, command=lambda: [win.destroy(), bootup()]).pack(pady=10)

        Button(win, text="🧠 Seasoned Operator", font=('Consolas', 18), bg='navy', fg='white',
               width=25, command=lambda: [win.destroy(), bootup()]).pack(pady=10)

        Button(win, text="💀 Expert Mode", font=('Consolas', 18), bg='darkred', fg='white',
               width=25, command=lambda: [win.destroy(), bootup()]).pack(pady=10)
        
        def selected_difficulty(self, win, level):
            DIFFICULTY[0] = level
            win.destroy()
            self.after(1000, bootup)

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
<<<<<<< Updated upstream
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)
=======
        # bg image
        self._bgImage = Image.open('graphics/images/background.jpg').resize((800, 480))
        self._bg = ImageTk.PhotoImage(self._bgImage)
        self._base = Label(self, image=self._bg)
        self._base.pack()
        
        self._boxTitle = Canvas(self._base, bg='#E03040', width=700, height=75)
        self._boxTitle.create_text(350, 38, text='The UTampa Trivia Bomb', font=('Consolas', 36, 'bold', 'italic'), fill='#FFFFFF')
        self._boxTitle.place(x=50, y=40)
        
        self._canvas1 = Canvas(self._base, width=200, height=75)
        self._btnK = tkinter.Button(self._canvas1, width=100, height=10, bg='#E0F0FF',text='Click to View\nKeypad Question', font=('Consolas', 14), command=self.keypad_screen)
        self._btnKWin = self._canvas1.create_window(100, 38, anchor=CENTER, window=self._btnK)
        self._canvas1.place(x=50, y=140)
        
        self._canvas2 = Canvas(self._base, width=200, height=75)
        self._btnT = tkinter.Button(self._canvas2, width=100, height=10, bg='#E0F0FF',text='Click to View\nToggles Question', font=('Consolas', 14), command=self.toggles_screen)
        self._btnTWin = self._canvas2.create_window(100, 38, anchor=CENTER, window=self._btnT)
        self._canvas2.place(x=300, y=140)
        
        self._canvas3 = Canvas(self._base, width=200, height=75)
        self._btnW = tkinter.Button(self._canvas3, width=100, height=10, bg='#E0F0FF',text='Click to View\nWires Questions', font=('Consolas', 14), command=self.wires_screen)
        self._btnWWin = self._canvas3.create_window(100, 38, anchor=CENTER, window=self._btnW)
        self._canvas3.place(x=550, y=140)
        
        self._boxDisplay = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText1 = self._boxDisplay.create_text(5, 5, text='keypad display\n...\ntoggles display\n...\nwires display\n...', font=('Consolas', 14), fill='#FFFFFF', anchor=NW)
        self._boxDisplay.place(x=50, y=240)
        
        self._exitImage = Image.open('graphics/images/exit.png').resize((32,32))
        self._exitImg = ImageTk.PhotoImage(self._exitImage)
        
        self._boxExtra = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText2 = self._boxExtra.create_text(320, 5, text='button display\n...\ntimer display\n...\nexit button', font=('Consolas', 14), fill='#FFFFFF', anchor=NE, justify=RIGHT)
        self._exit = tkinter.Button(self._boxExtra, width=32, height=32, image=self._exitImg, command=self.quit)
        self._exitWin = self._boxExtra.create_window(325, 200, anchor=SE, window=self._exit)
        self._boxExtra.place(x=425, y=240)
        
        self.pack(fill=BOTH, expand=True)

    def keypad_screen(self):
        win = Toplevel(self)
        win.title("Keypad Questions")
        win.geometry("800x480")
        win.configure(bg='black')

        canvas = Canvas(win, width=800, height=480, bg='black', highlightthickness=0)
        canvas.pack()

        canvas.create_text(400, 50, text="KEYPAD QUESTIONS:", fill='white', font=('Consolas', 24, 'bold'))
        canvas.create_text(400, 150, text=keypadQuestion, fill='white', font=('Consolas', 16), width=700)
        if keypadHint is True:
            canvas.create_text(400, 300, text=f"Hint: {keypadHint}", fill='gray', font=('Consolas', 14), width=700)

    def toggles_screen(self):
        win = Toplevel(self)
        win.title("Toggles Questions")
        win.geometry("800x480")
        win.configure(bg='black')

        canvas = Canvas(win, width=800, height=480, bg='black', highlightthickness=0)
        canvas.pack()

        canvas.create_text(400, 50, text="TOGGLES QUESTIONS:", fill='white', font=('Consolas', 24, 'bold'))
        canvas.create_text(400, 150, text=togglesQuestion, fill='white', font=('Consolas', 16), width=700)
        if togglesHint:
            canvas.create_text(400, 300, text=f"Hint: {togglesHint}", fill='gray', font=('Consolas', 14), width=700)

    def wires_screen(self):
        win = Toplevel(self)
        win.title("Wires Questions")
        win.geometry("800x480")
        win.configure(bg='black')

        canvas = Canvas(win, width=800, height=480, bg='black', highlightthickness=0)
        canvas.pack()

        canvas.create_text(400, 30, text="WIRES QUESTIONS:", fill='white', font=('Consolas', 24, 'bold'))

        wires = [wiresQ1[0], wiresQ2[0], wiresQ3[0], wiresQ4[0], wiresQ5[0]]
        y = 100
        for w in wires:
            canvas.create_text(400, y, text=w, fill='white', font=('Consolas', 14), width=700)
            y += 60

>>>>>>> Stashed changes

        # bg image
        self._bgImage = Image.open('graphics/images/background.jpg').resize((800, 480))
        self._bg = ImageTk.PhotoImage(self._bgImage)
        self._base = Label(self, image=self._bg)
        self._base.pack()
        
        self._boxTitle = Canvas(self._base, bg='#E03040', width=700, height=75)
        self._boxTitle.create_text(350, 38, text='The UTampa Trivia Bomb', font=('Consolas', 36, 'bold', 'italic'), fill='#FFFFFF')
        self._boxTitle.place(x=50, y=40)
        
        self._canvas1 = Canvas(self._base, width=200, height=75)
        self._btnK = tkinter.Button(self._canvas1, width=100, height=10, bg='#E0F0FF',text='Click to View\nKeypad Question', font=('Consolas', 14), command=self.keypad_screen)
        self._btnKWin = self._canvas1.create_window(100, 38, anchor=CENTER, window=self._btnK)
        self._canvas1.place(x=50, y=140)
        
        self._canvas2 = Canvas(self._base, width=200, height=75)
        self._btnT = tkinter.Button(self._canvas2, width=100, height=10, bg='#E0F0FF',text='Click to View\nToggles Question', font=('Consolas', 14), command=self.toggles_screen)
        self._btnTWin = self._canvas2.create_window(100, 38, anchor=CENTER, window=self._btnT)
        self._canvas2.place(x=300, y=140)
        
        self._canvas3 = Canvas(self._base, width=200, height=75)
        self._btnW = tkinter.Button(self._canvas3, width=100, height=10, bg='#E0F0FF',text='Click to View\nWires Questions', font=('Consolas', 14), command=self.wires_screen)
        self._btnWWin = self._canvas3.create_window(100, 38, anchor=CENTER, window=self._btnW)
        self._canvas3.place(x=550, y=140)
        
        self._boxDisplay = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText1 = self._boxDisplay.create_text(5, 5, text='keypad display\n...\ntoggles display\n...\nwires display\n...', font=('Consolas', 14), fill='#FFFFFF', anchor=NW)
        self._boxDisplay.place(x=50, y=240)
        
        self._exitImage = Image.open('graphics/images/exit.png').resize((32,32))
        self._exitImg = ImageTk.PhotoImage(self._exitImage)
        
        self._boxExtra = Canvas(self._base, bg='#081020', width=325, height=200)
        self._displayText2 = self._boxExtra.create_text(320, 5, text='button display\n...\ntimer display\n...\nexit button', font=('Consolas', 14), fill='#FFFFFF', anchor=NE, justify=RIGHT)
        self._exit = tkinter.Button(self._boxExtra, width=32, height=32, image=self._exitImg, command=self.quit)
        self._exitWin = self._boxExtra.create_window(325, 200, anchor=SE, window=self._exit)
        self._boxExtra.place(x=425, y=240)
        
        self.pack(fill=BOTH, expand=True)

    def keypad_screen(self):
        win = Toplevel(self)
        win.title("Keypad Phase")
        win.geometry("800x480")
        win.configure(bg='black')

        # Optional image (if available)
        try:
            img = Image.open("graphics/images/keypad_hint.jpg").resize((400, 200))
            photo = ImageTk.PhotoImage(img)
            img_label = Label(win, image=photo, bg='black')
            img_label.image = photo  # keeps reference
            img_label.pack(pady=(20, 10))
        except:
            pass  # image not required

        # Question
        Label(win,text=keypadQuestion,font=('Consolas', 16),fg='white',bg='black',wraplength=700,justify='center').pack(pady=10)

        # Optional hint
        if keypadHint:
            Label(win,text=f"Hint: {keypadHint}",font=('Consolas', 12, 'italic'),fg='gray',bg='black',wraplength=700).pack(pady=(0, 20))

        # Back button
        Button(win,text="← Back",font=('Consolas', 12),bg='red',fg='white',command=win.destroy).pack(pady=10)

    def toggles_screen(self):
        win = Toplevel(self)
        win.geometry("800x480")
        win.configure(bg='black')
        win.title("Toggles Phase")

        # Optional image
        img = Image.open("graphics/images/toggles_hint.jpg").resize((400, 200))
        photo = ImageTk.PhotoImage(img)
        Label(win, image=photo, bg='black').pack(pady=(20, 10))
        win.image = photo  # keeps reference

        # Question
        Label(win, text=togglesQuestion, font=('Consolas', 16), fg='white', bg='black',wraplength=700, justify='center').pack(pady=10)

        # Hint
        if togglesHint:
            Label(win, text=f"Hint: {togglesHint}", font=('Consolas', 12, 'italic'), fg='gray',bg='black', wraplength=700).pack(pady=5)

        # Back button
        Button(win, text="← Back", font=('Consolas', 12), bg='red', fg='white',command=win.destroy).pack(pady=20)

    def wires_screen(self):
        win = Toplevel(self)
        win.title("Wires Phase")
        win.geometry("800x480")
        win.configure(bg='black')

        # Optional image
        try:
            img = Image.open("graphics/images/wires_hint.jpg").resize((400, 200))
            photo = ImageTk.PhotoImage(img)
            img_label = Label(win, image=photo, bg='black')
            img_label.image = photo  # keep reference
            img_label.pack(pady=(20, 10))
        except:
            pass  # prevents crashing in case of no image

    # Combine all 5 wire questions
    wires = [wiresQ1[0], wiresQ2[0], wiresQ3[0], wiresQ4[0], wiresQ5[0]]
    question_text = "\n\n".join(wires)

    Label(
        win,text=question_text,font=('Consolas', 16),fg='white',bg='black',wraplength=750,justify='center').pack(pady=(10, 20))

    # Back button
    Button(win,text="← Back",font=('Consolas', 12),bg='red',fg='white',command=win.destroy).pack(pady=(10, 20))

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    #pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    def conclusion(self, success=False):
        win = Toplevel(self)
        win.title("Bomb Status")
        win.geometry("800x480")
        win.configure(bg='black')

        # Image (is optional, based on outcome)
        try:
            img_path = "graphics/images/defused.jpg" if success else "graphics/images/explosion.jpg"
            img = Image.open(img_path).resize((600, 300))
            photo = ImageTk.PhotoImage(img)
            img_label = Label(win, image=photo, bg='black')
            img_label.image = photo  # retains reference
            img_label.pack(pady=(20, 10))
        except:
            Label(win,text="SUCCESS" if success else "💥 BOOM 💥",font=('Consolas', 32, 'bold'),fg='green' if success else 'red',bg='black').pack(pady=30)

    #Message
    Label(win,text="Bomb successfully defused!" if success else "You failed to defuse the bomb in time.",font=('Consolas', 18),fg='white',bg='black',wraplength=700,justify='center').pack(pady=(10, 20))

    # Retry button
    Button(win,text="Retry",font=('Consolas', 14),bg='blue',fg='white',command=self.retry).pack(pady=(0, 10))

    # Quit button
    Button(win,text="Quit",font=('Consolas', 14),bg='red', fg='white',command=self.quit).pack(pady=(0, 10))
    # reattempts the bomb (after an explosion or a successful defusion
    def retry(self):
        # re-launches  the program (and exit this one)
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

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

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
                if (self._value == self._target):
                    self._defused = True
                # the combination is incorrect -> phase failed (strike)
                elif (self._value != self._target[0:len(self._value)]):
                    self._failed = True
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
        # TODO
        pass

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer

    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    if (not self._target or self._target in self._timer._sec):
                        self._defused = True
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
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
        # TODO
        pass

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass
