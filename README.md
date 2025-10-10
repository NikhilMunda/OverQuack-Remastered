## 🦆 OverQuack-Remastered
OverQuack-Remastered is a feature-rich, Rubber Ducky-style HID attack tool for the Raspberry Pi Pico family, supporting wireless payloads, mouse and keyboard injection, cross-platform compatibility, and fully customizable scripting and configuration.

## 🫡 Acknowledgments

This is the REMASTERED version of [VexilonHacker/OverQuack](https://github.com/VexilonHacker/OverQuack) and some [dbisu/pico-ducky](https://github.com/dbisu/pico-ducky). I liked their work and project so much that I thought on tweaking and fixing the Codes. I love Raspberry Pico W 💕 how well it worked with OverQuack code.

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

## ✅ Core Execution System
Complete executeNestedCode function with proper recursion handling

Memory management with garbage collection

## ✅ Advanced Control Structures
IF/ELSE_IF/END_IF with proper condition evaluation and nesting support

FUNCTION/END_FUNCTION definition and execution with nested support

WHILE/END_WHILE loops with iteration limits and nesting support

## ✅ Enhanced String Handling
STRING_BLOCK/END_STRING for multi-line string output

STRINGLN_BLOCK/END_STRINGLN for multi-line string with newlines

DISABLE_STRIP/ENABLE_STRIP formatting control

## ✅ 🖱️ Mouse Control Support
```
MOUSE_CLICK RIGHT             # Click mouse button: LEFT / RIGHT / MIDDLE
MOUSE_PRESS LEFT              # Press (hold down) mouse button
MOUSE_RELEASE LEFT            # Release previously pressed mouse button
MOUSE_MOVE 30 40              # Move mouse cursor to x=30, y=40
MOUSE_SCROLL 6                # Scroll up 6 lines
MOUSE_SCROLL -6               # Scroll down 6 lines
```
## 〰 Mouse Jiggler
```
JIGGLE_MOUSE 6000             # Jiggle mouse for 6000 ms
BACKGROUND_JIGGLE_MOUSE 5000 # Jiggle mouse for 5 seconds after payload ends
BACKGROUND_JIGGLE_MOUSE INF   # Jiggle mouse indefinitely after payload ends
```



For more INFO [Visit](https://github.com/VexilonHacker/OverQuack?tab=readme-ov-file#%EF%B8%8F-mouse-control-support)

## ✅ Advanced Key Management
HOLD and RELEASE commands for individual keys

RELEASE_ALL for clearing all pressed keys

Proper key state management

## ✅ Script Control Features

🔁 REPEAT

You can repeat specific lines multiple times using the REPEAT command.

✅ Basic example 1:
```
PRINT "hello world"
REPEAT LINES=1 TIMES=3
```
Result:

```
"hello world"
"hello world"
"hello world"
```

✅ Basic example 2:
```
PRINT "PEACE"         //2nd line
PRINT "hello world"  //1st line
REPEAT LINES=2 TIMES=3
```
Result:

```
"PEACE"
"hello world"
//It reapeated from 2nd line 3 times
"PEACE"     
"hello world"
"PEACE"
"hello world"
"PEACE"
"hello world"
```
## 🔤 Layout Selection

SELECT_LAYOUT for keyboard layout switching
```
SUPPORTED_LAYOUTS = {
    "US_DVO",
    "US",
    "MAC_FR",
    "WIN_BR",
    "WIN_CZ",
    "WIN_CZ1",
    "WIN_DA",
    "WIN_DE",
    "WIN_ES",
    "WIN_FR",
    "WIN_HU",
    "WIN_IT",
    "WIN_PO",
    "WIN_SW",
    "WIN_TR",
    "WIN_UK",
}
```
To change the keyboard layout, use the SELECT_LAYOUT command:

```
SELECT_LAYOUT WIN_FR  # Switch to French layout on Windows
```

RESTART_PAYLOAD and STOP_PAYLOAD commands

IMPORT script functionality

## ✅ Enhanced Variable System
Fixed random variable replacement with proper regex parsing

Safe expression evaluation (replacing dangerous eval with safe_eval)

Comprehensive variable and define replacement

Internal variables for system state

## ✅ Debugging and Output
BetterListOutput function for formatted debugging

Color-coded console output system

Comprehensive error messages and status reporting

PRINT command for script output

## 📦 Quick Start
Clone the repo:

shell
git clone https://github.com/NikhilMunda/OverQuack-Remastered.git


## ⚙️ Configuration:

Edit config.json for board settings, Wi-Fi/AP, payloads, and pins which can be found inside \OverQuack_src\

```
{
    "DEFAULT_PAYLOAD" :  "payload.oqs",
    "BOARD" : {
        "controll_mode_pin": 5,
        "desc_controll_mode_pin" : "Setting GPIO pin that will change from keystroke mode to storage mode as example pin 2, 6, 10, 13...",

        "enable_auto_switch_mode" : true,
        "desc_enable_auto_switch_mode" : "switch attack mode without  need to replug usb",

        "enable_auto_reload" : false,
        "desc_enable_auto_reload" : "when editing a file in PICO and saving it, it will auto reboot PICO"
    },
    "AP" : {
        "ssid": "WIFI-QUACK",
        "password": "passw1234",
        "channel": "RANDOM",
        "desc_channel" : "You can set random channel  value by using RANDOM or specify channel value as int in range [1,13]",
        "ip_address": "10.10.5.1",
        "ports": [80, 8000, 8080],
        "desc_ports" : "at least you should put 2 ports, other ports are used in emergency"
    }
}
```

## 📱 setup it manually

1) Download repo: [HERE](https://github.com/NikhilMunda/OverQuack-Remastered/archive/refs/heads/main.zip)

2) Plug your Pico into USB while holding the BOOTSEL button for 3 seconds, then release it. It will show up as "RPI-RP2".

3) Copy OverQuack_installation/firmwares/flash_nuke.uf2 to the RPI-RP2 drive and wait for the Pico to finish rebooting.

