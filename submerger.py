import datetime
import codecs

def srtparser(file):
    with codecs.open(file, 'r', 'utf-8') as f:
        file = f.read()

    file = file.split(sep='\n')
    srtdict = {}
    subctr = 1
    i = -1
    while True:
        i += 1
        if i >= len(file):
            break
        line = file[i].strip()
        if line == '':
            continue
        elif line.isnumeric() and int(line) == subctr:
            # print("Got Line Numbers")
            j = 0
            while True:
                j += 1
                if i+j >= len(file):
                    i = i+j
                    break
                line = file[i+j].strip()
                if line.isnumeric() and int(line) == subctr+1:
                    i = i+j-1
                    subctr += 1
                    break
                elif line == '':
                    continue
                elif " --> " in line:
                    # print("Got Timestamps")
                    timestamps = line.split(sep=' --> ')
                    timestamps = [datetime.datetime.strptime(t, '%H:%M:%S,%f') for t in timestamps]
                    srtdict[subctr] = timestamps
                else:
                    # print("Got Text")
                    srtdict[subctr].extend([line])
    for i in srtdict.keys():
        if len(srtdict[i]) > 3:
            # print("Correcting Lines")
            temp = srtdict[i][:2]
            temp.extend(["\r\n".join(srtdict[i][2:])])
            srtdict[i] = temp
    return srtdict

def srttostr(srtdict):
    srtstring = ""
    for i in srtdict.keys():
        srtstring = srtstring + str(i) + '\r\n' + srtdict[i][0].strftime('%H:%M:%S,%f')[:-3] + " --> " + srtdict[i][1].strftime('%H:%M:%S,%f')[:-3] + '\r\n' + srtdict[i][2] + '\r\n\r\n'
    return srtstring

def srtwriter(srtdict, file):
    srt = srttostr(srtdict)
    with codecs.open(file, 'w', 'utf-8') as f:
        f.write(srt)

def mergesrt(srt1, srt2, method='normal'):
    mergedsrt = srt1
    for key2 in srt2.keys():
        if key2 in srt2:
            mergedsrt[key2][-1] = mergedsrt[key2][-1] + '\r\n' + srt2[key2][-1]
        elif method == 'normal':
            mergedsrt[key2] = srt2[key2]
        elif method == 'nearest-cue': ## remaining
            pass
    return mergedsrt

def removelineno(srtdict):
    retsrt = {}
    for i in srtdict.keys():
        retsrt[srtdict[i][0]] = srtdict[i][1:]
    return retsrt

def addlineno(srtdict):
    retsrt = {}
    i = 1
    for key in sorted(srtdict.keys()):
        retsrt[i] = [key] + srtdict[key]
        i += 1
    return retsrt

def customisesrt(srtdict, loc=None, color=None):
    for i in srtdict.keys():
        if color != None:
            prefix = f'<font color="{color}">'
            suffix = "</font>"
            srtdict[i][-1] = prefix + srtdict[i][-1] + suffix

        if loc != None:
            if loc == 'center':
                srtdict[i][-1] = "{\\a10}" + srtdict[i][-1]
            elif loc == 'top-center':
                srtdict[i][-1] = "{\\a6}" + srtdict[i][-1]
            elif loc == 'top-left':
                srtdict[i][-1] = "{\\a5}" + srtdict[i][-1]
            elif loc == 'center-left':
                srtdict[i][-1] = "{\\a9}" + srtdict[i][-1]
    return srtdict



if __name__ == "__main__":
    srt1 = srtparser(r"001 Find out all about this course in less than 2 minutes.de.srt") 
    srt2 = srtparser(r"001 Find out all about this course in less than 2 minutes.en.srt")

    srt1 = removelineno(srt1)
    srt2 = removelineno(srt2)

    srt2 = customisesrt(srt2, color="#ffff54", loc='top-center') #Make the second srt look different

    mergedsrt = mergesrt(srt1, srt2, method='normal')

    mergedsrt = addlineno(mergedsrt)

    srtwriter(mergedsrt, r"output.srt")
