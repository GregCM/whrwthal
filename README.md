# whrwhtal #
Offline bible referencing for bible minded folk! Including UI display, verse and phrase lookup, and regular expressions to help accelerate bible learning past that of top scholars. Why is **whrwhtal** better than other systems (honorable mentions: [BLB](https://www.BlueLetterBible.org/), [bontibon's kjv](https://github.com/bontibon/kjv), [crosswire](https://crosswire.org/), [Xiphos](https://Xiphos.org/))? Read on!

*Note: whrwthal is still in early development, and not yet fit for regular use*

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

If this returns at least ``Python 3.5.X`` then skip ahead to [First-Use](README.md#First-Use).
``Python 2.X`` users will need to upgrade; ``Python 3.4.X`` users will also need to upgrade, with the extra caveat that your default Python3 environment will need to be changed from 3.X.Y to 3.5.X as follows in folder sequence:

> Control Panel > All Control Panel Items > System > Advanced System Settings > Environment Variables

### Python ###
If internet is unreliable and you want the ability to use **whrwhtal** on several machines (or share it so your recipients can use-as-is), see the install support pages below for embeddable versions of Python, with additional steps needed to include "tkinter". To circumvent these extra steps, and in general hit the ground running, simply install the latest from the first link:
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

Name the file ``whrwthal.desktop`` and populate it accordingly. An icon will now appear in your applications menu to easily access **whrwhtal**!

You can change the default settings stored during your first setup at any time through the Options menu; this includes Language, Colors, Directories, and more. Alternatively, directly alter "config.ini".

## Resources ##

For study tools to use in Christ-averse regions, see the following for print in your personal library. I haven't proof read these materials for doctrinal truth or accuracy; I don't speak any of these languages. In any case, I don't believe I should be gatekeeper. I leave it up to you to determine within your own conscience, Whether these things are true. See Acts 17:10-11, consider the Bereans!

- [Arabic](https://www.thegrace.com/)

- [Chinese](*pending*)

- [Korean](*pending*)

- [Others](*pending*)

## Bible Texts ##

Biblical translations in a variety of tongues are utilized to provide this graphical bible referencing to you for convenience; they are all in the public domain and reliable in their source and lineage, akin to the KJV (confirmed to the best of my ability). If you find it better to use these simple Text files instead of **whrwhtal**, you may find them [here](https://github.com/GregCM/whrwhtal/tree/texts).

You may download any or all of them, and please distribute them liberally. As mentioned, finding simple Text files like these online is very cumbersome, if at all possible, and one of the cheif motivations for this project has been to increase the visibility of such resources. Thank you!
