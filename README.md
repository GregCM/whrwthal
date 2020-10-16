# whrwhtal #
Offline bible referencing for bible minded folk! Including UI display, verse and phrase lookup, and regular expressions to help accelerate bible learning past that of top scholars. Why is **whrwhtal** better than other systems (honorable mentions: [crosswire](https://crosswire.org/) [BLB](https://www.BlueLetterBible.org/), [Xiphos](https://Xiphos.org/))? Read on!

## What is it? ##
whrwhtal (adverb), as in:

> Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. - Psalm 119:9

**whrwhtal** is a cross-platform lightweight application, compared to current alternatives. It is meant to be dirt simple and unassuming. It was inspired by the need for access to [rapidly distributable](https://flashdrivesforfreedom.org/) scriptures without fear of [persecution in closed-countries](https://www.opendoorsusa.org/christian-persecution/world-watch-list/).

As such, **whrwhtal** totals just under 5MB, or 3MB if low-footprint mode is enabled (consider Xiphos-Unix at just under 30MB, Xiphos-Windows at 47MB). It can inconspicuously reside on your thumb drive among photos, as well as be sent through email! (Gmail caps its message+attachment size at 25MB)

Using **whrwhtal** requires no internet connection, and therefore presents little threat on your own personal computer, or even plugged in at a public access computer or library. It communicates with no outside program, and requires no additional inputs beyond initial installation.

## Dependencies & Installation ##
**whrwhtal** lives here, so all you need in order to download it is

    git clone https://github.com/GregCM/whrwhtal directory/

where ``directory/`` is the folder where you want **whrwhtal**, and all its config and source files. For my Widnows/Mac friends without git, click your way through to "Download ZIP" under "Code" at the top of the page and extract it to ``directory/``.

**whrwhtal** is pure python, and runs on Windows, MacOS, and Linux. If you are running on Windows, you will likely need to install Python. You can check in your commmand prompt if you have Python3 already

``python --version``

If this returns at least ``Python 3.5.X`` then skip ahead to **First-Use**.
``Python 2.X`` users will need to upgrade; ``Python 3.4.X`` users will also need to upgrade, with the extra caveat that your default Python3 environment will need to be changed from 3.X.Y to 3.5.X as follows in folder sequence:

> Control Panel > All Control Panel Items > System > Advanced System Settings > Environment Variables

### Python ###
Keep in mind fresh-installing Python will take up about 60MB of space on your machine. The best thing to do where internet is reliable is install Python to your computer instead of your thumb drive, in order to maximize space on the thumb drive. If internet is unreliable and you want the ability to use **whrwhtal** on several machines (or share it so your recipients can use-as-is), see the install support pages below for embeddable versions of Python, with additional steps needed to include "tkinter". To circumvent these extra steps, and in general hit the ground running, simply install the latest from the first link:
- [quick and easy](https://www.python.org/downloads/latest), forget about it
- [detailed instructions](https://docs.python.org/3/using/windows.html) and embeddable

### Tkinter ###
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
On any OS, execute ``cd directory/`` to enter your install directory where whrwthal now resides. Now, you can run ``python -m whrwthal``.

**whrwhtal** will need to run a one-time setup, which should only take a few seconds. If you decide to enable low-footprint mode, this setup will happen every time you use **whrwthal**. You can start the same way through the command prompt every time, or more simply create a shortcut (associated with command ``python -m whrwthal``). This is trivial in Windows; just make sure it's set to run in the correct directory, and include the icon file if you like. MacOS shortcuts are a foreign and veiled mystery to me.

Desktop enviornment Linux users can create a desktop application referencing **whrwhtal** by writing to a desktop file (others, I recommend dmenu). Most likely, the best place for this is in

``~/.local/share/applications/``

Once there, make a file called "whrwhtal.desktop" populated by the following:

    [DESKTOP ENTRY]
    Version=1.0
    Encoding=UTF-8
    Name=Whrwhtal
    Comment=Offline Bible referencing
    Exec=python -m directory/whrwthal/__main__.py
    Icon=directory/icon.ico
    Path=directory/
    Terminal=false
    Type=Application
    Categories=Educational;Application;

An icon will now appear in your applications menu to easily access **whrwhtal**!

You can change the default settings stored during your first setup at any time through the Options menu; this includes Language, Colors, Directories, and more. Alternatively, directly alter "config.ini".

## WARNING ##
**If you live in a persecuted or close-country, PLEASE READ: DO NOT DOWNLOAD this software from github if you believe you are currently under government or other surveillance** (otherwise, feel free!). Consider that some online content is censored, some is surveilled; knowing the difference and different ways to fly under the radar is vital. If someone you know referred you to this software, obtain a copy from them. Otherwise, if possible, contact me at gregcaceres@gmail.com for a snail-mail copy on USB. I suggest you word your email inconspicuously, along these lines: "Hello, I recieved your promotional letter. I'm not interested, and I'd like you to please take me off your mailing list. The associated address is 1234 Example Street, Missionary City, God's Country."

### Security-Gaps -Flaws & -Considerations ###
Obfuscate your code or encrypt you install directory.
- For legal reasons, I don't do either in advance of distributing
- If you plan to redistribute, you should only encrypt your copy, not the shared one (see [license](./LICENSE))

Memory leak is a concern with Python, because Python decodes the text within an interpreter session and stores it in memory while the program is running. It's difficult to locate these storage points, and although memory is reallocated once your session is closed, some hardware is known to leak throughout. I know Intel CPUs have this issue, though they are in the process of upgrading. In all, those things are out of my control, and I only have the following recommendations:
- Consider [Sandboxing](https://en.wikipedia.org/wiki/Sandbox_(computer_security) "Wiki: Sandbox security") solutions 
    - [Firejail](https://github.com/netblue30/firejail)
    - [Bubblewrap](https://github.com/containers/bubblewrap)
    - [Containers](https://wiki.archlinux.org/index.php/Linux_Containers)
    - [VMs](https://wiki.archlinux.org/index.php/VirtualBox)
- Get better, more secure, hardware
- Don't use at work or some other networked machine that is liable to have a CPU observer pointed at it
- Don't let anyone know you're the one using this software (ie if you're logged in with personal information anywhere, don't read your bible)
- Be [reasonably] paranoid!
    - Again, if you're at home with a private computer and have no reason to believe "the man" is going to bust down your door and comb through your computer, live a little, read your bible

If you're concern is security and privacy, I cannot recommend highly enough that you
1. Migrate to Linux or other FOSS operating system
    - Free and Open-Source Software is rigorously reviewed by the user community to help guard against security flaws due to negligence of the designer or, worse yet, malicious intent by the proprietary powers that be (ie keylogging, memory access / watchmen, over-network code execution or even remote operation of your computer); companies like Microsoft and Apple OR companies that put out propriety software that resides on your Microsoft or Apple computer. This has happened, happens, and will happen, in part because of the invisible proprietary code impervious to peer review. Leave behind your proprietary crutches if security is your concern!
2. Choose TAILS as that operating system
    - The first concern that will be raised by proprietary software advocates about free and open-source software is the lack of rigorous code creation; the idea is that security measures are best implemented when the developers are getting paid to implement them. That point is moot with TAILS. See their philosophy, dedication, and impact at https://tails.boum.org/

It's practically written in the stars: TAILS and whrwthal are made for each other <3. Namely because where passing a usb stick along to share the bible is viable, so is passing along another with TAILS, holding in it means to: easily execute whrwthal, access otherwise censored information, and freely communicate with people around the world or within a community in annonymity! This USB toolbelt is indispensible for the persectued Christian and future Convert alike.

## Anti-Warning ##
If you live in a country that doesn't burn books, go crazy, download **TWO** copies.

> For I am not ashamed of the gospel of Christ: - Romans 1:16

## TODO ##

In future releases, expect to see:

- [ ] Regular expressions
    - [X] Ability to directly type in regular expressions for advanced users (superhumans)

    - [ ] Pre-defined regex Checkboxes for real humans who don't speak robot

- [X] A limitation on searching overloaded words like "the" or "I", to prevent slow downs and crashes

- [X] Eliminate requirements and need for pip with a Pure Python implementation

- [ ] A title / header == the verse displayed by user's search selection from list

- [ ] Searched word highlighting to replace the current capitalization

- [ ] In-Text-Box buttons under each word, for quick searching, as well as custom cross references

- [ ] Bug-fix for search result buttons that incorrectly display the verse preview (ie "... word of GOD..." when it should be "... word of GOD.", etc.)

- [ ] Calendar synced "Daily Readings" to serve as a structured study tool (retrieved from BLB sites)

- [ ] Better tkinter / python embedding (possible compression methods) to make install non-hellish for Windows users

- [ ] PGP cryptographic protections

- [ ] Frequency charts

- [ ] More translations in a variety of tongues, in the public domain and reliable in their source and lineage. Examples include:

    - [ ] French (OST)

    - [X] German (LUT)

    - [X] Hebrew (LC)

    - [ ] Greek (TR)

    - [ ] Russian (RUSV)
    
    - [ ] Chinese (CKJV)

See further candidates for use in this app [here](http://textus-receptus.com/wiki/List_of_languages)

## Resources ##

For study tools to use in Christ-averse regions, see the following for print in your personal library. I haven't proof read these materials for doctrinal truth or accuracy; I don't speak any of these languages. In any case, I don't believe I should be gatekeeper. I leave it up to you to determine within your own conscience, Whether these things are true. See Acts 17:10-11, consider the Bereans!

- [Arabic](https://www.thegrace.com/)

- [Chinese](*pending*)

- [Korean](*pending*)

- [Others](*pending*)

## Bible Texts ##

Biblical translations in a variety of tongues are utilized to provide this graphical bible referencing to you for convenience; they are all in the public domain and reliable in their source and lineage, akin to the KJV (confirmed to the best of my ability). If you find it better to use these simple Text files instead of **whrwhtal**, you may find them [here](https://github.com/GregCM/whrwhtal/tree/texts).

You may download any or all of them, and please distribute them liberally. As mentioned, finding simple Text files like these online is very cumbersome, if at all possible, and one of the cheif motivations for this project has been to increase the visibility of such resources. Thank you!

## FAQ and Psuedo-Lies ##

- Windows Install size > 25MB?
    - Okay, technically not lighter than the competition when you run in Windows, but it's at most 5MB sitting in the thumb drive. Why use Windows anyway?

- Why use Windows anyway?
    - Great question, this FAQ section is really shaping up.
