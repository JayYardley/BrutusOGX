# BrutusOGX
An open source and seriously hideous prompt-engineered python app that attempts to improve on the behaviours of "OGxHD", an Xbox executable patching program

Instructions

Click open file to import an .xbe file, select the types of hex data to search for and hit check.
You also have the ability to add additional hex data to search for. This will be extremely useful and likely will be more fleshed out in the future.

When you check a file, it will generate a .txt file in /Results/****.txt

The matched data window will appear, which lists every result inside the xbe that matched with what you searched for.
Select the changes you want to patch, and click "patch". You will be asked where to save the file, I don't recommend overwiting the file.

Brute Mode is a patching method I wanted to add to help diagnose which hex changes are problematic.
When you select which results you want changed and click Brute Mode, the app will generate numbered .xbe files named after and reflecting the result.
Example:
If you select result 27 and click Brute Mode, it will only generate a 27.xbe file with only the 27th results changes.
If you select 50 results, it will generate 50 .xbes all with their individual changes.

I found this incredibly useful for locating exact hex values that broke a particular game.

Let me know how it goes!
Discord: Jay - 197620001904132106
