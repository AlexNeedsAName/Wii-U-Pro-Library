# Wii-U-Pro-Library
A simple library for using the Wii U Pro Controller with your python programs

#Wii U Pro Controller Usage:

First, download `WiiUProInput.py`. To use it in your program, just use `import WiiUProInput`, then call `WiiUProInput.startInputThread()`. You can get a value from the button dictionary using `WiiUProInput.buttons[*ButtonName*]`. The axes work the same way, using `WiiUProInput.axes[*StickAndAxis*]`.

#Standard Wii Remote Usage:

First, download `WiiInput.py`. To use it in your program, just use `import WiiInput`, then call `WiiInput.startInputThread()`. You can get a value from the button dictionary using `WiiInput.buttons[*ButtonName*]`. You can get the IR cordinates with `WiiInput.IR[*XorY*]`. The x cordinate goes from 0 to roughly 1015, and the y goes from 0 to roughly 760. A value of -1 means nothing was detected. Accelerometer and Accesory support is comming soon!
