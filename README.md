# whrwhtal #
Offline bible referencing for bible minded folk! Including UI display, verse and/or phrase lookup, perl-like regular expressions for advanced searches to accelerate bible learning past that of tip top etymological scholars. Why is **whrwhtal** better than other systems (honorable mentions: https://www.BlueLetterBible.org/, SWORD Project & https://Xiphos.org/)? Read on!

## What is it? ##
whrwhtal (adverb), as in:

> Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. - Psalm 119:9

**whrwhtal** is a lightweight and easy to use cross-platform application, compared to current alternatives. It was inspired by the need for access to rapidly distributable scriptures without fear of persecution in closed-countries. See the following:

- https://www.opendoorsusa.org/christian-persecution/world-watch-list/
- https://flashdrivesforfreedom.org/

As such, **whrwhtal** totals just under 9MB, or 5MB if low-footprint mode is enabled (consider Xiphos-Unix at just under 30MB, Xiphos-Windows 47MB). It can inconspicuously reside on your thumb drive among photos, as well as be sent through email! (Gmail caps its message+attachment size at 25MB)

Using **whrwhtal** requires no internet connection, and therefore presents little or no threat to use on your own personal computer, laptop, or even plugged in at a public access computer such as a library. It communicates with no outside program, and requires no additional inputs beyond initial installation.

## Dependencies & Installation ##
**whrwhtal** lives here, so all you need in order to download it is

``git clone https://github.com/GregCM/whrwhtal *installdir*``

where *installdir* is the folder where you want **whrwhtal**, and all its config and source files. For my Widnows/Mac friends without git, click your way through to "Download ZIP" under "Code" at the top of the page and extract it to *installdir*.

**whrwhtal** is built only on Python, and runs on Windows, MacOS, and Linux. If you are running on MicroSoft Windows, you will likely need to install Python. You can check in your commmand prompt if you have Python3 already

``python --version``

If this returns at least ``Python 3.5.X`` then skip ahead to **First-Use**.
``Python 2.X`` users will need to upgrade; ``Python 3.4.X`` users will also need to upgrade, with the extra caveat that your default Python3 environment will need to be changed from 3.X.Y to 3.5.X as follows in folder sequence:

> Control Panel > All Control Panel Items > System > Advanced System Settings > Environment Variables

Keep in mind fresh-installing Python will take up about 60MB of space on your machine. The best thing to do where internet is reliable is install Python to your computer instead of your thumb drive, in order to maximize space on the thumb drive. If internet is unreliable and you want the ability to use **whrwhtal** on several machines (or share it so your recipients can use-as-is), see the install support pages below for embeddable versions of Python, with additional steps needed to include "tkinter". To circumvent these extra steps, and in general hit the ground running, simply install the latest from the first link:

### Python ###
- https://www.python.org/downloads/latest (quick and easy, forget about it)
- https://docs.python.org/3/using/windows.html (general instructions and embeddable)

Check that you have "tkinter" included in your Python install as follows:

    python -m tkinter

If this returns a sample tkinter window, you're set (again). If it's missing, see below:
    - https://tkdocs.com/tutorial/install.html
    - https://www.activestate.com/products/tcl/downloads/

#### A Sidenote: Embedding Python ####
If you do decide to download embedded Python, place it in your folder of choice and make sure to run **whrwhtal** in that same folder (ie if on your thumb drive, Python and Tkinter will both be embedded there; consider this will require more space that whrwthal on its own). Some reasons you may want to do this:
- You don't own a computer, but have access to computers at public or other workspaces (one would embedd python with the app on thumb drive to plug-n-play)
- You want to give an exact [no-nonsense] copy to someone(s) who doesn't own a computer, but has access to computers
- You want to demonstrate **whrwthal** to friends, team, or congregation (or other on-the-go scenarios)
- You're afraid of commitment, and embedding python will make deleting it altogether much easier

## First-Use ##
On any OS, execute ``cd *installdir*`` in your terminal / command prompt. Now, you can run ``thrto.py`` [Windows], or ``./thrto.py`` [Linux/MacOS].

**whrwhtal** will need to run a one-time setup and parse the text, which should only take a few seconds. If you decide to enable low-footprint mode, this setup will happen every time you use **whrwthal**. Otherwise, from first setup on you can proceed the same way through the command prompt, or more simply create a shortcut to the file "thrto.py"

You can change the default settings stored during this one-time setup at any time through the Options menu; this includes Language, Colors, Directories, and more.

Linux users can create a desktop application referencing **whrwhtal** by writing to a desktop file. Most likely, the best place for this is in

``~/.local/share/applications/``

Once you ``cd`` to this directory, make a file called "**whrwhtal**.desktop" populated by the following:

    [DESKTOP ENTRY]
    Version=1.0
    Encoding=UTF-8
    Name=**whrwhtal**
    Comment=Offline Bible referencing
    Exec=*installdir*/thrto.py
    Icon=*installdir*/icon.ico
    Path=*installdir*
    Terminal=false
    Type=Application
    Categories=Educational;Application;

An icon will now appear in your applications menu to easily access **whrwhtal**!

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

If you're concern is security and privacy, I cannot recommend highly enough that you
1. Migrate to Linux or other FOSS operating system
    - Free and Open-Source Software is rigorously reviewed by the user community to help guard against security flaws due to negligence of the designer or, worse yet, malicious intent by the proprietary powers that be (ie keylogging, memory access / wachmen, over-network code execution or even remote operation of your computer); companies like Microsoft and Apple OR companies that put out propriety software that resides on your Microsoft or Apple computer. This has happened, happens, and will happen, in part because of the invisible proprietary code impervious to peer review. Leave behind your proprietary crutches if security is your concern!
2. Choose TAILS as that operating system
    - The first concern that will be raised by proprietary software advocates about free and open-source software is the lack of rigorous code creation; the idea is that security measures are best implemented when the developers are getting paid to implement them. That point is moot with TAILS. See their philosophy, dedication, and impact at https://tails.boum.org/

## Anti-Warning ##
If you live in a country that doesn't burn books, go crazy, download **TWO** copies.

> For I am not ashamed of the gospel of Christ: - Romans 1:16

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

- [ ] Regular expressions
    - [X] Ability to directly type in regular expressions for advanced users (superhumans)

    - [ ] Pre-defined regex Checkboxes for intermediate users (real humans who don't speak robot)

- [ ] A title / header == the verse displayed by user's search selection from list

- [X] A limitation on searching overloaded words like "the" or "I", to prevent slow downs and crashes

- [ ] Searched word highlighting to replace the current capitalization

- [ ] In-Text-Box buttons under each word, for quick searching, as well as custom cross references

- [ ] Bug-fix for search result buttons that incorrectly display the verse preview (ie "... word of GOD..." when it should be "... word of GOD.", etc.)

- [ ] Calendar synced "Daily Readings" to serve as a structured study tool (retrieved from BLB sites)

- [ ] Better tkinter / python embedding (possible compression methods) to make install non-hellish for Windows users

- [ ] PGP cryptographic protections

- [ ] Frequency charts

- [X] Eliminate requirements and need for pip with a Pure Python implementation

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
