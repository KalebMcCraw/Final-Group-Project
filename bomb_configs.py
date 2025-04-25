#################################
# CSC 102 Defuse the Bomb Project
# Configuration file
# Team: Lama A., Janpolad G., Kaleb M., Teya S.
#################################

# constants
DEBUG = False        # debug mode?
RPi = True           # is this running on the RPi?
ANIMATE = False       # animate the LCD text?
SHOW_BUTTONS = True # show the Pause and Quit buttons on the main LCD GUI?
COUNTDOWN = 300      # the initial bomb countdown value (seconds)
NUM_STRIKES = 5      # the total strikes allowed before the bomb "explodes"
NUM_PHASES = 4       # the total number of initial active bomb phases

# imports
from random import randint, shuffle, choice, sample
from string import ascii_uppercase
if (RPi):
    import board
    from adafruit_ht16k33.segments import Seg7x4
    from digitalio import DigitalInOut, Direction, Pull
    from adafruit_matrixkeypad import Matrix_Keypad

#################################
# setup the electronic components
#################################
# 7-segment display
# 4 pins: 5V(+), GND(-), SDA, SCL
#         ----------7SEG---------
if (RPi):
    i2c = board.I2C()
    component_7seg = Seg7x4(i2c)
    # set the 7-segment display brightness (0 -> dimmest; 1 -> brightest)
    component_7seg.brightness = 0.5

# keypad
# 8 pins: 10, 9, 11, 5, 6, 13, 19, NA
#         -----------KEYPAD----------
if (RPi):
    # the pins
    keypad_cols = [DigitalInOut(i) for i in (board.D10, board.D9, board.D11)]
    keypad_rows = [DigitalInOut(i) for i in (board.D5, board.D6, board.D13, board.D19)]
    # the keys
    keypad_keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))

    component_keypad = Matrix_Keypad(keypad_rows, keypad_cols, keypad_keys)

# jumper wires
# 10 pins: 14, 15, 18, 23, 24, 3V3, 3V3, 3V3, 3V3, 3V3
#          -------JUMP1------  ---------JUMP2---------
# the jumper wire pins
if (RPi):
    # the pins
    component_wires = [DigitalInOut(i) for i in (board.D14, board.D15, board.D18, board.D23, board.D24)]
    for pin in component_wires:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

# pushbutton
# 6 pins: 4, 17, 27, 22, 3V3, 3V3
#         -BUT1- -BUT2-  --BUT3--
if (RPi):
    # the state pin (state pin is input and pulled down)
    component_button_state = DigitalInOut(board.D4)
    component_button_state.direction = Direction.INPUT
    component_button_state.pull = Pull.DOWN
    # the RGB pins
    component_button_RGB = [DigitalInOut(i) for i in (board.D17, board.D27, board.D22)]
    for pin in component_button_RGB:
        # RGB pins are output
        pin.direction = Direction.OUTPUT
        pin.value = True

# toggle switches
# 3x3 pins: 12, 16, 20, 21, 3V3, 3V3, 3V3, 3V3, GND, GND, GND, GND
#           -TOG1-  -TOG2-  --TOG3--  --TOG4--  --TOG5--  --TOG6--
if (RPi):
    # the pins
    component_toggles = [DigitalInOut(i) for i in (board.D12, board.D16, board.D20, board.D21)]
    for pin in component_toggles:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

