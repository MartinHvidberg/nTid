
import nTidCore

strMode = "Statistics" # ["Confirm","Statistics","ShowDoLo"]

def PrintStats():
    print "age        :",logWin.age()
    print "status     :",logWin.status()
    print "users      :",logWin.users()
    if len(logWin.users())>0:        
        for strU in logWin.users():
            print "report for :",strU
            #print logWin.report(strU,"LoginLogout","This week",{"Report":"Confirm"})
            #print logWin.report(strU,"LoginLogout","This week",{"Report":"Classic","DateFormat":"YY-MM-DD","TimeFormat":"hh.mm"})
            #print logWin.report(strU,"LoginLogout","This week",{"Report":"Classic","DateFormat":"<%a %d. %b>","TimeFormat":"<%H %M>"})
            print logWin.report(strU,"LoginLogout","This month",{"Report":"Classic_Duration","DateFormat":"<%a %d. %b>","TimeFormat":"<%H:%M>","DurationFormat":"hh.dd"})

      
print "\n *** Test DoLo ***"

# init #############
if True:
    print "\n * init *"
    logWin = nTidCore.Winlog()
    if strMode == "Statistics":
        PrintStats()
    if strMode == "ShowDoLo":
        print logWin.showdolo()
    

# TupleText() #############
if False:
    print "EarliestAcceptedDay",logWin.t["EarliestAcceptedDay"]
    for keyN in logWin.times():
        print keyN,logWin.t[keyN]
        print keyN,logWin.listdates(keyN)
    
    
# populate #############
if True:
    print "\n * populate *"
    #print logWin.populate.__doc__
    logWin.populate("winXPlog")
    if strMode == "Statistics":
        PrintStats()
    if strMode == "ShowDoLo":
        print logWin.showdolo()

# process #############
if True:
    print "\n * process *"
    #print logWin.rocess.__doc__
    logWin.process(logWin.users())
    if strMode == "Statistics":
        PrintStats()
    if strMode == "ShowDoLo":
        print logWin.showdolo()
  
print "\n *** Done test DoLo ***"