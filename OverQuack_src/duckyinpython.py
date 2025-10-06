# License: GPLv2.0

# Original copyright (c) 2023 Dave Bailey

# Original Author: Dave Bailey (dbisu, @daveisu)

# Original Project name: PicoDucky

# Modifications and improvements by: VexilonHacker (@VexilonHacker)

# Copyright (c) 2025 VexilonHacker

# Original Project name : OverQuack

#Custom Edit to fix all the issues: OverQuack

# Copyright (c) 2025 NikhilMunda

# Description:

# - Added full Rubber Ducky script functionality including mouse support

# - Introduced randomization features for payloads

# - Enhanced overall usability and feature set, bringing it closer to a full Rubber Ducky experience

# - Integrated wireless connection support for Pico W, enabling FULL wireless control over "OverQuack"

# - ENHANCED: Fixed stack exhaustion issues and proper IF/ELSE/ELSE_IF/END_IF handling

# - FIXED: Nested conditions, loops, and functions now work properly inside each other

import asyncio

import gc

import re

from random import choice, randint

from time import monotonic, sleep

from adafruit_hid.consumer_control import ConsumerControl

from adafruit_hid.consumer_control_code import ConsumerControlCode

from adafruit_hid.keyboard import Keyboard

from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout

from adafruit_hid.keycode import Keycode

from adafruit_hid.mouse import Mouse

from board import *

import board

from digitalio import DigitalInOut, Pull

from microcontroller import reset

from usb_hid import devices

def _Ap_Info(elem):

    import wifi

    if elem == 'ssid':

        return config['AP']['ssid']

    elif elem == 'password':

        return config['AP']['password']

    elif elem == 'bssid':

        return ":".join("{:02X}".format(b) for b in wifi.radio.mac_address)

    else:

        return ""

def _capsOn():

    if kbd.led_on(Keyboard.LED_CAPS_LOCK):

        return 1

    else:

        return 0

def _numOn():

    if kbd.led_on(Keyboard.LED_NUM_LOCK):

        return 1

    else:

        return 0

def _scrollOn():

    if kbd.led_on(Keyboard.LED_SCROLL_LOCK):

        return 1

    else:

        return 0

duckyKeys = {
    
    '0': Keycode.ZERO, '1': Keycode.ONE, '2': Keycode.TWO, '3': Keycode.THREE, '4': Keycode.FOUR, '5': Keycode.FIVE,
    
    'WINDOWS': Keycode.GUI, 'RWINDOWS': Keycode.RIGHT_GUI,

    'GUI': Keycode.GUI, 'RGUI': Keycode.RIGHT_GUI,

    'COMMAND': Keycode.GUI, 'RCOMMAND': Keycode.RIGHT_GUI,

    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION,

    'SHIFT': Keycode.SHIFT, 'RSHIFT': Keycode.RIGHT_SHIFT,

    'ALT': Keycode.ALT, 'RALT': Keycode.RIGHT_ALT,

    'OPTION': Keycode.ALT, 'ROPTION': Keycode.RIGHT_ALT,

    'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL, 'RCTRL': Keycode.RIGHT_CONTROL,

    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,

    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,

    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,

    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,

    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,

    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,

    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,

    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB, 'BACKSPACE': Keycode.BACKSPACE,

    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,

    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,

    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,

    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,

    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,

    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,

    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,

    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,

    'F12': Keycode.F12, 'F13': Keycode.F13, 'F14': Keycode.F14, 'F15': Keycode.F15,

    'F16': Keycode.F16, 'F17': Keycode.F17, 'F18': Keycode.F18, 'F19': Keycode.F19,

    'F20': Keycode.F20, 'F21': Keycode.F21, 'F22': Keycode.F22, 'F23': Keycode.F23,

    'F24': Keycode.F24

}



duckyConsumerKeys = {

    'MK_VOLUP': ConsumerControlCode.VOLUME_INCREMENT, 'MK_VOLDOWN': ConsumerControlCode.VOLUME_DECREMENT, 'MK_MUTE': ConsumerControlCode.MUTE,

    'MK_NEXT': ConsumerControlCode.SCAN_NEXT_TRACK, 'MK_PREV': ConsumerControlCode.SCAN_PREVIOUS_TRACK,

    'MK_PP': ConsumerControlCode.PLAY_PAUSE, 'MK_STOP': ConsumerControlCode.STOP

}



LAYOUTS_MAP = {

    "US_DVO": ("keyboard_layouts.keyboard_layout_us_dvo", "adafruit_hid.keycode"),

    "US": ("adafruit_hid.keyboard_layout_us", "adafruit_hid.keycode"),

    "MAC_FR": ("keyboard_layouts.keyboard_layout_mac_fr", "keycodes.keycode_mac_fr"),

    "WIN_BR": ("keyboard_layouts.keyboard_layout_win_br", "keycodes.keycode_win_br"),

    "WIN_CZ": ("keyboard_layouts.keyboard_layout_win_cz", "keycodes.keycode_win_cz"),

    "WIN_CZ1": ("keyboard_layouts.keyboard_layout_win_cz1", "keycodes.keycode_win_cz1"),

    "WIN_DA": ("keyboard_layouts.keyboard_layout_win_da", "keycodes.keycode_win_da"),

    "WIN_DE": ("keyboard_layouts.keyboard_layout_win_de", "keycodes.keycode_win_de"),

    "WIN_ES": ("keyboard_layouts.keyboard_layout_win_es", "keycodes.keycode_win_es"),

    "WIN_FR": ("keyboard_layouts.keyboard_layout_win_fr", "keycodes.keycode_win_fr"),

    "WIN_HU": ("keyboard_layouts.keyboard_layout_win_hu", "keycodes.keycode_win_hu"),

    "WIN_IT": ("keyboard_layouts.keyboard_layout_win_it", "keycodes.keycode_win_it"),

    "WIN_PO": ("keyboard_layouts.keyboard_layout_win_po", "keycodes.keycode_win_po"),

    "WIN_SW": ("keyboard_layouts.keyboard_layout_win_sw", "keycodes.keycode_win_sw"),

    "WIN_TR": ("keyboard_layouts.keyboard_layout_win_tr", "keycodes.keycode_win_tr"),

    "WIN_UK": ("keyboard_layouts.keyboard_layout_win_uk", "keycodes.keycode_win_uk"),

}



