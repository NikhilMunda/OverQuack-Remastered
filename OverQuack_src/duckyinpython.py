# License: GPLv2.0
# Original copyright (c) 2023 Dave Bailey
# Original Author: Dave Bailey (dbisu, @daveisu)
# Original Project name: PicoDucky
# Modifications and improvements by: VexilonHacker (@VexilonHacker)
# Copyright (c) 2025 VexilonHacker
# Original Project name : OverQuack
# Custom Edit to fix all the issues: OverQuack
# Copyright (c) 2025 NikhilMunda
# REMASTERED by 2025 NikhilMunda
# FIXED VERSION with all bug fixes applied: NikhilMunda

import asyncio
import re
import gc
from random import choice, randint
from time import monotonic, sleep
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import board  # Fixed: consolidated import
from digitalio import DigitalInOut, Pull
from microcontroller import reset
from usb_hid import devices

def _Ap_Info(elem):
    try:
        import wifi
        if elem == 'ssid':
            return config.get('AP', {}).get('ssid', 'OverQuackError')
        elif elem == 'password':
            return config.get('AP', {}).get('password', 'NeonBeonError')
        elif elem == 'bssid':
            return ":".join("{:02X}".format(b) for b in wifi.radio.mac_address)
    except ImportError:
        pass
    return ""

def _capsOn():
    return 1 if kbd.led_on(Keyboard.LED_CAPS_LOCK) else 0

def _numOn():
    return 1 if kbd.led_on(Keyboard.LED_NUM_LOCK) else 0

def _scrollOn():
    return 1 if kbd.led_on(Keyboard.LED_SCROLL_LOCK) else 0