###########
# functions
###########
'''
Generate keypad; return a random written-response question.
'''
def gen_keypad():
    # format: question, answers, hint, difficulty, image, voiceline, hint voice
    return choice([('Who is this?', ['75268', '4367975268', '43679275268'], 'The oldest building at the University of Tampa is named after this individual.', None, 'whoisthis1.jpg', 'kp_who1.mp3', 'hint-oldest.mp3'),
                 ('Who is this?', ['32452374', '83737232452374', '8373722246233732452374', '77374336832452374'], 'This individual is in charge of the University of Tampa.', None, 'whoisthis2.jpg>', 'kp_who2.mp3', 'hint-incharge.mp3'),
                 ('Which building headquarters for the Campus Safety team?', ['3259', '466682846628453464', '4666828466263265522672846628453464', '265522672846628453464'], 'The building is at the intersection of N Boulevard and W North A Street.', None, 'csafety.jpg', 'kp_hq1.mp3', 'hint-intersection.mp3'),
                 ('Which building headquarters for the Bursar’s office?', ['75268'], 'The building is the most famous one on the University of Tampa’s campus.', None, 'bursar.jpg', 'kp_hq2.mp3', 'hint-popular.mp3'),
                 ('Name a restaurant in the Vaughn Center.', ['85846283346464', '244253452', '3467834627684377', '37374273284667', '84347455', '8438847455', '8847455', '22338379', '52428262'], 'One of these places is one of the most popular fast food chains in the United States.', None, 'vaughn.jpg', 'kp_restaurant.mp3', 'hint-fastfood.mp3'),
                 ('Name one of the University of Tampa’s four colleges.', ['26553436327872635388377', '27872635388377', '7953726553436328746377', '26553436328746377', '28746377', '265534363628872543258472436237', '628872543258472436237', '2655343637624257243623762843628427263338228466', '7624257243623762843628427263338228466'], None, 'One of these colleges revolves around the study of corporate practice.', 'acollege.jpg', 'kp_colleges.mp3', 'hint-study.mp3'),
                 ('What is the University of Tampa’s mascot’s name?', ['772782287'], 'He is Spartan.', None, 'mascot.jpg', 'kp_mascot.mp3', 'hint-spartan.mp3'),
                 ('What was Plant Hall originally called?', ['8267222946835', '8246835', '8438267222946835', '8438246835'], 'The building operated as a hotel.', None, 'phall1.jpg', 'kp_phall.mp3', 'hint-hotel.mp3'),
                 ('Name a sport played at the University of Tampa.', ['22732255', '2275382255', '276772686879', '4653', '52276773', '762237', '79466464', '87225', '232248655392255', '769464', '76382255', '836647', '8655392255', '243375323464', '32623', '5822732255', '5852276773'], 'One of these sports is running-based.', None, 'sports.jpg', 'kp_sport.mp3', 'hint-sport.mp3'),
                 ('Name a previous president of the University of Tampa.', ['828446', '766253828446', '7662535828446', '783337', '32843783337', '328434783337', '726766', '27823726766', '278232726766', '24374473', '742427324374473', '7424273324374473', '69367', '2369367', '3356', '328433356', '3284363356', '62623', '355966362623', '3559663262623', '666639', '52637666639', '526373666639', '526373554688666639', '7437626', '56467437626', '564647437626', '56464278397437626', '772853464', '37333742772853464', '373337424772853464'], 'The oldest of these individuals had a road on the University of Tampa’s campus named after them.', None, 'president.jpg', 'kp_pres.mp3', 'hint-road.mp3')])

