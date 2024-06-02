![BrutusOGX](https://github.com/JayYardley/BrutusOGX/blob/main/Image.jpg)
# BrutusOGX | Original XBox .XBE patcher
An app that attempts to improve on the behaviours of "OGxHD", an Xbox executable patching program.

### Features
+ Importing of **.xbe** files (Actually supports any file type)
+ Fast file checking via **binary hex** definition lookup
+ **User defined** custom hex lookup
+ Organised results to improve workflow thoroughness
+ Results are saved to text in *'/Results folder'*
+ **Brute mode** - Generating individual patches via individual results en masse

### Installation
**[Download the Latest Release for Windows](https://github.com/JayYardley/BrutusOGX/releases/download/v0.2/BrutusOGX.v0.2.zip)**

**[Build your own version using the BrutusOGX.py](https://github.com/JayYardley/BrutusOGX/blob/main/BrutusOGX.py)**

### Instructions
1. Click **Open File** to import an .xbe file
2. Select the types of hex data to search for (add your own if necessary)
3. Click **Check** *(a timestamped .txt will be generated for safe keeping)*
4. In the results window, manually select the hex values you wish to change, or click **Select All**
5. Click **Patch** or **Brute Mode** *(don't overwrite your original file)*

**Brute Mode** is a patching method I wanted to add to help diagnose which hex changes are problematic.
When you select which results you want changed and click Brute Mode, the app will generate numbered .xbe files named after and reflecting the result.
Example:
+ If you select result #27 and click **Brute Mode**, it will only generate a *'27.xbe'* file with only the 27th result changes.
+ If you select 50 results, it will generate 50 numbered *'x.xbe'* files all with their individual changes.

I found this incredibly useful for locating exact hex values that broke a particular game.

**Let me know how it goes!**
**Discord: Jay - 197620001904132106**
