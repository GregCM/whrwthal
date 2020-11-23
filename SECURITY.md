## Reporting a Vulnerability
You may reach out directly to <gregcaceres@gmail.com> to report a security vulnerability.
I also encourage you to submit a detailed [issue](https://github.com/GregCM/issues) so that I can work on it, and direct others to that issue should I need help.
If the vulnerability is a matter of whrwthal's security measures, and if it's within my power to fix it, I will as my first priority.
If the vulnerability is a matter of your hardware or other software on your system, I ask that you do everything that you can to harden
your system on your own. I can offer advice, but writing code for whrwthal to rectify problems that are actually caused by some other program
or cause is not effective, efficient, or realistic. Those kinds of issues will recieve a won't-fix tag. I'll keep the issue open as long as
it's relevant, so that it's available to anyone who may actually have a solution to the problem outside of modifying whrwthal.

Please feel free to reach out. If you want to use whrwthal but can't because of security concerns, I will work on nothing but your issue until I fix it.
You'll recieve an update on my progress anytime I do a significant commit, or fix the issue. If the issue takes particularly long, I'll update you at
least biweekly, even if I haven't made any progress. When you report the vulnerability, let me know if there are any special precautions I should take
in updating or contacting you.

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
