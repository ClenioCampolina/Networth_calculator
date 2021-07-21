import time

def savetime():
    ct = time.localtime()
    if len(str(ct.tm_mday)) < 2:
        day = '0' + str(ct.tm_mday)
    else:
        day = str(ct.tm_mday)
    if len(str(ct.tm_mon)) < 2:
        mon = '0' + str(ct.tm_mon)
    else:
        mon = str(ct.tm_mon)
    savetime = str(ct.tm_year) + '_' + mon + '_' + day
    #print("Savetime created")
    return savetime


def day():
    ct = time.localtime()
    return ct.tm_mday

def month():
    ct = time.localtime()
    return ct.tm_mon

def year():
    ct = time.localtime()
    return ct.tm_year