duckyKeys = {
    '0': Keycode.ZERO, '1': Keycode.ONE, '2': Keycode.TWO, '3': Keycode.THREE, '4': Keycode.FOUR, '5': Keycode.FIVE,
    '6': Keycode.SIX, '7': Keycode.SEVEN, '8': Keycode.EIGHT, '9': Keycode.NINE,
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
    'MK_VOLUP': ConsumerControlCode.VOLUME_INCREMENT,
    'MK_VOLDOWN': ConsumerControlCode.VOLUME_DECREMENT,
    'MK_MUTE': ConsumerControlCode.MUTE,
    'MK_NEXT': ConsumerControlCode.SCAN_NEXT_TRACK,
    'MK_PREV': ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    'MK_PP': ConsumerControlCode.PLAY_PAUSE,
    'MK_STOP': ConsumerControlCode.STOP
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

# Global state
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

# Fixed configuration constants
DEFAULT_PIN_NUM = 5
oneshot = True
progStatusPin = None

# Initialize HID devices
kbd = Keyboard(devices)
consumerControl = ConsumerControl(devices)
layout = KeyboardLayout(kbd)
mouse = Mouse(devices)

# Fixed recursion and iteration limits
MAX_RECURSION_DEPTH = 20
MAX_ITERATIONS = 100000
current_recursion_depth = 0
iteration_count = 0

PROBLEM_CODE = "ERROR404"

# Color codes for output
RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_YELLOW = "\033[93m"
STEEL_BLUE = "\033[38;2;70;130;180m"
SILVER = "\033[38;2;192;192;192m"
GOLD = "\033[38;2;255;215;0m"

# Fixed SafeIterator class
class SafeIterator:
    """Safer iterator that prevents infinite loops"""
    def __init__(self, iterable):
        self.items = list(iterable) if not isinstance(iterable, list) else iterable
        self.index = 0
        self.max_iterations = max(len(self.items) * 2, 1000)  # Fixed: minimum safety limit

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
    """Fixed: Reduced console output for performance"""
    if isinstance(STRING, str) and len(STRING) < 200:  # Only print short messages
        print(f"{COLOR}{STRING}{RESET}", sep=sep, end=end)

def LoadJsonConf(json_file="config.json"):
    """Fixed: Better error handling for JSON config loading"""
    import json

    default_config = {
        'DEFAULT_PAYLOAD': "payload.oqs",
        'BOARD': {
            'enable_auto_reload': False,
            'enable_auto_switch_mode': True,
            'controll_mode_pin': 5
        },
        'AP': {
            "ssid": "OverQuackError",
            "password": "NeonBeonError", 
            "channel": 6,
            "ip_address": "192.168.4.1",
            "ports": [80, 8000, 8080]
        }
    }

    try:
        with open(json_file, "r") as f:
            config = json.load(f)
            print_with_color(f"Config loaded successfully from {json_file}", GREEN)
            return config
    except (OSError, ValueError) as e:
        print_with_color(f"Config load error: {e}, using defaults", RED)
        return default_config

config = LoadJsonConf()

def safe_eval(expression, local_vars=None):
    """Fixed: Safe expression evaluator to replace eval"""
    if local_vars is None:
        local_vars = {}

    # Simple safe evaluation for basic expressions
    allowed_operators = [
        '+','-','*','/','(',')',' ','and','or','not',
        '==','!=','>','<','>=','<=','**'
    ]

    # Check for dangerous operations
    dangerous = ['import','exec','eval','__','open','file']
    if any(d in str(expression).lower() for d in dangerous):
        raise ValueError("Unsafe expression")

    try:
        # Replace logical operators
        expr_str = (
            str(expression)
            .replace("&&", "and")
            .replace("||", "or")
            .replace("^", "**")
        )

        # Create safe globals with only builtins and provided locals
        safe_globals = {
            "__builtins__": {
                "abs": abs,
                "int": int,
                "float": float,
                "str": str,
                "len": len
            }
        }
        # Unpack the dict directly; no parentheses
        safe_globals.update(local_vars)

        return eval(expr_str, safe_globals, {})
    except Exception as e:
        raise ValueError(f"Expression eval error: {e}")


def evaluateExpression(expression):
    """Fixed: Uses safe_eval instead of eval"""
    expression = str(expression)
    expression = expression.replace("^^", "**")
    expression = expression.replace("&&", "and")
    expression = expression.replace("||", "or")

    try:
        # Merge all variable dictionaries for evaluation
        all_vars = {}
        all_vars.update(variables)
        for var, func in internalVariables.items():
            try:
                all_vars[var] = func()
            except:
                all_vars[var] = 0

        result = safe_eval(expression, all_vars)
        return result if result != PROBLEM_CODE else False
    except Exception as e:
        print_with_color(f"Invalid expression: {expression}, error: {e}", RED)
        return PROBLEM_CODE

def _getCodeBlock(lines_iter, start_kw="", end_kw=""):
    """Fixed: Consolidated code block extraction with proper nesting"""
    code = []
    depth = 1
    items = list(lines_iter) if not isinstance(lines_iter, list) else lines_iter

    i = 0
    while i < len(items) and depth > 0:
        line = items[i].strip().upper()

        if start_kw and line.startswith(start_kw):
            depth += 1
        elif end_kw and line.startswith(end_kw):
            depth -= 1

        if depth > 0:
            code.append(items[i])
        i += 1

    if depth > 0:
        raise SyntaxError(f"Missing {end_kw} for {start_kw}")

    return code, i

def extract_conditional_blocks(lines_iter):
    """Fixed: Improved conditional block extraction"""
    blocks = []
    current = []
    blocktype = 'IF'
    nest = 0
    lines_consumed = 0

    lines_list = list(lines_iter) if not isinstance(lines_iter, list) else lines_iter

    for i, line in enumerate(lines_list):
        l = line.strip()
        upl = l.upper()
        lines_consumed = i + 1

        if upl.startswith("IF") and nest == 0 and not current:
            blocktype = 'IF'
            continue

        if upl.startswith("IF"):
            nest += 1
        elif upl.startswith("END_IF"):
            nest -= 1
            if nest < 0:
                blocks.append((blocktype, current))
                return blocks, lines_consumed

        if nest == 0:
            if upl.startswith("ELSE_IF"):
                blocks.append((blocktype, current))
                condition_part = l[7:].strip()
                if condition_part.startswith('(') and condition_part.endswith(')'):
                    condition_part = condition_part[1:-1]

                try:
                    condition_part = replaceAll(condition_part)
                    cond_result = evaluateExpression(condition_part)
                    blocktype = 'ELSE_IF_TRUE' if cond_result and cond_result != PROBLEM_CODE else 'ELSE_IF_FALSE'
                except Exception:
                    blocktype = 'ELSE_IF_FALSE'

                current = []
                continue

            elif upl.startswith("ELSE") and not upl.startswith("ELSE_IF"):
                blocks.append((blocktype, current))
                blocktype = 'ELSE'
                current = []
                continue

        current.append(line)

    blocks.append((blocktype, current))
    return blocks, lines_consumed

def replaceDefines(line):
    """Replace defines in line"""
    for define, value in defines.items():
        line = line.replace(define, str(value))
    return line


def SelectLayout(layout_key):
    """Fixed: Layout selection function"""
    global KeyboardLayout, Keycode, layout

    layout_key = layout_key.upper()
    layout_entry = LAYOUTS_MAP.get(layout_key)
    print_with_color(f"LAYOUT_KEY: {layout_key}, LAYOUT_ENTRY: {layout_entry}", STEEL_BLUE)

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



def replaceVariables(line):
    """Replace variables in line"""
    for var in variables:
        line = line.replace(var, str(variables[var]))
    for var in internalVariables:
        try:
            line = line.replace(var, str(internalVariables[var]()))
        except:
            line = line.replace(var, "0")
    return line

def extract_random_placeholders(text):
    """Extract random placeholders from text"""
    expression_edited = False
    pattern = re.compile(r"(\$_RANDOM_[A-Z_]+)(?::(-?\d+))?")
    matches = []
    pos = 0
    original_number = None

    while True:
        match = pattern.search(text, pos)
        if not match:
            break

        name = match.group(1)
        number = match.group(2)
        original_number = number

        if number is None:
            number = "1"
        else:
            try:
                number = str(max(int(number), 1))
            except ValueError:
                number = "1"

        matches.append((name, number))
        pos = match.end()

        if number == "1":
            expression_edited = True

    return matches, expression_edited, original_number

def RandomizeData(data):
    """Randomize string data"""
    lst = list(str(data))
    for i in range(len(lst) - 1, 0, -1):
        j = randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

def replaceRandomVariables(expression):
    """Fixed: Improved random variable replacement"""
    if not any(var in expression for var in rng_variables):
        return expression

    random_matches, expression_edited, original_number = extract_random_placeholders(expression)

    for random_value in random_matches:
        rand_type = random_value[0]
        count = int(random_value[1])

        # Generate random value based on type
        if rand_type == "$_RANDOM_NUMBER":
            rand_value = ''.join(choice(numbers) for _ in range(count))
        elif rand_type == "$_RANDOM_LOWERCASE_LETTER":
            rand_value = ''.join(choice(letters) for _ in range(count))
        elif rand_type == "$_RANDOM_UPPERCASE_LETTER":
            rand_value = ''.join(choice(letters.upper()) for _ in range(count))
        elif rand_type == "$_RANDOM_LETTER":
            rand_value = ''.join(choice(letters + letters.upper()) for _ in range(count))
        elif rand_type == "$_RANDOM_SPECIAL":
            rand_value = ''.join(choice(specialChars) for _ in range(count))
        elif rand_type == "$_RANDOM_CHAR":
            rand_value = ''.join(choice(letters + letters.upper() + numbers + specialChars) for _ in range(count))
        else:
            rand_value = ""

        # Replace placeholder in expression
        if expression_edited:
            count = original_number if original_number else count

        placeholder = f"{rand_type}:{count}"
        expression = expression.replace(placeholder, rand_value)

    return expression

def replaceAll(line, enable_replace_vars=1, enable_replace_defines=1, enable_replace_randoms=1):
    """Fixed: Replace all variables and defines in line"""
    if enable_replace_defines:
        line = replaceDefines(line)
    if enable_replace_vars:
        line = replaceVariables(line)
    if enable_replace_randoms:
        line = replaceRandomVariables(line)
    return line

def convertLine(line):
    """Convert line to key commands"""
    commands = []
    for key in filter(None, line.split(" ")):
        key = key.upper()
        command_keycode = duckyKeys.get(key, None)
        command_consumer_keycode = duckyConsumerKeys.get(key, None)

        if command_keycode is not None:
            commands.append(command_keycode)
        elif command_consumer_keycode is not None:
            commands.append(1000+command_consumer_keycode)
        elif hasattr(Keycode, key):
            commands.append(getattr(Keycode, key))
        else:
            print_with_color(f"Unknown key: <{key}>", RED)

    return commands

def runScriptLine(line):
    """Execute a script line as key presses"""
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
    """Send string via HID Keyboard"""
    layout.write(line)

def BetterListOutput(ls):
    """Format list output for debugging"""
    return "[\n\t" + ",\n\t".join(str(i).strip() for i in ls if str(i).strip()) + "\n]"


def JiggleMouse(jiggle_delay, step=1, slp=0.5):
    """Jiggle mouse for specified duration"""
    print(f"jiggle_delay: {jiggle_delay}, step: {step}")
    start_time = monotonic()
    while (monotonic() - start_time) < jiggle_delay:
        print(f"Moving mouse right {step} pixels")
        mouse.move(x=step, y=0)
        sleep(slp)
        print(f"Moving mouse left {step} pixels")
        mouse.move(x=-step, y=0)
        sleep(slp)

def executeNestedCode(lines_list, context="general"):
    """Fixed: Execute nested code with proper recursion management"""
    global current_recursion_depth, iteration_count

    if current_recursion_depth >= MAX_RECURSION_DEPTH:
        print_with_color(f"Recursion limit reached: {MAX_RECURSION_DEPTH}", RED)
        return

    if iteration_count > MAX_ITERATIONS:
        print_with_color(f"Iteration limit reached: {MAX_ITERATIONS}", RED)
        return

    current_recursion_depth += 1
    try:
        if not lines_list:
            return

        script_iter = SafeIterator(lines_list)

        while True:
            try:
                line = next(script_iter)
                line = line.strip()
                if not line:
                    continue

                iteration_count += 1
                script_iter = parseLine(line, script_iter)

                if defaultDelay > 0:
                    sleep(float(defaultDelay) / 1000)

            except StopIteration:
                break
            except Exception as e:
                print_with_color(f"Nested execution error: {e}", RED)
                break

    finally:
        current_recursion_depth -= 1

def parseLine(line, script_lines):
    """Fixed: Main line parser with all bug fixes"""
    global defaultDelay, variables, functions, defines, iteration_count

    line = line.strip()
    if not line:
        return script_lines

    # Fixed: Check iteration limit
    iteration_count += 1
    if iteration_count > MAX_ITERATIONS:
        print_with_color("Script exceeded maximum iterations", RED)
        return script_lines

    # Replace random integers
    replaced_element_rng = str(randint(
        int(variables.get("$_RANDOM_MIN", 0)),
        int(variables.get("$_RANDOM_MAX", 65535))
    ))
    line = line.replace("$_RANDOM_INT", replaced_element_rng)
    line = replaceAll(line, 0, 1, 0)

    if not line:
        return script_lines

    # Fixed: Better comment handling
    if line.startswith("REM_BLOCK") or line.startswith("/*"):
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        comment_depth = 1

        for i, next_line in enumerate(remaining):
            next_line_strip = next_line.strip()
            if next_line_strip.startswith("REM_BLOCK") or next_line_strip.startswith("/*"):
                comment_depth += 1
            elif next_line_strip.startswith("END_REM") or next_line_strip.startswith("*/"):
                comment_depth -= 1
                if comment_depth == 0:
                    return SafeIterator(remaining[i+1:])

        print_with_color("Warning: Unclosed comment block", YELLOW)
        return SafeIterator([])

    if line.startswith("REM") or line.startswith("//"):
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
        return script_lines

    if line.startswith("BACKGROUND_JIGGLE_MOUSE"):
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
        return script_lines
  
  
    # Mouse commands
    if line.startswith("MOUSE_CLICK"):
        try:
            button = replaceAll(line[11:].upper().split()[0].strip())
            if button == "LEFT":
                mouse.click(Mouse.LEFT_BUTTON)
            elif button == "RIGHT":
                mouse.click(Mouse.RIGHT_BUTTON)
            elif button == "MIDDLE":
                mouse.click(Mouse.MIDDLE_BUTTON)
        except (IndexError, AttributeError):
            pass
        return script_lines
    
    if line.startswith("MOUSE_PRESS"):
        try:
            button = replaceAll(line[11:].upper().split()[0].strip())
            if button == "LEFT":
                mouse.press(Mouse.LEFT_BUTTON)
            elif button == "RIGHT":
                mouse.press(Mouse.RIGHT_BUTTON)
            elif button == "MIDDLE":
                mouse.press(Mouse.MIDDLE_BUTTON)
        except (IndexError, AttributeError):
            pass
        return script_lines

    if line.startswith("MOUSE_RELEASE"):
        try:
            button = replaceAll(line[13:].upper().split()[0].strip())
            if button == "LEFT":
                mouse.release(Mouse.LEFT_BUTTON)
            elif button == "RIGHT":
                mouse.release(Mouse.RIGHT_BUTTON)
            elif button == "MIDDLE":
                mouse.release(Mouse.MIDDLE_BUTTON)
        except (IndexError, AttributeError):
            pass
        return script_lines


    if line.startswith("MOUSE_MOVE"):
        try:
            coords_str = replaceAll(line[10:].replace(",", ""))
            coords = coords_str.split()
            if len(coords) >= 2:
                x, y = int(coords[0]), int(coords[1])
                mouse.move(x=x, y=y)
        except (ValueError, IndexError):
            print_with_color("Invalid MOUSE_MOVE coordinates", RED)
        return script_lines
    
    if line.startswith("MOUSE_SCROLL"):
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
        return script_lines
    

    # Key commands
    if line.startswith("HOLD"):
        key = replaceAll(line[4:].strip()).upper()
        for commandKeycode in key.split():
            keycode = duckyKeys.get(commandKeycode, None)
            if keycode:
                kbd.press(keycode)
        return script_lines

    if line.startswith("RELEASE"):
        if line.strip() == "RELEASE_ALL":
            kbd.release_all()
        else:
            key = replaceAll(line[7:].strip()).upper()
            for commandKeycode in key.split():
                keycode = duckyKeys.get(commandKeycode, None)
                if keycode:
                    kbd.release(keycode)
        return script_lines

    # Delay command
    if line.startswith("DELAY"):
        delay = replaceAll(line[5:].strip())
        delay_result = evaluateExpression(delay)
        if delay_result != PROBLEM_CODE:
            try:
                sleep(float(delay_result) / 1000)
            except (ValueError, TypeError):
                print_with_color(f"Invalid delay value: {delay}", RED)
        return script_lines

    # String commands
    if line.startswith("STRING"):
        if line.startswith("STRINGLN_BLOCK"):
            print_with_color("INSIDE_STRINGLN_BLOCK", CYAN)
            remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
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
                    pass # Skip comments
                else:
                    sendString(replaceAll(current_line))
                    kbd.press(Keycode.ENTER)
                    kbd.release(Keycode.ENTER)
                i += 1
            return SafeIterator([])

        elif line.startswith("STRING_BLOCK"):
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
                    pass # Skip comments
                else:
                    sendString(replaceAll(current_line))
                i += 1
            return SafeIterator([])

        elif line.startswith("STRINGLN"):
            sendString(replaceAll(line[8:].strip()))
            kbd.press(Keycode.ENTER)
            kbd.release(Keycode.ENTER)
        else:
            sendString(replaceAll(line[6:].strip()))
        return script_lines

    # Print command
    if line.startswith("PRINT"):
        print(f"[SCRIPT OUTPUT]: {replaceAll(line[5:])}")
        return script_lines

    # Import command - Fixed: Better error handling
    if line.startswith("IMPORT"):
        imported_script = replaceAll(line[6:].strip().replace("'", "").replace('"', ''))
        if imported_script:
            try:
                runScript(imported_script)
            except OSError:
                print_with_color(f"Cannot import script: {imported_script}", RED)
        return script_lines

    # Payload control commands
    if line.startswith("RESTART_PAYLOAD"):
        # This will be handled at a higher level in runScript
        return script_lines

    if line.startswith("STOP_PAYLOAD"):
        # This will be handled at a higher level in runScript
        return script_lines

    # Function execution
    if line in functions:
        print_with_color(f"FUNCTION_EXECUTION: {line}, Content: {BetterListOutput(functions[line])}", BRIGHT_GREEN)
        # FIXED: Use executeNestedCode instead of executeNonRecursive
        executeNestedCode(functions[line], f"FUNCTION_{line}")
        gc.collect()
        return script_lines    


    # Default delay
    if line.startswith("DEFAULT_DELAY") or line.startswith("DEFAULTDELAY"):
        prefix_len = 13 if line.startswith("DEFAULT_DELAY") else 12
        delay_str = line[prefix_len:].replace("=", "").strip()
        delay_val = evaluateExpression(replaceAll(delay_str))
        if delay_val != PROBLEM_CODE:
            try:
                defaultDelay = int(delay_val)
                print_with_color(f"Default delay set to: {defaultDelay}ms", BLUE)
            except (ValueError, TypeError):
                print_with_color(f"Invalid default delay: {delay_str}", RED)
        return script_lines

    # Variable assignment
    if line.startswith("VAR") or line.startswith("$"):
        pattern = r"(?:VAR\s+)?(\$\w+)\s*=\s*(.+)"
        match = re.match(pattern, line)
        if match:
            var_name = match.group(1)
            expression = replaceAll(match.group(2))
            value = evaluateExpression(expression)
            if value == PROBLEM_CODE:
                value = expression
            variables[var_name] = value
            print_with_color(f"Variable set: {var_name} = {value}", GREEN)
        return script_lines

    # Define command
    if line.startswith("DEFINE"):
        parts = line.split(None, 2)
        if len(parts) >= 3:
            define_name = parts[1]
            define_value = parts[2]
            calc_value = evaluateExpression(define_value)
            if calc_value != PROBLEM_CODE:
                define_value = calc_value
            defines[define_name] = define_value
            print_with_color(f"Define set: {define_name} = {define_value}", BLUE)
        return script_lines

    # Fixed: Function definition
    if line.startswith("FUNCTION"):
        func_name = line.split()[1]
        functions[func_name] = []
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)

        depth = 1
        i = 0
        while i < len(remaining) and depth > 0:
            current_line = remaining[i].strip()
            if current_line.startswith("FUNCTION"):
                depth += 1
            elif current_line.startswith("END_FUNCTION"):
                depth -= 1
                if depth == 0:
                    return SafeIterator(remaining[i+1:])

            if depth > 0:
                functions[func_name].append(current_line)
            i += 1

        return SafeIterator([])

    # Fixed: While loop
    if line.startswith("WHILE"):
        condition = line[5:].strip()
        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)

        loop_code, skip_count = _getCodeBlock(remaining, "WHILE", "END_WHILE")

        max_iterations = 1000
        loop_iteration = 0

        while evaluateExpression(replaceAll(condition)) and loop_iteration < max_iterations:
            executeNestedCode(loop_code, f"WHILE_LOOP_{loop_iteration}")
            loop_iteration += 1

        if loop_iteration >= max_iterations:
            print_with_color("While loop iteration limit reached", RED)

        return SafeIterator(remaining[skip_count:])

    # Fixed: If statement
    if line.upper().startswith("IF"):
        cond_expr = line.partition("IF")[2].strip()
        if cond_expr.startswith('(') and cond_expr.endswith(')'):
            cond_expr = cond_expr[1:-1]

        cond_result = evaluateExpression(replaceAll(cond_expr))
        if cond_result == PROBLEM_CODE:
            cond_result = False

        remaining = list(script_lines.remaining()) if hasattr(script_lines, 'remaining') else list(script_lines)
        blocks, lines_consumed = extract_conditional_blocks(SafeIterator(remaining))

        # Choose block to execute
        chosen_block = None
        if cond_result:
            for bt, bc in blocks:
                if bt == 'IF':
                    chosen_block = bc
                    break
        else:
            for bt, bc in blocks:
                if bt == 'ELSE_IF_TRUE':
                    chosen_block = bc
                    break
                elif bt == 'ELSE':
                    chosen_block = bc

        if chosen_block:
            executeNestedCode(chosen_block, "IF_BLOCK")

        return SafeIterator(remaining[lines_consumed:])

    # Fixed: Repeat command with bounds check
    if line.startswith("REPEAT"):
        try:
            # Parse REPEAT LINES=x TIMES=y format
            line_upper = replaceAll(line).upper().replace(" =", "=").replace("= ", "=")
            parts = line_upper.split()

            lines_value = times_value = 0
            for part in parts:
                if part.startswith("LINES="):
                    lines_value = int(part.split("=")[1])
                elif part.startswith("TIMES="):
                    times_value = int(part.split("=")[1])

            if lines_value > 0 and times_value > 0:
                # Get previous lines - Fixed: bounds check
                import __main__
                if hasattr(__main__, 'previousLines'):
                    prev_lines = __main__.previousLines
                    if lines_value <= len(prev_lines):
                        for _ in range(times_value):
                            for repeated_line in prev_lines[-lines_value:]:
                                executeNestedCode([repeated_line], "REPEAT")
                    else:
                        print_with_color(f"REPEAT: Not enough previous lines ({lines_value} requested, {len(prev_lines)} available)", RED)

        except (ValueError, IndexError, AttributeError):
            print_with_color("Invalid REPEAT syntax", RED)

        return script_lines

    # Function execution
    if line in functions:
        executeNestedCode(functions[line], f"FUNCTION_{line}")
        return script_lines

    # Default: execute as key combination
    runScriptLine(line)
    return script_lines