variables = {"$_RANDOM_MIN": 0, "$_RANDOM_MAX": 65535}

internalVariables = {

    "$_CAPSLOCK_ON": _capsOn,

    "$_NUMLOCK_ON": _numOn,

    "$_SCROLLLOCK_ON": _scrollOn,

    "$_BSSID": lambda: _Ap_Info('bssid'),

    "$_SSID": lambda: _Ap_Info('ssid'),

    "$_PASSWD": lambda: _Ap_Info('password'),

}



rng_variables = ["$_RANDOM_NUMBER", "$_RANDOM_LOWERCASE_LETTER", "$_RANDOM_UPPERCASE_LETTER",

                 "$_RANDOM_LETTER", "$_RANDOM_SPECIAL", "$_RANDOM_CHAR"]

letters = "abcdefghijklmnopqrstuvwxyz"

numbers = "0123456789"

specialChars = "!@#$%^&*()"

defines = {}

functions = {}

defaultDelay = 0

DEFAULT_PIN_NUM = 5

oneshot = True

progStatusPin = None

kbd = Keyboard(devices)

consumerControl = ConsumerControl(devices)

layout = KeyboardLayout(kbd)

mouse = Mouse(devices)

# Stack depth control to prevent recursion issues

MAX_RECURSION_DEPTH = 20  # Increased for better nested support

current_recursion_depth = 0

PROBLEM_CODE = "ERROR404"

# ANSI Color Codes

RESET = "\033[0m"

BLACK = "\033[30m"

RED = "\033[31m"

GREEN = "\033[32m"

YELLOW = "\033[33m"

BLUE = "\033[34m"

MAGENTA = "\033[35m"

CYAN = "\033[36m"

BRIGHT_BLACK = "\033[90m"

BRIGHT_RED = "\033[91m"

BRIGHT_GREEN = "\033[92m"

BRIGHT_YELLOW = "\033[93m"

BRIGHT_BLUE = "\033[94m"

BRIGHT_MAGENTA = "\033[95m"

BRIGHT_CYAN = "\033[96m"

WHITE = "\033[37m"

GOLD = "\033[38;2;255;215;0m"

SILVER = "\033[38;2;192;192;192m"

BRONZE = "\033[38;2;205;127;50m"

PINK = "\033[38;2;255;105;180m"

STEEL_BLUE = "\033[38;2;70;130;180m"

class SafeIterator:

    """Safer iterator that prevents infinite loops"""

    def __init__(self, iterable):

        self.items = list(iterable) if not isinstance(iterable, list) else iterable

        self.index = 0

        self.max_iterations = len(self.items) * 2  # Safety limit

    def __iter__(self):

        return self

    def __next__(self):

        if self.index >= len(self.items) or self.index >= self.max_iterations:

            raise StopIteration

        item = self.items[self.index]

        self.index += 1

        return item

    def remaining(self):

        return self.items[self.index:]

    def pop(self, index=0):

        if self.index + index < len(self.items):

            return self.items.pop(self.index + index)

        raise IndexError("Index out of range")

def print_with_color(STRING, COLOR=WHITE, sep=" ", end="\n"):

    print(f"{COLOR}{STRING}{RESET}", sep=sep, end=end)

def LoadJsonConf(json_file="config.json"):

    import json

    config = {}

    try:

        with open(json_file, "r") as f:

            config = json.load(f)

    except (OSError, ValueError) as e:

        print_with_color(f"ERR: {e}\nconfig = {config}", RED)

        config['DEFAULT_PAYLOAD'] = "payload.oqs"

        config['BOARD'] = {}

        config['BOARD']['enable_auto_reload'] = False

        config['BOARD']['enable_auto_switch_mode'] = True

        config['BOARD']['controll_mode_pin'] = 5

        config['AP'] = {}

        config['AP']["ssid"] = "OverQuackError"

        config['AP']["password"] = "NeonBeonError"

        config['AP']["channel"] = 6

        config['AP']["ip_address"] = "192.168.4.1"

        config['AP']["ports"] = [80, 8000, 8080]

    return config

config = LoadJsonConf()

def _getIfCondition(line):

    return str(line.split("IF")[1].strip())

def _isCodeBlock(line):

    line = line.upper().strip()

    if line.startswith("IF") or line.startswith("WHILE"):

        return True

    return False

def _getCodeBlock(linesIter):

    """Returns the code block starting at the given line."""

    print(f'[_getCodeBlock] : inside')

    code = []

    depth = 1

    items = list(linesIter) if not isinstance(linesIter, list) else linesIter

    for line in items:

        line = line.strip()

        print(f'[_getCodeBlock] {line}')

        if line.upper().startswith("END_"):

            print(f'[_getCodeBlock] you found THE END_')

            depth -= 1

        elif _isCodeBlock(line):

            print(f'[_getCodeBlock] you found THE SUSY')

            depth += 1

        if depth <= 0:

            print(f'[_getCodeBlock] DEPTH = 0')

            break

        code.append(line)

        print(f'[_getCodeBlock] line was added to code : {code}')

    return code

def SelectLayout(layout_key):

    layout_key = layout_key.upper()

    layout_entry = LAYOUTS_MAP.get(layout_key)

    print_with_color(f"LAYOUT_KEY: {layout_key}, LAYOUT_ENTERY: {layout_entry}", STEEL_BLUE)

    if not layout_entry:

        print(f"[INVALID_LAYOUT] {layout_key}")

        return None, None

    # import layout module

    layout_module_path = layout_entry[0]

    layout_module = __import__(layout_module_path)

    for part in layout_module_path.split(".")[1:]:

        layout_module = getattr(layout_module, part)

    # import keycode module

    keycode_module_path = layout_entry[1]

    keycode_module = __import__(keycode_module_path)

    for part in keycode_module_path.split(".")[1:]:

        keycode_module = getattr(keycode_module, part)

    # access class objects

    KeyboardLayoutClass = getattr(layout_module, "KeyboardLayout")

    KeycodeClass = getattr(keycode_module, "Keycode")

    return KeyboardLayoutClass, KeycodeClass

