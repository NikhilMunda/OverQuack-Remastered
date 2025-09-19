## 🦆 OverQuack-Remastered
OverQuack-Remastered is a feature-rich, Rubber Ducky-style HID attack tool for the Raspberry Pi Pico family, supporting wireless payloads, mouse and keyboard injection, cross-platform compatibility, and fully customizable scripting and configuration.

## 🫡 Acknowledgments

This is the REMASTERED version of [VexilonHacker/OverQuack](https://github.com/VexilonHacker/OverQuack) and some [dbisu/pico-ducky](https://github.com/dbisu/pico-ducky). I liked their project so I thought on tweaking and fixing some of the Codes. I love Raspberry Pico W 💕 how well it worked with OverQuack code.

## 🚀 Features

Full DuckyScript 3.0 support: Includes custom variables, functions, logic, and advanced blocks

All Pico variants: Works with Pico, Pico W, Pico 2, Pico 2 W

Wireless payloads: Upload, execute, and manage scripts remotely via Wi-Fi (Pico W/2W)

Plug & Play: Automatic Mass Storage ↔ HID switching (toggle via GPIO pin)

Cross-platform payloads: Supports Windows, Mac, and Linux

Mouse & Keyboard injection: Precise mouse move/click/jiggle and full keyboard control

Modular and extensible: Easy script imports, custom layouts, and debugging via serial

Easy configuration: All settings adjustable with config.json

Open source, GPLv2.0

## 📦 Quick Start
Clone the repo:

shell
git clone https://github.com/NikhilMunda/OverQuack-Remastered.git


## Configure:

Edit config.json for board settings, Wi-Fi/AP, payloads, and pins

## 📱 setup it manually

Download repo: [HERE](https://github.com/NikhilMunda/OverQuack-Remastered)

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
## You can also Compile your written scripts on

[Compiler](https://nikhilmunda.github.io/)

## FOR MORE INFO ABOUT PAYLOADS AND SCRIPTS VISIT 

[VexilonHacker/OverQuack](https://github.com/VexilonHacker/OverQuack)

## 🛡️ Disclaimer

For authorized testing and education only. Never use on systems you do not own or have clear written permission to test. The authors take no responsibility for misuse or damage.

Stay ethical. Hack responsibly.

