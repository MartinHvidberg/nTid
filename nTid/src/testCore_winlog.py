
import nTidCore

def PrintStats():
    print "Age      :",logWin.age()
    print "Status   :",logWin.status()
    print "Stat.usrs:",logWin.users()#[1]
    #print "Stat.user:",logWin.stat("user")[1]
    #print "Stat.time:",logWin.stat("time")[1]
      
print "\n *** Test winlog ***"

#init
print "\n * init *"
#print(logWin.__doc__)
logWin = nTidCore.Winlog()
PrintStats()

#populate
print "\n * populate *"
#print logWin.populate.__doc__
logWin.populate("winXPlog")
PrintStats()

#process()
print "\n * process *"
#print logWin.process.__doc__
logWin.process(["RES\\mahvi"])
PrintStats()
#logWin.process(logWin.stat("users")[1])
#PrintStats()

#stat(mode)
#get(user,time,mode)

print "\n *** Done test winlog ***"