def extract_conditional_blocks(lines_iter):

    """Returns blocks as [(type, content_list)], skips to END_IF, handles nesting."""

    blocks = []

    nest = 0

    current = []

    blocktype = 'IF'

    lines_consumed = 0

    for line in lines_iter:

        l = line.strip()

        upl = l.upper()

        lines_consumed += 1

        if upl.startswith("IF") and not current:  # main IF line - skip it

            blocktype = 'IF'

            continue

        if upl.startswith("ELSE_IF") and nest == 0:

            blocks.append((blocktype, current))

            # Extract condition from ELSE_IF line

            condition_part = l[7:].strip()

            if condition_part.startswith('(') and condition_part.endswith(')'):

                condition_part = condition_part[1:-1]

            # Evaluate the ELSE_IF condition

            try:

                condition_part = replaceAll(condition_part)

                cond_result = evaluateExpression(condition_part)

                if cond_result and cond_result != PROBLEM_CODE:

                    blocktype = 'ELSE_IF_TRUE'

                else:

                    blocktype = 'ELSE_IF_FALSE'

            except Exception:

                blocktype = 'ELSE_IF_FALSE'

            current = []

            continue

        if upl.startswith("ELSE") and not upl.startswith("ELSE_IF") and nest == 0:

            blocks.append((blocktype, current))

            blocktype = 'ELSE'

            current = []

            continue

        if upl.startswith("END_IF") and nest == 0:

            blocks.append((blocktype, current))

            return blocks, lines_consumed

        if upl.startswith("IF"):

            nest += 1

            current.append(line)

            continue

        if upl.startswith("END_IF"):

            nest -= 1

            current.append(line)

            continue

        current.append(line)

    # Return whatever collected if EOF without END_IF

    blocks.append((blocktype, current))

    return blocks, lines_consumed

def evaluateExpression(expression):

    """Evaluates an expression with variables and returns the result."""

    # Ensure the input is a string

    expression = str(expression)

    print_with_color(f'[1_EVALUATE_EXPRESION] BEGIN, expression: "{expression}"', YELLOW)

    expression = expression.replace("^", "**")  # Replace ^ with ** for exponentiation

    expression = expression.replace("&&", "and")

    expression = expression.replace("||", "or")

    result = PROBLEM_CODE

    try:

        result = eval(expression)

        print_with_color(f'[2_EVALUATE_EXPRESION] expression: "{expression}", result "{result}"', YELLOW)

    except Exception:

        print_with_color(f"[EVALUATE_EXPRESION_ERRO] INVALID EXPRESSION: {expression}, RESULT = {result}", RED)

    return result

def convertLine(line):

    commands = []

    # loop on each key - the filter removes empty values

    for key in filter(None, line.split(" ")):

        key = key.upper()

        # find the keycode for the command in the list

        command_keycode = duckyKeys.get(key, None)

        command_consumer_keycode = duckyConsumerKeys.get(key, None)

        if command_keycode is not None:

            # if it exists in the list, use it

            commands.append(command_keycode)

        elif command_consumer_keycode is not None:

            # if it exists in the list, use it

            commands.append(1000+command_consumer_keycode)

        elif hasattr(Keycode, key):

            # if it's in the Keycode module, use it (allows any valid keycode)

            commands.append(getattr(Keycode, key))

        else:

            # if it's not a known key name, show the error for diagnosis

            print(f"Unknown key: <{key}>")

    return commands

def runScriptLine(line):

    keys = convertLine(line)

    for k in keys:

        if k > 1000:

            consumerControl.press(int(k-1000))

        else:

            kbd.press(k)

    for k in reversed(keys):

        if k > 1000:

            consumerControl.release()

        else:

            kbd.release(k)

def sendString(line):

    """Send String via HID Keyboard"""

    layout.write(line)

def replaceDefines(line):

    for define, value in defines.items():

        line = line.replace(define, str(value))

    return line

def replaceVariables(line):

    for var in variables:

        line = line.replace(var, str(variables[var]))

    for var in internalVariables:

        line = line.replace(var, str(internalVariables[var]()))

    return line

def replaceRandomVariables(expression):

    """FIXED: Proper indentation for this function"""

    if not any(var in expression for var in rng_variables):

        print_with_color(f"[RANDOM_DEBUG] Expression \"{expression}\" not in \"RNG_VARIABLES_LIST\" = {BetterListOutput(rng_variables)}", BLUE)

        return expression

    # Find all placeholders FOR $_RANDOM_[A-Z]_

    Random_matches, expression_edited, original_number = extract_random_placeholders(expression)

    print_with_color(f"\[DEBUG_Random_matches] {Random_matches}", YELLOW)

    rand_value = None

    if Random_matches:

        # Loop through matches and print details - FIXED: Proper indentation

        for random_value in Random_matches:

            rand_type = random_value[0]

            count = int(random_value[1])

            # Generate random value based on type

            if rand_type == "$_RANDOM_NUMBER":

                rand_value = ''.join(choice(RandomizeData(numbers)) for _ in range(count))

            elif rand_type == "$_RANDOM_LOWERCASE_LETTER":

                rand_value = ''.join(choice(RandomizeData(letters)) for _ in range(count))

            elif rand_type == "$_RANDOM_UPPERCASE_LETTER":

                rand_value = ''.join(choice(RandomizeData(letters.upper())) for _ in range(count))

            elif rand_type == "$_RANDOM_LETTER":

                rand_value = ''.join(choice(RandomizeData(letters + letters.upper())) for _ in range(count))

            elif rand_type == "$_RANDOM_SPECIAL":

                rand_value = ''.join(choice(RandomizeData(specialChars)) for _ in range(count))

            elif rand_type == "$_RANDOM_CHAR":

                rand_value = ''.join(choice(RandomizeData(letters + letters.upper() + numbers + specialChars)) for _ in range(count))

            # Replace the placeholder in expression

            if expression_edited:

                count = original_number

            placeholder = f"{rand_type}:{count}"

            print_with_color(f"[RANDOM_REPLACING] Replacing '{placeholder}' with '{rand_value}' in expression '{expression}'", GREEN)

            expression = expression.replace(placeholder, rand_value)

            print_with_color(f"[RANDOM_REPLACING_UPDATE] Updated expression: {expression}", GREEN)

            try:

                rand_value = int(rand_value)

                print_with_color(f"[DEBUG_RNG] next_Value_is_int = {rand_value} nice", MAGENTA)

            except ValueError:

                print_with_color(f"[DEBUG_RNG] value = {rand_value}", RED)

    return expression

