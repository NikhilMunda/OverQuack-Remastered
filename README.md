## 🦆 OverQuack-Remastered
OverQuack-Remastered is a feature-rich, Rubber Ducky-style HID attack tool for the Raspberry Pi Pico family, supporting wireless payloads, mouse and keyboard injection, cross-platform compatibility, and fully customizable scripting and configuration.

## 🫡 Acknowledgments

This is the REMASTERED version of [VexilonHacker/OverQuack](https://github.com/VexilonHacker/OverQuack) and some [dbisu/pico-ducky](https://github.com/dbisu/pico-ducky). I liked their project so I thought on tweaking and fixing some of the Codes. I love Raspberry Pico W 💕 how well it worked with OverQuack code.

## 🚀 Features

Full DuckyScript 3.0 support: Includes custom variables, functions, logic, and advanced blocks

All Pico variants: Works with Pico, Pico W, Pico 2, Pico 2 W

Wireless payloads: Upload, execute, and manage scripts remotely via Wi-Fi (Pico W/2W)

Plug & Play: Automatic Mass Storage ↔ HID switching (toggle via GPIO pin)

Cross-platform payloads: Supports Windows, Mac, and Linux, Android

Mouse & Keyboard injection: Precise mouse move/click/jiggle and full keyboard control

Modular and extensible: Easy script imports, custom layouts, and debugging via serial

Easy configuration: All settings adjustable with config.json

## :wrench: UPDATE v 1.0
The Update version now includes:

✅ Core Execution System
Complete executeNestedCode function with proper recursion handling

Memory management with garbage collection

✅ Advanced Control Structures
IF/ELSE_IF/END_IF with proper condition evaluation and nesting support

FUNCTION/END_FUNCTION definition and execution with nested support

WHILE/END_WHILE loops with iteration limits and nesting support

✅ Enhanced String Handling
STRING_BLOCK/END_STRING for multi-line string output

STRINGLN_BLOCK/END_STRINGLN for multi-line string with newlines

DISABLE_STRIP/ENABLE_STRIP formatting control

✅ Complete Mouse Support
MOUSE_CLICK (LEFT/RIGHT/MIDDLE)

MOUSE_PRESS and MOUSE_RELEASE

MOUSE_MOVE with coordinates

MOUSE_SCROLL with direction

JIGGLE_MOUSE and BACKGROUND_JIGGLE_MOUSE with asyncio support

✅ Advanced Key Management
HOLD and RELEASE commands for individual keys

RELEASE_ALL for clearing all pressed keys

Proper key state management

✅ Script Control Features
REPEAT command with LINES= and TIMES= syntax

SELECT_LAYOUT for keyboard layout switching

RESTART_PAYLOAD and STOP_PAYLOAD commands

IMPORT script functionality

✅ Enhanced Variable System
Fixed random variable replacement with proper regex parsing

Safe expression evaluation (replacing dangerous eval with safe_eval)

Comprehensive variable and define replacement

Internal variables for system state

✅ Debugging and Output
BetterListOutput function for formatted debugging

Color-coded console output system

Comprehensive error messages and status reporting

PRINT command for script output

## Open source, GPLv2.0

## 📦 Quick Start
Clone the repo:

shell
git clone https://github.com/NikhilMunda/OverQuack-Remastered.git


## Configure:

Edit config.json for board settings, Wi-Fi/AP, payloads, and pins

## 📱 setup it manually

Download repo: [HERE](https://github.com/NikhilMunda/OverQuack-Remastered/archive/refs/heads/main.zip)

Plug your Pico into USB while holding the BOOTSEL button for 3 seconds, then release it. It will show up as "RPI-RP2".

Copy OverQuack_installation/firmwares/flash_nuke.uf2 to the RPI-RP2 drive and wait for the Pico to finish rebooting.

Copy OverQuack_installation/firmwares/adafruit-circuitpython-raspberry_pi_<YOUR_PICO_MODULE>-en_US-9.2.1.uf2 to the RPI-RP2 drive and wait for the Pico to finish rebooting and it going to show up as "CIRCUITPY".

<details>
  <summary>Available firmwares</summary>
  
  ```
  -adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.1.uf2
  -adafruit-circuitpython-raspberry_pi_pico2-en_US-9.2.1.uf2
  -adafruit-circuitpython-raspberry_pi_pico2_w-en_US-9.2.1.uf2
  -adafruit-circuitpython-raspberry_pi_pico_w-en_US-9.2.8.uf2
  ```
</details>

⚠️NOTE: If you want, you can edit/config the file before going to the next step else you will not be able to edit/config later.

copy all content of OverQuack_src to CIRCUITPY

Setup complete. OverQuack is ready to use. Proceed with your tasks responsibly.

## Toggle mode:

Connect a switch between GPIO 5 and GND to switch HID/Mass Storage without replugging

OR You can connect a wire between GPIO 5 and GND to switch HID and remove the wire to switch Mass Storage

## Wireless control:

Run and manage payloads from another device with OverQuack_client.go (Pico W/2W only)

Have support for Android App [OverQuack_Client](https://github.com/NikhilMunda/OverQuack_App/)

<img width="240" height="540" alt="image" src="https://github.com/user-attachments/assets/1787ea3c-95b4-42b6-9333-24481db67266" /> <img width="240" height="540" alt="image" src="https://github.com/user-attachments/assets/5e2ca8f1-64f1-40b3-ac2c-3d27b8938996" />

⚙️ Highlights
Advanced Scripting: DuckyScript with variables, logic, comments, blocks, random/gen functions, imports, and more

Keyboard Layouts: US, FR, DE, and more—easily extend or create your own

Debug & Development: Serial monitor output, debug messages with PRINT, and importable payload chains

Works Everywhere: Windows, Linux, macOS; wireless on supported hardware

## 🖥️ Accessing the Serial Monitor

🔧 For Linux Users:

You can use picocom to access the serial monitor. Install it using your package manager, then run the following command:
```
while true; do if [ -e /dev/ttyACM0 ]; then picocom -b 9600 /dev/ttyACM0; fi; sleep 1; done
```

ℹ️ This command continuously checks for /dev/ttyACM0 and connects when available.

You'll see ongoing output in the terminal.

PRINT messages are color-coded for easier readability.

This works in both Storage Device Mode and HID Mode.

## 🪟 For Windows Users:

You can use PuTTY to access the serial monitor.

 1. Connect your device via USB.

 2. Open the app (PuTTY or Tera Term).

 3. Choose Serial as the connection type.

 4. Set the COM port (e.g., COM3) and baud rate to 9600.

 5. Start the session to begin viewing output.

💡 Tip: You can find your device's COM port in Device Manager under Ports (COM & LPT).

📖 Example Payload
```
REM This is a sample OverQuack-Remastered payload

DEFINE @delay 1000
$username = "Test"
FUNCTION OpenShell()
  DELAY @delay
  GUI r
  STRING powershell
  ENTER
END_FUNCTION

OpenShell()
STRINGLN echo "Hi $username!"
```

📖 Example 2 Payload for support type C-style comments and IF, ELSE_IF, ELSE, END_IF
```
// Advanced Ducky Script Example - C-style comments
/* 
This demonstrates both comment styles
Multi-line C-style comment block 
*/

REM SUPPORT FOR IF, ELSE_IF, ELSE, END_IF

VAR $number = 42

IF ($number < 10)
    STRINGLN Number is small
ELSE_IF ($number < 50)
    STRINGLN Number is medium  # This will execute
ELSE_IF ($number < 100)
    STRINGLN Number is large
ELSE
    STRINGLN Number is very large
END_IF

REM Traditional Ducky comment
VAR $username = "admin"
VAR $delay_time = 500

DEFINE $FAST_TYPE 50

FUNCTION open_notepad
  GUI r
  DELAY $delay_time
  STRING notepad    // Open notepad
  ENTER
  DELAY 1000
END_FUNCTION

IF $_CAPSLOCK_ON == 1
  CAPSLOCK
END_IF

open_notepad

STRING_BLOCK
Hello, this is a test
Written by: $username
Current delay: $delay_time ms
END_STRING

STRINGLN
DELAY $FAST_TYPE
STRING This line has a fast delay

MOUSE_MOVE 100 100
MOUSE_CLICK LEFT    // Click at position
DELAY 500

WHILE $delay_time > 100
  DELAY $delay_time
  $delay_time = $delay_time - 100
END_WHILE

/*
This is a C-style block comment
Multiple lines can go here
*/

REM_BLOCK
This is a traditional Ducky block comment
Both styles are supported
END_REM
```
📖 Example 3 Now Suppports Complex Nesting:
```
REM payload.oqs

DEFINE @waqt 1000 

DEFAULT_DELAY = 1000

$username = "NIKHIL"

FUNCTION OPEN_NOTEPAD()
    DELAY @waqt
    GUI r 
    // supports math operation
    DELAY @waqt - 200 
    STRING notepad 
    SHIFT ENTER
    DELAY 1500 
    ENTER
    STRINGLN_BLOCK
    Jinki manzil ek hoti hai ... woh raaston par hi toh milte hai
    END_STRINGLN
END_FUNCTION

OPEN_NOTEPAD()

$A = 35

WHILE $A>0
    IF ($A > 25)
       IF ($A<30)
         STRINGLN $A is LESS THAN 30
       ELSE_IF ($A < 25)
         STRINGLN $A is LESS THAN 20
       ELSE
         BREAK
    END_IF

$A = $A-1
END_WHILE

```

## You can also Compile your written scripts on

[Compiler](https://nikhilmunda.github.io/)

## FOR MORE INFO ABOUT PAYLOADS AND SCRIPTS VISIT 

[VexilonHacker/OverQuack](https://github.com/VexilonHacker/OverQuack)

## 🛡️ Disclaimer

For authorized testing and education only. Never use on systems you do not own or have clear written permission to test. The authors take no responsibility for misuse or damage.

Stay ethical. Hack responsibly.

