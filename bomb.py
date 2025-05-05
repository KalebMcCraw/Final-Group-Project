#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: Lama A., Janpolad G., Kaleb M., Teya S.
#################################

# import the configs
from bomb_configs import *
# import the phases
from bomb_phases import *

###########
# functions
###########
# generates the bootup sequence on the LCD
def bootup(n=0):
    # if we're not animating (or we're at the end of the bootup text)
    if (not ANIMATE or n == len(boot_text)):
        # if we're not animating, render the entire text at once (and don't process \x00)
#         if (not ANIMATE):
#             gui._lscroll["text"] = boot_text.replace("\x00", "")
        # configure the remaining GUI widgets
        gui.diff_screen()
        
        soundsThread = Sounds()
        soundsThread.start()
        
        # setup the phase threads, execute them, and check their statuses
        if (RPi):
            setup_phases()
            check_phases()
#     # if we're animating
#     else:
#         # add the next character (but don't render \x00 since it specifies a longer pause)
#         if (boot_text[n] != "\x00"):
#             gui._lscroll["text"] += boot_text[n]
# 
#         # scroll the next character after a slight delay (\x00 is a longer delay)
#         gui.after(25 if boot_text[n] != "\x00" else 750, bootup, n + 1)

# sets up the phase threads
def setup_phases():
    global timer, keypad, wires, button, toggles
    
    #(removed)
    #if DIFFICULTY[0] == "casual":
    #    COUNTDOWN = 180
    #elif DIFFICULTY[0] == "seasoned":
    #    COUNTDOWN = 120
    #elif DIFFICULTY[0] == "expert":
    #    COUNTDOWN = 90
    
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    gui.setTimer(timer)
    # setup the keypad thread
    keypad = Keypad(component_keypad, keypadAnswers)
    # setup the jumper wires thread
    wires = Wires(component_wires, wiresTarget)
    # setup the pushbutton thread
    button = Button(component_button_state, component_button_RGB)
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(component_toggles, togglesTarget)

    # start the phase threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()

# checks the phase threads
def check_phases():
    global active_phases
    
    displayTxt1 = "Keypad Input:\n"
    displayTxt2 = "Button Input:\n"
    # check the button
    if (button._running):
        # update the GUI
        displayTxt2 += f"{button}\n"
        # check the button status to apply to the timer
        if (button._activated):
            # timer.process(button._runColor)
            #This is what happens when the button is pressed
            if button._runColor == 0: #Red
                timer._value -= 15
                
            elif button._runColor == 1: #Green
                timer._value += 10
                
            else: #Blue
                if randint(0,1):
                    gui.show_hint("Keypad", keypadHint, keypadHintVL)
                else:
                    gui.show_hint("Toggles", togglesHint, togglesHintVL)
                    
            button._activated = False
    else:
        displayTxt1 += f"...\n"
    # check the timer
    if (timer._running):
        # update the GUI
        displayTxt1 += f"Time Remaining:\n{timer}"
    else:
        # the countdown has expired -> explode!
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, False)
        # don't check any more phases
        return
    # check the keypad
    if (keypad._running):
        # update the GUI
        displayTxt1 += f"{keypad}\n"
        # the phase is defused -> stop the thread
        if (keypad._defused):
            keypad._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (keypad._failed):
            strike()
            # reset the keypad
            keypad._failed = False
            keypad._value = ""
    else:
        displayTxt1 += "...\n"
    # check the toggles
    if (toggles._running):
        # update the GUI
        displayTxt1 += f"Toggles Input:\n{toggles}\n"
        # the phase is defused -> stop the thread
        if (toggles._defused):
            toggles._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (toggles._failed):
            strike()
            # reset the toggles
            toggles._failed = False
    else:
        displayTxt1 += "Toggles Input:\n...\n"
    # check the wires
    if (wires._running):
        # update the GUI
        displayTxt1 += f"Wires Input:\n{wires}"
        # the phase is defused -> stop the thread
        if (wires._defused):
            wires._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (wires._failed):
            strike()
            # reset the wires
            wires._failed = False
    else:
        displayTxt1 += "Wires Input:\n..."
    
    # fully udpate GUI text
    gui._boxDisplay.itemconfigure(gui._displayText1, text=displayTxt1)
    gui._boxExtra.itemconfigure(gui._displayText2, text=displayTxt2)
    # too many strikes -> explode!
    if (strikes_left == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(1000, gui.conclusion, False)
        # stop checking phases
        return

    # the bomb has been successfully defused!
    if (active_phases == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, True)
        # stop checking phases
        return

    # check the phases again after a slight delay
    gui.after(100, check_phases)

# handles a strike
def strike():
    # gui._diff is the difficulty
    timer._value -= 30 if gui._diff == 'e' else 60 if gui._diff == 'n' else 120


# turns off the bomb
def turn_off():
    # stop all threads
    timer._running = False
    keypad._running = False
    wires._running = False
    button._running = False
    toggles._running = False

    # turn off the 7-segment display
    component_7seg.blink_rate = 0
    component_7seg.fill(0)
    # turn off the pushbutton's LED
    for pin in button._rgb:
        pin.value = True

######
# MAIN
######

pygame.init()
pygame.mixer.init()

# initialize the LCD GUI
window = Tk()
gui = Lcd(window)

# initialize the bomb strikes and active phases (i.e., not yet defused)
# strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

# boot the bomb
bootup()

# display the LCD GUI
window.mainloop()