def replaceAll(line, enable_replace_vars=1, enable_replace_defines=1, enable_replace_randoms=1):

    if enable_replace_defines:

        line = replaceDefines(line)

    if enable_replace_vars:

        line = replaceVariables(line)

    if enable_replace_randoms:

        line = replaceRandomVariables(line)

    return line

def extract_random_placeholders(text):

    """

    Extracts all $_RANDOM_ or $_RANDOM_: patterns.

    If number is not provided or not integer, defaults to "0".

    Returns:

    List of tuples: [(placeholder_name, number_as_string), ...]

    Example: [("$_RANDOM_NAME", "10"), ("$_RANDOM_AGE", "0")]

    """

    expression_edited = False

    pattern = re.compile(r"(\$_RANDOM_[A-Z_]+)(?::(-?\d+))?")

    print_with_color(f"[EXTRACT_RADNOM] text : {text}", CYAN)

    matches = []

    pos = 0

    Original_number = None

    number = None

    while True:

        match = pattern.search(text, pos)

        print_with_color(f"[EXTRACT_RADNOM] bool match : {match}", YELLOW)

        if not match:

            break

        name = match.group(1)

        number = match.group(2)

        Original_number = number

        print_with_color(f"[EXTRACT_RADNOM] name : {name}, number : {number}", RED)

        if number is None:

            number = "1"

        else:

            try:

                number = str(max(int(number), 1))

            except ValueError:

                number = "1"  # fallback in case of unexpected input

        matches.append((name, number))

        pos = match.end()

        if number == "1":

            expression_edited = True

    print_with_color(f"[EXTRACT_RADNOM] matches: {matches}", RED)

    return matches, expression_edited, Original_number

def RandomizeData(data):

    lst = list(str(data))

    for i in range(len(lst) - 1, 0, -1):

        j = randint(0, i)

        lst[i], lst[j] = lst[j], lst[i]

    return ''.join(lst)

def BetterListOutput(ls):

    return "[\n\t" + ",\n\t".join(

        str(i).strip() for i in ls if str(i).strip()

    ) + "\n]"

def JiggleMouse(jiggle_delay, step=1, slp=0.5):

    print(f"jiggle_delay: {jiggle_delay}, step: {step}")

    start_time = monotonic()

    while (monotonic() - start_time) < jiggle_delay:

        print(f"Moving mouse right {step} pixels")

        mouse.move(x=step, y=0)

        sleep(slp)

        print(f"Moving mouse left {step} pixels")

        mouse.move(x=-step, y=0)

        sleep(slp)

async def JiggleMouseInBackground(jiggle_delay, step=1, slp=0.5, INF=0):

    print_with_color(f"[BACKGROUND_JIGGLE_MOUSE]: jiggle_delay={jiggle_delay}, sleep={slp}, pixle_jiggle_intervale=[{-step},{step}]", BRIGHT_MAGENTA)

    if INF:

        while 1:

            mouse.move(x=step, y=0)

            await asyncio.sleep(slp)

            mouse.move(x=-step, y=0)

            await asyncio.sleep(slp)

    else:

        start_time = monotonic()

        while (monotonic() - start_time) < jiggle_delay or INF:

            print_with_color(f"Moving mouse right {step} pixels", BRIGHT_MAGENTA)

            mouse.move(x=step, y=0)

            await asyncio.sleep(slp)

            print_with_color(f"Moving mouse left {step} pixels", BRIGHT_MAGENTA)

            mouse.move(x=-step, y=0)

            await asyncio.sleep(slp)

# ======================================
# FIXED EXECUTION SYSTEM
# ======================================

def executeNestedCode(lines_list, context="general"):
    """
    Execute a list of lines with proper nested structure support.
    This replaces the problematic executeNonRecursive function.
    """
    global current_recursion_depth

    if current_recursion_depth >= MAX_RECURSION_DEPTH:
        print_with_color(f"[RECURSION_LIMIT] Maximum recursion depth reached: {MAX_RECURSION_DEPTH}", RED)
        return

    current_recursion_depth += 1

    try:
        if not lines_list:
            return

        # Create a SafeIterator for the lines
        script_iter = SafeIterator(lines_list)

        print_with_color(f"[EXECUTE_NESTED] Starting execution in context: {context}, lines: {len(lines_list)}", BRIGHT_CYAN)

        # Process each line in the nested context
        while True:
            try:
                line = next(script_iter)
                line = line.strip()

                if not line:
                    continue

                print_with_color(f"[NESTED_LINE] {line}", BRIGHT_YELLOW)

                # Update the iterator with the result from parseLine
                script_iter = parseLine(line, script_iter)

                # Small delay for default behavior
                if defaultDelay > 0:
                    sleep(float(defaultDelay) / 1000)

            except StopIteration:
                break
            except Exception as e:
                print_with_color(f"[NESTED_EXECUTION_ERROR] {e}", RED)
                break

        print_with_color(f"[EXECUTE_NESTED] Completed execution in context: {context}", BRIGHT_CYAN)

    except Exception as e:
        print_with_color(f"[EXECUTE_NESTED_FATAL] {e}", RED)
    finally:
        current_recursion_depth -= 1

def executeNonRecursive(line, remaining_lines):
    """
    FIXED: Non-recursive execution function that properly handles nested structures
    """
    global current_recursion_depth

    if current_recursion_depth >= MAX_RECURSION_DEPTH:
        print_with_color(f"[RECURSION_LIMIT] Maximum recursion depth reached: {MAX_RECURSION_DEPTH}", RED)
        return remaining_lines

    current_recursion_depth += 1

    try:
        # Execute the single line with proper context
        result_iter = parseLine(line, SafeIterator(remaining_lines))
        return list(result_iter.remaining()) if hasattr(result_iter, 'remaining') else remaining_lines

    except Exception as e:
        print_with_color(f"[EXECUTION_ERROR] {e}", RED)
        return remaining_lines
    finally:
        current_recursion_depth -= 1

