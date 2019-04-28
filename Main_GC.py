# -*- coding: cp1255 -*-
#!! -*- coding: utf-8 -*-
"""
Created on 27/04/19

@author: Symbiomatrix

Todo:

Features:
Convert escaped vcs file to plain utf.

Future:
 

Notes:
- The file contains utf in the form of hex separated by equal signs.
  Newlines separated by double sign which prevents import completely.
  Gcal doesn't seem to encode this utf in any format, but it accepts it as utf files.
- Heb may occur in any field (summary, location, description and continuation),
  so any double = in a line is interpreted as such (timezone contains one),
  or starting with = (continuation may have only one hex pair).
- Useful list: https://www.fileformat.info/info/charset/UTF-8/list.htm?start=1024
- When non heb chars appear in same field, they are converted to utf as well, handy.
- You should import to a separate calendar under the user, for the sake of order.

Bugs:
- Gcalendar seems to struggle with 3k events in the same file.
  Splitting to 2 worked just fine (~30s import, only 4 were dropped).

Version log:
28/04/19 V1.0 Simple converter complete. 
27/04/19 V0.0 New.

"""

# Example conversion: 
# From UTF8=D7=99= ... 
# vv = codecs.decode("D799D795D79D20D794D795D79CD793D7AA20D" +
#                    "79CD799D7A0D795D79920D795D7A8D799D7A0D794", "hex").decode('utf-8')
# Contains a number.
# =D7=91=D7=99=D7=AA=20=D7=AA=D7=91=D7=95=D7=A8=20=33=37
# Pure eng encoded.
# =4C=75=6E=63=68=2E

import codecs
import os

UTFENC = "utf-8-sig"
UTFENC2 = "utf-8"
NEWLINE = "\r\n"
DEFDIR = ""
#DEFIN = "calendar.vcs"
DEFIN = "Testcalendar1.vcs"
#DEFOUT = "calendarOut.vcs"
DEFOUT = "TestCalenderOut.vcs"  

def Hex_Convert(mrgln):
    """Converts hex delimited string to utf.
    
    Format: (normal):=hexp1=hexp2=hexp1=hexp2=..."""
    pln = "".join(mrgln)
    isplit = pln.find(":=") + 1
    # Leave the normal info intact.
    pln2 = [pln[:isplit],pln[isplit:]]
    pln2[1] = pln2[1].replace("=","")
    pln2[1] = codecs.decode(pln2[1],"hex").decode(UTFENC2)
    pln2.append(NEWLINE)
    plnc = "".join(pln2)
    
    return plnc

def Read_Convert(fldir = DEFDIR,flin = DEFIN,flout = DEFOUT):
    """Converts escaped utf to plain.
    
    Provide path and in / out files.
    Mind, continued lines are the only cause of merger -
    one heb inscription may be followed by another, both converted separately."""
    flinpt = os.path.join(fldir,flin)
    floutpt = os.path.join(fldir,flout)
    mrgln = [] 
    with codecs.open(flinpt,"r",UTFENC) as flr:
        with codecs.open(floutpt,"w",UTFENC) as flw:
            for ln in flr:
                indcont = False
                if ln.startswith("="):
                    indcont = True
                if not indcont: # Convert utf lines and flush the buffer.
                    if len(mrgln) > 0:
                        plnc = Hex_Convert(mrgln)
                        flw.write(plnc)
                    mrgln = []
                if indcont or ln.count(":=") >= 1:
                    # Conversion may consist of multiple parts, add them to queue.
                    # Final newline shall be added later.
                    lntrim = ln.lstrip("=").rstrip(NEWLINE)
                    mrgln.append(lntrim)
                else: # Simple line is written instantly.
                    flw.write(ln)
                
            if len(mrgln) > 0:
                plnc = Hex_Convert(mrgln)
                flw.write(plnc)
                
    return 0

def Main():
    """Activates function calls.
    
    Main."""
    verr = 0
    verr = Read_Convert()
    print("\nFin.")
    
    return verr

if __name__ == "__main__":
    Main()
