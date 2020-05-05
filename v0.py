#!/usr/bin/python3
    
'''
_______________________________________________ 

This text-based app was written by Greg Caceres.
It is free to use, access, or edit. It is open
source, free as in beer and as in speech.

The Biblical translations used herein are all
in the public domain, and free to use, quote,
or share without limit, provided no changes
are made to the content therein.

If you are running on MicroSoft Windows,
see the install support for Python at

https://docs.python.org/3/using/windows.html

For other support, or if you have any 
questions about the app's functionality,
the content of the word of God, or
anything else related, contact at

gregcaceres@gmail.com
_______________________________________________
'''

from configparser import ConfigParser
import random as rnd
import curses.ascii
import collections
import subprocess
import json
import time
import sys
import os
import re


class bible:
    
    
    def __init__(self):
        
        '''
        ##################
        ##              ##
        ## Initializing ##
        ##              ##
        ##################
        '''

        self.config_obj = ConfigParser()
        try:
            self.config_obj.read('config.ini')
            self.fileLocation = self.config_obj['PATH']['main']
            self.language = self.config_obj['LANGUAGE']['current']
            self.type_speed = 'in'
            os.chdir(self.fileLocation)
        except KeyError:
            # Manual input required if searchpath isn't
            # already defined. This will then be saved for
            # next time and used as the working directory.
            fd =  input('\n'.join(["Bible's file location?",
                                   " Input: >> "]))
            # This directory contains BIBLE.txt & the directory's name itself.
            os.chdir(fd)

            self.config_obj['PATH'] = {'dir': fd}
            self.fileLocation = self.config_obj['PATH']['dir']

            self.config_obj['LANGUAGE'] = {'current': 'eng',
                                           'options':
                                           'eng,spa,fre,ger,heb,gre'}
            self.config_obj['TYPE SPEED'] = {'current': 'in',
                                             'options': 'ls,re,lt,in'}
            # Defaults:
            self.language = self.config_obj['LANGUAGE']['current']
            self.type_speed = self.config_obj['TYPE SPEED']['current']

            # Change to Defaults available in Settings menubar
            with open('config.ini', 'w') as cfg:
                    self.config_obj.write(cfg)

        fileName = ''.join(['.ToC_', self.language, '.json'])
        # Path for the full bible text.
        with open(fileName, 'r') as TableCont:
            [self.bkNames, self.bkAbbrv] = json.load(TableCont)

        if self.type_speed.upper()   == 'IN':
            self.type_speed = 0
        
        elif self.type_speed.upper() == 'LT':
            self.type_speed = 5000
         
        elif self.type_speed.upper() == 'RE':
            self.type_speed = 2500
        
        elif self.type_speed.upper() == 'LS':
            self.type_speed = 1250
        
        else:
            self.type_speed = 2500
        
        fileName = ''.join(['.BibDict_', self.language,'.json'])
        try:
            with open(fileName, 'r') as Bib:
                self.BibDict = json.load(Bib,object_pairs_hook=collections.OrderedDict)
        except:
            self.BibDict = self.makeBibDict(self)
            with open(fileName, 'w') as b:
                json.dump(self.BibDict, b, ensure_ascii=True)
    
    ## ______________________________ ##
    ##                                ##
    ## For Searching Verse References ## 
    ## ______________________________ ##                                         # TODO: Hide files for closed country safety
    
    def VerseRef(self, toShow='None'):
        
        BibDict = self.BibDict
        bkNames = self.bkNames
        bkAbbrv = self.bkAbbrv
        self.type_speed = self.type_speed
        
        if sys.platform.startswith('linux'):                                     # NOTE: Only works for Linux
            cmd  = ['xrandr']                                                         
            cmd2 = ['grep', '*']                                                     
            p  = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
            p.stdout.close()
            
            screenRatio = 135/1366                                               # On the source computer used to compile
            resString,foo = p2.communicate()                                     # this app, width resolution was 1366 pixels,
            resolution    = resString.split()[0]                                 # fullscreen window width was 135 characters.
            width, height = resolution.split(b'x')                                  
            screenWidth   = ''
            for l in str(width):
                if l.isnumeric():                                                # 'screenRatio' multiplied by whatever
                    screenWidth += l                                             # screen width will be used ensures the
            screenWidth    = int(screenRatio * float(screenWidth))               # character output always fits the screen.
        else:                                                                    # FIXME: Find a way to do the above if on
            screenWidth    = 135                                                 #        Windows and Mac OS-X  .  .  .
                                                                                 # NOTE: GUI application has this covered.
                                                                                 #       Terminal use will likely only be
                                                                                 #       Linux-based, possibly OS-X inclusive.
        
        truth = ''                                                               # Initialize 'truth' for concatenation.
        if toShow == 'Short':
            self.miniBibPreamble(self)
        elif toShow == 'Long':
            self.BibPreamble(self)                                                  # Nice little message with instructions.
        elif toShow == 'None':
            print('') 
        location = '' 
        while not location:                                                      # LOOPS UNTIL
            location = input('\n Where To?  ')                                   # <-- (asks for a place to go)
                                                                                 # INPUT IS GIVEN
        self.cls()
        print(' ' + location)                                                        
        time.sleep(0.25)
        
        loc     = list()
        locAlph = ''
        locNumb = ''
        for char in location:          
            if char.isalpha():                                                   # Saves the alphabetic part of location
                locAlph += char        
            else:                                                                # Saves the numeric part of location
                locNumb += char 
        loc.append(locAlph)
        loc.append(locNumb.strip())                                              # Combine the alphabetic and numeric parts to loc
        n = len(bkNames)                                                         # 66 books!
        book = ''                                                                # Book is empty by default, filled in this loop:
        for b in range(n):                                                       # LOOP THROUGH BOOKS
            LenAbb = len(bkAbbrv[b])                                             # Compare strings to see if input is in
            inToC  = (bkAbbrv[b] == location.upper()[0:LenAbb])                  # Table of Contents (ignore case); accounts
            if inToC:                                                            # for abbreviations of books.
                book   = bkAbbrv[b]
                bkMark = bkNames[b]                                              # <-- For use in troubleshooting (Line 233)
                break                                                            # Finish loop and save book.
            else:                                                                # Proceed to next book. If no match is  
                continue                                                         # found, 'book' would remain empty.
        
        if len(loc) > 1 :                                                        # parts (Lines 101-102 )... 
            chpRef = (loc[1])                                                    # <- This IF catches an empty numeric part --- 
            if not chpRef:                                                       # 0 indicates that no Chapters were specified: 
                chpRef = '0'                                                     # The book will be the only output.            
                                                                                 # <- ELSE catches the lack of numeric part --- 
        else:                                                                    
            chpRef = '0'
        
        if not chpRef == '0':                                                    # If there is a numeric part of 'loc',
            loc = chpRef                                                         # it can be used as the chapter reference.
            vrsRef  =  '0'
            for char in loc:           
                if char == ':':                                                  # If there is a colon, there is a verse ref.
                    loc = re.split(char,loc)
                    chpRef = loc [ 0 ]
                    vrsRef = loc [ 1 ]
            
            severalVrs = False
            for char in vrsRef:           
                if char == '-':                                                  # If there's a dash, there are multiple verses.
                    severalVrs   = True
                    vrsStart2Fin = re.split('-', vrsRef)
                    firstVerse   = vrsStart2Fin [ 0 ]
                    lastVerse    = vrsStart2Fin [ 1 ]
                    fV           = int(firstVerse)
                    lV           = int(lastVerse) + 1
            
            if not severalVrs: 
                firstVerse   = vrsRef
                fV           = int(firstVerse)
                lV           = 0
        
        if not location:
            toShow = 'None'
            self.VerseRef(toShow)
        elif location.upper() == 'DONE':
                self.cls()
                return '\n'
        elif location.upper() == 'ABOUT':
                print('\n'.join([
                             ' _______________________________________________\n',
                             
                             ' This text-based app was written by Greg Caceres',
                             ' It is free to use, access, or edit. It is open',
                             ' source, free as in beer and speech. The King',
                             ' James Bible has its publishing and usage rights',
                             ' vested in the Crown within the UK. Everywhere',
                             ' else it is in the public domain, and is free',
                             ' to use, quote, or share without limit provided',
                             ' no changes are made to the content therein.',
                             ' For support, or if you have any questions',
                             ' about the app\'s functionality, the content',
                             ' of the word of God, or anything else related,',
                             ' contact at\n',
                             ' gregcaceres@gmail.com',
                             ' _______________________________________________']))
                toShow = 'Long'
                self.VerseRef(toShow)
        elif location.upper() == 'OPTIONS':
                self.cls()
                ToC[0] = '_________________________'
                ToC[1] = '                         '
                ToC[2] = 'Table of Contents --- ToC'
                ToC[3] = '_________________________'
                ToC[4] = '                         '
                for i in range(5,(n+4)):
                    ToC[i] = bkNames[i-4] + ' ... ' + bkAbbrv[i-4]
                
                ToC[66+5]    = bkNames[66] + ' ... ' + bkAbbrv[66]
                print(ToC)
                toShow = 'None'
                self.VerseRef(toShow)
        elif location.upper() == 'HELP':
                toShow = 'Long' 
                self.VerseRef(toShow)
        elif location.upper() == 'PHRASE':
                self.PhraseSearch(self, bkNames, bkAbbrv, BibDict)
        
        if not book:
            fortunate = rnd.randint(0,1)
            if fortunate:
                noBRef = '\n F'
            else:
                noBRef = '\n Unf'
            
            noBRef = ''.join([
             '%sortunately, that book isn\'t found in scripture...' %(noBRef),
             ' Type \"options\" to see the table of',
             ' contents and book abbreviations. \n' ])
            
            input('\n'.join([noBRef,'\n PRESS ENTER']))
            toShow = 'None'
            self.VerseRef(toShow)
        else:                                                                    # Assign structure value for BOOKS
            truthFind   = BibDict[book]                                          # according to input if it was found
            truth       = ''                                                     # in the table of contents (Lines -42 to -24).
            if chpRef is '0':                                                    # If only book name is input, output whole book  
                                                                                 # LOOP through chapter keys
                cKeyList = range(len(truthFind.keys()))
                for cKey in cKeyList:                                            # Hone in on a chapter for the verse loop sake: 
                    cKey  = str(cKey+1)
                    cFind = truthFind[cKey]                                      # LOOP through verses keys                     
                    vKeyList = range(len(cFind.keys()))
                    for vKey in vKeyList:                                        # and concatenate each verse-field's string.
                        vKey   = str(vKey+1)
                        if vKey == '1':
                            cPrint = '\n\n Chapter %s \n\n' %(cKey)
                        else:
                            cPrint = '\n'
                        lines      = cFind[vKey]
                        truthLen   = len(lines)
                        lines2Loop = range(int(truthLen // screenWidth))
                        line       = [lines]
                        
                        for l in lines2Loop:
                            if truthLen > screenWidth:                           # For formatting, if verse longer than 1 line
                                begin       = screenWidth*l
                                end         = screenWidth*(l+1)
                                spcSearch   = line[l][begin:end]                 # (based on fullscreen pixle size == 135),
                                finalSpace  = spcSearch.rfind(' ')               # break the line at the last space.
                                if lines[1].isnumeric():
                                    delim   = '\n  '
                                else:
                                    delim   = '\n '
                                lines       =  delim.join([
                                               (line[l])[0:finalSpace],
                                               (line[l])[finalSpace:]
                                                         ]) 
                                truthLen    = len(line[l])                       # Loop as many times as overflow lines appear.
                            
                            cFind[vKey] = lines
                            
                        truth += cPrint + cFind[vKey]                            # <- Truth acquired!
                       # for i in range(10):
                       #     if chr(truth[i]) > 500:
                       #          FIXME: PRINT BACKWARDS
                    
                    print(''.join(['\n', self.slowType( truth, self.type_speed // (len(truthFind.keys())) )]))
            
            else:
                cKey   =   chpRef
                try:
                    cFind  =   truthFind[cKey]
                except:
                    cMax   =   len(truthFind.keys())
                    if cMax is 1:                                                    # Plural or not?
                        noCRef = 'ortunetly, %s only has %i chapter' %(bkMark,cMax)
                    else:
                        noCRef = 'ortunetly, %s only has %i chapters' %(bkMark,cMax)
                    fortunate = rnd.randint(0,1)
                    if fortunate:
                        noCRef = '\n F' + noCRef
                    else:
                        noCRef = '\n Unf' + noCRef
                  
                    print(noCRef)
                    toShow = 'None'
                    self.VerseRef(toShow)
                
                if vrsRef is '0':                                                  # If only chapter is input, output whole chapter
                    vKeyList = range(len(cFind.keys()))
                    for vKey in vKeyList:                                          # LOOP through these verses,
                        vKey       = str(vKey+1)
                        lines      = cFind[vKey]
                        line       = [lines]
                        truthLen   = len(lines)
                        lines2Loop = range(int(truthLen // screenWidth))
                        lines      = ''
                        for l in lines2Loop:
                            if truthLen > screenWidth:                           # For formatting, if verse longer than 1 line
                                begin       = screenWidth*l
                                end         = screenWidth*(l+1)
                                spcSearch   = line[l][begin:end]                 # (based on fullscreen pixle size == 135),
                                finalSpace  = spcSearch.rfind(' ')               # break the line at the last space.
                                if line[0][1].isnumeric():
                                    delim   = '\n  '
                                else:
                                    delim   = '\n '
                                lines      +=  delim.join([
                                               (line[l])[0:finalSpace],
                                               (line[l])[finalSpace:]
                                                         ]) 
                                line        = re.split('\n',lines)
                                truthLen    = len(line[l])                       # Loop as many times as overflow lines appear.
                                cFind[vKey] = lines
                            
                        truth   +=   '\n' + cFind[vKey]                            # and concatenate each verse-field\'s string.
                     
                    print(''.join(['\n',
                             self.slowType( truth, self.type_speed//len(cFind.keys()) )]))
                elif severalVrs:
                    for verseNum in range(fV,lV): 
                        vKey   =   str(verseNum)
                        try:
                            lines      = cFind[vKey]
                            line       = [lines]
                            truthLen   = len(lines)
                            lines2Loop = range(int(truthLen // screenWidth))
                            lines      = ''
                            for l in lines2Loop:
                                if truthLen > screenWidth:                           # For formatting, if verse longer than 1 line
                                    begin       = screenWidth*l
                                    end         = screenWidth*(l+1)
                                    spcSearch   = line[l][begin:end]                 # (based on fullscreen pixle size == 135),
                                    finalSpace  = spcSearch.rfind(' ')               # break the line at the last space.
                                    if line[0][1].isnumeric():
                                        delim   = '\n  '
                                    else:
                                        delim   = '\n '
                                    lines      +=  delim.join([
                                                   (line[l])[0:finalSpace],
                                                   (line[l])[finalSpace:]
                                                             ]) 
                                    line        = re.split('\n',lines)
                                    truthLen    = len(line[l])                       # Loop as many times as overflow lines appear.
                                    cFind[vKey] = lines
                            
                            truth += '\n' + cFind[vKey]                              # <- Truth acquired!
                        except:
                            vMax      = len(cFind.keys())
                            noVRef    = 'ortunetly, %s %s only has %i verses' %(bkMark,chpRef,vMax)
                            fortunate = rnd.randint(0,1)
                            if fortunate:
                                noVRef = '\n F' + noVRef
                            else:
                                noVRef = '\n Unf' + noVRef
                            print(noVRef)
                            self.VerseRef()
                    
                    print(''.join(['\n', self.slowType( truth, self.type_speed//(lV-fV) )]))
                  
                else:                                                              # Just one verse.
                    vKey   =   vrsRef
                    try:
                        lines      = cFind[vKey]
                        truthLen   = len(lines)
                        lines2Loop = range(int(truthLen // screenWidth))
                        line       = [lines]
                        for l in lines2Loop:
                            if truthLen > screenWidth:                             # For formatting, if verse longer than 1 line
                                spcSearch   = line[l][0:screenWidth]               # (based on fullscreen pixle size == 135),
                                finalSpace  = spcSearch.rfind(' ')                 # break the line at the last space.
                                if lines[1].isnumeric():
                                    delim   = '\n  '
                                else:
                                    delim   = '\n '
                                lines       =  delim.join([
                                               (line[l])[0:finalSpace],
                                               (line[l])[finalSpace:]
                                                         ])
                        truth     = '\n' + cFind[vKey]                             # <- Truth acquired!
                    except:
                      vMax      = len(cFind.keys())
                      noVRef    = ('ortunetly, %s %s only has %i verses'
                                                  %(bkMark,chpRef,vMax))
                      fortunate = rnd.randint(0,1)
                      if fortunate:
                          noVRef = '\n F' + noVRef
                      else:
                          noVRef = '\n Unf' + noVRef
                      print(noVRef)
                      toShow = 'None'
                      self.VerseRef(toShow)
                     
                    print(''.join(['\n', self.slowType(truth,self.type_speed)]))
        
        self.VerseRef('None')
        
    
    
    ## _____________________ ##
    ##                       ##
    ## For Searching Phrases ##
    ## _____________________ ##
    
    def PhraseSearch(self, toShow='None'):
        
        BibDict = self.BibDict
        bkNames = self.bkNames
        bkAbbrv = self.bkAbbrv
        
        if sys.platform.startswith('linux'):                                         # NOTE: Only works for Linux
            cmd = ['xrandr']                                                         
            cmd2 = ['grep', '*']                                                     
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
            p.stdout.close()
            
            screenRatio = 135/1366                                                   # On the source computer used to compile
            resString,junk = p2.communicate()                                        # this app, width resolution was 1366 pixels,
            resolution     = resString.split()[0]                                    # fullscreen window width was 135 characters.
            width, height  = resolution.split(b'x')                                  
            screenWidth    = ''
            for l in str(width):
                if l.isnumeric():                                                    # 'screenRatio' multiplied by whatever
                    screenWidth += l                                                 # screen width will be used ensures the
            screenWidth    = int(screenRatio * float(screenWidth))                   # character output always fits the screen.
        else:                                                                        # FIXME: Find a way to do the above if on
            screenWidth    = 135                                                     #        Windows and Mac OS-X  .  .  .
        
        sLine       = ' ' + '_'*int(screenWidth-2) + ' '
        qrtrSpace   = ' ' + ' '*int(0.25*(screenWidth-2)) + ' \n'              
        qrtrLine    = ' ' + '_'*int(0.25*(screenWidth-2)) + ' \n'                         
        hsLine      = qrtrSpace + qrtrLine
        
        if not toShow == 'None':
            self.miniBibPreamble(self)
            print('\n'.join([' Type \"\\Ref\" to switch over to verse referencing.\n',
    
                          '        Options -- \"\\Opt\"      Exit -- \"\\Done\" ',
                          '         ___________________________________________     \n']))
        
        Srch = ''
        while not Srch:
            Srch = input(' Search: ')
            self.cls()
        
        print(' Search: ' + Srch)
        
        if Srch.upper() == '\\OPT':
            print('\n '.join([ '',
                               'By default, the search will return',
                               'exact words and phrases. It is case-',
                               'insensitive and inclusive.',
                               'EX: \"hope\" will return \"Hopeful\".\n',
                               
                               'By default, whole phrases can only be searched',
                               'in sequence (i.e. \"the God LORD\" will not',
                               'return \"the LORD God\"... \"he lord go\" will).\n',
                               
                               'For extra options, type the following',
                               'in front of the the word or phrase.',
                               '[Separate all options with a space]\n',
                               
                               '  AO -- Any Of (At least one of the words you typed)',
                               '  (i.e. \"VB hope\" will only return \"hope\", excluding \"Hope\", \"hopeful\", etc.)\n',
                               
                               '  VB -- Verbose (Exactly as you type it)',
                               '  (i.e. \"VB hope\" will only return \"hope\", excluding \"Hope\", \"hopeful\", etc.)\n',
                               
                               '  BW -- Beginning of a word',
                               '  (i.e. \"BW wh\" will return \"who\", \"where\", \"whence\", etc.)\n',
                               
                               '  MW -- Middle of a word',
                               '  (i.e. \"MW id\" will return \"middle\", \"midst\", \"tide\", etc.)\n',
                               
                               '  EW -- End of a word',
                               '  (i.e. \"EW el\" will return \"Michael\", \"Gabriel\", \"Abel\",etc.)\n']))
        
        elif Srch.upper() == '\\DONE':
            exit()
        elif Srch.upper() == '\\REF':
            self.VerseRef(self, 'Long')
        else:
            first_addOns = ''
            last_addOns = ''
            addOns = ''
            reSrch = ''
            addList = ['AO','VB','BW','MW','EW']
            addOn_Count = 0
            while not reSrch:
                try:
                   cmd = re.split(' ',Srch)
                   if addList[1] in Srch.upper().split(' '):                        # VB -- VERBOSE
                       reOpt = re.VERBOSE
                       Srch = ' '.join([el for el in cmd if el.upper() not in addList[1]])

                   elif addList[2] in Srch.upper().split(' '):                      # BW -- BEGINNING OF WORD
                       if addOn_Count > 0: first_addOns += r'|(?<![a-zA-Z])'
                       else: first_addOns += r'(?<=\s)'
                       addOn_Count += 1
                       Srch = ' '.join([el for el in cmd if el.upper() not in addList[2]])
                   
                   elif addList[3] in Srch.upper().split(' '):                      # MW -- MIDDLE OF WORD
                       if addOn_Count > 0: first_addOns += r'|\b(?=[a-z]{2})'; last_addOns += r'|(?=[a-z]{2})\b'
                       else: addOns += r'(?<=(\\b[a-zA-Z]{1}))(?=[a-z])'
                       addOn_Count += 1
                       Srch = ' '.join([el for el in cmd if el.upper() not in addList[3]])
                   
                   elif addList[4] in Srch.upper().split(' '):                      # EW -- END OF WORD
                       if addOn_Count > 0: addOns += r'|(?![a-zA-Z])'
                       else: addOns += r'(?![a-zA-Z])'
                       addOn_Count += 1
                       Srch = ''.join([el for el in cmd if el.upper() not in addList[4]])
                   
                   elif addList[0] in Srch.upper().split(' '):                      # AO -- ANY OF
                       if addOn_Count > 0: addOns += r''
                       else: addOns += r''
                       addOn_Count += 1
                       Srch = ' '.join([el for el in cmd if el.upper() not in addList[0]])
                   
                   else:
                       Srch = ' '.join(cmd)
                       if addOn_Count > 1: addOns = ''.join(['(',addOns,')'])
                       reSrch = ''.join([r'(%s)' %(Srch),addOns])
                       m = re.compile(reSrch)
                       print(reSrch)
                       time.sleep(1)
                except Exception as inst: 
                    print(inst.args)
                    print(inst)
                    time.sleep(10)
            
            print((sLine + '\n')*2)
            count = 0
            verses = []
            vFound  = list()
            for bKeySpaced in bkAbbrv:
                bKey = bKeySpaced.replace(' ','')
                chpDict = BibDict[bKey]
                chpIter = chpDict.keys()
                for cKey in chpIter:
                    vrsDict = chpDict[cKey]
                    vrsIter = vrsDict.keys()
                    for vKey in vrsIter:
                        lines      = vrsDict[vKey]
                        truthLen   = len(lines)
                        lines2Loop = range(int(truthLen // screenWidth))
                        line       = list()
                        vrsList    = list()
                        vrsList.append(lines)                                    
                        if re.search(reSrch,vrsList[0]):
                            vFound.append(m.sub(Srch.upper(),vrsList[0]))        # Precompiled - pattern.sub(replacement,str)

                                                                                  # TODO: Externalize as function applied to Dict.
                        #if truthLen > screenWidth:                               # For formatting, if verse longer than 1 line
                        #    for l in lines2Loop:
                        #        line.append(lines[0:(l*screenWidth)])
                        #        lines       = lines[(l*screenWidth):]
                        #        spcSearch   = line[l][0:screenWidth]             # (based on fullscreen pixel size == 135),
                        #        finalSpace  = spcSearch.rfind(' ')               # break the line at the last space.
                        #        try:
                        #            if lines[2].isnumeric():
                        #                delim   = '\n   '
                        #            elif lines[1].isnumeric():
                        #                delim   = '\n  '
                        #            else:
                        #                delim   = '\n '
                        #        except:
                        #            failures.append(lines + bKey + '--' + cKey + ':' + vKey)
                        #        
                        #        vrsList[v]     =  delim.join([
                        #                       (line[l])[0:finalSpace],
                        #                       (line[l])[finalSpace:]
                        #                                    ])
                        
                        
                        vLen = len(vFound)
                        if vLen > 0:
                            for v in range(vLen):
                                if not (vFound[v])[0].isnumeric():
                                    ref = ''.join([bKeySpaced, ' ', cKey, ':1 '])
                                    print('\n '.join(['', ref, vFound[v], '\n']))
                                
                                else:
                                    vrsAlph,vrsNumb = '',''
                                    for char in vFound[v]: 
                                        if char.isdigit():                       # Saves the numeric part of the verse.
                                            vrsNumb += char 
                                        
                                        else:
                                            vrsAlph += char 
                                    
                                    ref = ''.join([' ', bKeySpaced, ' ', cKey, ':', vrsNumb])
                                    print('\n'.join(['', ref, '', vrsAlph, '\n', ]))
                                
                                del vFound[0]
                                print(hsLine)
                            count += vLen
            
            if count is 0:
               print('\n '.join(['\n','THERE ARE %i VERSES WHICH CONTAIN %s' %( count, Srch.upper() ),'']))
               
            elif count is 1:
               print('\n '.join(['\n','THERE IS %i VERSE WHICH CONTAINS %s'  %( count, Srch.upper() ),'']))
               
            else:
               print('\n '.join(['\n','THERE ARE %i VERSES WHICH CONTAIN %s' %( count, Srch.upper() ),'']))
            
            print(sLine)
            print(sLine)
            print('\n')
        self.PhraseSearch(self, 'None')
    
    def slowType(string,typeSpeed):
        if typeSpeed > 0:                                                            # Progressive output printing
            for char in string:                                                      # for progressive output print
                sys.stdout.write(char)                                               # friendly folk.
                sys.stdout.flush()
                time.sleep(rnd.random()*10.0/typeSpeed)                              # Typing speed in words per minute.
        else:
            sys.stdout.write(string)
        
        return ''
    
    def cls():
        
        ispc    = sys.platform.startswith('win')
        ismac   = sys.platform.startswith('darwin')                                  # Platform name for Mac OS X
        islinux = sys.platform.startswith('linux')
        
        if ispc:
            _ = os.system('cls')
        elif ismac or islinux:
            _ = os.system('clear')
         
        return ''
    
    def BibPreamble(self, *args):
        
        self.cls()
        cross = '\n'.join(['\n\n                 ',
                         '    \\             /  ',
                         '     \\     _     /   ',
                          '          | |        ',
                          '          | |        ',
                          '     _____| |_____   ',
                          '    |_____   _____|  ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          |_|        ',
                          '  _______/   \\_______\n\n'])
        
        version = '\n'.join([' ______________________\n',
        
                             '  THE KING JAMES BIBLE   ',
                             ' ______________________\n',
            
                             ' Please rightly divide and handle with prayer. \n\n'])
        
        AppFormat = '\n'.join([' The format: \n\n When queried "Where To?", a good response would be one of the following...\n',
        
                         ' To find a verse-to-verse passage -- "Book Chapter:Verse-Verse".',
                         '         EX: "Romans 5:8-10"\n',
        
                         ' To find only one verse -- "Book Chapter:Verse".',
                         '         EX: "John 3:16"\n',
                         ' To find full chapters -- "Book Chapter".',
                         '         EX: "Psalm 119"\n',
                         ' To find full books -- "Book".',
                         '         EX: "Philemon"\n\n',
                         ' ______________________________________________________________ \n',
                        
                         ' Type "Help" to display this page again.',
                         ' Type "About" for information about the app.',
                         ' Type "Options" for a list of recognized book names.',
                         ' Type "Phrase" to switch over to phrase searching.',
                         ' Type "Done" to finish searching and quit.\n'])
        
        return [self.slowType(cross,self.type_speed),self.slowType(version,self.type_speed),self.slowType(AppFormat,self.type_speed)]
    
    def miniBibPreamble(self):
        
        self.cls()
        
        cross = '\n'.join(['\n\n                 ',
                         '    \\             /  ',
                         '     \\     _     /   ',
                          '          | |        ',
                          '          | |        ',
                          '     _____| |_____   ',
                          '    |_____   _____|  ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          | |        ',
                          '          |_|        ',
                          '  _______/   \\_______\n\n'])
        
        version = '\n'.join([' ______________________\n',
        
                             '  THE KING JAMES BIBLE   ',
                             ' ______________________\n',
        
                             ' Please rightly divide and handle with prayer. \n\n'])
        
        return self.slowType(cross + version,self.type_speed)

    def makeBibDict(self):
        if self.ispc: 
            pathPart = '\\'                                                                                     
        elif (self.ismac or self.islinux):
            pathPart = '/'

        bfile = self.pathPart.join([self.fileLocation, 'BIBLE.txt'])
        with open(bfile, 'r') as f:
            bib = f.read()

        # TODO: Add verbal details to progress bar status updates
        child = tk.Tk()
        child.title('Importing')
        msg = 'Please wait while the text is compiled...'
        info = tk.Label(child, text=msg, relief='flat')
        progress = ttk.Progressbar(child, orient='horizontal',
                                   length=100, mode='determinate')
        info.pack(padx=5, pady=5)
        progress.pack(padx=5, pady=5)

        progress['value'] = 1
        prog_max = len(bib)

        # Letters and space for Concordance compilation
        alpha_space = string.ascii_letters + ' '

        n = len(self.bkNames)
        books = []
        trim_books = []
        trim_text = ''
        for b in range(n):
            m = re.compile(r'^(%s)' % (self.bkNames[b]))
            if b < 65:
                text = re.split(self.bkNames[b+1], bib)[0]
                # Exclude titles from text.
                bib = m.sub('', bib)
                text = m.sub('', text)

            elif b == 65:
                text = bib

            # Clear books already coverd.
            bkWiper = ''
            bkToWipe = text
            bib = bib.replace(bkToWipe, bkWiper)

            books.append(text)
            trim_text += ''.join([l for l in text if l in alpha_space])
            trim_books.append(trim_text)

        bible = ''.join(books)
        trim_bible = ''.join(trim_books)
        # Whole Bible excluding punctuation and book titles.
        bib_letters = ''.join([l for l in trim_bible])
        bib_words = re.split(' ', bib_letters)
        bib_words = [w for w in bib_words if w != '']
        # Concordance equivalent
        unique_words = [s for s in set(bib_words) if s not in self.bkNames]

        BibDict = collections.OrderedDict()
        # Loops to populate the book structure.
        for b in range(n):
            # Chapters marked uniquely (":1 " =  c.x:v.1)
            chapters = re.split(':1 ', books[b])[1:]
            cLen = len(chapters)
            chpDict = collections.OrderedDict()
            # Loops to populate the chapter structure.
            for c in range(cLen):
                # Add the verse 1 marker again for verse indexing:
                chapters[c] = ':1 ' + chapters[c]
                # Indexes the places where verses MAY appear.
                idx = chapters[c].find(':')
                for x in [idx]:
                    if (chapters[c])[x+1].isnumeric():
                        # Only the numeral indexed places are retained
                        # (i.e. "1:2" retained, "Behold: Foo" is not).
                        delim = str(c+1) + ':'
                        verses = re.split(delim, chapters[c])
                vLen = len(verses)
                vrsDict = collections.OrderedDict()
                # Loops to populate the verse structure.
                for v in range(vLen):
                    if v == 0:
                        # Removes the extra colon left in each verse 1.
                        m = re.compile(':1 ')
                        verses[v] = m.sub('1 ',verses[v])

                    # Beginning of line whitespace strip
                    m = re.compile(r'(^\s*)')
                    verses[v] = m.sub('',verses[v])

                    # End of line whitespace / misc. strip
                    # EX: "Amen. I" / "Amen. 1" / "Amen.  "
                    m = re.compile(r'([\s\dI]{1,}$)')
                    verses[v] = m.sub('',verses[v])

                    vrsKey = str(v + 1)
                    vrsDict[vrsKey] = verses[v]

                # Structure field names cannot or
                # should not start with numbers.
                # Dictionary field names cannot
                # contain spaces (I SAM is ISAM).
                chpKey = str(c+1)
                chpDict[chpKey] = vrsDict

            bkKey = (self.bkAbbrv[b]).replace(' ', '')
            BibDict[bkKey] = chpDict

        BibDict['CONCORDANCE'] = unique_words
        return BibDict

    def ismember(a,b):
       bind = {} 
       for i,elt in enumerate(b):
           if elt not in bind:
               bind[elt] = i
               return [bind.get(itm,None) for itm in a]

def navigation():
    
    ## ___________________ ##
    ##                     ##
    ## Picking Your Poison ##
    ## ___________________ ##
    
    inLoop = True
    while inLoop:
        bible.cls()
        bible.BibPreamble(bible)
        inLoop  = False
        What2Do = input('\n '.join([
                        'BIBLE NAVIGATION MENU',
                         '    Verse Reference?',
                         '      Phrase Search?',
                         '            [V/P] >> ']))
        
        if What2Do.upper()   == 'V':
            bible.VerseRef(bible, 'Long')
        elif What2Do.upper() == 'P':
            bible.PhraseSearch(bible, 'Long')
        else:
            inLoop = True 
        

if __name__ == '__main__':
    bible.__init__(bible)
    navigation()

