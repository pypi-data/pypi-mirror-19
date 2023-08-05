import rowingdata
#from rowingdata import TCXParser,RowProParser,ErgDataParser,TCXParserNoHR
#from rowingdata import BoatCoachParser
#from rowingdata import MysteryParser
#from rowingdata import painsledDesktopParser,speedcoachParser,ErgStickParser
#from rowingdata import SpeedCoach2Parser,FITParser,fitsummarydata
import os

def checkfile(f2,verbose=False):
    fileformat = rowingdata.get_file_type(f2)
    notread = 1
    if verbose:
        print fileformat

    if len(fileformat)==3 and fileformat[0]=='zip':
        with zipfile.ZipFile(f2) as z:
            f = z.extract(z.namelist()[0],path='C:/Downloads')
            fileformat = fileformat[2]
            os.remove(f_to_be_deleted)
            
    if fileformat == 'unknown':
	return 0

    # handle non-Painsled
    if (fileformat != 'csv'):
	# handle RowPro:
	if (fileformat == 'rp'):
	    row = rowingdata.RowProParser(f2)
	    # handle TCX
	if (fileformat ==  'tcx'):
	    row = rowingdata.TCXParser(f2)
            row.write_csv(f2+'o.csv')
            row = rowingdata.rowingdata(csvfile=f2+'o.csv')
            os.remove(f2+'o.csv')
            notread = 0

	# handle Mystery
	if (fileformat == 'mystery'):
	    row = rowingdata.MysteryParser(f2)

	# handle TCX no HR
	if (fileformat == 'tcxnohr'):
	    row = rowingdata.TCXParserNoHR(f2)
            row.write_csv(f2+'o.csv')
            row = rowingdata.rowingdata(csvfile=f2+'o.csv')
            os.remove(f2+'o.csv')
            notread = 0
	    
	# handle ErgData
	if (fileformat == 'ergdata'):
	    row = rowingdata.ErgDataParser(f2)

	# handle BoatCoach
	if (fileformat == 'boatcoach'):
	    row = rowingdata.BoatCoachParser(f2)

	# handle painsled desktop
	if (fileformat == 'painsleddesktop'):
	    row = rowingdata.painsledDesktopParser(f2)

	# handle speed coach GPS
	if (fileformat == 'speedcoach'):
	    row = rowingdata.speedcoachParser(f2)

	# handle speed coach GPS 2 
	if (fileformat == 'speedcoach2'):
	    row = rowingdata.SpeedCoach2Parser(f2)
    
	# handle ErgStick
        if (fileformat == 'ergstick'):
	    row = rowingdata.ErgStickParser(f2)
		    
	# handle FIT
	if (fileformat == 'fit'):
	    row = rowingdata.FITParser(f2)
            row.write_csv(f2+'o.csv')
            row = rowingdata.rowingdata(csvfile=f2+'o.csv')
            os.remove(f2+'o.csv')
            notread = 0

        if notread:
            row = rowingdata.rowingdata(df=row.df)

    else:
        row = rowingdata.rowingdata(csvfile=f2)

    nr_of_rows = row.number_of_rows
    distmax = row.df['cum_dist'].max()
    timemax = row.df['TimeStamp (sec)'].max()-row.df['TimeStamp (sec)'].min()
    nrintervals = len(row.df[' lapIdx'].unique())
    
    if verbose:
        print "nr lines",row.number_of_rows
        print "data ",row.rowdatetime
        print "dist ",distmax
        print "Time ",timemax
        print "Nr intervals ",nrintervals

    res =  row.intervalstats_values()
    int1time = res[0][0]
    int1dist = res[1][0]

    if verbose:
        print "Interval 1 time ",int1time
        print "Interval 1 dist ",int1dist

    y = row.rowdatetime.year
    m = row.rowdatetime.month
    d = row.rowdatetime.day
    h = row.rowdatetime.hour
    minute = row.rowdatetime.minute
    sec = row.rowdatetime.second

    results = {
        'type':fileformat,
        'nr_lines':nr_of_rows,
        'year':y,
        'month':m,
        'day':d,
        'hour':h,
        'minute':minute,
        'second':sec,
        'dist':int(distmax),
        'seconds':int(timemax),
        'nrintervals':nrintervals,
        'lap 1 time': int(int1time),
        'lap 1 dist': int(int1dist),
        }
    
    return results
        
