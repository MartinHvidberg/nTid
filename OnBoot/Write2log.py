import sys
import datetime

print("====== Write2Log.py - Start ============================================")
strMessage = "Boot - presumably"
strComputer = "some computer"
if len(sys.argv) > 1:
	strMessage = sys.argv[1].strip()
	if len(sys.argv) > 2:
		strComputer = sys.argv[2].strip()
strLog = "\n"+str(datetime.datetime.now())+" : " + strMessage + strComputer
print(sys.argv[0] + " says: " + strLog)
f = open("OnBoot.ecl","a")
f.write(strLog)
f.close()
print("------ Write2Log.py - End ----------------------------------------------")