def getProgrammingStatus():
    """Get programming status from pin"""
    global oneshot, progStatusPin

    pin_num = config.get('BOARD', {}).get('controll_mode_pin', DEFAULT_PIN_NUM)
    if not isinstance(pin_num, int):
        pin_num = DEFAULT_PIN_NUM

    pin_name = f"GP{pin_num}"

    if oneshot:
        try:
            progStatusPin = DigitalInOut(getattr(board, pin_name))
            progStatusPin.switch_to_input(pull=Pull.UP)
            oneshot = False
        except AttributeError:
            print_with_color(f"Pin {pin_name} not found", RED)
            return True

    return progStatusPin.value if progStatusPin else True

def runScript(duckyScriptPath):
    """Fixed: Main script execution function"""
    global defaultDelay, defines, variables, current_recursion_depth, iteration_count

    try:
        print_with_color(f'Running script: {duckyScriptPath}', BRIGHT_CYAN)

        # Reset global state
        current_recursion_depth = 0
        iteration_count = 0
        restart = True

        while restart:
            restart = False

            try:
                with open(duckyScriptPath, "r", encoding='utf-8') as f:
                    lines = f.readlines()

                script_lines = SafeIterator(lines)
                previous_lines = []

                # Make previousLines available globally for REPEAT
                import __main__
                __main__.previousLines = previous_lines

                while True:
                    try:
                        line = next(script_lines)
                        line = line.strip()
                        if not line:
                            continue

                        if line.startswith("RESTART_PAYLOAD"):
                            restart = True
                            break
                        elif line.startswith("STOP_PAYLOAD"):
                            restart = False
                            break
                        else:
                            script_lines = parseLine(line, script_lines)
                            previous_lines.append(line)

                            if defaultDelay > 0:
                                sleep(float(defaultDelay) / 1000)

                    except StopIteration:
                        break
                    except Exception as e:
                        print_with_color(f"Script execution error: {e}", RED)
                        break

            except OSError:
                print_with_color(f'Unable to open file "{duckyScriptPath}"', RED)
                break
            except Exception as e:
                print_with_color(f"Script error: {e}", RED)
                break

    except Exception as e:
        print_with_color(f"Fatal script error: {e}", RED)

    finally:
        # Reset global state
        variables = {"$_RANDOM_MIN": 0, "$_RANDOM_MAX": 65535}
        defines = {}
        functions = {}
        current_recursion_depth = 0
        iteration_count = 0
        print_with_color(f"Script completed: {duckyScriptPath}", BRIGHT_GREEN)

