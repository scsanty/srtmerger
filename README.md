# srtmerger
To merge two subtitles together.

Steps:
1) parse two separate srt files using 'srtparser'
e.g. Usage:
srt1 = srtparser(r"001 Find out all about this course in less than 2 minutes.de.srt") 
srt2 = srtparser(r"001 Find out all about this course in less than 2 minutes.en.srt")

2) remove the line numbers from the parsed srt texts using 'removelineno'
e.g. Usage: 
srt1 = removelineno(srt1)
srt2 = removelineno(srt2)

3) You may customise the srt to differentiate the, using 'customisesrt'
e.g. Usage:
srt2 = customisesrt(srt2, color="#ffff54", loc='top-center')
color and loc are named arguments, color accept Color Hex codes, loc accepts 'center', 'top-center', 'top-left', 'center-left'

4) You can now merge this two srts using 'mergesrt'
e.g. Usage:
mergedsrt = mergesrt(srt1, srt2, method='normal')
method, named argument has two procesdures, a) time-wise juxtaposing the same subtitles together, b) time-wise copying to the nearest cue for srt file 1 (under development)

5) Add the line numbers back again, before writting them back into file.
e.g. Usage:
mergedsrt = addlineno(mergedsrt)

6) Write the subtitle back into a file.
e.g. Usage:
srtwriter(mergedsrt, r"output.srt")

Any developmental inputs are welcomed.

In development:
1) Nearest Cue, method of merging
2) GUI
3) Executor(Executor GUI) to batch merge, multiple files.