'''
Generate toggles; return a random question with a numeric answer between 1 & 15.
'''
def gen_toggles():
    # format: question, answer, hint, difficulty, image, voiceline, hint voice
    return choice([('How many rivers does the University of Tampa border?', '0001', 'Like someone who doesn\'t have a spouse.', None, 'utmap.jpg', 'tog_1.mp3', 'hint-1.mp3'),
                 ('How many baseball fields are there on campus?', '0010', 'Equitable to a hand-based peace symbol.', None, 'baseball.jpg', 'tog_2.mp3', 'hint-2.mp3'),
                 ('How many years are there between Tampa’s incorporation as a city and the opening of the Tampa Bay Hotel?', '0011', 'The _____ Musketeers.', None, 'oldmap.jpg', 'tog_3.mp3', 'hint-3.mp3'),
                 ('How many colleges does the University of Tampa have?', '0100', 'The university uses the "____-College Model".', None, 'colleges.jpg', 'tog_4.mp3', 'hint-4.mp3'),
                 ('When did the City of Tampa purchase Tampa Bay Hotel (now Plant Hall)?', '0101', 'The same year the Russo-Japanese war concluded.', None, 'historic.jpg', 'tog_5.mp3', 'hint-5.mp3'),
                 ('How many minarets does Plant Hall have?', '0110', 'The number is afraid of seven.', None, 'minaret.jpg', 'tog_6.mp3', 'hint-6.mp3'),
                 ('What time does Ultimate Dining open on weekdays?', '0111', 'Many people\'s lucky number.', None, 'udining.jpg', 'tog_7.mp3', 'hint-7.mp3'),
                 ('When did the Cass Building open?', '1000', 'The same year a unique president was elected.', None, 'cass.jpg', 'tog_8.mp3', 'hint-8.mp3'),
                 ('What time does the Benson and Alex Fitness Center open on Saturday?', '1001', 'What number of lives people claim cats have.', None, 'fitness.jpg', 'tog_9.mp3', 'hint-9.mp3'),
                 ('How many stories tall is the Grand Center?', '1010', 'A big fat hen!', None, 'gc.jpg', 'tog_10.mp3', 'hint-10.mp3'),
                 ('University of Tampa president Teresa Abi-Nader Dahlberg is the ___th president of the university.', '1011', 'Each president has, on average, served for around 8-9 years.', None, 'dahlberg.jpg', 'tog_11.mp3', 'hint-11.mp3'),
                 ('How many residence halls are at the University of Tampa?', '1100', 'A dime...', None, 'residence.jpg', 'tog_12.mp3', 'hint-12.mp3'),
                 ('How many sororities are there in the University of Tampa?', '1101', 'A spooky Friday.', None, 'sorority.jpg', 'tog_13.mp3', 'hint-13.mp3'),
                 ('What rank does U.S. News & World Report give the University of Tampa in the Regional Universities South category? (2025 Rankings)', '1110', 'The same as the youngest age one can drive in the U.S.', None, 'tampa.jpg', 'tog_14.mp3', 'hint-14.mp3'),
                 ('What are the final two digits of the LASER Team’s phone number?', '1111', 'The same number as the iPhone model that released in 2023.', None, 'laser.jpg', 'tog_15.mp3', 'hint-15.mp3')])
'''
Generate wires; return 5 random True/False statements.
'''
def gen_wires():
    # format: statement, value, difficulty, voiceline
    return sample([['There is a McDonalds on the University of Tampa’s campus.', False, None, 'w_mcd.mp3'],
                   ['The University of Tampa is the largest university in Tampa.', False, None, 'w_largest.mp3'],
                   ['The University of Tampa has fraternities and sororities.', True, None, 'w_frat.mp3'],
                   ['You can rent media recording equipment from the Cass Communications Building.', True, None, 'w_media.mp3'],
                   ['The University of Tampa has a safety team that works 24/7.', True, None, 'w_safety.mp3'],
                   ['The tallest building at the University of Tampa is the Ferman Center for the Arts.', False, None, 'w_ferman.mp3'],
                   ['The University of Tampa opened before any development of Harbour Island, Tampa.', True, None, 'w_harbour.mp3'],
                   ['The newest building at the University of Tampa is the Jenkins Tech Building.', False, None, 'w_jenkins.mp3'],
                   ['There are over 1,000 faculty members at the University of Tampa.', False, None, 'w_faculty.mp3'],
                   ['The University of Tampa has an electrical engineering program.', False, None, 'w_engineer.mp3'],
                   ['The University of Tampa’s official colors are red, black, and orange.', False, None, 'w_colors.mp3'],
                   ['The University of Tampa was founded in 1931.', True, None, 'w_found.mp3'],
                   ['There are over 200 majors offered by the University of Tampa.', False, None, 'w_major.mp3'],
                   ['The University of Tampa competes in NCAA Division II sports.', True, None, 'w_ncaa.mp3'],
                   ['There have been 11 presidents of the University of Tampa.', True, None, 'w_pres.mp3'],
                   ['In our context, UT stands for the University of Texas.', False, None, 'w_texas.mp3'],
                   ['Plant Hall is designated as a national historic landmark.', True, None, 'w_landmark.mp3'],
                   ['The University of Tampa has hundreds of student clubs.', True, None, 'w_clubs.mp3'],
                   ['The University of Tampa offers rentable e-scooters to students and faculty.', False, None, 'w_rentable.mp3'],
                   ['You can see downtown Tampa from campus.', True, None, 'w_downtown.mp3'],
                   ['The University of Tampa is always running, even during extreme weather events such as hurricanes.', False, None, 'w_running.mp3'],
                   ['The University of Tampa has a special alert messaging service for emergency use.', True, None, 'w_alert.mp3'],
                   ['The current mayor of Tampa, Jane Castor, is a University of Tampa alumni.', True, None, 'w_castor.mp3'],
                   ['Elvis Presley performed in the Sykes Chapel.', False, None, 'w_elvis.mp3'],
                   ['The University of Tampa is situated directly on the shore of Tampa Bay.', False, None, 'w_bay.mp3']], 5)
