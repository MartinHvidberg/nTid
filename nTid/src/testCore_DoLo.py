
import nTidCore

def PrintStats():
    print "age        :",logWin.age()
    print "status     :",logWin.status()
    print "users      :",logWin.users()
      
print "\n *** Test DoLo ***"

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

print "\n * process *"
#print logWin.rocess.__doc__
logWin.process(logWin.users())
PrintStats()

#GetStatText()

print "\n *** Done test DoLo ***"

print logWin.Report