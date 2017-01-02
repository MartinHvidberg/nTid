

import win32com.client

computer = "."
SWbemServices = win32com.client.Moniker("winmgmts:{impersonationLevel=impersonate,(Security)}!\\\\" + computer + "\\root\\cimv2")
LoggedEvents = SWbemServices.ExecQuery("Select * from win32_NTLogEvent WHERE Logfile = 'Security'") 

lstEventCode = []
lstEventName = []
for itm in LoggedEvents:
    if ((itm.Category == 2)):                    #  and (itm.EventCode == 682)(itm.User == 'RES\mahvi') and 
        if itm.EventCode not in lstEventCode:
            lstEventCode.append(itm.EventCode)
        #print ' TimeGenerated',itm.TimeGenerated
        #print ' TimeWritten',itm.TimeWritten
        #print ' Category',itm.Category
        #print ' CategoryString',itm.CategoryString
        #print ' ComputerName',itm.ComputerName
        #print ' Data',itm.Data                            # Always None
        #print ' EventCode',itm.EventCode
        #print ' EventIdentifier',itm.EventIdentifier
        #print ' EventType',itm.EventType  
        #print ' Type',itm.Type
        #print ' InsertionStrings',itm.InsertionStrings
        #print ' LogFile',itm.LogFile
        #print ' Message',itm.Message    
        strEventName = itm.Message[0:itm.Message.index(':')]
        if not strEventName in lstEventName:
            lstEventName.append(strEventName)
        #print ' RecordNumber',itm.RecordNumber
        #print ' SourceName',itm.SourceName
        #print ' User',itm.User
        #print '======'

print lstEventCode
print lstEventName
# Category == 4 => 'Anvendelse af rettigheder' ('Specielle rettigheder tildelt nyt logon')   
# Category == 2 => 'Logon/Logoff' ('Brugerlogoff'  || 'Logon lykkedes')

# [528] [u'Logon lykkedes']
# [529] [u'Logonfejl']
# [537] [u'Logonfejl']
# [538] [u'Brugerlogoff']
# [540] [u'Netv\xe6rkslogon lykkedes']
# [551] [u'Brugerstartet logoff']
# [682] [u'Sessionen genoprettede forbindelsen til WinStation']