def parseLine(line, script_lines):
    """FIXED: Main code handler with proper nested structure support"""
    global defaultDelay, variables, functions, defines

    line = line.strip()

    # Replace random integers
    replaced_element_rng = str(
        randint(
            int(variables.get("$_RANDOM_MIN", 0)),
            int(variables.get("$_RANDOM_MAX", 65535))
        )
    )

    line = line.replace("$_RANDOM_INT", replaced_element_rng)
    line = replaceAll(line, 0, 1, 0)

    if not line:
        return script_lines

    # Mouse commands
    if line.startswith("JIGGLE_MOUSE"):
        jiggle_delay = replaceAll(line[12:].strip())
        print(f"jiggle_delay: {jiggle_delay}")
        try:
            jiggle_delay = float(jiggle_delay) / 1000
        except ValueError:
            return script_lines
        JiggleMouse(jiggle_delay)

    elif line.startswith("BACKGROUND_JIGGLE_MOUSE"):
        try:
            jiggle_delay = replaceAll(line[23:].upper().split()[0].strip())
        except IndexError:
            jiggle_delay = "INF"
        print_with_color(f"[BACKGROUND_JIGGLE_DELAY]: jiggle_delay: {jiggle_delay}, condition: {'INF' in jiggle_delay}", BRIGHT_MAGENTA)
        if "INF" in jiggle_delay:
            asyncio.create_task(JiggleMouseInBackground(jiggle_delay, INF=1))
        else:
            try:
                jiggle_delay = float(jiggle_delay) / 1000
            except ValueError:
                return script_lines
            asyncio.create_task(JiggleMouseInBackground(jiggle_delay))
        print_with_color("CREATING_TASK: JiggleMouseInBackground", BRIGHT_MAGENTA)

    elif line.startswith("MOUSE_CLICK"):
        try:
            button = replaceAll(line[11:].upper().split()[0].strip())
        except IndexError:
            return script_lines
        print_with_color(f"[MOUSE_CLICK] button={button}", STEEL_BLUE)
        if button == "LEFT":
            mouse.click(Mouse.LEFT_BUTTON)
        elif button == "RIGHT":
            mouse.click(Mouse.RIGHT_BUTTON)
        elif button == "MIDDLE":
            mouse.click(Mouse.MIDDLE_BUTTON)

    elif line.startswith("MOUSE_PRESS"):
        try:
            button = replaceAll(line[11:].upper().split()[0].strip())
        except IndexError:
            return script_lines
        print_with_color(f"[MOUSE_PRESS] button={button}", STEEL_BLUE)
        if button == "LEFT":
            mouse.press(Mouse.LEFT_BUTTON)
        elif button == "RIGHT":
            mouse.press(Mouse.RIGHT_BUTTON)
        elif button == "MIDDLE":
            mouse.press(Mouse.MIDDLE_BUTTON)

    elif line.startswith("MOUSE_RELEASE"):
        try:
            button = replaceAll(line[13:].upper().split()[0].strip())
        except IndexError:
            return script_lines
        print_with_color(f"[MOUSE_RELEASE] button={button}", STEEL_BLUE)
        if button == "LEFT":
            mouse.release(Mouse.LEFT_BUTTON)
        elif button == "RIGHT":
            mouse.release(Mouse.RIGHT_BUTTON)
        elif button == "MIDDLE":
            mouse.release(Mouse.MIDDLE_BUTTON)

    elif line.startswith("MOUSE_MOVE"):
        line = replaceAll(line[10:].replace(",", ""))
        coords = line.split()
        if len(coords) >= 2:
            x, y = coords[0], coords[1]
            print_with_color(f"[MOUSE_MOVE] x={x}, y={y}", BRIGHT_YELLOW)
            try:
                x, y = int(x), int(y)
            except ValueError:
                print_with_color("VALUE ERROR MOUSE_MOVE", RED)
                return script_lines
            mouse.move(x=x, y=y)

    elif line.startswith("MOUSE_SCROLL"):
        line = replaceAll(line[12:].replace(",", ""))
        direction = line.upper().split()[0]
        print_with_color(f"[MOUSE_SCROLL] direction: {direction}", BRIGHT_YELLOW)
        try:
            direction = int(direction)
        except ValueError:
            print_with_color("VALUE ERROR MOUSE_SCROLL", RED)
            return script_lines
        # negative number == scroll down else : scroll up
        mouse.move(wheel=direction)

    elif line.startswith("REM_BLOCK") or line.startswith("/*"):
        # Skip comment blocks
        current_line = line
        items = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        for i, next_line in enumerate(items):
            if next_line.startswith("END_REM") or next_line.startswith("*/"):
                return SafeIterator(items[i+1:])
        return SafeIterator([])

    elif line.startswith("REM") or line.startswith("//"):
        return script_lines

    elif line.startswith("HOLD"):
        # HOLD command to press and hold a key
        key = line[4:].strip()
        key = replaceAll(key, 1, 1, 0)
        key = key.upper()
        keys_ls = key.split()
        print_with_color(f"[DEBUG_HOLD] key: {key}, keys_ls: {keys_ls}", BRIGHT_CYAN)
        if not keys_ls:
            return script_lines
        for commandKeycode in keys_ls:
            commandKeycode = duckyKeys.get(commandKeycode, None)
            if commandKeycode:
                kbd.press(commandKeycode)
            else:
                print(f"Unknown key to HOLD: <{commandKeycode}>")

    elif line.startswith("RELEASE"):
        # RELEASE command to release a held key
        key = line[8:].strip()
        key = replaceAll(key, 1, 1, 0)
        key = key.upper()
        keys_ls = key.split()
        print_with_color(f"[DEBUG_RELEASE] key: {key}, keys_ls: {keys_ls}", BRIGHT_CYAN)
        if not keys_ls:
            return script_lines
        for commandKeycode in keys_ls:
            commandKeycode = duckyKeys.get(commandKeycode, None)
            if commandKeycode:
                kbd.release(commandKeycode)
            else:
                print(f"Unknown key to RELEASE: <{commandKeycode}>")

    elif line == "RELEASE_ALL":
        # releases all keys that might be pressed, ensuring nothing is stuck
        kbd.release_all()

    elif line[0:5] == "DELAY":
        delay = line[5:].strip()
        delay = replaceAll(delay)
        delay = evaluateExpression(delay)
        print(f"[0_DELAY_DEBUG]: line={line}, delay={delay}")
        try:
            delay = int(delay)
            sleep(float(delay/1000))
        except Exception as e:
            print(f"[ANGRY_DEBUG]: Really BRO >:\ Entering This Value to DELAY: \"{delay}\"!!!!, error: {e}")

    elif line.startswith("STRINGLN_BLOCK") or line == "STRINGLN":
        print_with_color("INSIDE_STRINGLN_BLOCK")
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        print_with_color(f"ALL VALUES IN STRINGLN_BLOCK: {BetterListOutput(remaining)}")
        enable_strip = True
        i = 0
        while i < len(remaining):
            current_line = remaining[i].strip() if enable_strip else remaining[i]
            if current_line.startswith("END_STRINGLN"):
                return SafeIterator(remaining[i+1:])
            elif current_line.startswith("DISABLE_STRIP"):
                enable_strip = False
            elif current_line.startswith("ENABLE_STRIP"):
                enable_strip = True
            elif current_line.startswith("//") or current_line.startswith("REM"):
                pass  # Skip comments
            else:
                sendString(current_line)
                kbd.press(Keycode.ENTER)
                kbd.release(Keycode.ENTER)
            i += 1
        return SafeIterator([])

    elif line.startswith("STRING_BLOCK") or line == "STRING":
        print_with_color("INSIDE_STRING_BLOCK", SILVER)
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        enable_strip = True
        i = 0
        while i < len(remaining):
            current_line = remaining[i].strip() if enable_strip else remaining[i]
            if current_line.startswith("END_STRING"):
                return SafeIterator(remaining[i+1:])
            elif current_line.startswith("DISABLE_STRIP"):
                enable_strip = False
            elif current_line.startswith("ENABLE_STRIP"):
                enable_strip = True
            elif current_line.startswith("//") or current_line.startswith("REM"):
                pass  # Skip comments
            else:
                sendString(current_line)
            i += 1
        return SafeIterator([])

    elif line[0:5] == "PRINT":
        line = replaceAll(line[6:])
        print(f"[FROM_SCRIPT_TO_SERIAL_MONITOR ->^w^-> ]: {line}")

    elif line[0:8] == "STRINGLN":
        vle = replaceAll(line[9:])
        print(f"[STRINGLN_VALUE] {vle}")
        sendString(vle)
        kbd.press(Keycode.ENTER)
        kbd.release(Keycode.ENTER)

    elif line[0:6] == "STRING":
        sendString(replaceAll(line[7:]))

    elif line[0:6] == "IMPORT":
        imported_script = replaceAll(line[7:].strip().replace("'", "").replace('"', ''), 1, 1, 0)
        print(f"[IMPORTING]: {imported_script}")
        if imported_script:
            runScript(imported_script)
        else:
            print("[WARNING]: Empty import script")

    elif line[0:13] == "DEFAULT_DELAY":
        defaultDelay = line[14:].replace("=", "").strip()
        defaultDelay = replaceAll(defaultDelay)
        try:
            defaultDelay = int(defaultDelay)
        except ValueError:
            return script_lines
        print_with_color(f"[DEFAULT_DELAY]: {defaultDelay} ms", STEEL_BLUE)

    elif line[0:12] == "DEFAULTDELAY":
        defaultDelay = line[13:].replace("=", "").strip()
        defaultDelay = replaceAll(defaultDelay)
        try:
            defaultDelay = int(defaultDelay)
        except ValueError:
            return script_lines
        print_with_color(f"[DEFAULTDELAY]: {defaultDelay} ms", STEEL_BLUE)

    elif line.startswith("VAR"):
        match = re.match(r"VAR\s+\$(\w+)\s*=\s*(.+)", line)
        if match:
            varName = f"${match.group(1)}"
            varValue = match.group(2)
            print_with_color(f"[0_DEBUG_VAR] expression: {varValue}", BLUE)
            varValue = replaceAll(varValue)
            print_with_color(f"[1_DEBUG_VAR] expression: {varValue}", BLUE)
            value = evaluateExpression(varValue)
            if value == PROBLEM_CODE:
                value = varValue
            variables[varName] = value
            print(f"variable: {varName}, value: {value}")
        else:
            print(f"Invalid variable declaration: {line}")

    elif line.startswith("$"):
        match = re.match(r"\$(\w+)\s*=\s*(.+)", line)
        if match:
            varName = f"${match.group(1)}"  # $FOO
            expression = match.group(2)  # 42 + 3
            expression = replaceAll(expression)
            print_with_color(f"[DEBUG] expression: {expression}, ", BLUE)
            print_with_color(f'[0_EVALUATE_EXPRESION] BEGIN, expression: "{expression}"', GREEN)
            value = evaluateExpression(expression)  # DO MATH OPERATION AND CONDITION
            if value == PROBLEM_CODE:
                value = expression
            variables[varName] = value
            print_with_color(f"[VARIABLE_ASSIGNING] variable: {varName}, value: {value}", GREEN)
        else:
            print(f"[VARIABLE_ASSIGNING_ERROR] Invalid variable update, declare variable first: {line}")

    elif line.startswith("DEFINE"):
        define_ls = line.split()
        if len(define_ls) < 2:
            return script_lines
        defineName = define_ls[1]
        defineValue = line.split(defineName, 1)[1].strip()
        print_with_color(f"[DEFINE] line={line}, defineName={defineName}, defineValue={defineValue}", BRIGHT_BLUE)
        Calc_value = evaluateExpression(defineValue)
        if Calc_value != PROBLEM_CODE:
            defineValue = Calc_value
        defines[defineName] = defineValue
        print_with_color(f"[DEFINE] defineName={defineName}, defineValue={defineValue}", BRIGHT_BLUE)

    # ======================================
    # FIXED: FUNCTION DEFINITION WITH NESTED SUPPORT
    # ======================================
    elif line.startswith("FUNCTION"):
        func_name = line.split()[1]
        print_with_color(f"[FUNCTION_DEFINITION]: {func_name}", BRIGHT_GREEN)
        functions[func_name] = []
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        i = 0
        depth = 1  # Track nesting depth
        while i < len(remaining):
            current_line = remaining[i].strip()

            # Handle nested FUNCTION definitions
            if current_line.startswith("FUNCTION"):
                depth += 1
            elif current_line.startswith("END_FUNCTION"):
                depth -= 1
                if depth == 0:  # Found the matching END_FUNCTION
                    print_with_color(f"[FUNCTION_DEFINITION_END]: {func_name} with {len(functions[func_name])} lines", BRIGHT_GREEN)
                    return SafeIterator(remaining[i+1:])

            # Only add lines to function if we're still in the main function scope
            if depth > 0:
                functions[func_name].append(current_line)
            i += 1
        return SafeIterator([])

    # ======================================
    # FIXED: WHILE LOOP WITH NESTED SUPPORT
    # ======================================
    elif line.startswith("WHILE"):
        condition = line[5:].strip()
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)

        print_with_color(f'[WHILE_LOOP]: CONDITION = "{condition}"', BRIGHT_MAGENTA)
        print_with_color(f'[SCRIPT_LINES_REM]: {BetterListOutput(remaining)}\n', CYAN)

        # FIXED: Properly extract the loop body with nesting support
        loopCode = []
        depth = 1
        skip_count = 0

        for i, loop_line in enumerate(remaining):
            loop_line_upper = loop_line.strip().upper()

            if loop_line_upper.startswith("WHILE"):
                depth += 1
            elif loop_line_upper.startswith("END_WHILE"):
                depth -= 1
                if depth == 0:
                    skip_count = i + 1
                    break

            if depth > 0:
                loopCode.append(loop_line)

        print_with_color(f'\n[WHILE_LOOP_BODY]: {BetterListOutput(loopCode)}\n', YELLOW)

        # FIXED: Execute with proper nested support
        max_iterations = 1000
        iteration_count = 0

        while evaluateExpression(replaceAll(condition)) == True and iteration_count < max_iterations:
            print_with_color(f"[WHILE_LOOP_ITERATION]: {iteration_count + 1}", BRIGHT_BLUE)

            # FIXED: Use executeNestedCode instead of executeNonRecursive
            executeNestedCode(loopCode, f"WHILE_LOOP_{func_name if 'func_name' in locals() else 'MAIN'}")

            iteration_count += 1
            gc.collect()

        if iteration_count >= max_iterations:
            print_with_color(f"[WHILE_LOOP_LIMIT] Maximum iterations reached: {max_iterations}", RED)

        return SafeIterator(remaining[skip_count:])

    # ======================================
    # FIXED: IF STATEMENT WITH NESTED SUPPORT
    # ======================================
    elif line.upper().startswith("IF"):
        # Extract the condition for the IF
        cond_expr = line.partition("IF")[2].strip()
        if cond_expr.startswith('(') and cond_expr.endswith(')'):
            cond_expr = cond_expr[1:-1]

        print_with_color(f"[IF_STATEMENT_START] line={line}, condition={cond_expr}", BRIGHT_MAGENTA)

        # Replace variables in condition
        cond_expr_eval = replaceAll(cond_expr)
        print_with_color(f"[IF_STATEMENT_START] condition_replaced={cond_expr_eval}", BRIGHT_MAGENTA)

        # Evaluate condition
        try:
            result = evaluateExpression(cond_expr_eval)
            if result == PROBLEM_CODE:
                result = False
        except Exception as e:
            print_with_color(f"[IF_ERROR] Error evaluating condition: {e}", RED)
            result = False

        # FIXED: Collect all IF/ELSE_IF/ELSE blocks with proper nesting
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        blocks = []
        current_block = []
        block_type = 'IF'
        depth = 1
        lines_consumed = 0

        for i, block_line in enumerate(remaining):
            block_line_strip = block_line.strip()
            block_line_upper = block_line_strip.upper()
            lines_consumed = i + 1

            # Handle nested IF statements
            if block_line_upper.startswith("IF"):
                depth += 1
                current_block.append(block_line)
            elif block_line_upper.startswith("END_IF"):
                depth -= 1
                if depth == 0:  # Found the matching END_IF
                    blocks.append((block_type, current_block))
                    break
                else:
                    current_block.append(block_line)
            elif depth == 1:  # Only handle ELSE/ELSE_IF at the main level
                if block_line_upper.startswith("ELSE_IF"):
                    blocks.append((block_type, current_block))
                    # Extract and evaluate ELSE_IF condition
                    else_if_condition = block_line_strip[7:].strip()
                    if else_if_condition.startswith('(') and else_if_condition.endswith(')'):
                        else_if_condition = else_if_condition[1:-1]
                    try:
                        else_if_condition = replaceAll(else_if_condition)
                        else_if_result = evaluateExpression(else_if_condition)
                        block_type = 'ELSE_IF_TRUE' if else_if_result and else_if_result != PROBLEM_CODE else 'ELSE_IF_FALSE'
                    except Exception:
                        block_type = 'ELSE_IF_FALSE'
                    current_block = []
                elif block_line_upper.startswith("ELSE") and not block_line_upper.startswith("ELSE_IF"):
                    blocks.append((block_type, current_block))
                    block_type = 'ELSE'
                    current_block = []
                else:
                    current_block.append(block_line)
            else:
                current_block.append(block_line)

        # FIXED: Choose and execute the appropriate block
        chosen_block = None
        chosen_type = None

        if result:  # IF condition is true
            for bt, bc in blocks:
                if bt == 'IF':
                    chosen_block = bc
                    chosen_type = bt
                    break
        else:  # IF condition is false, check ELSE_IF then ELSE
            for bt, bc in blocks:
                if bt == 'ELSE_IF_TRUE':
                    chosen_block = bc
                    chosen_type = bt
                    break
                elif bt == 'ELSE':
                    chosen_block = bc
                    chosen_type = bt
                    # Don't break here, continue looking for ELSE_IF_TRUE

        # Execute the chosen block with nested support
        if chosen_block:
            print_with_color(f"[IF_EXECUTION] Executing {len(chosen_block)} lines from {chosen_type} branch", BRIGHT_GREEN)
            # FIXED: Use executeNestedCode for proper nested structure support
            executeNestedCode(chosen_block, f"IF_BLOCK_{chosen_type}")
        else:
            print_with_color("[IF_EXECUTION] No block chosen for execution", YELLOW)

        # Skip all consumed lines in the main iterator
        return SafeIterator(remaining[lines_consumed:])

    # ======================================
    # FIXED: FUNCTION EXECUTION WITH NESTED SUPPORT
    # ======================================
    elif line in functions:
        print_with_color(f"FUNCTION_EXECUTION: {line}, Content: {BetterListOutput(functions[line])}", BRIGHT_GREEN)
        # FIXED: Use executeNestedCode instead of executeNonRecursive
        executeNestedCode(functions[line], f"FUNCTION_{line}")
        gc.collect()

    else:
        runScriptLine(line)  # THE GOAT

    gc.collect()
    return script_lines

