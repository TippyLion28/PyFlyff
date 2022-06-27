# PyFlyff
QtWebEngine to play Flyff Universe

# Client Hotkeys

Ctrl+Shift+F5 = reload client back to https://universe.flyff.com/play

Ctrl+Shift+F11 = enter/exit main window fullscreen

Ctrl+Shift+PgUp (PageUp) open a new client window

To stop the Mini Ftool loop, press the Activation Key again.

# Features

Mini Ftool: You can setup an auto hotkey to automatically use a skill/item for you (good for heal spam or mage/psy/elementor 1x1) to stop it, press the same key you used to start it.

Alt Control: You can set hotkeys for the Main Client to send a direct command to the Alt Client. Good if you don't want to use the Mini Ftool, but still want to command your FS/RM without having to alt+tab. To set multiple keys (up to 20 keys) add commas between each one.

Example:

Main Client Hotkey: q,e,f1...

Alt Client Hotkey: 1,2,3...

Reset Hotkeys: Clear the variables values from Mini Ftool and Alt Control keys as well as the variable containing the value that is used to identify which window is the Main Client and which window is the Alt Client. Good in case you want to switch keys on both Mini Ftool and Alt Control without the need of completly restarting the PyFlyff Client.

User Agent: You can use this to spoof from where you are playing Flyff Universe, or, you can use it in case you are having trouble with your Google Account login / recaptcha challenge (see the "Known Issues so far" section of this README)

Community: You can access community links within the client, like Flyffipedia, Madrigal Inside, Flyffulator, Madrigal Maps, Flyff Model Viewer, Skillulator

# Disclaimer

As you can see, I added bot like features to my Client. They are simple, yet, very convenient tools to make the grind a bit more bearable, but keep in mind that using automation is against the rules and you might get banned for it. The Mini Ftool generate a random wait time for every repeatable action, but this does not prevent from a GM to identify that you are in fact botting, so try to not abuse it, you have been very much warned.

And no, I won't make a fully functional Ftool in my client, this takes time to make (something I don't have much) and to debug, and will just encourage botting, and I don't want that. Be happy that You can spam one key and send one key to your alt. Just try to play the game "fair".

I'll continue to implement stuff and fixing bugs, but for now, enjoy yourself.

# Known Issues so far

If when you try to login wih your Google Account, and Google mark my Client as unsafe, set your User Agent by pressing the button "Set User Agent" in the toolbar and type in the input box: None

Hit save and restart the Client, it should let you login with no problem now.

Sometimes you won't be able to resolve the recaptcha challenge since it will report that PyFlyff is an outdated browser, to fix it, set your User Agent to anything really and it will bypass this check.

# How to compile it yourself

You i'll need to pip install those modules to your Python installation:

pip install pyinstaller pywin32 PyQt5 PyQtWebEngine

Then create a .BAT file with this:

IF your Python installation is ACCESSIBLE from Windows Env variables:

pyinstaller PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole

IF your Python installation is NOT accessible from Windows Env variables, then you will have to fully tell both python.exe and pyinstaller script locations in the command line:

Path/to/your/python.exe path/to/your/pyinstaller.py PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole

pyinstaller.py script is located in your Python installation folder - Scripts

Save both .BAT and put it inside the project folder and run it, wait for the compilation to finish and the resulted folder named "PyFlyff" will appear inside the dist folder created by pyinstaller inside the project folder.

After the compilation is finished, copy the icons folder inside the project folder to the created PyFlyff folder by pyinstaller inside the dist folder, else there will be bugs since tkinter is using the icon as well.

# Android Client

I also made an Android Client that makes it easier for your to Dual Client using your Android Device.

Here is the link: https://github.com/ils94/FlyffUWebViewClient

#  Donations

I didn't think of receiving donates for this, since I just like to code as a hobby, but since someone asked if they could donate something for me, here is my Cardano address if you would like to give me some ADA cryptocurrency :)

Here is my address: addr1q9ez0lgwrult58fcm2x7wh0d62v20gtpxh7szlly2zsn75kgga3cu427gtnywnn60jcuaj7r2tnqp6ltj7atveyta53seegl5t
