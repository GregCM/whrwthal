# whrwhtal #
Offline bible referencing for bible minded folk! Including terminal and/or UI display, verse and/or phrase lookup, perl-like regular expressions for advanced searches to accelerate bible learning past that of tip top etymological scholars. Why is **whrwhtal** better than other systems (honorable mentions: https://www.BlueLetterBible.org/, SWORD Project & https://Xiphos.org/)? Read on!

## What is it? ##
whrwhtal (adverb), as in:

> Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. - Psalm 119:9

W-H-R-W-T-H-A-L (acronymn):

  >Whrwthal
  >Helps
  >Rake
  >Wverses
  >That're
  >Hallowed
  >And
  >Laudable

**whrwhtal** is a lightweight and easy to use cross-platform application, compared to current alternatives. It was inspired by the need for access to rapidly distributable scriptures without fear of persecution in closed-countries. See the following:

- https://www.opendoorsusa.org/christian-persecution/world-watch-list/
- https://flashdrivesforfreedom.org/

As such, **whrwhtal** totals just under 9MB, or 5MB if low-footprint mode is enabled (consider Xiphos-Unix at just under 30MB, Xiphos-Windows 47MB). It can inconspicuously reside on your thumb drive among photos, as well as be sent through email! (Gmail caps its message+attachment size at 25MB)

**whrwhtal** requires no internet connection, and therefore presents no threat to use on your own personal computer, laptop, or even plugged in at a public access computer such as a library. It communicates with no outside program, and requires no additional input beyond initial installation.

## WARNING ##
**If you live in a persecuted or close-country, PLEASE READ: DO NOT DOWNLOAD this software from github if you believe you are currently under government or other surveillance** (otherwise, feel free!). Consider that some online content is censored, some is surveilled; knowing the difference and different ways to fly under the radar is vital, be safe. If someone you know referred you to this software, try to obtain a copy from them. Otherwise, where possible, contact me at gregcaceres@gmail.com for a snail-mail copy on USB/CD. I suggest you word your email in an inconspicuous phrasing, along these lines: "Hello, I recieved your promotional letter. I'm not interested, and I'd like you to please take me off your mailing list. The associated address is 1234 Example Street, Missionary City, God's Country."

### Security-Gaps -Flaws & -Considerations ###
I plan to anonymize source code variables and comments as much as I can. This will help if some very curious person with an untrained-eye takes a peak, but anyone who knows what they're looking at (be it the general format of scripture or python) will figure things out pretty quick.
- Consider that this README document is the only other revealing item in the repository. Act accordingly, keeping an eye towards redistribution if you have the heart for it (see LICENSE for your responsibilities should you choose to redistribute)

Obfuscation will *help* protect against those people who know what they're doing; encryption will do somewhat the same, but will enable good people who know what they're doing and end up with your copy + password to improve or modify the program.
- For legal reasons, I don't do either in advance of distributing **whrwthal**, and likewise (if you plan to redistribute **whrwthal**) I encourage you to only engage in encryption of the entirety of your *installdir*, if you're concerned about securtiy.

Memory leak is a concern in Python namespaces, because even in low-footprint mode (where the text is unreadable without the accompanying codec) Python decodes the text within an interpreter session and holds it in memory while the program is running. It's difficult to locate these various storage points within computer memory, and although memory is reallocated once your session is closed, some hardware is known to leak throughout. I know Intel CPU's have this issue, though they are in the process of upgrading to meet AMD's current security measures. In all, those things are out of my control, and I only have the following recommendations:
- Get better, more secure, hardware
- Don't use at work or some other networked machine that is liable to have a CPU observer pointed at it
- Don't let anyone know you're the one using this software (ie if you're logged in with personal information anywhere, don't read your bible)
- Be [reasonably] paranoid!
    - Again, if you're at home with a private computer and have no reason to believe "the man" is going to bust down your door and comb through your computer, live a little, read your bible

## Anti-Warning ##
If you live in a country that doesn't burn books, go crazy, download **TWO** copies. Being coy about things you should be bold about is less Christ- and more -ism.

> For I am not ashamed of the gospel of Christ: - Romans 1:16

## Dependencies & Installation ##
**whrwhtal** lives here, so all you need in order to download it is

``git clone https://github.com/GregCM/whrwhtal *installdir*``

where *installdir* is the folder where you want **whrwhtal**, and all its config and source files. For my Widnows/Mac friends without git, click your way through to "Download ZIP" under "Code" at the top of the page.

**whrwhtal** is built only on Python, and runs on Windows, MacOS, and Linux. If you have Python already, skip ahead to **PIP** to complete your install and you'll be able to use **whrwthal** right away! If you are running on MicroSoft Windows, you will likely need to install Python. You can check in your commmand prompt if you have Python3 already

``python --version``

If this returns ``Python 3.5.X`` then you're all set. ``Python 2.X`` users will need to upgrade, as will ``Python 3.X.Y`` (for X < 5). You will need to include "pip" and "tkinter" in your Python install to use **whrwhtal**.

Keep in mind Python will take up about 60MB of space on your machine. The best thing to do where internet is reliable is install Python to your computer instead of your thumb drive, in order to maximize space on the thumb drive. If internet is unreliable and you want the ability to use **whrwhtal** on several machines (or share it so your recipients can use-as-is), see the install support pages below for embeddable versions of Python, with additional steps needed to include "pip" and "tkinter". To circumvent these extra steps, and in general hit the ground running, simply install the latest from the first link:

### Python ###
- https://www.python.org/downloads/latest (quick and easy, forget about it)
- https://docs.python.org/3/using/windows.html (general instructions and embeddable)

    - PIP
        - https://pip.pypa.io/en/stable/installing/

    - Tkinter
        - https://tkdocs.com/tutorial/install.html
        - https://www.activestate.com/products/tcl/downloads/

### PIP ###
If you have PIP, install dependencies from *installdir* with ``pip install -r requirements.txt --user`` (internet required). At this point, you're all done, ready to read!

### A Sidenote: Embedding Python ###
If you do decide to download embedded Python, place it in your folder of choice and make sure to run **whrwhtal** in that same folder (ie if on your thumb drive, Python, pip, and Tkinter will all be embedded there; consider this will total about 50MB). Some reasons you may want to do this:
- You don't own a computer, but have access to computers at public or other workspaces (one would embedd python with the app on thumb drive to plug-n-play)
- You want to give an exact [no-nonsense] copy to someone(s) who doesn't own a computer, but has access to computers
- You want to demonstrate **whrwthal** to friends, team, or congregation (or other on-the-go scenarios)
- You're afraid of commitment, and embedding python with the app will make deleting it altogether much easier
- You're afraid of commitment, and embedding python will make deleting it altogether much easier

## First-Use ##
On any OS, execute ``cd *installdir*`` in your terminal / command prompt. Now, you can run ``main.py`` [Windows], or ``./main.py`` [Linux/MacOS].

**whrwhtal** will need to run a one-time setup and parse the text, which should only take a few seconds. If you decide to enable low-footprint mode, this setup will happen every time you use **whrwthal**. Otherwise, from first setup on you can proceed the same way through the command prompt, or more simply create a shortcut to the file "main.py"

You can change the default settings stored during this one-time setup at any time through the Options menu; this includes Language, Colors, Directories, and more.

Linux users can create a desktop application referencing **whrwhtal** by writing to a desktop file. Most likely, the best place for this is in

``~/.local/share/applications/``

Once you ``cd`` to this directory, make a file called "**whrwhtal**.desktop" populated by the following:

    [DESKTOP ENTRY]
    Version=1.0
    Encoding=UTF-8
    Name=**whrwhtal**
    Comment=Offline Bible referencing
    Exec=*installdir*/main.py
    Icon=*installdir*/icon.ico
    Path=*installdir*
    Terminal=false
    Type=Application
    Categories=Educational;Application;

An icon will now appear in your applications menu to easily access **whrwhtal**!

## TODO ##

In future releases, expect to see:

- [ ] Time optimizations (numba)
- [ ] More translations in a variety of tongues, in the public domain and reliable in their source and lineage, akin to the KJV. Examples include:

    - [ ] French (OST)

    - [X] German (LUT)

    - [X] Hebrew (LC)

    - [ ] Greek (TR)

    - [ ] Russian (RUSV)
    
    - [ ] Chinese (CKJV)

(See further candidates for use in this app here -- http://textus-receptus.com/wiki/List_of_languages)

- [ ] Regular expression checkbox options on a per-search basis, plus directly typing in regular expressions for advanced users

- [ ] A limitation on searching overloaded words like "the" or "I", to prevent slow downs and crashes

- [ ] Searched word highlighting to replace the current capitalization

- [ ] In-Text-Box buttons under each word, for quick searching, as well as custom cross references

- [ ] Bug-fix for search result buttons that incorrectly display the verse preview (ie "... word of GOD..." when it should be "... word of GOD.", etc.)

- [ ] Calendar synced "Daily Readings" to serve as a structured study tool (retrieved from BLB sites)

- [ ] Better tkinter / pip embedding (possible compression methods) to make install non-hellish for Windows users

- [ ] PGP cryptographic protections

## Resources ##

For study tools to use in Christ-averse regions, see the following for print in your personal library. Please note, I haven't proof read these materials to check for doctrinal truth / accuracy, as I don't speak any of these languages. All the same, I don't believe I should be such a gatekeeper anyhow. I leave it up to you as a user to determine within your own conscience and in the privacy of your own reading of scriptures and prayerful heart towards God, whether these things are true. See Acts 17:10-11, consider the Bereans!

- Arabic -- https://www.thegrace.com/

- Chinese -- *todo*

- Korean -- *todo*

- Others -- *todo*

Biblical translations in a variety of tongues are utilized to provide this graphical bible referencing app to you for convenience; they are all in the public domain and reliable in their source and lineage, akin to the KJV (as mentioned above, they are so confirmed to the best of my ability, not guaranteed in their quality or under any warranty whatsoever). If, under your personal circumstances, you find it better to use these simple Text files instead of **whrwhtal**, you may find them at

``https://github.com/GregCM/whrwhtal/tree/texts``

You may download any or all of them, and please distribute them liberally. As aforementioned, finding simple Text files like these online is very cumbersome, if at all possible, and one of the cheif motivations for this project has been to increase the visibility of such resources. Thank you!

## FAQ and Psuedo-Lies ##

- Windows Install size > 25MB?
    - Okay, technically not lighter than the competition when you run in Windows, but at least it's only 9MB sitting in the thumb drive. Python has the advantage of being native where C isn't for example, but the same is true other way around. Why use Windows anyway?

- Why use Windows anyway?
    - Great question, this FAQ section is really shaping up.
