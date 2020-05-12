# whrwthal
Offline bible referencing for bible minded folk! Including terminal and/or UI display, verse and/or phrase lookup, perl-like regular expressions for advanced searches to accelerate bible learning past that of tip top etymological scholars. Why is whrwthal better than other systems (honorable mentions: BlueLetterBible.org, SWORD Project & Xiphos.org)? Read on:

# What is it?
whrwthal (adverb):

 As in "Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word." - Psalm 119:9

W-H-R-W-T-H-A-L (acronymn):

  Whrwthal
  Helps
  Rake
  Wverses
  That're
  Hallowed
  And
  Laudable

whrwthal is a lightweight and easy to use cross-platform application, compared to current alternatives. It was inspired by the need for access to rapidly distributable scriptures without fear of persecution in closed-countries. See https://www.opendoorsusa.org/christian-persecution/world-watch-list/,

https://flashdrivesforfreedom.org/

As such, whrwthal totals just under 9MB, or 5MB if low-footprint mode is on (consider Xiphos-Unix at just under 30MB, Xiphos-Windows 47MB). It can inconspicuously reside on your thumb drive among photos, as well as be sent through email! (Gmail caps its message+attachment size at 25MB)

whrwthal requires no internet connection, and therefore presents no threat to use on your own personal computer, laptop, or even plugged in at a public access computer such as a library. It communicates with no outside program, and requires no additional input beyond initial installation.

# WARNING
IF YOU LIVE IN A PERSECUTED OR CLOSED-COUNTRY, PLEASE READ: DO NOT DOWNLOAD THIS SOFTWARE FROM GITHUB IF YOU BELIEVE YOU ARE CURRENTLY UNDER GOVERNMENT OR OTHER SURVEILLANCE (otherwise, feel free!). IF SOMEONE YOU KNOW REFERRED YOU TO THIS SOFTWARE, TRY TO OBTAIN A COPY FROM THEM. OTHERWISE, WHERE POSSIBLE, CONTACT ME AT GREGCACERES@GMAIL.COM FOR A SNAIL-MAIL COPY ON USB/CD. WORD YOUR EMAIL IN AN INCONSPICUOUS PHRASING, ALONG THESE LINES: "Hello, I recieved your promotional letter. I'm not interested, and I'd like you to please take me off your mailing list. The associated address is 1234 Example Street, Missionary City, God's Country."

# Installation
whrwthal runs on Windows, MacOS, and Linux. If you are running on MicroSoft Windows, you will likely need to install Python. You can check if you have Python3 already by typing

"python --version"

into your command prompt. If you see

"Python 3.X.X"

returned, you're good to go. Python 2.X users will need to upgrade. To get Python, see the install support at

https://www.python.org/downloads/windows/

You will need to include "pip" and "tkinter" in your install to use whrwthal.v1. For the easiest method, choose "web-based installer".

Keep in mind this will take up about 60MB of space on your machine, which is a drop in the bucket compared to putting the same on a thumb drive. The best thing to do where internet is reliable is install python to your computer instead of your thumb drive, in order to maximize space on the drive. If internet is unreliable, see the install support pages below for embeddable versions of Python, with additional steps needed to include "pip" and "tkinter".

https://docs.python.org/3/using/windows.html,

https://pip.pypa.io/en/stable/installing/,

https://tkdocs.com/tutorial/install.html,

To circumvent these extra steps, and enjoy an overall much more lightweight experience, simply download embedded Python and run whrwthal.v0 in the same folder (still totaling just under 25MB).

# FIRST-USE
On Windows, open the command prompt and type

"cd *installdir*"

where *installdir* is the folder where you downloaded this repository. Now, you can run "v1.py" in the command prompt; whrwthal will need to run a one-time setup and parse the text, which should only take a few seconds. From now on, you can proceed the same way through the command prompt, or simply create a shortcut to the file v1.py

On Mac or Linux, open a terminal and proceed the same way. Instead of running "v1.py", however, you'll type

"./v1.py"

You can change the default settings stored during this one-time setup at any time through the options menubar; this includes language, colors, directories, and more!