def getProgrammingStatus():
    global oneshot, progStatusPin
    pin_num = config['BOARD']['controll_mode_pin']
    if not isinstance(pin_num, int) or not hasattr(board, f"GP{pin_num}"):
        print(f"Invalid or missing pin in config, defaulting to GP{DEFAULT_PIN_NUM}")
        pin_num = DEFAULT_PIN_NUM
    pin_name = f"GP{pin_num}"
    # check GP5 for setup mode
    if oneshot:
        progStatusPin = DigitalInOut(getattr(board, pin_name))
        oneshot = False
    progStatusPin.switch_to_input(pull=Pull.UP)
    return progStatusPin.value

def runScript(duckyScriptPath):
    global defaultDelay, defines, variables, KeyboardLayout, Keycode, layout, current_recursion_depth
    restart = True

    try:
        print_with_color(f'[RUN] Injecting Keystrokes from "{duckyScriptPath}" ', BRIGHT_CYAN)

        while restart:
            restart = False
            current_recursion_depth = 0  # Reset recursion depth

            with open(duckyScriptPath, "r", encoding='utf-8') as f:
                lines = f.readlines()

            script_lines = SafeIterator(lines)
            previousLines = []

            while True:
                try:
                    line = next(script_lines)
                    line = line.strip()

                    if not line:
                        continue

                    gc.collect()
                    free_memory = gc.mem_free()
                    allocated_memory = gc.mem_alloc()
                    print_with_color(f"free_memory: {free_memory}, allocated_memory: {allocated_memory}", SILVER)

                    print_with_color(f"[MAIN_LINE] {line}", WHITE)

                    if line.startswith("SELECT_LAYOUT"):
                        ls = line.split()
                        if len(ls) < 2:
                            continue
                        new_KeyboardLayout, new_Keycode = SelectLayout(ls[1])
                        if new_KeyboardLayout and new_Keycode:
                            KeyboardLayout = new_KeyboardLayout
                            Keycode = new_Keycode
                            layout = KeyboardLayout(kbd)

                    elif line.startswith("REPEAT"):
                        line = replaceAll(line)
                        line = line.upper()
                        while " =" in line or "= " in line:
                            line = line.replace(" =", "=").replace("= ", "=")
                        print(f"treated line : {line}")
                        repeat_ls = line.split()
                        print(f"repeat_ls: {repeat_ls}")
                        if not (len(repeat_ls) >= 3 and "LINES=" in line and "TIMES=" in line):
                            print("[ERROR] Invalid REPEAT syntax")
                            continue
                        line_idx, time_idx = 0, 0
                        for index, value in enumerate(repeat_ls):
                            value = value.replace(" ", "")
                            if value.startswith("LINES="):
                                line_idx = index
                            elif value.startswith("TIMES="):
                                time_idx = index
                        print(f"LINES index: {line_idx}, TIMES index: {time_idx}")
                        if not line_idx or not time_idx:
                            continue
                        lines_value, times_value = 0, 0
                        try:
                            lines_value = int(repeat_ls[line_idx].split("=")[1].strip())
                            times_value = int(repeat_ls[time_idx].split("=")[1].strip())
                        except ValueError:
                            continue
                        print("[STARTING_REPEATING]")
                        for _ in range(times_value):
                            # repeat the last command
                            for repeated_line in previousLines[-lines_value:]:
                                executeNestedCode([repeated_line], "REPEAT")
                            sleep(float(defaultDelay) / 1000)

                    elif line.startswith("RESTART_PAYLOAD"):
                        restart = True
                        break

                    elif line.startswith("STOP_PAYLOAD"):
                        restart = False
                        break

                    else:
                        # IMPORTANT: Always update script_lines with the returned iterator
                        script_lines = parseLine(line, script_lines)
                        previousLines.append(line)

                    sleep(float(defaultDelay) / 1000)

                except StopIteration:
                    break
                except Exception as e:
                    print_with_color(f"[SCRIPT_EXECUTION_ERROR] {e}", RED)
                    break

    except OSError:
        print_with_color(f'Unable to open file "{duckyScriptPath}"', RED)
    except Exception as error:
        print_with_color(f"Error: {error}", RED)

    # Reset global state
    variables = {"$_RANDOM_MIN": 0, "$_RANDOM_MAX": 65535}
    defines = {}
    functions = {}
    current_recursion_depth = 0

    print_with_color(f"[{duckyScriptPath.upper().replace('.oqs', '')}_COMPLETED] 200", BRIGHT_GREEN)
    gc.collect()

async def blink_led(led):
    print("Blink")
    await BlinkLedPico(led)

async def BlinkLedPico(led):
    led_state = False
    min_ms = 100
    max_ms = 600
    initial_status = getProgrammingStatus()
    print(f"[BLINK] delay_intervale = [{min_ms}, {max_ms}] ms")

    while True:
        if config['BOARD']['enable_auto_switch_mode'] in [True, "True", "true", "1", 1] and initial_status != getProgrammingStatus():
            print_with_color("Changing OverQuack MODE")
            reset()
        seconds = (randint(min_ms, max_ms)) / 1000
        if led_state:
            led.value = 1
            await asyncio.sleep(seconds)
            led_state = False
        else:
            led.value = 0
            await asyncio.sleep(seconds)
            led_state = True


