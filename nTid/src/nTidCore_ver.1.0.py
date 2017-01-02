#!/usr/bin/python

"""
This program holds all the functionality needed for getting the windows log file, and presenting 
it in a nice, filtered and formatted way. I use it to assist me in filling in 'time registration'.

It is intented to be called from other Python programs, in particulary one that handle GUI or
command line interfaces.

A 'normal' use would typically be:
1) Create a variable of type Winlog, this calls __init__ that builds an initial DoLo data structure
2) Call populate() to fill in data from the windows log file
3) Call users() to see which users have been using this computer
4) Call process() to build statistics for one or more of these users
5) Call report to create text report for one user, in one time interval.
6,... Keep calling process and report for various combinations of information...
"""

## History
# ver. 1.0 The basic and most important functionality is in place, and released for live user test...

## ToDo list
# XXX Clean up the mess with "About three months back...", and friends, being hard-coded in multiple places...
# XXX Introduce Date-format and Time-format
# XXX Introduce more Styles
#    Including, Weekdays, Duration, ... maybe user defined formats...
# XXX Implement Reverse sorting order
# XXX Introduce file that remember user settings from run to run
# XXX Nicen up the GUI with logo and stuff

#import string
from datetime import datetime
from datetime import date
from datetime import timedelta

class Winlog:

    """
    This is the Winlog Class Doc-string
    
    Winlog has a custom data structure DoLo that you don't need to know about when calling through
    the functions, but is important to understand if you intent to edit the code.
    
    """
    
    def __init__(self):
        self.d = { # Data dictionary
                  "__EC_d_status":0, # "Empty"
                  "__EC_timenow":datetime.now(), # Now, in the sense: When this program is running
                  "__EC_statistics":{}} # One dic of Stat, e.i. 1 DoLo, per user
                  
        self.g = { # General dictionary - information not exclusive to the concrete log instance
                  "__EC_modes":["LoginLogout","Security"],
                  "__EC_times":["This week", "Last week", "This week + last week", "This month", "Last month", "About three months back..."],
                  "__EC_process_status":{0:"Empty",
                                         1:"Populating",
                                         2:"Populated",
                                         3:"Partly processed",
                                         4:"Processed"},
                  "__EC_DoLo_status":{0:"Empty",
                                      1:"LOE",
                                      2:"DOS"},
                  "__EC_LLcodes":{528:"Successful Logon",
                                  538:"User Logoff",
                                  540:"Successful Network Logon",
                                  551:"User initiated logoff",
                                  576:"Special privileges assigned to new logon"
                                  },                  
                  "__EC_lstUserFilter":["AUTHORITY","lpeassistent"] # Strings, or substrings, that exclude users from this program...
                  }
        # Calculating Fixed dates - Calculated here to calc. them only once.
        datToday = date.today()
        datFirstDayofThisWeek = datToday - timedelta(days=datToday.timetuple()[6]) # i.e. most recent Monday
        datFirstDayofLastWeek = datFirstDayofThisWeek - timedelta(weeks=1)
        datFirstDayofThisMonth = datToday.replace(day=1)
        y = datToday.year
        m = datToday.month
        d = 1
        if m == 1:
            y -= 1
            m = 12
        else:
            m -= 1
        datFirstDayofLastMonth = date(y,m,d)
        datADateAboutThreeMonthsAgo = datFirstDayofThisWeek - timedelta(weeks=12)   
        self.t = { # General dictionary - informations about dates, fixed relative to now (today)
                "EarliestAcceptedDay" : datADateAboutThreeMonthsAgo,
                "This week":(datFirstDayofThisWeek,datToday),
                "Last week":(datFirstDayofLastWeek,datFirstDayofThisWeek - timedelta(days=1)),
                "This week + last week":(datFirstDayofLastWeek,datToday),
                "This month":(datFirstDayofThisMonth,datToday),
                "Last month":(datFirstDayofLastMonth,datFirstDayofThisMonth - timedelta(days=1)),
                "About three months back...":(datADateAboutThreeMonthsAgo,datToday)
                }
        self.f

    def status(self):
        """ Return the Status of the 'd' data structure, as a string"""
        return [self.d["__EC_d_status"],self.g["__EC_process_status"][self.d["__EC_d_status"]]]
    
    def showdolo(self):
        """
        Shows (return as multi-line string) the DoLo data structure.
        This is Only intented for debugging purposes!
        """
        strReport = "<<< DoLo - begin >>>"
        strReport += "\n   .d status: "+str(self.d["__EC_d_status"])+" => "+self.g["__EC_process_status"][self.d["__EC_d_status"]]
        #return strReport
        if self.d["__EC_d_status"] < 2:
            strReport += "\n   self.d is Un-populated. There are no DoLo's"
        else: # self.d is at least 'populated'
            strReport += "\n   Users in .d: "+str(self.users())
            for strUser in self.users():
                doloR = self.d["__EC_statistics"][strUser]
                strReport += "\n    User: "+strUser
                strReport += "\n     DoLo-status: "+str(doloR["DoLo_Status"])+" => "+self.g["__EC_DoLo_status"][doloR["DoLo_Status"]]
                if doloR["DoLo_Status"] == 1: # LOE
                    strReport += "\n     len(LOE): "+str(len(doloR["LOE"]))
                    for objN in doloR["LOE"]:
                        strReport += "\n      "+repr(objN)
                if doloR["DoLo_Status"] == 2: # DOS
                    for keyDL in doloR["DOS"]:
                        strReport += "\n      keyDL: "+keyDL+" len() "+str(len(doloR["DOS"][keyDL]))
                        if len(doloR["DOS"][keyDL])>0:
                            for keyDate in doloR["DOS"][keyDL]:
                                    strReport += "\n       keyDate: "+str(keyDate)+" "+str(type(doloR["DOS"][keyDL][keyDate]))+" len() "+str(len(doloR["DOS"][keyDL][keyDate]))
                                    if len(doloR["DOS"][keyDL][keyDate])>0:
                                        for keyODS in doloR["DOS"][keyDL][keyDate]:
                                            strReport += "\n        ODS: "+str(keyODS)+repr(doloR["DOS"][keyDL][keyDate][keyODS])
                
        strReport += "\n<<< DoLo - end >>>"
        return strReport
    
    def age(self):
        """ Return the Age of the 'd' data structure, as a <type 'datetime.timedelta'>  __  Only used for debugging"""
        return datetime.now() - self.d["__EC_timenow"]
    
    def modes(self):
        """Return list of known 'modes' as strings."""
        return self.g["__EC_modes"]
    
    def times(self):
        """Return the 'times', i.e. time intervals, known to the program"""
        return self.g["__EC_times"]
            
    def users(self):
        """Returns a list of known 'users' as strings. Requires populate() to be run first"""
        if self.d["__EC_d_status"]<2:
            return [] # Can't call populate() is we don't know which mode...
        else:
            return self.d["__EC_statistics"].keys()
            
    def listdates(self,strT):
        lstDates = []
        datN, datStop = self.t[strT]
        while datN<=datStop:
            lstDates.append(datN)
            datN += timedelta(days=1)
        return lstDates

    def populate(self,strMode):
        """ Populate the data structure, by reading raw data from the win log files    
            
            This function gets the Log data and place them in a DoLo data structure.
            It will also populate some general statistics object.
            
            Requires: a mode
                Modes supported:
                    winXPlog: Default
                    win7log: Remains to be seen         
            
            Returns: a ReturnCode (integer)
            
            Valid ReturnCodes, and their meaning:
                0   : Success
                101 : Winlog: Error - Invalid mode
                102 : Winlog: Error - Trying to populate a non-empty data structure
        """
        
        if self.d["__EC_d_status"] != 0: # "Empty"
            print "Winlog: Error - Trying to populate a non-empty data structure"
            return 102
        else:
            self.d["__EC_d_status"] = 1 # "Populating..."
        
        def PutTUCinDoLo(TUC):           
            if TUC['user'] not in self.d["__EC_statistics"].keys(): # user never seen before, open new DoLo 
                DoLo =  {"DoLo_Status":0,"LOE":[],"DOS":{"LOD":{},"POT":{}}} # Dic-of-List-of. POT is Pre.fabs Of Text and is not used yet
                self.d["__EC_statistics"][TUC['user']] = DoLo        
                self.d["__EC_statistics"][TUC['user']]["DoLo_Status"] = 1 # "LEO"             
            self.d["__EC_statistics"][TUC['user']]["LOE"].append(TUC)
            return
        
        if strMode=="winXPlog":  
            import win32com.client
            computer = "."
            SWbemServices = win32com.client.Moniker("winmgmts:{impersonationLevel=impersonate,(Security)}!\\\\" + computer + "\\root\\cimv2")
            LoggedEvents = SWbemServices.ExecQuery("Select * from win32_NTLogEvent WHERE Logfile = 'Security'")    

            for itm in LoggedEvents:
                bolLegalUser = True
                if str(type(itm.User)) == "<type 'NoneType'>": # I don't know where they come from, but they must go
                    bolLegalUser = False
                if bolLegalUser: # more tests...
                    for strFilter in self.g["__EC_lstUserFilter"]: # Excluding system users log events
                        if strFilter in itm.User:
                            bolLegalUser = False
                if bolLegalUser: # For non-filtered user names ...      
                    TUC = {} # Time User Code
                    TUC['time'] = datetime.strptime(itm.TimeGenerated.split(".")[0],"%Y%m%d%H%M%S")       
                    if TUC['time'].date() >= self.t["EarliestAcceptedDay"]:                    
                        TUC['user'] = itm.User
                        TUC['code'] = itm.EventCode
                        PutTUCinDoLo(TUC)       
            del TUC
            self.d["__EC_d_status"] = 2 # "Populated"
            return 0
        else:
            print('Winlog: Error - Invalid mode')
            return 101

    def process(self,lstUsers):
        
        def UpdateFirstLast(ODSn,TUC):
            
            # ODS = {"LoginLogout":[Earliest, Latest],"Security":[Earliest, Latest]}
            # event = TUC = {"time":datetime,"user":unicode,"code":int}
            
            def UpdFstLst(lstFL,timT):
                if timT < lstFL[0]:
                    lstFL[0] = timT
                if timT > lstFL[1]:
                    lstFL[1] = timT
                return lstFL
            
            t = TUC["time"]
            for m in self.g["__EC_modes"]:
                if m == "Security":
                    # if 'code' apply to Security, well they all do...
                    ODSn[m] = UpdFstLst(ODSn[m],t)
                if m == "LoginLogout":
                    if TUC["code"] in self.g["__EC_LLcodes"]:
                        ODSn[m] = UpdFstLst(ODSn[m],t)
            return ODSn
        
        for usrN in lstUsers:
            if usrN in self.users():                
                # --- Process one user
                doloS = self.d["__EC_statistics"][usrN] # Get the DoLo out
                #XXX Check if the user is allready processed...
                if doloS["DoLo_Status"]!=2:
                    # -- Begin: Build DOS-LOD from LOE - Tactic 1. is more data, less process
                    LOE = doloS["LOE"]
                    LOD = doloS["DOS"]["LOD"] # Checking out the LOD
                    for evnt in LOE: # Sort from LOE, by date into DOS.LOD
                        d = evnt["time"].date()
                        if d in LOD.keys():
                            LOD[d].append(evnt)
                        else:
                            LOD[d] = [evnt]
                    del LOE, d
                    # -- Process DOS.LOD from list of events to dic of Stat
                    for d in LOD:                    
                        ODS = {} # Make empty ODS One Days of Statistics 
                        for m in self.g["__EC_modes"]: # So far ["LoginLogout","Security"]
                            ODS[m] = [datetime.max,datetime.min] # List of (Earliest, Latest)
                        for e in LOD[d]: # Fill ODS from list in LOD[d]
                            ODS = UpdateFirstLast(ODS,e)
                        LOD[d]=ODS # putting it back...                 
                    #for k in LOD.keys():
                    #    print "k:",k
                    
                    doloS["DOS"]["LOD"] = LOD # putting the LOD back...    
                    doloS["DoLo_Status"] = 2 # "DOS"
                    # -- End: Build DOS-LOD from LOE
                self.d["__EC_statistics"][usrN] = doloS # put the DoLo back...
            else:
                print "Error - Trying to process unknown user. You should never see this message !!! : "+usrN
        return 0
    
    def report(self,strUser,strMode,strTime,dicStyle={"Report":"Default","DateFormat":"ISO","TimeFormat":"ISO","Reverse":False}):
        # Check that relevant statistics is build 
        if self.d["__EC_d_status"] < 2:
            return "\n report() : self.d seems to be un-populated"
        doloR = self.d["__EC_statistics"][strUser]
        if doloR["DoLo_Status"] == 0:
            return "\n report() : DoLo for this user seems to be Empty"
        if doloR["DoLo_Status"] == 1:
            return "\n report() : DoLo for this user is LOE - Use showdolo() if you wan't to see the LEO..."
        
        # Handling Styles separately ...
        
        if dicStyle["Report"] == "Confirm": # Confirm my request 
            return "Confirming :: U:"+strUser+" M:"+strMode+" T:"+strTime+" R:"+dicStyle["Report"]
        
        dicLOD = doloR["DOS"]["LOD"]
            
        if dicStyle["Report"] == "Classic":           
            strReport = ""
            for dayN in self.listdates(strTime):
                strReport += "\n"+str(dayN)
                if dayN in dicLOD:
                    strReport += " : "+str(dicLOD[dayN][strMode][0].time())+" >> "+str(dicLOD[dayN][strMode][1].time())
                    
                else:
                    strReport += " :    No records"
                
        
            #for keyN in dicLOD:
            #    strReport += "\n k "+str(type(keyN))+str(keyN)
            
            return strReport
        
        else: # Unknown strReportStyle
            return "You selected a report for: \n  - "+strUser+"\n  - "+strMode+"\n  - "+strTime+"\nBut the ReportStyle do not recognized ("+dicStyle["Report"]+")"
        
if __name__ == '__main__':
    
    print(" ! This is not a Main program, please don't call it directly...")