###############################
# generate the bomb's specifics
###############################
# # generate the bomb's serial number (which also gets us the toggle and jumper target values)
# #  serial: the bomb's serial number
# #  toggles_target: the toggles phase defuse value
# #  wires_target: the wires phase defuse value
# serial, toggles_target, wires_target = genSerial()
# 
# # generate the combination for the keypad phase
# #  keyword: the plaintext keyword for the lookup table
# #  cipher_keyword: the encrypted keyword for the lookup table
# #  rot: the key to decrypt the keyword
# #  keypad_target: the keypad phase defuse value (combination)
# #  passphrase: the target plaintext passphrase
# keyword, cipher_keyword, rot, keypad_target, passphrase = genKeypadCombination()
# 
# # generate the color of the pushbutton (which determines how to defuse the phase)
# button_color = choice(["R", "G", "B"])
# # appropriately set the target (R is None)
# button_target = None
# # G is the first numeric digit in the serial number
# if (button_color == "G"):
#     button_target = [ n for n in serial if n.isdigit() ][0]
# # B is the last numeric digit in the serial number
# elif (button_color == "B"):
#     button_target = [ n for n in serial if n.isdigit() ][-1]

'''
These variables are used to put information from the trivia lists into the components, gui, etc.
'''
keypadQuestion, keypadAnswers, keypadHint, keypadDiff, keypadImg, keypadVL, keypadHintVL = gen_keypad()
togglesQuestion, togglesTarget, togglesHint, togglesDiff, togglesImg, togglesVL, togglesHintVL = gen_toggles()
wiresQ1, wiresQ2, wiresQ3, wiresQ4, wiresQ5 = gen_wires()
wiresTarget = ''.join([str(int(wiresQ1[1])), str(int(wiresQ2[1])), str(int(wiresQ3[1])), str(int(wiresQ4[1])), str(int(wiresQ5[1]))])

if (DEBUG):
    print(f"Keypad Question: {keypadQuestion}")
    print(f"Toggles Question: {togglesQuestion}")
    print(f"Wires Statements: \n\t{wiresQ1[0]}\n\t{wiresQ2[0]}\n\t{wiresQ3[0]}\n\t{wiresQ4[0]}\n\t{wiresQ5[0]}")

# set the bomb's LCD bootup text
boot_text = f"Keypad Question: \x00{keypadQuestion}\x00\n"\
            f"Toggles Question: \x00{togglesQuestion}\x00\n"\
            f"Wires Statements: \x00\n\t{wiresQ1[0]}\n\t{wiresQ2[0]}\n\t{wiresQ3[0]}\n\t{wiresQ4[0]}\n\t{wiresQ5[0]}\x00\n"
