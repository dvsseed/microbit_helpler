# About microbit_helpler
microbit_helpler is try to create a Scratch 2.0 Extension for BBC micro:bit through the COM serial port to send/receive the self-defined data.

## Installation:
1. python2 -m pip install blockext==0.2.0a2
2. python2 -m pip install pyserial
3. To download and install the **Scratch 2.0 Offline Editor** from [https://scratch.mit.edu/download](https://scratch.mit.edu/download)

## Basic Usage
1. Open the **Scratch 2.0 Offline Editor**
2. Import the extension description (**Shift**-click on "**File**" and select "**Import Experimental HTTP Extension**" from the menu)
choice the file of _microbit_helper.s2e_
3. The new extension blocks will appear in the More Blocks palette
4. Test your extension and iterate!

or directly to the **ScratchFiles/ScratchProjects/** directory and Double-click at _microbit_sample.sb2_ sample file and you can play the demo game.

## Source files

* microbit_hex.hex  (micropython compiled to intel-hex file)
* microbit_helper.py  (python code follow the Scratch 2.0 Extension helper apps for micro:bit by blockext package)
* ScratchFiles/ExtensionDescriptors/microbit_helper_zh_tw.s2e  (Scratch Extension helper block with Chinese)
* ScratchFiles/ExtensionDescriptors/microbit_helper.s2e  (Scratch Extension helper block with English)
* ScratchFiles/ScratchProjects/microbit_sample.sb2  (Sample Game for Scratch)

## Screenshot
![image](https://github.com/dvsseed/microbit_helpler/blob/master/Scratch_2_Offline_Editor.png)

## Reference

## Notes and Credits
* [BBC micro:bit](http://microbit.org/)
* [MIT SCRATCH](https://scratch.mit.edu/)
* [Python](https://www.python.org/)
* [Teacher HSIEH, Li-Yi](https://github.com/lyshie/scratch2-microbit)
* [blockext](http://blockext.org)

## License

The Laravel framework is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).

-----------------------------------------------------------