4) Copy OverQuack_installation/firmwares/adafruit-circuitpython-raspberry_pi_<YOUR_PICO_MODULE>-en_US-9.2.9.uf2 to the RPI-RP2 drive and wait for the Pico to finish rebooting and it going to show up as "CIRCUITPY".

<details>
  <summary>Available firmwares</summary>
  
  ```
  -adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.9.uf2
  -adafruit-circuitpython-raspberry_pi_pico2-en_US-9.2.9.uf2
  -adafruit-circuitpython-raspberry_pi_pico2_w-en_US-9.2.9.uf2
  -adafruit-circuitpython-raspberry_pi_pico_w-en_US-9.2.9.uf2
  ```
</details>

⚠️NOTE: If you want, you can edit/config the file before going to the next step else you will not be able to edit/config later.

⚠️NOTE: If you want, you can remove/delete the extra keyboad layouts from OverQuack_src\lib\ Keyboard_layouts and keycodes, which doesnot seems neccesarry according to your preference.

5) copy all content of OverQuack_src to CIRCUITPY

6) Setup complete. OverQuack is ready to use. Proceed with your tasks responsibly.

## 🔄 Toggle mode: Mass Storage ⇄ HID Keyboard

Connect a switch between GPIO 5 and GND to switch HID/Mass Storage without replugging

OR You can connect a wire between GPIO 5 and GND to switch HID and remove the wire to switch Mass Storage

![simplified_pico_pinout](https://github.com/user-attachments/assets/443b500a-49f5-4912-8235-e995e251129a)

🔁 No need to unplug the USB or manually replug the device after flipping the switch — simply toggle the switch, and OverQuack will automatically reboot into the selected mode.


## 🛜 Wireless control:

Run and manage payloads from another device with OverQuack_client.go clients available for both linux and windows. For (Pico W/2W only)

## LINUX:
<img width="840" height="566" alt="LinuxClient" src="https://github.com/user-attachments/assets/77989c35-90fa-406e-a536-8ea05ce7594f" />


## WINDOWS:
<img width="840" height="466" alt="WindowsCLient" src="https://github.com/user-attachments/assets/cc7e9700-5ca5-47b8-86a7-2d64e36b1f52" />

✅ Available Operations:

📂 List all payloads/files

📥 Upload / 📤 Download payloads

📝 Read / ❌ Delete payloads

▶️ Run payload remotely

And Now, Have support for Android App [OverQuack_Client](https://github.com/NikhilMunda/OverQuack_App/releases)

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

// HAVE SUPPORT for IMPORT to use or import other payloads from pico w
DEFAULT_DELAY 500
// HERE USING IMPORT WILL RUN THE BYPASSWINDOW.oqs CODE
IMPORT BYPASSWINDOW.oqs

//--------------NEXT CODE--------------------

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

//--------------NEXT CODE---------------

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

MOUSE_MOVE 100 100   //Move the cursor
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
DEFINE @waqt 1000 

DEFAULT_DELAY = 1000

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

## 🔑 You can also Compile your written scripts on

Online Enhanced [Compiler](https://nikhilmunda.github.io/) 

<img width="840" height="466" alt="Screenshot 2025-10-10 102447" src="https://github.com/user-attachments/assets/e57d063a-a03f-4a4d-8a55-d61d4bfcb256" />


## ❗ FOR MORE INFO ABOUT PAYLOADS SCRIPTS AND COMMANDS VISIT 

[VexilonHacker/OverQuack](https://github.com/VexilonHacker/OverQuack)


## 📜 License

Distributed under the **GPLv2.0 License**. See [LICENSE](https://github.com/NikhilMunda/nikhilmunda.github.io/blob/main/LICENSE) for more information.


## 🛡️ Disclaimer

For authorized testing and education only. Never use on systems you do not own or have clear written permission to test. The authors take no responsibility for misuse or damage.

Stay ethical. Hack responsibly.

