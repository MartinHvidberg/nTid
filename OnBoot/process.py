
""" Giving you the numbers you need for tidsregistrering. """

import datetime

NORMAL_HOURS = 7.5

def ceilfloor2minute(dtt, mode='ceil', step=5):
    if mode in ['ceil', 'floor']:
        hour = dtt.hour
        minu = dtt.minute
        while minu%step != 0:
            if mode == 'ceil':
                minu -= 1
            elif mode == 'floor':
                minu += 1
        return datetime.datetime(dtt.year, dtt.month, dtt.day, hour, minu)
    else:
        return dtt

str_filename_in = "OnBoot.ecl"
dic_workdays = dict()

## Read in the file data
with open(str_filename_in, 'r') as fil_in:
    for lin in fil_in:
        if not ":" in lin:
            continue  # Likely not a valid line
        lst_tok = [l.strip() for l in lin.rsplit(":", 1)]
        try:  # Extract the date
            ddt_lin = datetime.datetime.strptime(lst_tok[0], "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as e:
            print("Error: {}".format(e))
            ddt_lin = None
            continue
        ##print("raw: {} time: {}".format(lst_tok, dt_lin))
        dat_lin = ddt_lin.date()
        if not dat_lin in dic_workdays.keys():
            dic_workdays[dat_lin] = list()
        dic_workdays[dat_lin].append(ddt_lin)

## Calculate each days work, and present it...
print("\nWorkday\t\tarr.\tdep.\thours")
dic_flex = dict()
for k in sorted(dic_workdays.keys()):
    ##print("{}".format(k))
    lst_ddt = dic_workdays[k]
    lst_ddt.sort()
    #for d in lst_ddt:
    #    print("\t{}".format(d))
    if len(lst_ddt) > 1:
        arr_tim = ceilfloor2minute(lst_ddt[0], 'ceil', 5)
        dep_tim = ceilfloor2minute(lst_ddt[-1], 'floor', 5)
        dur_hours = (dep_tim - arr_tim).total_seconds()/(60*60)
        num_flex = dur_hours - NORMAL_HOURS
        ##print("\t< {} \n\t> {}".format(str(arr_tim.time())[:5], str(dep_tim.time())[:5]))
        ##print("\t= {} hours".format(round(dur_hours, 2)))
        print("{0}\t{1}\t{2}\t{3:5.2f}\t{4:5.2f}".format(
            k,
            str(arr_tim.time())[:5],
            str(dep_tim.time())[:5],
            round(dur_hours, 2),
            round(num_flex, 2)))
        # record flex
        if not k.month in dic_flex.keys():
            dic_flex[k.month] = list()
        dic_flex[k.month].append(num_flex)
    else:
        print("{}\t...".format(k))

## Frint the Flex-statistics
print("\nFlex:")
for k in sorted(dic_flex.keys()):
    print("Month {} = {} hours".format(k, round(sum(dic_flex[k])), 3))

## Figure out when to go home today :-)
dat_today = datetime.datetime.now().date()
for k in dic_workdays.keys():
    if k == dat_today:
        dtt_first = sorted(dic_workdays[k])[0]
        dtt_free = dtt_first + datetime.timedelta(hours=NORMAL_HOURS)
        print("\nToday you can go home at: {}".format(str(dtt_free.time())[:5]))


### End of Python script ...