# Async functions for background operations
async def JiggleMouseInBackground(jiggle_delay, step=1, slp=0.5, INF=0):
    print_with_color(f"[BACKGROUND_JIGGLE_MOUSE]: jiggle_delay={jiggle_delay}, sleep={slp}, pixle_jiggle_intervale=[{-step},{step}]", BRIGHT_MAGENTA)
    if INF:
        while True:
            mouse.move(x=step, y=0)
            await asyncio.sleep(slp)
            mouse.move(x=-step, y=0)
            await asyncio.sleep(slp)
    else:
        start_time = monotonic()
        while (monotonic() - start_time) < jiggle_delay:
            mouse.move(x=step, y=0)
            await asyncio.sleep(slp)
            mouse.move(x=-step, y=0)
            await asyncio.sleep(slp)

async def BlinkLedPico(led):
    """Background LED blink function"""
    led_state = False
    min_ms = 100
    max_ms = 600
    initial_status = getProgrammingStatus()

    while True:
        if (config.get('BOARD', {}).get('enable_auto_switch_mode', False) and 
            initial_status != getProgrammingStatus()):
            print_with_color("Mode change detected", YELLOW)
            reset()

        seconds = randint(min_ms, max_ms) / 1000
        led.value = 1 if not led_state else 0
        await asyncio.sleep(seconds)
        led_state = not led_state

# Main execution entry point5
if __name__ == "__main__":
    payload_file = config.get('DEFAULT_PAYLOAD', 'payload.oqs')
    if getProgrammingStatus():
        print_with_color("Programming mode enabled", GREEN)
    else:
        print_with_color(f"Executing payload: {payload_file}", BRIGHT_CYAN)
        runScript(payload_file)

