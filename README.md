# whrwthal
Offline bible referencing for bible minded folk! Including terminal and/or UI display, verse and/or phrase lookup, perl-like regular expressions for advanced searches to accelerate bible learning past that of tip top etymological scholars. Why is whrwthal better than other systems (honorable mentions: https://www.BlueLetterBible.org/, SWORD Project & https://Xiphos.org/)? Read on:

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

whrwthal is a lightweight and easy to use cross-platform application, compared to current alternatives. It was inspired by the need for access to rapidly distributable scriptures without fear of persecution in closed-countries. See https://www.opendoorsusa.org/christian-persecution/world-watch-list/, https://flashdrivesforfreedom.org/

As such, whrwthal totals just under 9MB, or 5MB if low-footprint mode is on (consider Xiphos-Unix at just under 30MB, Xiphos-Windows 47MB). It can inconspicuously reside on your thumb drive among photos, as well as be sent through email! (Gmail caps its message+attachment size at 25MB)

whrwthal requires no internet connection, and therefore presents no threat to use on your own personal computer, laptop, or even plugged in at a public access computer such as a library. It communicates with no outside program, and requires no additional input beyond initial installation.

# WARNING
IF YOU LIVE IN A PERSECUTED OR CLOSED-COUNTRY, PLEASE READ: DO NOT DOWNLOAD THIS SOFTWARE FROM GITHUB IF YOU BELIEVE YOU ARE CURRENTLY UNDER GOVERNMENT OR OTHER SURVEILLANCE (otherwise, feel free!). If someone you know referred you to this software, try to obtain a copy from them. Otherwise, where possible, contact me at gregcaceres@gmail.com for a snail-mail copy on USB/CD. I suggest you word your email in an inconspicuous phrasing, along these lines: "Hello, I recieved your promotional letter. I'm not interested, and I'd like you to please take me off your mailing list. The associated address is 1234 Example Street, Missionary City, God's Country."

# Dependencies & Installation
whrwthal lives here, so all you need to download is

``git clone https://github.com/GregCM/whrwthal *installdir*``

where *installdir* is the folder where you want whrwthal, and all its config and source files. For my Widnows/Mac friends without git, click your way through to "Download ZIP" under "Code" at the top of the page.

whrwthal is built on pure Python, and runs on Windows, MacOS, and Linux. If you have Python already, you'll be able to use whrwthal right away, no further install needed! If you are running on MicroSoft Windows, you will likely need to install Python. You can check in your commmand prompt if you have Python3 already

``python --version``

If this returns ``Python 3.X.X`` then you're all set. Python 2.X users will need to upgrade. To get Python3, see the install support at https://www.python.org/downloads/windows/

You will need to include "pip" and "tkinter" in your Python install to use whrwthal. For the easiest method, choose "web-based installer".

Keep in mind this will take up about 60MB of space on your machine. The best thing to do where internet is reliable is install Python to your computer instead of your thumb drive, in order to maximize space on the thumb drive. If internet is unreliable and you want the ability to use whrwthal on several machines (or share it so recipients can use-as-is), see the install support pages below for embeddable versions of Python, with additional steps needed to include "pip" and "tkinter".

Embedded Python:
https://docs.python.org/3/using/windows.html,

PIP:
https://pip.pypa.io/en/stable/installing/,

Tkinter:
https://tkdocs.com/tutorial/install.html,

To circumvent these extra steps, and enjoy an overall much more lightweight experience, simply download embedded Python to your folder of choice and run whrwthal in the same folder (still totaling under 25MB).

# First-Use
On any OS, execute ``cd *installdir*`` in your terminal / command prompt. Now, you can run ``main.py`` [Windows], or ``./main.py`` [Linux/MacOS].

whrwthal will need to run a one-time setup and parse the text, which should only take a few seconds. If you decide to enable low-footprint mode, this setup will happen every time you use whrwthal. Otherwise, from first setup on you can proceed the same way through the command prompt, or more simply create a shortcut to the file "main.py"

You can change the default settings stored during this one-time setup at any time through the Options menu; this includes Language, Colors, Directories, and more.

Linux users can create a desktop application referencing whrwthal by writing to a desktop file. Most likely, the best place for this is in

``~/.local/share/applications/``

Once you ``cd`` to this directory, make a file called "whrwthal.desktop" populated by the following:

``
[DESKTOP ENTRY]
Version=1.0
Encoding=UTF-8
Name=whrwthal
Comment=Offline Bible referencing
Exec=*installdir*/v1.py
Icon=*installdir*/icon.ico
Path=*installdir*
Terminal=false
Type=Application
Categories=Educational;Application;
``

An icon will now appear in your applications menu to easily access whrwthal!

# TODO

In future releases, expect to see:

- More translations in a variety of tongues, in the public domain and reliable in their source and lineage, akin to the KJV. Examples include:

    French (OST)

    German (LUT)

    Hebrew (LC)

    Greek (TR)

    Russian (RUSV)
    
    Chinese (CKJV)

    (See further candidates for use in this app here -- http://textus-receptus.com/wiki/List_of_languages)

- Regular expression checkbox options on a per-search basis, plus directly typing in regular expressions for advanced users

- A limitation on searching overloaded words like "the" or "I", to prevent slow downs and crashes

- Searched word highlighting to replace the current capitalization

- In-Text-Box buttons under each word, for quick searching, as well as custom cross references

- Bug-fix for search result buttons that incorrectly display the verse preview (ie "... word of GOD..." when it should be "... word of GOD.", etc.)

- Calendar synced "Daily Readings" to serve as a structured study tool (retrieved from BLB sites)

# Resources

For study tools to use in Christ-averse regions, see the following for print in your personal library. Please note, I haven't proof read these materials to check for doctrinal truth / accuracy, as I don't speak any of these languages. All the same, I don't believe I should be such a gatekeeper anyhow, and leave it up to you as a user to determine within your own conscience and in the privacy of your own reading of scriptures and prayerful heart towards God, whether these things are true. See Acts 17:10-11, consider the Bereans!

Arabic -- https://www.thegrace.com/

Chinese -- ...

Korean -- ...

Others -- ...

Biblical translations in a variety of tongues are utilized to provide this graphical bible referencing app to you for convenience; they are all in the public domain and reliable in their source and lineage, akin to the KJV (as mentioned above, they are so confirmed to the best of my ability, not guaranteed in their quality or under any warranty whatsoever). If, under your personal circumstances, you find it better to use these simple Text files instead of whrwthal, you may find them at

``https://github.com/GregCM/whrwthal/tree/texts``

You may download any or all of them, and please distribute them liberally. As aforementioned, finding simple Text files like these online is very cumbersome, if at all possible, and one of the cheif motivations for this project has been to increase the visibility of such resources. Thank you!
