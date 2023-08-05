import math
import numpy as np
#import pylab
#import scipy
import re
import warnings
import checkdatafiles

#warnings.warn("Experimental version. Downgrade to 0.93.6 if you are not adventurous.",UserWarning)

__version__ = "0.93.7"

try:
    from Tkinter import Tk
    tkavail = 1
except ImportError:
    tkavail = 0


import matplotlib

if tkavail == 0:
    matplotlib.use('Agg')


import matplotlib.pyplot as plt
from matplotlib import figure
import os
import pickle
import getpass
import mechanize
import pandas as pd

from tqdm import tqdm

from fitparse import FitFile

from utils import *

from csvparsers import (
    CSVParser,
    painsledDesktopParser,
    BoatCoachParser,
    speedcoachParser,
    ErgDataParser,
    ErgStickParser,
    MysteryParser,
    RowProParser,
    SpeedCoach2Parser,
    totimestamp,
    make_cumvalues_array,
    make_cumvalues,
    timestrtosecs,
    timestrtosecs2,
    get_file_type,
    get_file_line,
    skip_variable_footer,
    get_rowpro_footer,
    skip_variable_header,
    lbstoN,
    )

from otherparsers import (
    fitsummarydata,
    FITParser,
    TCXParserNoHR,
    TCXParser,
    )

weknowphysics = 0

try:
    import rowingphysics
    weknowphysics = 1
    theerg = rowingphysics.erg()
except ImportError:
    weknowphysics = 0

import time
import datetime
import iso8601
from calendar import timegm
from pytz import timezone as tz,utc


import dateutil
import writetcx
import trainingparser

from dateutil import parser

from lxml import objectify,etree
from math import sin,cos,atan2,sqrt
from numpy import isnan,isinf
from matplotlib.pyplot import grid
from pandas import Series, DataFrame
    
from matplotlib.ticker import MultipleLocator,FuncFormatter,NullFormatter
from sys import platform as _platform

from scipy import interpolate
from scipy.interpolate import griddata






def main():
    str = "Executing rowingdata version %s. " % __version__
    if weknowphysics:
	str += rowingphysics.main()
    return str

def my_autopct(pct,cutoff=5):
    return ('%4.1f%%' % pct) if pct > cutoff else ''

def nanstozero(nr):
    if isnan(nr) or isinf(nr):
	return 0
    else:
	return nr



def spm_toarray(l):
    o = np.zeros(len(l))
    for i in range(len(l)):
	o[i] = l[i]

    return o


def make_cumvalues_rowingdata(df):
    """ Takes entire dataframe, calculates cumulative distance
    and cumulative work distance
    """

    workoutstateswork = [1,4,5,8,9,6,7]
    workoutstatesrest = [3]
    workoutstatetransition = [0,2,10,11,12,13]

    xvalues = df[' Horizontal (meters)']
    mask = df[' WorkoutState'].isin(workoutstatesrest)
    xvalues.loc[mask] = 0.0*xvalues.loc[mask]

    mask = df[' WorkoutState'].isin(workoutstatetransition)
    xvalues.loc[mask] = 0.0*xvalues.loc[mask]

    res = make_cumvalues(xvalues)
    cumworkmeters = res[0]

    res = make_cumvalues(df[' Horizontal (meters)'])
    cummeters = res[0]
    lapidx = res[1]

    return [cummeters,lapidx,cumworkmeters]
	


def tailwind(bearing,vwind,winddir,vstream=0):
    """ Calculates head-on head/tailwind in direction of rowing

    positive numbers are tail wind

    """

    b = math.radians(bearing)
    w = math.radians(winddir)

    vtail = -vwind*cos(w-b)-vstream
    
    return vtail

def copytocb(s):
    	""" Copy to clipboard for pasting into blog

	Doesn't work on Mac OS X
	"""
	if (_platform == 'win32'):
	    r = Tk()
	    r.withdraw()
	    r.clipboard_clear()
	    r.clipboard_append(s)
	    r.destroy
	    print "Summary copied to clipboard"

	else:
	    res = "Your platform {pl} is not supported".format(
		pl = _platform
		)
	    print res

def phys_getpower(velo,rower,rigging,bearing,vwind,winddirection,vstream=0):
    power = 0
    tw = tailwind(bearing,vwind,winddirection,vstream=0)
    velowater = velo-vstream
    if (weknowphysics==1):
	res = rowingphysics.constantvelofast(velowater,rower,rigging,Fmax=600,
					     windv=tw)
	force = res[0]
	power = res[3]
	ratio = res[2]
	res2 = rowingphysics.constantwattfast(power,rower,rigging,Fmax=600,windv=0)
	vnowind = res2[1]
	pnowind = 500./res2[1]
	if (power>100):
	    try:
#		reserg = rowingphysics.constantwatt_ergtempo(power,rower,
#							     theerg,theconst=1.0,
#							     aantal=20,aantal2=20,
#							     ratio=ratio)

		reserg = rowingphysics.constantwatt_erg(power,rower,
							theerg,theconst=1.0,
							aantal=20,aantal2=20,
							ratiomin=ratio-0.2,ratiomax=ratio+0.2)
	    except:
		# reserg = [0,0,0,0,0]
		reserg = [np.nan,np.nan,np.nan,np.nan,np.nan]
	else:
	    # reserg = [0,0,0,0,0]
	    reserg = [np.nan,np.nan,np.nan,np.nan,np.nan]
	ergpower = reserg[4]
	
	result = [power,ratio,force,pnowind,ergpower]
    else:
	# result = [0,0,0,0,0]
	result = [np.nan,np.nan,np.nan,np.nan,np.nan]

    return result

	    
def write_obj(obj,filename):
    """ Save an object (e.g. your rower) to a file
    """
    pickle.dump(obj,open(filename,"wb"))

def read_obj(filename):
    """ Read an object (e.g. your rower, including passwords) from a file
        Usage: john = rowingdata.read_obj("john.txt")
    """
    res = pickle.load(open(filename))
    return res

def getrigging(fileName="my1x.txt"):
    """ Read a rigging object
    """

    try:
	rg = pickle.load(open(fileName))
    except (IOError,ImportError,ValueError):
	if __name__ == '__main__':
	    print "Getrigging: File doesn't exist or is not valid. Creating new"
	    print fileName
	if (weknowphysics == 1):
	    rg = rowingphysics.rigging()
	else:
	    rg = 0

    return rg

def getrower(fileName="defaultrower.txt",mc=70.0):
    """ Read a rower object

    """

    try:
	r = pickle.load(open(fileName))
    except (IOError,ImportError):
	if __name__ == '__main__':
	    print "Getrower: Default rower file doesn't exist. Create new rower"
	r = rower(mc=mc)

    return r


def getrowtype():
    rowtypes = dict([
	('Indoor Rower',['1']),
	('Indoor Rower with Slides',['2']),
	('Dynamic Indoor Rower',['3']),
	('SkiErg',['4']),
	('Paddle Adapter',['5']),
	('On-water',['6']),
	('On-snow',['7'])
	])
    
    return rowtypes

def running_mean(x):
    cumsum = np.cumsum(x)
    return cumsum/(1.+np.arange(len(x)))

def histodata(rows):
    # calculates Power/Stroke Histo data from a series of rowingdata class rows
    power = np.array([])
    for row in rows:
	    power = np.concatenate((power,row.df[' Power (watts)'].values))


    return power
	
def cumcpdata(rows):
    # calculates CP data from a series of rowingdata class rows
    maxt = 0
    for row in rows:
	thismaxt = row.df[' ElapsedTime (sec)'].max() 
	if thismaxt > maxt:
	    maxt = thismaxt

    maxlog10 = np.log10(maxt)

    logarr = np.arange(100)*maxlog10/100.

    logarr = 10.**(logarr)
    
    delta = []
    dist = []
    cpvalue = []
    velovalue = []
    spms = []

    for row in rows:
	cumdist = row.df['cum_dist']
	elapsedtime = row.df[' ElapsedTime (sec)']
#	spm = row.df[' Cadence (stokes/min)']
	

	for i in range(len(cumdist)-2):
	    resdist = cumdist.ix[i+1:]-cumdist.ix[i]
	    restime = elapsedtime.ix[i+1:]-elapsedtime[i]
	    timedeltas = np.nan_to_num(restime.diff())

	    velo = resdist/restime
	    pace = 500./velo
	    power = 2.8*velo**3
#	    spmv = running_mean(spm[i+1:])

	    power.name = 'Power'
	    restime.name = 'restime'
	    resdist.name = 'resdist'
	    velo.name = 'Velo'
	    #cpvalues = power.values
	    #distvalues = resdist.values
	    #logarr = restime.values
	    cpvalues = griddata(restime.values,power.values,
				logarr,method='linear',fill_value=0)
	    distvalues = griddata(restime.values,resdist.values,
				  logarr,method='linear',
				  fill_value=resdist.max())

#	    spmvalues = griddata(restime.values,spmv.values,
#				  logarr,method='linear',
#				  fill_value=spmv.max())


	    for cpv in cpvalues:
		cpvalue.append(cpv)
	    for d in logarr:
		delta.append(d)
	    for d in distvalues:
		dist.append(d)
#	    for s in spmvalues:
#		spms.append(s)
		
    delta = pd.Series(delta,name='Delta')
    cpvalue = pd.Series(cpvalue,name='CP')
    dist = pd.Series(dist,name='Distance')
#    spms = pd.Series(spms,name='SPM')

    df = pd.DataFrame({'Delta':delta,
		       'CP':cpvalue,
		       'Distance':dist,
#		       'SPM':spms,
		       })

    

#    df = df.sort_values(['Delta','CP','Distance','SPM'],ascending=[1,0,1,1])
    df = df.sort_values(['Delta','CP','Distance'],ascending=[1,0,1])
    df = df.drop_duplicates(subset='Delta',keep='first')

#    df = df[df['CP'] <= 1000]

    return df


def interval_string(nr,totaldist,totaltime,avgpace,avgspm,
		    avghr,maxhr,avgdps,avgpower,
		    separator='|'):
    """ Used to create a nifty text string with the data for the interval
    """

    stri = "{nr:0>2.0f}{sep}{td:0>5.0f}{sep}{inttime:0>5}{sep}".format(
	nr = nr,
	sep = separator,
	td = totaldist,
	inttime = format_pace(totaltime)
	)

    stri += "{tpace:0>7}{sep}{tpower:0>5.1f}{sep}{tspm:0>4.1f}{sep}{thr:3.1f}".format(
	tpace=format_pace(avgpace),
	sep=separator,
	tspm=avgspm,
	thr = avghr,
        tpower = avgpower,
	)

    stri += "{sep}{tmaxhr:3.1f}{sep}{tdps:0>4.1f}".format(
	sep = separator,
	tmaxhr = maxhr,
	tdps = avgdps
	)


    stri += "\n"
    return stri

def workstring(totaldist,totaltime,avgpace,avgspm,avghr,maxhr,avgdps,
               avgpower,
	       separator="|",symbol='W'):

    if np.isnan(totaldist):
	totaldist = 0
    if np.isnan(avgpace):
	avgpace = 0
    if np.isnan(avgspm):
	avgspm = 0
    if np.isnan(avghr):
	avghr = 0
    if np.isnan(maxhr):
	maxhr = 0
    if np.isnan(avgdps):
	avgdps = 0
    if np.isnan(avgpower):
	avgpower = 0
    if np.isnan(totaltime):
	totaltime = 0

    pacestring = format_pace(avgpace)


    

    stri1 = symbol
    stri1 += "-{sep}{dtot:0>5.0f}{sep}".format(
	sep = separator,
	dtot = totaldist,
	#tottime = format_time(totaltime),
	# pacestring = pacestring
	)

    stri1 += format_time(totaltime)+separator+pacestring
	

    stri1 += "{sep}{avgpower:0>5.1f}{sep}{avgsr:0>4.1f}{sep}{avghr:0>5.1f}{sep}".format(
	avgsr = avgspm,
        avgpower = avgpower,
	sep = separator,
	avghr = avghr
	)

    stri1 += "{maxhr:3.1f}{sep}{avgdps:0>4.1f}\n".format(
	sep = separator,
	maxhr = maxhr,
	avgdps = avgdps
	)

    return stri1
    

def summarystring(totaldist,totaltime,avgpace,avgspm,avghr,maxhr,
                  avgdps,avgpower,
		  readFile="",
		  separator="|"):
    """ Used to create a nifty string summarizing your entire row
    """

    if np.isnan(totaldist):
	totaldist = 0
    if np.isnan(avgpace):
	avgpace = 0
    if np.isnan(avgspm):
	avgspm = 0
    if np.isnan(avghr):
	avghr = 0
    if np.isnan(maxhr):
	maxhr = 0
    if np.isnan(avgdps):
	avgdps = 0
    if np.isnan(avgpower):
	avgpower = 0
    if np.isnan(totaltime):
	totaltime = 0

    stri1 = "Workout Summary - "+readFile+"\n"
    stri1 += "--{sep}Total{sep}-Total-{sep}--Avg--{sep}-Avg-{sep}Avg-{sep}-Avg-{sep}-Max-{sep}-Avg\n".format(sep=separator)
    stri1 += "--{sep}Dist-{sep}-Time--{sep}-Pace--{sep}-Pwr-{sep}SPM-{sep}-HR--{sep}-HR--{sep}-DPS\n".format(sep=separator)

    pacestring = format_pace(avgpace)


    #    stri1 += "--{sep}{dtot:0>5.0f}{sep}{tottime:7.1f}{sep}".format(
    stri1 += "--{sep}{dtot:0>5.0f}{sep}".format(
	sep = separator,
	dtot = totaldist,
	#tottime = format_time(totaltime),
	# pacestring = pacestring
	)

    stri1 += format_time(totaltime)+separator+pacestring
	
    stri1 += "{sep}{avgpower:0>5.1f}".format(
        sep = separator,
        avgpower = avgpower,
        )
    
    stri1 += "{sep}{avgsr:2.1f}{sep}{avghr:3.1f}{sep}".format(
	avgsr = avgspm,
	sep = separator,
	avghr = avghr
	)

    stri1 += "{maxhr:3.1f}{sep}{avgdps:0>4.1f}\n".format(
	sep = separator,
	maxhr = maxhr,
	avgdps = avgdps
	)

    return stri1


def format_pace_tick(x,pos=None):
	min=int(x/60)
	sec=int(x-min*60.)
	sec_str=str(sec).zfill(2)
	template='%d:%s'
	return template % (min,sec_str)


def y_axis_range(ydata,miny=0,padding=.1,ultimate=[-1e9,1e9]):

    # ydata must by a numpy array

    ymin = np.ma.masked_invalid(ydata).min()
    ymax = np.ma.masked_invalid(ydata).max()


    yrange = ymax-ymin
    yrangemin = ymin
    yrangemax = ymax



    if (yrange == 0):
	if ymin == 0:
	    yrangemin = -padding
	else:
	    yrangemin = ymin-ymin*padding
	if ymax == 0:
	    yrangemax = padding
	else:
	    yrangemax = ymax+ymax*padding
    else:
	yrangemin = ymin-padding*yrange
	yrangemax = ymax+padding*yrange

    if (yrangemin < ultimate[0]):
	yrangemin = ultimate[0]

    if (yrangemax > ultimate[1]):
	yrangemax = ultimate[1]


    
    return [yrangemin,yrangemax]
    

def format_dist_tick(x,pos=None):
	km = x/1000.
	template='%6.3f'
	return template % (km)

def format_time_tick(x,pos=None):
	hour=int(x/3600)
	min=int((x-hour*3600.)/60)
	min_str=str(min).zfill(2)
	template='%d:%s'
	return template % (hour,min_str)


class summarydata:
    """ This is used to create nice summary texts from CrewNerd's summary CSV

    Usage: sumd = rowingdata.summarydata("crewnerdsummary.CSV")

           sumd.allstats()

	   sumd.shortstats()

	   """
    
    def __init__(self, readFile):
	self.readFile = readFile
	sumdf = pd.read_csv(readFile,sep=None)
	try:
	    sumdf['Strokes']
	except KeyError:
	    sumdf = pd.read_csv(readFile,sep=None)
	self.sumdf = sumdf

	# prepare Work Data
	# remove "Just Go"
	#s2 = self.sumdf[self.sumdf['Workout Name']<>'Just Go']
	s2 = self.sumdf
	s3 = s2[~s2['Interval Type'].str.contains("Rest")]
	self.workdata = s3

    def allstats(self,separator="|"):



	stri2 = "Workout Details\n"
	stri2 += "#-{sep}SDist{sep}-Split-{sep}-SPace-{sep}SPM-{sep}AvgHR{sep}MaxHR{sep}DPS-\n".format(
	    sep = separator
	    )

	avghr = self.workdata['Avg HR'].mean()
	avgsr = self.workdata['Avg SR'].mean()
	maxhr = self.workdata['Max HR'].mean()
	maxsr = self.workdata['Max SR'].mean()
	totaldistance = self.workdata['Distance (m)'].sum()
	totalstrokes = self.workdata['Strokes'].sum()




	# min=int(avgpace/60)
	# sec=int(10*(avgpace-min*60.))/10.
	# pacestring = str(min)+":"+str(sec)


	nr_rows = self.workdata.shape[0]

	tothour = 0
	totmin = 0
	totsec = 0
	tottimehr = 0
	tottimespm = 0

	
	for i in range(nr_rows):
	    inttime = self.workdata['Time'].iloc[i]
	    thr = self.workdata['Avg HR'].iloc[i]
	    td = self.workdata['Distance (m)'].iloc[i]
	    tpace = self.workdata['Avg Pace (/500m)'].iloc[i]
	    tspm = self.workdata['Avg SR'].iloc[i]
	    tmaxhr = self.workdata['Max HR'].iloc[i]
	    tstrokes = self.workdata['Strokes'].iloc[i]

	    tdps = td/(1.0*tstrokes)
				 
	    try:
		t = datetime.datetime.strptime(inttime, "%H:%M:%S.%f")
	    except ValueError:
		try:
		    t = datetime.datetime.strptime(inttime, "%M:%S")
		except ValueError:
		    t = datetime.datetime.strptime(inttime, "%H:%M:%S")


	    tothour = tothour+t.hour
	    tottimehr += (t.hour*3600+t.minute*60+t.second)*thr
	    tottimespm += (t.hour*3600+t.minute*60+t.second)*tspm

	    totmin = totmin+t.minute
	    if (totmin >= 60):
		totmin = totmin-60
		tothour = tothour+1

	    totsec = totsec+t.second+0.1*int(t.microsecond/1.e5) # plus tenths
	    if (totsec >= 60):
		totsec = totsec - 60
		totmin = totmin+1


	    stri2 += "{nr:0>2}{sep}{td:0>5}{sep} {inttime:0>5} {sep}".format(
		nr = i+1,
		sep = separator,
		td = td,
		inttime = inttime
		)

	    stri2 += "{tpace:0>7}{sep}{tspm:0>4.1f}{sep}{thr:3.1f}".format(
		tpace=tpace,
		sep=separator,
		tspm=tspm,
		thr = thr
		)

	    stri2 += "{sep}{tmaxhr:3.1f}{sep}{tdps:0>4.1f}".format(
		sep = separator,
		tmaxhr = tmaxhr,
		tdps = tdps
		)


	    stri2 += "\n"

	
	tottime = "{totmin:0>2}:{totsec:0>2}".format(
	    totmin = totmin+60*tothour,
	    totsec = totsec)

	totaltime = tothour*3600+totmin*60+totsec

	avgspeed = totaldistance/totaltime
	avgpace = 500./avgspeed
	avghr = tottimehr/totaltime
	avgsr = tottimespm/totaltime
	
	min=int(avgpace/60)
	sec=int(10*(avgpace-min*60.))/10.
	pacestring = str(min)+":"+str(sec)

	avgdps = totaldistance/(1.0*totalstrokes)
	if isnan(avgdps):
	    avgdps = 0


	stri1 = summarystring(totaldistance,totaltime,avgpace,avgsr,
			      avghr,maxhr,avgdps,0,
			      readFile=self.readFile,
			      separator=separator)

	
	# print stri1+stri2

	copytocb(stri1+stri2)

	return stri1+stri2

    def shortstats(self):
	avghr = self.workdata['Avg HR'].mean()
	avgsr = self.workdata['Avg SR'].mean()
	maxhr = self.workdata['Max HR'].mean()
	maxsr = self.workdata['Max SR'].mean()
	totaldistance = self.workdata['Distance (m)'].sum()
	avgspeed = self.workdata['Avg Speed (m/s)'].mean()
	avgpace = 500/avgspeed

	min=int(avgpace/60)
	sec=int(10*(avgpace-min*60.))/10.
	pacestring = str(min)+":"+str(sec)


	nr_rows = self.workdata.shape[0]

	totmin = 0
	totsec = 0

	
	for i in range(nr_rows):
	    inttime = self.workdata['Time'].iloc[i]
	    try:
		t = time.strptime(inttime, "%H:%M:%S")
	    except ValueError:
		t = time.strptime(inttime, "%M:%S")

	    totmin = totmin+t.tm_min
	    totsec = totsec+t.tm_sec
	    if (totsec > 60):
		totsec = totsec - 60
		totmin = totmin+1

	stri =  "=========WORK DATA=================\n"
	stri = stri+"Total Time     : "+str(totmin)+":"+str(totsec)+"\n"
	stri = stri+ "Total Distance : "+str(totaldistance)+" m\n"
	stri = stri+"Average Pace   : "+pacestring+"\n"
	stri = stri+"Average HR     : "+str(int(avghr))+" Beats/min\n"
	stri = stri+"Average SPM    : "+str(int(10*avgsr)/10.)+" /min\n"
	stri = stri+"Max HR         : "+str(int(maxhr))+" Beats/min\n"
	stri = stri+"Max SPM        : "+str(int(10*maxsr)/10.)+" /min\n"
	stri = stri+"==================================="

	copytocb(stri)

	print stri
	



class rower:
    """ This class contains all the personal data about the rower

    * HR threshold values

    * C2 logbook username and password

    * weight category

    """
    
    def __init__(self,hrut2=142,hrut1=146,hrat=160,
		 hrtr=167,hran=180,hrmax=192,
		 c2username="",
		 c2password="",
		 weightcategory="hwt",
		 mc=72.5,
		 strokelength=1.35,ftp=226,
		 powerperc=[55,75,90,105,120]):
	self.ut2=hrut2
	self.ut1=hrut1
	self.at=hrat
	self.tr=hrtr
	self.an=hran
	self.max=hrmax
	self.c2username=c2username
	self.c2password=c2password
	self.ftp = ftp
	self.powerperc = powerperc
	if (weknowphysics==1):
	    self.rc = rowingphysics.crew(mc=mc,strokelength=strokelength)
	else:
	    self.rc = 0
	if (weightcategory <> "hwt") and (weightcategory <> "lwt"):
	    print "Weightcategory unrecognized. Set to hwt"
	    weightcategory = "hwt"
	    
	self.weightcategory=weightcategory

    def write(self,fileName):
	res = write_obj(self,fileName)


def roweredit(fileName="defaultrower.txt"):
    """ Easy editing or creation of a rower file.
    Mainly for using from the windows command line

    """

    try:
	r = pickle.load(open(fileName))
    except IOError:
	print "Roweredit: File does not exist. Reverting to defaultrower.txt"
	r = getrower()
    except ImportError:
	print "Roweredit: File is not valid. Reverting to defaultrower.txt"
	r = getrower()

    try:
	rc = r.rc
    except AttributeError:
	if (weknowphysics==1):
	    rc = rowingphysics.crew(mc=70.0)
	else:
	    rc = 0

    try:
	ftp = r.ftp
    except AttributeError:
	ftp = 225

    print "Functional Threshold Power"
    print "Your Functional Threshold Power is set to {ftp}".format(
	ftp = ftp
	)
    strin = raw_input('Enter new FTP (just ENTER to keep {ftp}:'.format(ftp=ftp))
    if (strin <> ""):
	try:
	    r.ftp = int(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"
	    

    print "Heart Rate Training Bands"
    # hrmax
    print "Your HR max is set to {hrmax} bpm".format(
	hrmax = r.max
	)
    strin = raw_input('Enter HR max (just ENTER to keep {hrmax}):'.format(hrmax=r.max))
    if (strin <> ""):
	try:
	    r.max = int(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"

    
    # hrut2, hrut1
    print "UT2 zone is between {hrut2} and {hrut1} bpm ({percut2:2.0f}-{percut1:2.0f}% of max HR)".format(
	hrut2 = r.ut2,
	hrut1 = r.ut1,
	percut2 = 100.*r.ut2/r.max,
	percut1 = 100.*r.ut1/r.max
	)
    strin = raw_input('Enter UT2 band lower value (ENTER to keep {hrut2}):'.format(hrut2=r.ut2))
    if (strin <> ""):
	try:
	    r.ut2 = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    strin = raw_input('Enter UT2 band upper value (ENTER to keep {hrut1}):'.format(hrut1=r.ut1))
    if (strin <> ""):
	try:
	    r.ut1 = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    
    print "UT1 zone is between {val1} and {val2} bpm ({perc1:2.0f}-{perc2:2.0f}% of max HR)".format(
	val1 = r.ut1,
	val2 = r.at,
	perc1 = 100.*r.ut1/r.max,
	perc2 = 100.*r.at/r.max
	)

    strin = raw_input('Enter UT1 band upper value (ENTER to keep {hrat}):'.format(hrat=r.at))
    if (strin <> ""):
	try:
	    r.at = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    
    print "AT zone is between {val1} and {val2} bpm ({perc1:2.0f}-{perc2:2.0f}% of max HR)".format(
	val1 = r.at,
	val2 = r.tr,
	perc1 = 100.*r.at/r.max,
	perc2 = 100.*r.tr/r.max
	)

    strin = raw_input('Enter AT band upper value (ENTER to keep {hrtr}):'.format(hrtr=r.tr))
    if (strin <> ""):
	try:
	    r.tr = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    
    
    print "TR zone is between {val1} and {val2} bpm ({perc1:2.0f}-{perc2:2.0f}% of max HR)".format(
	val1 = r.tr,
	val2 = r.an,
	perc1 = 100.*r.tr/r.max,
	perc2 = 100.*r.an/r.max
	)

    strin = raw_input('Enter TR band upper value (ENTER to keep {hran}):'.format(hran=r.an))
    if (strin <> ""):
	try:
	    r.an = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"


    print ""

    # weightcategory    
    print "Your weight category is set to {weightcategory}.".format(
	weightcategory = r.weightcategory
	)
    strin = raw_input('Enter lwt for Light Weight, hwt for Heavy Weight, or just ENTER: ')
    if (strin <> ""):
	if (strin == 'lwt'):
	    r.weightcategory = strin
	    print "Setting to "+strin
	elif (strin == 'hwt'):
	    r.weightcategory = strin
	    print "Setting to "+strin
	else:
	    print "Value not recognized"

    print ""


    mc = rc.mc
    # weight
    strin = raw_input("Enter weight in kg (or ENTER to keep {mc} kg):".format(
	mc = mc
	))
    if (strin <> ""):
	rc.mc = float(strin)

    # strokelength
    strin = raw_input("Enter strokelength in m (or ENTER to keep {l} m:".format(
	l = rc.strokelength
	))
    if (strin <>""):
	rc.strokelength = float(strin)

    r.rc = rc

    # c2username
    if (r.c2username <> ""):
	print "Your Concept2 username is set to {c2username}.".format(
	    c2username = r.c2username
	)
	strin = raw_input('Enter new username (or just ENTER to keep): ')
	if (strin <> ""):
	    r.c2username = strin


    # c2password
    if (r.c2username == ""):
	print "We don't know your Concept2 username"
	strin = raw_input('Enter new username (or ENTER to skip): ')
	r.c2username = strin

    if (r.c2username <> ""):
	if (r.c2password <> ""):
	    print "We have your Concept2 password."
	    changeyesno = raw_input('Do you want to change/erase your password (y/n)')
	    if changeyesno == "y":
		strin1 = getpass.getpass('Enter new password (or ENTER to erase):')
		if (strin1 <> ""):
		    strin2 = getpass.getpass('Repeat password:')
		    if (strin1 == strin2):
			r.c2password = strin1
		    else:
			print "Error. Not the same."
		if (strin1 == ""):
			print "Forgetting your password"
			r.c2password = ""
	elif (r.c2password == ""):
	    print "We don't have your Concept2 password yet."
	    strin1 = getpass.getpass('Concept2 password (or ENTER to skip):')
	    if (strin1 <> ""):
		strin2 = getpass.getpass('Repeat password:')
		if (strin1 == strin2):
		    r.c2password = strin1
		else:
		    print "Error. Not the same."
    
    


    r.write(fileName)
    
    print "Done"
    return 1

def boatedit(fileName="my1x.txt"):
    """ Easy editing or creation of a boat rigging data file.
    Mainly for using from the windows command line

    """

    try:
	rg = pickle.load(open(fileName))
    except IOError:
	print "Boatedit: File does not exist. Reverting to my1x.txt"
	rg = getrigging()
    except (ImportError,ValueError):
	print "Boatedit: File is not valid. Reverting to my1x.txt"
	rg = getrigging()

    print "Number of rowers"
    # Lin
    print "Your boat has {Nrowers} seats".format(
	Nrowers = rg.Nrowers
	)
    strin = raw_input('Enter number of seats (just ENTER to keep {Nrowers}):'.format(
	Nrowers = rg.Nrowers
	))
    if (strin <> ""):
	try:
	    rg.Nrowers = int(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"

    print "Rowing or sculling"
    # roworscull
    strin = raw_input('Row (r) or scull (s) - ENTER to keep {roworscull}:'.format(
	roworscull = rg.roworscull
	))
    if (strin == "s"):
	rg.roworscull = 'scull'
    elif (strin == "r"):
	rg.roworscull = 'row'
    

    print "Boat weight"
    # mb
    print "Your {Nrowers} boat weighs {mb} kg".format(
	Nrowers = rg.Nrowers,
	mb = rg.mb
	)
    strin = raw_input('Enter boat weight including cox (just ENTER to keep {mb}):'.format(
	mb = rg.mb
	))
    if (strin <> ""):
	try:
	    rg.mb = float(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"

    print "Rigging Data"
    # Lin
    print "Your inboard is set to {lin} m".format(
	lin = rg.lin
	)
    strin = raw_input('Enter inboard (just ENTER to keep {lin} m):'.format(
	lin = rg.lin
	))
    if (strin <> ""):
	try:
	    rg.lin = float(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"

    print "Your scull/oar length is set to {lscull} m".format(
	lscull = rg.lscull
	)
    print "For this number, you need to subtract half of the blade length from the classical oar/scull length measurement"
    strin = raw_input('Enter length (subtract half of blade length, just ENTER to keep {lscull}):'.format(
	lscull = rg.lscull
	))
    if (strin <> ""):
	try:
	    rg.lscull = float(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"


    if (rg.roworscull == 'row'):
	print "Your spread is set to {spread} m".format(
	    spread = rg.spread
	    )
	strin = raw_input('Enter new spread (or ENTER to keep {spread} m):'.format(
	    spread = rg.spread
	    ))
	if (strin <> ""):
	    try:
		rg.spread = float(spread)
	    except ValueError:
		print "Not a valid number. Keeping original value"
    else:
	print "Your span is set to {span} m".format(
	    span = rg.span
	    )
	strin = raw_input('Enter new span (or ENTER to keep {span} m):'.format(
	    span = rg.span
	    ))
	if (strin <> ""):
	    try:
		rg.span = float(span)
	    except ValueError:
		print "Not a valid number. Keeping original value"
	
    # Blade Area
    print "Your blade area is set to {bladearea} m2 (total blade area per rower, take two blades for scullers)".format(
	bladearea = rg.bladearea
	)
    strin = raw_input('Enter blade area (just ENTER to keep {bladearea} m2):'.format(
	bladearea = rg.bladearea
	))
    if (strin <> ""):
	try:
	    rg.bladearea = float(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"

    # Catch angle
    catchangledeg = -np.degrees(rg.catchangle)

    print "We define catch angle as follows."
    print " - 0 degrees is a catch with oar shaft perpendicular to the boat"
    print " - 90 degrees is a catch with oar shaft parallel to the boat"
    print " - Use positive values for normal catch angles"
    print "Your catch angle is {catchangledeg} degrees."
    strin = raw_input('Enter catch angle in degrees (or ENTER to keep {catchangledeg}):'.format(
	catchangledeg = catchangledeg
	))
    if (strin <> ""):
	try:
	    rg.catchangle = -np.radians(float(strin))
	except ValueError:
	    print "Not a valid number. Keeping original value"

    write_obj(rg,fileName)
    
    print "Done"
    return 1

def addpowerzones(df,ftp,powerperc):
    number_of_rows = df.shape[0]

    df['pw_ut2'] = np.zeros(number_of_rows)
    df['pw_ut1'] = np.zeros(number_of_rows)
    df['pw_at'] = np.zeros(number_of_rows)
    df['pw_tr'] = np.zeros(number_of_rows)
    df['pw_an'] = np.zeros(number_of_rows)
    df['pw_max'] = np.zeros(number_of_rows)

    percut2,percut1,percat,perctr,percan = np.array(powerperc)/100.

    ut2,ut1,at,tr,an = ftp*np.array(powerperc)/100.

    df['limpw_ut2'] = percut2*ftp
    df['limpw_ut1'] = percut1*ftp
    df['limpw_at'] = percat*ftp
    df['limpw_tr'] = perctr*ftp
    df['limpw_an'] = percan*ftp

    # create the columns containing the data for the colored bar chart
    # attempt to do this in a way that doesn't generate dubious copy warnings
    mask = (df[' Power (watts)']<=ut2)&(df[' Stroke500mPace (sec/500m)']<300)
    df.loc[mask,'pw_ut2'] = df.loc[mask,' Power (watts)']

    mask = (df[' Power (watts)']<=ut1)&(df[' Power (watts)']>ut2)&(df[' Stroke500mPace (sec/500m)']<300)
    df.loc[mask,'pw_ut1'] = df.loc[mask,' Power (watts)']

    mask = (df[' Power (watts)']<=at)&(df[' Power (watts)']>ut1)&(df[' Stroke500mPace (sec/500m)']<300)
    df.loc[mask,'pw_at'] = df.loc[mask,' Power (watts)']

    mask = (df[' Power (watts)']<=tr)&(df[' Power (watts)']>at)&(df[' Stroke500mPace (sec/500m)']<300)
    df.loc[mask,'pw_tr'] = df.loc[mask,' Power (watts)']

    mask = (df[' Power (watts)']<=an)&(df[' Power (watts)']>tr)&(df[' Stroke500mPace (sec/500m)']<300)
    df.loc[mask,'pw_an'] = df.loc[mask,' Power (watts)']

    mask = (df[' Power (watts)']>an)&(df[' Stroke500mPace (sec/500m)']<300)
    df.loc[mask,'pw_max'] = df.loc[mask,' Power (watts)']

    df = df.fillna(method='ffill')

    return df

def addzones(df,ut2,ut1,at,tr,an,mmax):
    	# define an additional data frame that will hold the multiple bar plot data and the hr 
	# limit data for the plot, it also holds a cumulative distance column

	number_of_rows = df.shape[0]

	df['hr_ut2'] = np.zeros(number_of_rows)
	df['hr_ut1'] = np.zeros(number_of_rows)
	df['hr_at'] = np.zeros(number_of_rows)
	df['hr_tr'] = np.zeros(number_of_rows)
	df['hr_an'] = np.zeros(number_of_rows)
	df['hr_max'] = np.zeros(number_of_rows)

	df['lim_ut2'] = ut2
	df['lim_ut1'] = ut1
	df['lim_at'] = at
	df['lim_tr'] = tr
	df['lim_an'] = an
	df['lim_max'] = mmax




	# create the columns containing the data for the colored bar chart
	# attempt to do this in a way that doesn't generate dubious copy warnings
	mask = (df[' HRCur (bpm)']<=ut2)&(df[' Stroke500mPace (sec/500m)']<300)
	df.loc[mask,'hr_ut2'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=ut1)&(df[' HRCur (bpm)']>ut2)&(df[' Stroke500mPace (sec/500m)']<300)
	df.loc[mask,'hr_ut1'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=at)&(df[' HRCur (bpm)']>ut1)&(df[' Stroke500mPace (sec/500m)']<300)
	df.loc[mask,'hr_at'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=tr)&(df[' HRCur (bpm)']>at)&(df[' Stroke500mPace (sec/500m)']<300)
	df.loc[mask,'hr_tr'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=an)&(df[' HRCur (bpm)']>tr)&(df[' Stroke500mPace (sec/500m)']<300)
	df.loc[mask,'hr_an'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']>an)&(df[' Stroke500mPace (sec/500m)']<300)
	df.loc[mask,'hr_max'] = df.loc[mask,' HRCur (bpm)']



	# fill cumulative distance column with cumulative distance
	# ignoring resets to lower distance values
	try:
	    cumdist = df['cum_dist']
	except KeyError:
	    df['cum_dist'] = np.zeros(number_of_rows)

	    df['cum_dist'] = make_cumvalues(df[' Horizontal (meters)'])[0]


	df = df.fillna(method='ffill')

	return df

class rowingdata:
    """ This is the main class. Read the data from the csv file and do all
    kinds
    of cool stuff with it.

    Usage: row = rowingdata.rowingdata("testdata.csv",rowtype = "Indoor Rower")
           row.plotmeters_all()
	   
    The default rower looks for a defaultrower.txt file. If it is not found,
    it reverts to some arbitrary rower.
    

    """
    
    def __init__(self,*args,**kwargs):
#                 readFile,
#		 rower=rower(),
#		 rowtype="Indoor Rower"):


        if 'csvfile' in kwargs:
            readFile = kwargs['csvfile']
        else:
            readFile = 0

        if args:
            readFile = args[0]
            warnings.warn("Depreciated. Use rowingdata(csvfile=csvfile)",UserWarning)

        rwr = kwargs.get('rower',rower())

        rowtype = kwargs.get('rowtype','Indoor Rower')

        sled_df = DataFrame()
        if 'df' in kwargs:
            sled_df = kwargs['df']
            #new_index = range(len(sled_df))
            #sled_df = sled_df.reindex(index=new_index)
            readFile = 0
        elif readFile != 0:
            try:
	        sled_df = pd.read_csv(readFile)
            except IOError:
                sled_df = pd.read_csv(readFile+'.gz')
            
        if readFile != 0:
	    try:
	        self.readfilename = readFile.name
	    except AttributeError:
	        self.readfilename = readFile
        else:
            self.readfilename = 'rowing dataframe'

	
	self.readFile = readFile
	self.rwr = rwr
	self.rowtype = rowtype


        # check for missing column names
        mandatorynames = [
            'TimeStamp (sec)',
	    ' Horizontal (meters)',
	    ' Cadence (stokes/min)',
	    ' HRCur (bpm)',
	    ' Stroke500mPace (sec/500m)',
	    ' Power (watts)',
	    ' DriveLength (meters)',
	    ' StrokeDistance (meters)',
	    ' DriveTime (ms)',
	    ' DragFactor',
	    ' StrokeRecoveryTime (ms)',
	    ' AverageDriveForce (lbs)',
	    ' PeakDriveForce (lbs)',
	    ' lapIdx',
	    ' ElapsedTime (sec)',
	]

        for name in mandatorynames:
            if name not in sled_df.columns:
                sled_df[name] = 0

        self.dragfactor = sled_df[' DragFactor'].mean()
	# get the date of the row
	starttime = sled_df['TimeStamp (sec)'].values[0]

	# using UTC time for now
	self.rowdatetime = datetime.datetime.utcfromtimestamp(starttime)
	    	
	# remove the start time from the time stamps
	sled_df['TimeStamp (sec)']=sled_df['TimeStamp (sec)']-sled_df['TimeStamp (sec)'].values[0]

	number_of_columns = sled_df.shape[1]
	number_of_rows = sled_df.shape[0]

	# these parameters are handy to have available in other routines
	self.number_of_rows = number_of_rows

	# add HR zone data to dataframe
	self.df = addzones(sled_df,self.rwr.ut2,
		      self.rwr.ut1,
		      self.rwr.at,
		      self.rwr.tr,
		      self.rwr.an,
		      self.rwr.max
		      )

	self.df = addpowerzones(self.df,self.rwr.ftp,self.rwr.powerperc)

    def getvalues(self,keystring):
	""" Just a tool to get a column of the row data as a numpy array

	You can also just access row.df[keystring] to get a pandas Series

	"""
	
	return self.df[keystring].values

    def write_csv(self,writeFile,gzip=False):
	data = self.df
	data = data.drop(['index',
			  'hr_ut2',
			  'hr_ut1',
			  'hr_at',
			  'hr_tr',
			  'hr_an',
			  'hr_max',
			  'lim_ut2',
			  'lim_ut1',
			  'lim_at',
			  'lim_tr',
			  'lim_an',
			  'lim_max',
			  'pw_ut2',
			  'pw_ut1',
			  'pw_at',
			  'pw_tr',
			  'pw_an',
			  'pw_max',
			  'limpw_ut2',
			  'limpw_ut1',
			  'limpw_at',
			  'limpw_tr',
			  'limpw_an',
			  'limpw_max',
			  ],1,errors='ignore')
	    

	# add time stamp to
	starttimeunix = time.mktime(self.rowdatetime.timetuple())
	data['TimeStamp (sec)'] = data['TimeStamp (sec)']+starttimeunix

        if gzip:
            return data.to_csv(writeFile+'.gz',index_label='index',
                               compression='gzip')
        else:
	    return data.to_csv(writeFile,index_label='index')

    def spm_fromtimestamps(self):
	df = self.df
	dt = (df[' DriveTime (ms)']+df[' StrokeRecoveryTime (ms)'])/1000.
	spm = 60./dt
	df[' Cadence (stokes/min)'] = spm
	self.df = df


    def erg_recalculatepower(self):
	df = self.df
	velo = df[' Speed (m/sec)']
	pwr = 2.8*velo**3
	df[' Power (watts)'] = pwr
	self.df = df

    def exporttotcx(self,fileName,notes="Exported by Rowingdata"):
	df = self.df

	writetcx.write_tcx(fileName,df,row_date=self.rowdatetime.isoformat(),notes=notes)


    def intervalstats(self,separator='|'):
	""" Used to create a nifty text summary, one row for each interval

	Also copies the string to the clipboard (handy!)

	Works for painsled (both iOS and desktop version) because they use
	the lapIdx column

	"""
	
	df = self.df

	workoutstateswork = [1,4,5,8,9,6,7]
	workoutstatesrest = [3]
	workoutstatetransition = [0,2,10,11,12,13]

	intervalnrs = pd.unique(df[' lapIdx'])

	stri = "Workout Details\n"
	stri += "#-{sep}SDist{sep}-Split-{sep}-SPace-{sep}-Pwr-{sep}SPM-{sep}AvgHR{sep}MaxHR{sep}DPS-\n".format(
	    sep = separator
	    )

	previousdist = 0.0
	previoustime = 0.0

	for idx in intervalnrs:
	    td = df[df[' lapIdx'] == idx]

	    # assuming no stroke type info
	    tdwork = td

		
	    avghr = tdwork[' HRCur (bpm)'].mean()
	    maxhr = tdwork[' HRCur (bpm)'].max()
	    avgspm = tdwork[' Cadence (stokes/min)'].mean()
            avgpower = tdwork[' Power (watts)'].mean()

	    intervaldistance = tdwork[' Horizontal (meters)'].max()
	    
	    previousdist = tdwork['cum_dist'].max()

	    intervalduration = tdwork['TimeStamp (sec)'].max()-previoustime
	    previoustime = tdwork['TimeStamp (sec)'].max()

	    intervalpace = 500.*intervalduration/intervaldistance
	    avgdps = intervaldistance/(intervalduration*avgspm/60.)
	    if isnan(avgdps) or isinf(avgdps):
		avgdps = 0


	    stri += interval_string(idx+1,intervaldistance,intervalduration,
				    intervalpace,avgspm,
				    avghr,maxhr,avgdps,avgpower,
				    separator=separator)
	    


	return stri

    def intervalstats_values(self):
	""" Used to create a nifty text summary, one row for each interval

	Also copies the string to the clipboard (handy!)

	Works for painsled (both iOS and desktop version) because they use
	the lapIdx column

	"""

	df = self.df

	workoutstateswork = [1,4,5,8,9,6,7]
	workoutstatesrest = [3]
	workoutstatetransition = [0,2,10,11,12,13]

	intervalnrs = pd.unique(df[' lapIdx'])

	itime = []
	idist = []
	itype = []

	previousdist = 0.0
	previoustime = 0.0

	try:
	    test = df[' WorkoutState']
	except KeyError:
	    df[' WorkoutState'] = 4


	for idx in intervalnrs:
	    td = df[df[' lapIdx'] == idx]

	    # get stroke info
	    tdwork = td[~td[' WorkoutState'].isin(workoutstatesrest)]
	    tdrest = td[td[' WorkoutState'].isin(workoutstatesrest)]

	    try:
		workoutstate = tdwork.ix[tdwork.index[-1],' WorkoutState']
	    except IndexError:
		workoutstate = 4
					

	    intervaldistance = tdwork['cum_dist'].max()-previousdist
	    if isnan(intervaldistance) or isinf(intervaldistance):
		intervaldistance = 0

	    
	    previousdist = td['cum_dist'].max()

	    intervalduration = tdwork['TimeStamp (sec)'].max()-previoustime
	    # previoustime = tdrest[' ElapsedTime (sec)'].max()
	    previoustime = td['TimeStamp (sec)'].max()

            intervalduration = nanstozero(intervalduration)
	    restdistance = nanstozero(tdrest['cum_dist'].max()-tdwork['cum_dist'].max())

	    restduration = nanstozero(tdrest['TimeStamp (sec)'].max()-tdwork['TimeStamp (sec)'].max())


	    
	    #    if intervaldistance != 0:
            itime += [int(10*intervalduration)/10.,
                      int(10*restduration)/10.]
            idist += [int(intervaldistance),
                      int(restdistance)]
            itype += [workoutstate,3]


	return itime,idist,itype

    def intervalstats_painsled(self,separator='|'):
	""" Used to create a nifty text summary, one row for each interval

	Also copies the string to the clipboard (handy!)

	Works for painsled (both iOS and desktop version) because they use
	the lapIdx column

	"""

	df = self.df

	workoutstateswork = [1,4,5,8,9,6,7]
	workoutstatesrest = [3]
	workoutstatetransition = [0,2,10,11,12,13]

	intervalnrs = pd.unique(df[' lapIdx'])

	stri = "Workout Details\n"
	stri += "#-{sep}SDist{sep}-Split-{sep}-SPace-{sep}-Pwr-{sep}SPM-{sep}AvgHR{sep}MaxHR{sep}DPS-\n".format(
	    sep = separator
	    )

	previousdist = 0.0
	previoustime = 0.0

	try:
	    test = df[' WorkoutState']
	except KeyError:
	    return self.intervalstats()


	for idx in intervalnrs:
	    td = df[df[' lapIdx'] == idx]

	    # get stroke info
	    tdwork = td[~td[' WorkoutState'].isin(workoutstatesrest)]
	    tdrest = td[td[' WorkoutState'].isin(workoutstatesrest)]

		
	    avghr = tdwork[' HRCur (bpm)'].mean()
	    maxhr = tdwork[' HRCur (bpm)'].max()
	    avgspm = tdwork[' Cadence (stokes/min)'].mean()
            avgpower = tdwork[' Power (watts)'].mean()
	    

	    intervaldistance = tdwork['cum_dist'].max()-previousdist
            if isnan(intervaldistance) or isinf(intervaldistance):
		intervaldistance = 0

	    
	    previousdist = td['cum_dist'].max()

	    intervalduration = tdwork['TimeStamp (sec)'].max()-previoustime
	    # previoustime = tdrest[' ElapsedTime (sec)'].max()
	    previoustime = td['TimeStamp (sec)'].max()
	    
	    if intervaldistance != 0:
		intervalpace = 500.*intervalduration/intervaldistance
	    else:
		intervalpace = 0
	    
	    avgdps = intervaldistance/(intervalduration*avgspm/60.)
	    if isnan(avgdps) or isinf(avgdps):
		avgdps = 0
	    if isnan(intervalpace) or isinf(intervalpace):
		intervalpace = 0
	    if isnan(avgspm) or isinf(avgspm):
		avgspm = 0
	    if isnan(avghr) or isinf(avghr):
		avghr = 0
	    if isnan(maxhr) or isinf(maxhr):
		maxhr = 0

	    if intervaldistance != 0:
		stri += interval_string(idx+1,intervaldistance,intervalduration,
				    intervalpace,avgspm,
				        avghr,maxhr,avgdps,avgpower,
				    separator=separator)
	    


	return stri

    def restoreintervaldata(self):
	
	try:
	    self.df[' Horizontal (meters)'] = self.df['orig_dist']
	    self.df['TimeStamp (sec)'] = self.df['orig_time']
	    self.df[' ElapsedTime (sec)'] = self.df['orig_reltime'] 
	    self.df[' LapIdx'] = self.df['orig_idx'] 
	    self.df[' WorkoutState'] = self.df['orig_state']
	except KeyError:
	    pass
    



    def updateintervaldata(self,
			   ivalues,
			   iunits,
			   itypes,
			   iresults = [],
			   ):
	""" Edits the intervaldata. For example a 2x2000m
	values = [2000,120,2000,120]
	units = ['meters','seconds','meters','seconds']
	types = ['work','rest','work','rest']
	"""
	
	df = self.df
	try:
	    origdist = df['orig_dist']
	    df[' Horizontal (meters)'] = df['orig_dist']
	    df['TimeStamp (sec)'] = df['orig_time']
	    df[' ElapsedTime (sec)'] = df['orig_reltime'] 
	    df[' LapIdx'] = df['orig_idx'] 
	    df[' WorkoutState'] = df['orig_state'] 
	except KeyError:
	    df['orig_dist'] = df[' Horizontal (meters)']
	    df['orig_time'] = df['TimeStamp (sec)']
	    df['orig_reltime'] = df[' ElapsedTime (sec)']
	    df['orig_idx'] = df[' lapIdx']
	    try:
		df['orig_state'] = df[' WorkoutState']
	    except KeyError:
		df['orig_state'] = 1

	intervalnr = 0
	startmeters = 0
	timezero = -df.ix[0,'TimeStamp (sec)']+df.ix[0,' ElapsedTime (sec)']
	startseconds = 0
	
	endseconds = startseconds
	endmeters = startmeters

	# erase existing lap data
	df[' lapIdx'] = 0
	df[' WorkoutState'] = 1
	df[' ElapsedTime (sec)'] = df['TimeStamp (sec)']+timezero
	df[' Horizontal (meters)'] = df['cum_dist']

	for i in range(len(ivalues)):
	    thevalue = ivalues[i]
	    theunit = iunits[i]
	    thetype = itypes[i]

	    if thetype == 'rest':
		intervalnr = intervalnr - 1

	    workouttype = 1
	    if theunit == 'meters' and thevalue>0:
		workouttype = 5

		if thetype == 'rest':
		    workouttype = 3
		    
		endmeters = startmeters+thevalue
		mask = (df['cum_dist']>startmeters)
		df.loc[mask,' lapIdx'] = intervalnr
		df.loc[mask,' WorkoutState'] = workouttype
		df.loc[mask,' ElapsedTime (sec)'] = df.loc[mask,'TimeStamp (sec)']-startseconds
		df.loc[mask,' Horizontal (meters)'] = df.loc[mask,'cum_dist']-startmeters

		mask = (df['cum_dist']<=endmeters)


		# correction for missing part of last stroke
		recordedmaxmeters = df.loc[mask,'cum_dist'].max()
		deltadist = endmeters-recordedmaxmeters

		try:
		    res = iresults[i]
		    mask2 = (df['cum_dist'] == recordedmaxmeters)
		    if res == 0:
			raise IndexError
		    deltatime = res-df.loc[mask2,' ElapsedTime (sec)']
		    mask2 = (df['cum_dist']==recordedmaxmeters)
		    df.loc[mask2,' ElapsedTime (sec)'] = res
		    df.loc[mask2,'TimeStamp (sec)'] += deltatime
		    df.loc[mask2,' Horizontal (meters)'] += deltadist
		except IndexError:
		    if deltadist>25:
			deltadist = 0
		    mask2 = (df['cum_dist']==recordedmaxmeters)
		    paceend = df.loc[mask2,' Stroke500mPace (sec/500m)'].values[0]
		    veloend = 500./paceend
		    deltatime = deltadist/veloend

		    df.loc[mask2,' ElapsedTime (sec)'] += deltatime
		    df.loc[mask2,'TimeStamp (sec)'] += deltatime
		    df.loc[mask2,' Horizontal (meters)'] += deltadist
		    df.loc[mask2,'cum_dist'] += deltadist		  
		
		endseconds = df.loc[mask,'TimeStamp (sec)'].max() #+ deltatime?

	    if theunit == 'seconds' and thevalue>0:
		workouttype = 4

		if thetype == 'rest':
		    workouttype = 3

		endseconds = startseconds+thevalue
		mask = (df['TimeStamp (sec)']>startseconds)
		df.loc[mask,' lapIdx'] = intervalnr
		df.loc[mask,' WorkoutState'] = workouttype
		df.loc[mask,' ElapsedTime (sec)'] = df.loc[mask,'TimeStamp (sec)']-startseconds
		df.loc[mask,' Horizontal (meters)'] = df.loc[mask,'cum_dist']-startmeters

		mask = (df['TimeStamp (sec)']<=endseconds)


		# correction for missing part of last stroke
		recordedmaxtime = df.loc[mask,'TimeStamp (sec)'].max()
		deltatime = endseconds-recordedmaxtime
		try:
		    res = iresults[i]
		    mask2 = (df['TimeStamp (sec)']==recordedmaxtime)
		    deltadist = res-df.loc[mask2,' Horizontal (meters)']
		    if res == 0:
			raise IndexError
		    mask2 = (df['TimeStamp (sec)']==recordedmaxtime)
		    df.loc[mask2,' ElapsedTime (sec)'] += deltatime
		    df.loc[mask2,' Horizontal (meters)'] = res
		    df.loc[mask2,'TimeStamp (sec)'] += deltatime
		    df.loc[mask2,'cum_dist'] += deltadist
		except IndexError:
		    if deltatime>6 and thetype != 'rest':
			deltatime = 0
		    mask2 = (df['TimeStamp (sec)']==recordedmaxtime)
		    paceend = df.loc[mask2,' Stroke500mPace (sec/500m)'].values[0]
		    veloend = 500./paceend
		    deltadist = veloend*deltatime
		    if deltatime>5 and thetype == 'rest':
			deltadist = 0

		    df.loc[mask2,' ElapsedTime (sec)'] += deltatime
		    df.loc[mask2,' Horizontal (meters)'] += deltadist
		    df.loc[mask2,'cum_dist'] += deltadist
		    df.loc[mask2,'TimeStamp (sec)'] += deltatime

		mask = (df['TimeStamp (sec)']<=endseconds)

		endmeters = df.loc[mask,'cum_dist'].max()  #+ deltadist?
	    
	    intervalnr += 1

	    startseconds = endseconds
	    startmeters = endmeters
        
	self.df = df



    def updateinterval_string(self,s):
	res = trainingparser.parse(s)
	values = trainingparser.getlist(res)
	units = trainingparser.getlist(res,sel='unit')
	typ = trainingparser.getlist(res,sel='type')

	self.updateintervaldata(values,units,typ)


    def add_bearing(self,window_size=20):
	""" Adds bearing. Only works if long and lat values are known

	"""
	nr_of_rows = self.df.shape[0]
	df = self.df

	bearing = np.zeros(nr_of_rows)
	
	for i in range(nr_of_rows-1):
	    try:
		long1 = df.ix[i,' longitude']
		lat1 = df.ix[i,' latitude']
		long2 = df.ix[i+1,' longitude']
		lat2 = df.ix[i+1,' latitude']
	    except KeyError:
		long1 = 0
		lat1 = 0
		long2 = 0
		lat2 = 0
	    res = geo_distance(lat1,long1,lat2,long2)
	    bearing[i] = res[1]

	bearing2 = ewmovingaverage(bearing,window_size)


	df['bearing'] = 0
	df['bearing'] = bearing2

	self.df = df

    def add_stream(self,vstream,units='m'):
	# foot/second
	if (units == 'f'):
	    vstream = 0.3048*vstream

	# knots
	if (units == 'k'):
	    stream = stream/1.994

	# pace difference (approximate)
	if (units == 'p'):
	    stream = stream*8/500.

	df = self.df

	df['vstream'] = vstream

	self.df = df

    def add_wind(self,vwind,winddirection,units='m'):

	# beaufort
	if (units == 'b'):
	    vwind = 0.837*vwind**(3./2.)
	# knots
	if (units == 'k'):
	    vwind = vwind*1.994

	# km/h
	if (units == 'kmh'):
	    vwind = vwind/3.6

	# mph
	if (units == 'mph'):
	    vwind = 0.44704*vwind

	df = self.df

	df['vwind'] = vwind
	df['winddirection'] = winddirection

	self.df = df

    def update_stream(self,stream1,stream2,dist1,dist2,units='m'):
	try:
	    vs = self.df.ix[:,'vstream']
	except KeyError:
	    self.add_stream(0)

	df = self.df

	# foot/second
	if (units == 'f'):
	    stream1 = 0.3048*stream1
	    stream2 = 0.3048*stream2

	# knots
	if (units == 'k'):
	    stream1 = stream1/1.994
	    stream2 = stream2/1.994

	# pace difference (approximate)
	if (units == 'p'):
	    stream1 = stream1*8/500.
	    stream2 = stream2*8/500.

	aantal = len(df)

	for i in range(aantal):
	    if (df.ix[i,'cum_dist']>dist1 and df.ix[i,'cum_dist']<dist2):
		# doe iets
		x = df.ix[i,'cum_dist']
		r = (x-dist1)/(dist2-dist1)
		stream = stream1+(stream2-stream1)*r
		try:
		    df.ix[i,'vstream']  = stream
		except:
		    pass


	self.df = df
	

    def update_wind(self,vwind1,vwind2,winddirection1,
		    winddirection2,dist1,dist2,units='m'):

	try:
	    vw = self.df.ix[:,'vwind']
	except KeyError:
	    self.add_wind(0,0)
	
	df = self.df
	
	# beaufort
	if (units == 'b'):
	    vwind1 = 0.837*vwind1**(3./2.)
	    vwind2 = 0.837*vwind2**(3./2.)

	# knots
	if (units == 'k'):
	    vwind1 = vwind1/1.994
	    vwind2 = vwind2/1.994

	# km/h
	if (units == 'kmh'):
	    vwind1 = vwind1/3.6
	    vwind2 = vwind2/3.6

	# mph
	if (units == 'mph'):
	    vwind1 = 0.44704*vwind1
	    vwind2 = 0.44704*vwind2

	aantal = len(df)

	for i in range(aantal):
	    if (df.ix[i,'cum_dist']>dist1 and df.ix[i,'cum_dist']<dist2):
		# doe iets
		x = df.ix[i,'cum_dist']
		r = (x-dist1)/(dist2-dist1)
		try:
		    vwind = vwind1+(vwind2-vwind1)*r
		    df.ix[i,'vwind']  = vwind
		except:
		    pass
		try:
		    dirwind = winddirection1+(winddirection2-winddirection1)*r
		    df.ix[i,'winddirection'] = dirwind
		except:
		    pass



	self.df = df


	    
    def otw_setpower(self,skiprows=0,rg=getrigging(),mc=70.0,
                     powermeasured=False):
	""" Adds power from rowing physics calculations to OTW result

	For now, works only in singles

	"""

	print "EXPERIMENTAL"
	
	nr_of_rows = self.number_of_rows
	rows_mod = skiprows+1
	df = self.df
	df['nowindpace'] = 300
	df['equivergpower']= 0
	df['power (model)']= 0
        df['averageforce (model)'] = 0
        df['drivelength (model)'] = 0
        
	# creating a rower and rigging for now
        # in future this must come from rowingdata.rower and rowingdata.rigging
	r = self.rwr.rc
	r.mc = mc

	# this is slow ... need alternative (read from table)
	for i in tqdm(range(nr_of_rows)):
	    p = df.ix[i,' Stroke500mPace (sec/500m)']
	    spm = df.ix[i,' Cadence (stokes/min)']
	    r.tempo = spm
	    try:
		drivetime = 60.*1000./float(spm)  # in milliseconds
	    except ZeroDivisionError:
		drivetime = 4000.
	    if (p != 0) & (spm != 0) & (p<210):
		velo = 500./p
		try:
		    vwind = df.ix[i,'vwind']
		    winddirection = df.ix[i,'winddirection']
		    bearing = df.ix[i,'bearing']
		except KeyError:
		    vwind = 0.0
		    winddirection = 0.0
		    bearing = 0.0
		try:
		    vstream = df.ix[i,'vstream']
		except KeyError:
		    vstream = 0

		if (i % rows_mod == 0):
		    try:
			res = phys_getpower(velo,r,rg,bearing,vwind,winddirection,
					    vstream)
		    except:
			res = [np.nan,np.nan,np.nan,np.nan,np.nan]
		else:
		    res = [np.nan,np.nan,np.nan,np.nan,np.nan]
		df.ix[i,'power (model)'] = res[0]
		df.ix[i,'averageforce (model)'] = res[2]/lbstoN
		df.ix[i,' DriveTime (ms)'] = res[1]*drivetime
		df.ix[i,' StrokeRecoveryTime (ms)'] = (1-res[1])*drivetime
		df.ix[i,'drivelength (model)'] = r.strokelength
		df.ix[i,'nowindpace'] = res[3]
		df.ix[i,'equivergpower'] = res[4]

		if res[4]>res[0]:
		    print "Power ",res[0]
		    print "Equiv erg Power ",res[4]
		    print "Boat speed (m/s) ",velo
		    print "Stroke rate ",r.tempo
		    print "ratio ",res[1]
		# update_progress(i,nr_of_rows)

	    else:
		velo = 0.0

	self.df = df.interpolate()
        if not powermeasured:
            self.df[' Power (watts)'] = self.df['power (model)']
            self.df[' AverageDriveForce (lbs)'] = self.df['averageforce (model)']
            self.df[' DriveLength (meters)'] = self.df['drivelength (model)']



    def otw_setpower_silent(self,skiprows=0,rg=getrigging(),mc=70.0,
                            powermeasured=False):
	""" Adds power from rowing physics calculations to OTW result

	For now, works only in singles

	"""

	nr_of_rows = self.number_of_rows
	rows_mod = skiprows+1
	df = self.df
	df['nowindpace'] = 300
	df['equivergpower']= 0
        df['power (model)'] = 0 
        df['averageforce (model)'] = 0
        df['drivelength (model)'] = 0
        
	# creating a rower and rigging for now
	# in future this must come from rowingdata.rower and rowingdata.rigging
	r = self.rwr.rc
	r.mc = mc

	# this is slow ... need alternative (read from table)
	for i in range(nr_of_rows):
	    p = df.ix[i,' Stroke500mPace (sec/500m)']
	    spm = df.ix[i,' Cadence (stokes/min)']
	    r.tempo = spm

	    try:
		drivetime = 60.*1000./float(spm)  # in milliseconds
	    except ZeroDivisionError:
		drivetime = 4000.
	    if (p != 0) & (spm != 0) & (p<210):
		velo = 500./p
		try:
		    vwind = df.ix[i,'vwind']
		    winddirection = df.ix[i,'winddirection']
		    bearing = df.ix[i,'bearing']
		except KeyError:
		    vwind = 0.0
		    winddirection = 0.0
		    bearing = 0.0
		try:
		    vstream = df.ix[i,'vstream']
		except KeyError:
		    vstream = 0

		if (i % rows_mod == 0):
		    try:
			res = phys_getpower(velo,r,rg,bearing,vwind,winddirection,
					    vstream)
		    except:
			res = [np.nan,np.nan,np.nan,np.nan,np.nan]
		else:
		    res = [np.nan,np.nan,np.nan,np.nan,np.nan]
		df.ix[i,'power (model)'] = res[0]
		df.ix[i,'averageforce (model)'] = res[2]/lbstoN
		df.ix[i,' DriveTime (ms)'] = res[1]*drivetime
		df.ix[i,' StrokeRecoveryTime (ms)'] = (1-res[1])*drivetime
		df.ix[i,'drivelength (model)'] = r.strokelength
		df.ix[i,'nowindpace'] = res[3]
		df.ix[i,'equivergpower'] = res[4]
		# update_progress(i,nr_of_rows)

	    else:
		velo = 0.0

	self.df = df.interpolate()
        if not powermeasured:
            self.df[' Power (watts)'] = self.df['power (model)']
            self.df[' AverageDriveForce (lbs)'] = self.df['averageforce (model)']
            self.df[' DriveLength (meters)'] = self.df['drivelength (model)']

	    
    def otw_setpower_verbose(self,skiprows=0,rg=getrigging(),mc=70.0,
                             powermeasured=False):
	""" Adds power from rowing physics calculations to OTW result

	For now, works only in singles

	"""

	print "EXPERIMENTAL"
	
	nr_of_rows = self.number_of_rows
	rows_mod = skiprows+1
	df = self.df
	df['nowindpace'] = 300
	df['equivergpower']= 0
	df['power (model)']= 0
        df['averageforce (model)'] = 0
        df['drivelength (model)'] = 0

	# creating a rower and rigging for now
	# in future this must come from rowingdata.rower and rowingdata.rigging
	r = self.rwr.rc
	r.mc = mc

	# this is slow ... need alternative (read from table)
	for i in range(nr_of_rows):
	    p = df.ix[i,' Stroke500mPace (sec/500m)']
	    spm = df.ix[i,' Cadence (stokes/min)']
	    r.tempo = spm
	    try:
		drivetime = 60.*1000./float(spm)  # in milliseconds
	    except ZeroDivisionError:
		drivetime = 4000.
	    if (p != 0) & (spm != 0) & (p<210):
		velo = 500./p
		try:
		    vwind = df.ix[i,'vwind']
		    winddirection = df.ix[i,'winddirection']
		    bearing = df.ix[i,'bearing']
		except KeyError:
		    vwind = 0.0
		    winddirection = 0.0
		    bearing = 0.0
		try:
		    vstream = df.ix[i,'vstream']
		except KeyError:
		    vstream = 0

		if (i % rows_mod == 0):
		    try:
			res = phys_getpower(velo,r,rg,bearing,vwind,winddirection,
					    vstream)
			print i, r.tempo, p,res[0],res[3],res[4]
		    except KeyError:
			res = [np.nan,np.nan,np.nan,np.nan,np.nan]
		else:
		    res = [np.nan,np.nan,np.nan,np.nan,np.nan]
		df.ix[i,'power (model)'] = res[0]
		df.ix[i,'averageforce (model)'] = res[2]/lbstoN
		df.ix[i,' DriveTime (ms)'] = res[1]*drivetime
		df.ix[i,' StrokeRecoveryTime (ms)'] = (1-res[1])*drivetime
		df.ix[i,'drivelength (model)'] = r.strokelength
		df.ix[i,'nowindpace'] = res[3]
		df.ix[i,'equivergpower'] = res[4]
		# update_progress(i,nr_of_rows)
	    else:
		velo = 0.0

	self.df = df.interpolate()
        if not powermeasured:
            self.df[' Power (watts)'] = self.df['power (model)']
            self.df[' AverageDriveForce (lbs)'] = self.df['averageforce (model)']
            self.df[' DriveLength (meters)'] = self.df['drivelength (model)']

    def otw_testphysics(self,rg=getrigging(),mc=70.0,p=120.,spm=30.):
	""" Check if erg pace is in right order

	For now, works only in singles

	"""

	print "EXPERIMENTAL"
	
	# creating a rower and rigging for now
	# in future this must come from rowingdata.rower and rowingdata.rigging
	r = self.rwr.rc
	r.mc = mc
	r.tempo = spm
	drivetime = 60.*1000./float(spm)  # in milliseconds
	if (p != 0) & (spm != 0) & (p<210):
	    velo = 500./p
	    vwind = 0.0
	    winddirection = 0.0
	    bearing = 0.0
	    vstream = 0.0
	    res = phys_getpower(velo,r,rg,bearing,vwind,winddirection,
				vstream)

	    print 'Pace ',p
	    print 'Power (watts)', res[0]
	    print 'Average Drive Force (N)',res[2]
	    print ' DriveTime (ms)',res[1]*drivetime
	    print ' StrokeRecoveryTime (ms)', (1-res[1])*drivetime
	    print ' DriveLength (meters)', r.strokelength
	    print 'nowindpace', res[3]
	    print 'equivergpower',  res[4]

	else:
	    velo = 0.0



    def summary(self,separator='|'):
	""" Creates a nifty text string that contains the key data for the row
	and copies it to the clipboard

	"""
	
	df = self.df

	# total dist, total time, avg pace, avg hr, max hr, avg dps

	times,distances,types = self.intervalstats_values()

	times = np.array(times)
	distance = np.array(distances)
	types = np.array(types)

	totaldist = np.array(distances).sum()
        totaltime = np.array(times).sum()

	avgpace = 500*totaltime/totaldist
	avghr = df[' HRCur (bpm)'].mean()
	maxhr = df[' HRCur (bpm)'].max()
	avgspm = df[' Cadence (stokes/min)'].mean()
	avgdps = totaldist/(totaltime*avgspm/60.)
        avgpower = df[' Power (watts)'].mean()


	stri = summarystring(totaldist,totaltime,avgpace,avgspm,
			     avghr,maxhr,avgdps,avgpower,
			     readFile=self.readFile,
			     separator=separator)


	try:
	    test = df[' WorkoutState']
	except KeyError:
	    return stri

	
	workoutstateswork = [1,4,5,8,9,6,7]
	workoutstatesrest = [3]
	workoutstatetransition = [0,2,10,11,12,13]
	
	intervalnrs = pd.unique(df[' lapIdx'])

	previousdist = 0.0
	previoustime = 0.0

	workttot = 0.0
	workdtot = 0.0

	workspmavg = 0
	workhravg = 0
	workdpsavg = 0
	workhrmax = 0
	workpoweravg = 0

	restttot = 0.0
	restdtot = 0.0

	restspmavg = 0
	resthravg = 0
	restdpsavg = 0
	restpoweravg = 0
	resthrmax = 0

	for idx in intervalnrs:
	    td = df[df[' lapIdx'] == idx]

	    # get stroke info
	    tdwork = td[~td[' WorkoutState'].isin(workoutstatesrest)]
	    tdrest = td[td[' WorkoutState'].isin(workoutstatesrest)]

	    avghr = nanstozero(tdwork[' HRCur (bpm)'].mean())
	    maxhr = nanstozero(tdwork[' HRCur (bpm)'].max())
	    avgspm = nanstozero(tdwork[' Cadence (stokes/min)'].mean())
            avgpower = nanstozero(tdwork[' Power (watts)'].mean())

	    avghrrest = nanstozero(tdrest[' HRCur (bpm)'].mean())
	    maxhrrest = nanstozero(tdrest[' HRCur (bpm)'].max())
	    avgspmrest = nanstozero(tdrest[' Cadence (stokes/min)'].mean())
            avgrestpower = nanstozero(tdrest[' Power (watts)'].mean())

	    intervaldistance = tdwork['cum_dist'].max()-previousdist
	    if isnan(intervaldistance) or isinf(intervaldistance):
		intervaldistance = 0

	    

	    intervalduration = nanstozero(tdwork['TimeStamp (sec)'].max()-previoustime)

	    previoustime = td['TimeStamp (sec)'].max()


	    restdistance = tdrest['cum_dist'].max()-tdwork['cum_dist'].max()
            if np.isnan(tdwork['cum_dist'].max()):
                        restdistance = tdrest['cum_dist'].max()-previousdist
                        
            restdistance = nanstozero(restdistance)
	    previousdist = td['cum_dist'].max()

	    restduration = nanstozero(tdrest[' ElapsedTime (sec)'].max())

	    if intervaldistance != 0:
		intervalpace = 500.*intervalduration/intervaldistance
	    else:
		intervalpace = 0
		
	    if restdistance > 0:
		restpace = 500.*restduration/restdistance
	    else:
		restpace = 0
		
	    if (intervalduration*avgspm>0):
		avgdps = intervaldistance/(intervalduration*avgspm/60.)
	    else:
		avgdps = 0

	    if (restduration*avgspmrest>0):
		restdpsavg = restdistance/(restduration*avgspmrest/60.)
	    else:
		restdpsavg = 0
	    if isnan(avgdps) or isinf(avgdps):
		avgdps = 0

	    if isnan(restdpsavg) or isinf(restdpsavg):
		restdpsavg = 0

	    workspmavg = workspmavg*workttot+intervalduration*avgspm
	    workhravg = workhravg*workttot+intervalduration*avghr
	    workdpsavg = workdpsavg*workttot+intervalduration*avgdps
            workpoweravg = workpoweravg*workttot+intervalduration*avgpower
	    if workttot+intervalduration>0:
		workspmavg = workspmavg/(workttot+intervalduration)
		workhravg = workhravg/(workttot+intervalduration)
		workdpsavg = workdpsavg/(workttot+intervalduration)
                workpoweravg = workpoweravg/(workttot+intervalduration)


	    workhrmax = max(workhrmax,maxhr)

	    restspmavg = restspmavg*restttot+restduration*avgspmrest
	    resthravg = resthravg*restttot+restduration*avghrrest
	    restdpsavg = restdpsavg*restttot+restduration*restdpsavg
	    restpoweravg = restpoweravg*restttot+restduration*avgrestpower

	    if restttot+restduration>0:
		restspmavg = restspmavg/(restttot+restduration)
		resthravg = resthravg/(restttot+restduration)
		restdpsavg = restdpsavg/(restttot+restduration)
		restpoweravg = restpoweravg/(restttot+restduration)

	    resthrmax = max(resthrmax,maxhr)


	    workttot += intervalduration
	    workdtot += intervaldistance

	    restttot += restduration
	    restdtot += restdistance

	if restdtot != 0:
	    avgrestpace = 500.*restttot/restdtot
	else:
	    avgrestpace = 0

	if workdtot != 0:
	    avgworkpace = 500.*workttot/workdtot
	else:
	    avgworkpace = 500.*workttot/workdtot

	stri += workstring(workdtot,workttot,avgworkpace,workspmavg,
			   workhravg,workhrmax,workdpsavg,workpoweravg,
			   separator=separator,
			   symbol='W')

	stri += workstring(restdtot,restttot,avgrestpace,restspmavg,
			   resthravg,resthrmax,restdpsavg,restpoweravg,
			   separator=separator,
			   symbol='R')

	return stri

    def allstats(self,separator='|'):
	""" Creates a nice text summary, both overall summary and a one line
	per interval summary

	Works for painsled (both iOS and desktop)

	Also copies the string to the clipboard (handy!)

	"""

	stri = self.summary(separator=separator)+self.intervalstats_painsled(separator=separator)


	return stri

    def plotcp(self):
	cumdist = self.df['cum_dist']
	elapsedtime = self.df[' ElapsedTime (sec)']

	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(1,1,1)
	ax.set_xlabel('Duration')
	ax.set_ylabel('Power')

	delta = []
	cpvalue = []

	for i in range(len(cumdist)-1):
	    resdist = cumdist.ix[i+1:]-cumdist.ix[i]
	    restime = elapsedtime.ix[i+1:]-elapsedtime[i]
	    velo = resdist/restime
	    power = 2.8*velo**3
	    power.name = 'Power'
	    restime.name = 'restime'
	    df = pd.concat([restime,power],axis=1).reset_index()
	    maxrow = df.loc[df['Power'].idxmax()]
	    delta.append(maxrow['restime'])
	    cpvalue.append(maxrow['Power'])

	ax.scatter(delta,cpvalue)
	plt.show()


    def getcp(self):
	cumdist = self.df['cum_dist']
	elapsedtime = self.df[' ElapsedTime (sec)']

	delta = []
	dist = []
	cpvalue = []

	for i in range(len(cumdist)-1):
	    resdist = cumdist.ix[i+1:]-cumdist.ix[i]
	    restime = elapsedtime.ix[i+1:]-elapsedtime[i]
	    velo = resdist/restime
	    power = 2.8*velo**3
	    power.name = 'Power'
	    restime.name = 'restime'
	    resdist.name = 'resdist'
	    df = pd.concat([restime,resdist,power],axis=1).reset_index()
	    maxrow = df.loc[df['Power'].idxmax()]
	    delta.append(maxrow['restime'])
	    cpvalue.append(maxrow['Power'])
	    dist.append(maxrow['resdist'])

	delta = pd.Series(delta,name='Delta')
	cpvalue = pd.Series(cpvalue,name='CP')
	dist = pd.Series(dist,name='Distance')

	return pd.concat([delta,cpvalue,dist],axis=1).reset_index()
	

    def plototwergpower(self):
	df = self.df
	pe = df['equivergpower']
	pw = df[' Power (watts)']

	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(1,1,1)
	ax.scatter(pe,pw)
	ax.set_xlabel('Erg Power (W)')
	ax.set_ylabel('OTW Power (W)')

	plt.show()

    def plotmeters_erg(self):
	""" Creates two images containing interesting plots

	x-axis is distance

	Used with painsled (erg) data
	

	"""
	
	df = self.df

	# distance increments for bar chart
	dist_increments = -df.ix[:,'cum_dist'].diff()
	dist_increments[0] = dist_increments[1]
	

	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- HR / Pace / Rate / Power"
	fig_title += " Drag %d" % self.dragfactor

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],
		width = dist_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],
		width = dist_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],
		width = dist_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],
		width = dist_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],
		width = dist_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],
		width = dist_increments,
		color='r',ec='r')

	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')

	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,100,1.1*self.rwr.max])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax2.axis([0,end_dist,yrange[1],yrange[0]])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,95,-5))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,' Power (watts)'])
	yrange = y_axis_range(df.ix[:,' Power (watts)'],
			      ultimate=[50,550])
	ax4.axis([0,end_dist,yrange[0],yrange[1]])
	ax4.set_xticks(range(1000,end_dist,1000))
	ax4.set_xlabel('Dist (km)')
	ax4.set_ylabel('Watts')
#	ax4.set_yticks(range(150,450,50))
	grid(True)
	majorKmFormatter = FuncFormatter(format_dist_tick)
	majorLocator = (1000)
	ax4.xaxis.set_major_formatter(majorKmFormatter)

	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- Stroke Metrics"
	
	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax5.axis([0,end_dist,yrange[1],yrange[0]])
	ax5.set_xticks(range(1000,end_dist,1000))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(175,95,-10))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.yaxis.set_major_formatter(majorFormatter)
	
	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveLength (meters)'])
	yrange = y_axis_range(df.ix[:,' DriveLength (meters)'],
			      ultimate = [1,15])
	ax6.axis([0,end_dist,yrange[0],yrange[1]])
	ax6.set_xticks(range(1000,end_dist,1000))
	ax6.set_ylabel('Drive Len(m)')
#	ax6.set_yticks(np.arange(1.,2.,0.05))
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	s = np.concatenate((df.ix[:,' DriveTime (ms)'].values/1000.,
			   df.ix[:,' StrokeRecoveryTime (ms)'].values/1000.))
	yrange = y_axis_range(s,ultimate=[0.5,4])
	
	ax7.axis([0,end_dist,yrange[0],yrange[1]])
	ax7.set_xticks(range(1000,end_dist,1000))
	ax7.set_ylabel('Drv / Rcv Time (s)')
#	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'cum_dist'],
		 df.ix[:,' AverageDriveForce (lbs)']*lbstoN)
	ax8.plot(df.ix[:,'cum_dist'],
		 df.ix[:,' PeakDriveForce (lbs)']*lbstoN)
	s = np.concatenate((df.ix[:,' AverageDriveForce (lbs)'].values*lbstoN,
			   df.ix[:,' PeakDriveForce (lbs)'].values*lbstoN))
	yrange = y_axis_range(s,ultimate=[0,1000])

	ax8.axis([0,end_dist,yrange[0],yrange[1]])
	ax8.set_xticks(range(1000,end_dist,1000))
	ax8.set_xlabel('Dist (m)')
	ax8.set_ylabel('Force (N)')
#	ax8.set_yticks(range(25,300,25))
	grid(True)
	majorLocator = (1000)
	ax8.xaxis.set_major_formatter(majorKmFormatter)
	

	plt.subplots_adjust(hspace=0)

	plt.show()
	print "done"


    def plotmeters_powerzones_erg(self):
	""" Creates two images containing interesting plots

	x-axis is distance

	Used with painsled (erg) data
	

	"""
	
	df = self.df

	# distance increments for bar chart
	dist_increments = -df.ix[:,'cum_dist'].diff()
	dist_increments[0] = dist_increments[1]
	

	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- HR / Pace / Rate / Power"
	fig_title += " Drag %d" % self.dragfactor

	# First panel, Power
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_ut2'],
		width = dist_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_ut1'],
		width = dist_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_at'],
		width = dist_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_tr'],
		width = dist_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_an'],
		width = dist_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_max'],
		width = dist_increments,
		color='r',ec='r')


	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_an'],color='k')


	ut2,ut1,at,tr,an = self.rwr.ftp*np.array(self.rwr.powerperc)/100.

	ax1.text(5,ut2+1.5,"UT2",size=8)
	ax1.text(5,ut1+1.5,"UT1",size=8)
	ax1.text(5,at+1.5,"AT",size=8)
	ax1.text(5,tr+1.5,"TR",size=8)
	ax1.text(5,an+1.5,"AN",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,50,1.5*an])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('Power (Watts)')
#	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax2.axis([0,end_dist,yrange[1],yrange[0]])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,95,-5))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)

	# Fourth Panel, HR
	ax4 = fig1.add_subplot(4,1,4)
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],
		width = dist_increments,
		color='gray', ec='gray')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],
		width = dist_increments,
		color='y',ec='y')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],
		width = dist_increments,
		color='g',ec='g')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],
		width = dist_increments,
		color='blue',ec='blue')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],
		width = dist_increments,
		color='violet',ec='violet')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],
		width = dist_increments,
		color='r',ec='r')

	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')

	ax4.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax4.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax4.text(5,self.rwr.at+1.5,"AT",size=8)
	ax4.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax4.text(5,self.rwr.an+1.5,"AN",size=8)
	ax4.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax4.axis([0,end_dist,100,1.1*self.rwr.max])
	ax4.set_xticks(range(1000,end_dist,1000))
	ax4.set_ylabel('BPM')
	ax4.set_yticks(range(110,200,10))

	grid(True)
	majorKmFormatter = FuncFormatter(format_dist_tick)
	majorLocator = (1000)
	ax4.xaxis.set_major_formatter(majorKmFormatter)

	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- Stroke Metrics"
	
	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax5.axis([0,end_dist,yrange[1],yrange[0]])
	ax5.set_xticks(range(1000,end_dist,1000))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(175,95,-10))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.yaxis.set_major_formatter(majorFormatter)
	
	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveLength (meters)'])
	yrange = y_axis_range(df.ix[:,' DriveLength (meters)'],
			      ultimate = [1,15])
	ax6.axis([0,end_dist,yrange[0],yrange[1]])
	ax6.set_xticks(range(1000,end_dist,1000))
	ax6.set_ylabel('Drive Len(m)')
#	ax6.set_yticks(np.arange(1.,2.,0.05))
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	s = np.concatenate((df.ix[:,' DriveTime (ms)'].values/1000.,
			   df.ix[:,' StrokeRecoveryTime (ms)'].values/1000.))
	yrange = y_axis_range(s,ultimate=[0.5,4])
	
	ax7.axis([0,end_dist,yrange[0],yrange[1]])
	ax7.set_xticks(range(1000,end_dist,1000))
	ax7.set_ylabel('Drv / Rcv Time (s)')
#	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'cum_dist'],
		 df.ix[:,' AverageDriveForce (lbs)']*lbstoN)
	ax8.plot(df.ix[:,'cum_dist'],
		 df.ix[:,' PeakDriveForce (lbs)']*lbstoN)
	s = np.concatenate((df.ix[:,' AverageDriveForce (lbs)'].values*lbstoN,
			   df.ix[:,' PeakDriveForce (lbs)'].values*lbstoN))
	yrange = y_axis_range(s,ultimate=[0,1000])

	ax8.axis([0,end_dist,yrange[0],yrange[1]])
	ax8.set_xticks(range(1000,end_dist,1000))
	ax8.set_xlabel('Dist (m)')
	ax8.set_ylabel('Force (N)')
#	ax8.set_yticks(range(25,300,25))
	grid(True)
	majorLocator = (1000)
	ax8.xaxis.set_major_formatter(majorKmFormatter)
	

	plt.subplots_adjust(hspace=0)

	plt.show()
    
    def plottime_erg(self):
	""" Creates two images containing interesting plots

	x-axis is time

	Used with painsled (erg) data
	

	"""

	df = self.df

	# time increments for bar chart
	time_increments = df.ix[:,' ElapsedTime (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))


	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- HR / Pace / Rate "
	fig_title += " Drag %d" % self.dragfactor


	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],
		width=time_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],
		width=time_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],
		width=time_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],
		width=time_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],
		width=time_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],
		width=time_increments,
		color='r',ec='r')

	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)


	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax2.axis([0,end_time,yrange[1],yrange[0]])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
#	rate_ewma = pd.ewma
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Power (watts)'])
	yrange = y_axis_range(df.ix[:,' Power (watts)'],
			      ultimate=[50,555])
	ax4.axis([0,end_time,yrange[0],yrange[1]])
	ax4.set_xticks(range(0,end_time,300))
	ax4.set_xlabel('Time (h:m)')
	ax4.set_ylabel('Watts')
#	ax4.set_yticks(range(150,450,50))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax4.xaxis.set_major_formatter(majorTimeFormatter)

	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- Stroke Metrics"

	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax5.axis([0,end_time,yrange[1],yrange[0]])
	ax5.set_xticks(range(0,end_time,300))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(145,90,-5))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.xaxis.set_major_formatter(timeTickFormatter)
	ax5.yaxis.set_major_formatter(majorFormatter)

	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveLength (meters)'])
	yrange = y_axis_range(df.ix[:,' DriveLength (meters)'],
			      ultimate = [1.0,15])
	ax6.axis([0,end_time,yrange[0],yrange[1]])
	ax6.set_xticks(range(0,end_time,300))
	ax6.set_xlabel('Time (sec)')
	ax6.set_ylabel('Drive Len(m)')
#	ax6.set_yticks(np.arange(1.35,1.6,0.05))
	ax6.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	s = np.concatenate((df.ix[:,' DriveTime (ms)'].values/1000.,
			   df.ix[:,' StrokeRecoveryTime (ms)'].values/1000.))
	yrange = y_axis_range(s,ultimate=[0.5,4])
	
	
	ax7.axis([0,end_time,yrange[0],yrange[1]])
	ax7.set_xticks(range(0,end_time,300))
	ax7.set_xlabel('Time (sec)')
	ax7.set_ylabel('Drv / Rcv Time (s)')
#	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	ax7.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' AverageDriveForce (lbs)']*lbstoN)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' PeakDriveForce (lbs)']*lbstoN)
	s = np.concatenate((df.ix[:,' AverageDriveForce (lbs)'].values*lbstoN,
			   df.ix[:,' PeakDriveForce (lbs)'].values*lbstoN))
	yrange = y_axis_range(s,ultimate=[0,1000])
	
	ax8.axis([0,end_time,yrange[0],yrange[1]])
	ax8.set_xticks(range(0,end_time,300))
	ax8.set_xlabel('Time (h:m)')
	ax8.set_ylabel('Force (N)')
#	ax8.set_yticks(range(25,300,25))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax8.xaxis.set_major_formatter(majorTimeFormatter)


	plt.subplots_adjust(hspace=0)

	plt.show()

	self.piechart()
	

    def get_metersplot_otw(self,title):
	df = self.df

	# distance increments for bar chart
	dist_increments = -df.ix[:,'cum_dist'].diff()
	dist_increments[0] = dist_increments[1]
#	dist_increments = abs(dist_increments)+dist_increments

	#	fig1 = plt.figure(figsize=(12,10))
	fig1 = figure.Figure(figsize=(12,10))
	fig_title = title

	# First panel, hr
	ax1 = fig1.add_subplot(3,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],
		width = dist_increments,align='edge',
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],
		width = dist_increments,align='edge',
		color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],
		width = dist_increments,align='edge',
		color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],
		width = dist_increments,align='edge',
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],
		width = dist_increments,align='edge',
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],
		width=dist_increments,align='edge',
		color='r',ec='r')

	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')

	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,100,1.1*self.rwr.max])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(3,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate=[85,190])
	
	ax2.axis([0,end_dist,yrange[1],yrange[0]])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(175,95,-10))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(3,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_xlabel('Distance (m)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)


	plt.subplots_adjust(hspace=0)

	return fig1

    def get_metersplot_erg2(self,title):
	df = self.df
	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])
	fig2 = plt.figure(figsize=(12,10))
	fig_title = title
	fig_title += " Drag %d" % self.dragfactor
	
	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax5.axis([0,end_dist,yrange[1],yrange[0]])
	ax5.set_xticks(range(1000,end_dist,1000))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(175,95,-10))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.yaxis.set_major_formatter(majorFormatter)
	
	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveLength (meters)'])
	yrange = y_axis_range(df.ix[:,' DriveLength (meters)'],
			      ultimate = [1,15])
	ax6.axis([0,end_dist,yrange[0],yrange[1]])
	ax6.set_xticks(range(1000,end_dist,1000))
	ax6.set_ylabel('Drive Len(m)')
#	ax6.set_yticks(np.arange(1.,2.,0.05))
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	s = np.concatenate((df.ix[:,' DriveTime (ms)'].values/1000.,
			   df.ix[:,' StrokeRecoveryTime (ms)'].values/1000.))
	yrange = y_axis_range(s,ultimate=[0.5,4])
	
	ax7.axis([0,end_dist,yrange[0],yrange[1]])
	ax7.set_xticks(range(1000,end_dist,1000))
	ax7.set_ylabel('Drv / Rcv Time (s)')
#	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'cum_dist'],
		 df.ix[:,' AverageDriveForce (lbs)']*lbstoN)
	ax8.plot(df.ix[:,'cum_dist'],
		 df.ix[:,' PeakDriveForce (lbs)']*lbstoN)
	s = np.concatenate((df.ix[:,' AverageDriveForce (lbs)'].values*lbstoN,
			   df.ix[:,' PeakDriveForce (lbs)'].values*lbstoN))
	yrange = y_axis_range(s,ultimate=[0,1000])

	ax8.axis([0,end_dist,yrange[0],yrange[1]])
	ax8.set_xticks(range(1000,end_dist,1000))
	ax8.set_xlabel('Dist (m)')
	ax8.set_ylabel('Force (N)')
#	ax8.set_yticks(range(25,300,25))
	grid(True)
	majorKmFormatter = FuncFormatter(format_dist_tick)

	majorLocator = (1000)
	ax8.xaxis.set_major_formatter(majorKmFormatter)
	

	plt.subplots_adjust(hspace=0)

	return fig2

    def get_timeplot_erg2(self,title):
	df = self.df
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	fig2 = plt.figure(figsize=(12,10))
	fig_title = title
	fig_title += " Drag %d" % self.dragfactor
	
	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax5.axis([0,end_time,yrange[1],yrange[0]])
	ax5.set_xticks(range(0,end_time,300))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(145,90,-5))
	grid(True)
	timeTickFormatter = NullFormatter()

	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.xaxis.set_major_formatter(timeTickFormatter)
	ax5.yaxis.set_major_formatter(majorFormatter)

	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveLength (meters)'])
	yrange = y_axis_range(df.ix[:,' DriveLength (meters)'],
			      ultimate = [1.0,15])
	ax6.axis([0,end_time,yrange[0],yrange[1]])
	ax6.set_xticks(range(0,end_time,300))
	ax6.set_xlabel('Time (sec)')
	ax6.set_ylabel('Drive Len(m)')
#	ax6.set_yticks(np.arange(1.35,1.6,0.05))
	ax6.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	s = np.concatenate((df.ix[:,' DriveTime (ms)'].values/1000.,
			   df.ix[:,' StrokeRecoveryTime (ms)'].values/1000.))
	yrange = y_axis_range(s,ultimate=[0.5,4])
	
	
	ax7.axis([0,end_time,yrange[0],yrange[1]])
	ax7.set_xticks(range(0,end_time,300))
	ax7.set_xlabel('Time (sec)')
	ax7.set_ylabel('Drv / Rcv Time (s)')
#	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	ax7.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' AverageDriveForce (lbs)']*lbstoN)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' PeakDriveForce (lbs)']*lbstoN)
	s = np.concatenate((df.ix[:,' AverageDriveForce (lbs)'].values*lbstoN,
			   df.ix[:,' PeakDriveForce (lbs)'].values*lbstoN))
	yrange = y_axis_range(s,ultimate=[0,1000])
	
	ax8.axis([0,end_time,yrange[0],yrange[1]])
	ax8.set_xticks(range(0,end_time,300))
	ax8.set_xlabel('Time (h:m)')
	ax8.set_ylabel('Force (N)')
#	ax8.set_yticks(range(25,300,25))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax8.xaxis.set_major_formatter(majorTimeFormatter)
	

	plt.subplots_adjust(hspace=0)

	return fig2

    def get_timeplot_otw(self,title):
	df = self.df

	# time increments for bar chart
	time_increments = df.ix[:,' ElapsedTime (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	


	fig1 = plt.figure(figsize=(12,10))
	
	fig_title = title

	# First panel, hr
	ax1 = fig1.add_subplot(3,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],
		width=time_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],
		width=time_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],
		width=time_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],
		width=time_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],
		width=time_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],
		width=time_increments,
		color='r',ec='r')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,190,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(3,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,190])
	ax2.axis([0,end_time,yrange[1],yrange[0]])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(175,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(3,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
#	rate_ewma = pd.ewma(df,span=20)
#	ax3.plot(rate_ewma.ix[:,'TimeStamp (sec)'],
#		 rate_ewma.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)


	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax3.set_xlabel('Time (h:m)')
	ax3.xaxis.set_major_formatter(majorTimeFormatter)
	plt.subplots_adjust(hspace=0)

	return fig1

    def get_pacehrplot(self,title):
	df = self.df

	t = df.ix[:,' ElapsedTime (sec)']
	p = df.ix[:,' Stroke500mPace (sec/500m)']
	hr = df.ix[:,' HRCur (bpm)']
	end_time = int(df.ix[df.shape[0]-1,' ElapsedTime (sec)'])

	fig, ax1 = plt.subplots(figsize=(5,4))

	ax1.plot(t,p,'b-')
	ax1.set_xlabel('Time (h:m)')
	ax1.set_ylabel('(sec/500)')

	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,190])
	plt.axis([0,end_time,yrange[1],yrange[0]])

	ax1.set_xticks(range(1000,end_time,1000))
	ax1.set_yticks(range(185,90,-10))
	ax1.set_title(title)
	plt.grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	timeTickFormatter = NullFormatter()
	
	ax1.yaxis.set_major_formatter(majorFormatter)

	for tl in ax1.get_yticklabels():
	    tl.set_color('b')

	ax2 = ax1.twinx()
	ax2.plot(t,hr,'r-')
	ax2.set_ylabel('Heart Rate',color='r')
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax2.xaxis.set_major_formatter(majorTimeFormatter)
	ax2.patch.set_alpha(0.0)
	for tl in ax2.get_yticklabels():
	    tl.set_color('r')
    
	plt.subplots_adjust(hspace=0)

	return fig

    def bokehpaceplot(self):
	df = self.df

	# time increments for bar chart
	time_increments = df.ix[:,'TimeStamp (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	
	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])


	t = df.ix[:,' ElapsedTime (sec)']
	p = df.ix[:,' Stroke500mPace (sec/500m)']
	hr = df.ix[:,' HRCur (bpm)']

	return 1

    def get_paceplot(self,title):
	df = self.df

	# time increments for bar chart
	time_increments = df.ix[:,'TimeStamp (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	
	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])


	t = df.ix[:,' ElapsedTime (sec)']
	p = df.ix[:,' Stroke500mPace (sec/500m)']
	hr = df.ix[:,' HRCur (bpm)']

	fig, ax1 = plt.subplots()
	ax1.plot(t,p,'b-')
	ax1.set_xlabel('Time')
	ax1.set_ylabel('Pace (sec/500)')

	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,190])
	plt.axis([0,end_time,yrange[1],yrange[0]])

	ax1.set_xticks(range(1000,end_time,1000))
	ax1.set_yticks(range(185,90,-10))
	ax1.set_title(title)
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	timeTickFormatter = NullFormatter()
	
	ax1.yaxis.set_major_formatter(majorFormatter)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax1.xaxis.set_major_formatter(majorTimeFormatter)

	for tl in ax1.get_yticklabels():
	    tl.set_color('b')

	ax2 = ax1.twinx()
	ax2.plot(t,hr,'r-')
	ax2.set_ylabel('Heart Rate',color='r')

	for tl in ax2.get_yticklabels():
	    tl.set_color('r')

	return fig

    def get_metersplot_erg(self,title):

	df = self.df

	# distance increments for bar chart
	dist_increments = df.ix[:,'cum_dist'].diff()
	dist_increments[0] = dist_increments[1]
	dist_increments = 0.5*(dist_increments+abs(dist_increments))

	fig1 = plt.figure(figsize=(12,10))

	fig_title = title
	fig_title += " Drag %d" % self.dragfactor

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],
		width = dist_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],
		width = dist_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],
		width = dist_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],
		width = dist_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],
		width = dist_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],
		width = dist_increments,
		color='r',ec='r')

	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')

	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,100,1.1*self.rwr.max])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax2.axis([0,end_dist,yrange[1],yrange[0]])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,95,-5))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_ut2'],
		width = dist_increments,
		color='gray', ec='gray')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_ut1'],
		width = dist_increments,
		color='y',ec='y')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_at'],
		width = dist_increments,
		color='g',ec='g')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_tr'],
		width = dist_increments,
		color='blue',ec='blue')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_an'],
		width = dist_increments,
		color='violet',ec='violet')
	ax4.bar(df.ix[:,'cum_dist'],df.ix[:,'pw_max'],
		width = dist_increments,
		color='r',ec='r')


	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_ut2'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_ut1'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_at'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_tr'],color='k')
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,'limpw_an'],color='k')


	ut2,ut1,at,tr,an = self.rwr.ftp*np.array(self.rwr.powerperc)/100.

	ax4.text(5,ut2+1.5,"UT2",size=8)
	ax4.text(5,ut1+1.5,"UT1",size=8)
	ax4.text(5,at+1.5,"AT",size=8)
	ax4.text(5,tr+1.5,"TR",size=8)
	ax4.text(5,an+1.5,"AN",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	yrange = y_axis_range(df.ix[:,' Power (watts)'],
			      ultimate=[50,555])
	ax4.axis([0,end_dist,yrange[0],yrange[1]])
	ax4.set_xticks(range(1000,end_dist,1000))
	ax4.set_xlabel('Dist (m)')
	ax4.set_ylabel('Power (Watts)')
#	ax4.set_yticks(range(110,200,10))


	grid(True)

	plt.subplots_adjust(hspace=0)

	return(fig1)


    def get_timeplot_erg(self,title):


	df = self.df

	# time increments for bar chart
	time_increments = df.ix[:,' ElapsedTime (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	


	fig1 = plt.figure(figsize=(12,10))
	
	fig_title = title
	fig_title += " Drag %d" % self.dragfactor

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],
		width=time_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],
		width=time_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],
		width=time_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],
		width=time_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],
		width=time_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],
		width=time_increments,
		color='r',ec='r')

	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,160])
	ax2.axis([0,end_time,yrange[1],yrange[0]])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
#	rate_ewma = pd.ewma
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'pw_ut2'],
		width = time_increments,
		color='gray', ec='gray')
	ax4.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'pw_ut1'],
		width = time_increments,
		color='y',ec='y')
	ax4.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'pw_at'],
		width = time_increments,
		color='g',ec='g')
	ax4.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'pw_tr'],
		width = time_increments,
		color='blue',ec='blue')
	ax4.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'pw_an'],
		width = time_increments,
		color='violet',ec='violet')
	ax4.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'pw_max'],
		width = time_increments,
		color='r',ec='r')


	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'limpw_ut2'],color='k')
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'limpw_ut1'],color='k')
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'limpw_at'],color='k')
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'limpw_tr'],color='k')
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'limpw_an'],color='k')


	ut2,ut1,at,tr,an = self.rwr.ftp*np.array(self.rwr.powerperc)/100.

	ax4.text(5,ut2+1.5,"UT2",size=8)
	ax4.text(5,ut1+1.5,"UT1",size=8)
	ax4.text(5,at+1.5,"AT",size=8)
	ax4.text(5,tr+1.5,"TR",size=8)
	ax4.text(5,an+1.5,"AN",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	yrange = y_axis_range(df.ix[:,' Power (watts)'],
			      ultimate=[50,555])
	ax4.axis([0,end_time,yrange[0],yrange[1]])
	ax4.set_xticks(range(0,end_time,300))
	ax4.set_xlabel('Time (h:m)')
	ax4.set_ylabel('Watts')
#	ax4.set_yticks(range(150,450,50))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax4.xaxis.set_major_formatter(majorTimeFormatter)

	plt.subplots_adjust(hspace=0)
	

	return(fig1)

    def get_time_otwpower(self,title):
	df = self.df
	# calculate erg power

	try:
	    nowindpace = df.ix[:,'nowindpace']
	except KeyError:
	    nowindpace = df[' Stroke500mPace (sec/500m)']
	    df['nowindpace'] = nowindpace
	try:
	    equivergpower = df.ix[:,'equivergpower']
	except KeyError:
	    equivergpower = 0*df[' Stroke500mPace (sec/500m)']+50.
	    df['equivergpower'] = equivergpower
	
	ergvelo = (equivergpower/2.8)**(1./3.)
    
	ergpace = 500./ergvelo
	ergpace[ergpace == np.inf] = 240.


	# time increments for bar chart
	time_increments = df.ix[:,' ElapsedTime (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	


	fig1 = plt.figure(figsize=(12,10))

	fig_title = title

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],
		width=time_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],
		width=time_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],
		width=time_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],
		width=time_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],
		width=time_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],
		width=time_increments,
		color='r',ec='r')

	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,'nowindpace'])

	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 ergpace)

	ax2.legend(['Pace','Wind corrected pace','Erg Pace'],
		   prop={'size':10},loc=0)
	
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	s = np.concatenate((df.ix[:,' Stroke500mPace (sec/500m)'].values,
			    df.ix[:,'nowindpace'].values,
			    ergpace))
	
	yrange = y_axis_range(s,ultimate=[90,210])

	ax2.axis([0,end_time,yrange[1],yrange[0]])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
#	rate_ewma = pd.ewma
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Power (watts)'])
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'equivergpower'])
	ax4.legend(['Power','Erg display power'],prop={'size':10})
	yrange = y_axis_range(df.ix[:,' Power (watts)'],
			      ultimate=[50,555])
	ax4.axis([0,end_time,yrange[0],yrange[1]])
	ax4.set_xticks(range(0,end_time,300))
	ax4.set_xlabel('Time (h:m)')
	ax4.set_ylabel('Watts')
#	ax4.set_yticks(range(150,450,50))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax4.xaxis.set_major_formatter(majorTimeFormatter)

	plt.subplots_adjust(hspace=0)

	return fig1
	
    def plottime_otwpower(self):
	""" Creates two images containing interesting plots

	x-axis is time

	Used with painsled (erg) data
	

	"""

	df = self.df

	# calculate erg power
	pp = df['equivergpower']
	ergvelo = (pp/2.8)**(1./3.)
	ergpace = 500./ergvelo
	

	# time increments for bar chart
	time_increments = df.ix[:,' ElapsedTime (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	


	fig1 = plt.figure(figsize=(12,10))

	fig_title = "Input File:  "+self.readfilename+" --- HR / Pace / Rate "

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],
		width=time_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],
		width=time_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],
		width=time_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],
		width=time_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],
		width=time_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],
		width=time_increments,
		color='r',ec='r')

	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,'nowindpace'])

	ax2.plot(df.ix[:,'TimeStamp (sec)'],
		 ergpace)

	ax2.legend(['Pace','Wind corrected pace','Erg Pace'],
		   prop={'size':10},loc=0)
	
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	s = np.concatenate((df.ix[:,' Stroke500mPace (sec/500m)'].values,
			   df.ix[:,'nowindpace'].values))
	yrange = y_axis_range(s,ultimate=[90,210])

	ax2.axis([0,end_time,yrange[1],yrange[0]])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(145,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
#	rate_ewma = pd.ewma
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Power (watts)'])
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'equivergpower'])
	ax4.legend(['Power','Erg display power'],prop={'size':10})
	yrange = y_axis_range(df.ix[:,' Power (watts)'],
			      ultimate=[50,555])
	ax4.axis([0,end_time,yrange[0],yrange[1]])
	ax4.set_xticks(range(0,end_time,300))
	ax4.set_xlabel('Time (h:m)')
	ax4.set_ylabel('Watts')
#	ax4.set_yticks(range(150,450,50))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax4.xaxis.set_major_formatter(majorTimeFormatter)

	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- Stroke Metrics"

	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' Stroke500mPace (sec/500m)'])

	ax5.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,'nowindpace'])

	ax5.plot(df.ix[:,'TimeStamp (sec)'],
		 ergpace)

	ax5.legend(['Pace','Wind corrected pace','erg pace'],
		   prop={'size':10},loc=0)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])

	s = np.concatenate((df.ix[:,' Stroke500mPace (sec/500m)'].values,
			   df.ix[:,'nowindpace'].values))
	yrange = y_axis_range(s,ultimate=[90,210])

	ax5.axis([0,end_time,yrange[1],yrange[0]])
	ax5.set_xticks(range(0,end_time,300))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(145,90,-5))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.xaxis.set_major_formatter(timeTickFormatter)
	ax5.yaxis.set_major_formatter(majorFormatter)

	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveLength (meters)'])
	yrange = y_axis_range(df.ix[:,' DriveLength (meters)'],
			      ultimate = [1.0,15])
	ax6.axis([0,end_time,yrange[0],yrange[1]])
	ax6.set_xticks(range(0,end_time,300))
	ax6.set_xlabel('Time (sec)')
	ax6.set_ylabel('Drive Len(m)')
#	ax6.set_yticks(np.arange(1.35,1.6,0.05))
	ax6.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	s = np.concatenate((df.ix[:,' DriveTime (ms)'].values/1000.,
			   df.ix[:,' StrokeRecoveryTime (ms)'].values/1000.))
	yrange = y_axis_range(s,ultimate=[0.5,4])
	
	
	ax7.axis([0,end_time,yrange[0],yrange[1]])
	ax7.set_xticks(range(0,end_time,300))
	ax7.set_xlabel('Time (sec)')
	ax7.set_ylabel('Drv / Rcv Time (s)')
#	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	ax7.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' AverageDriveForce (lbs)']*lbstoN)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' PeakDriveForce (lbs)']*lbstoN)
	s = np.concatenate((df.ix[:,' AverageDriveForce (lbs)'].values*lbstoN,
			   df.ix[:,' PeakDriveForce (lbs)'].values*lbstoN))
	yrange = y_axis_range(s,ultimate=[0,1000])
	
	ax8.axis([0,end_time,yrange[0],yrange[1]])
	ax8.set_xticks(range(0,end_time,300))
	ax8.set_xlabel('Time (h:m)')
	ax8.set_ylabel('Force (N)')
#	ax8.set_yticks(range(25,300,25))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax8.xaxis.set_major_formatter(majorTimeFormatter)


	plt.subplots_adjust(hspace=0)

	plt.show()

	self.piechart()
	
	print "done"

    def plottime_hr(self):
	""" Creates a HR vs time plot

	"""
	
	df = self.df
	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- HR "

	# First panel, hr
	ax1 = fig1.add_subplot(1,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],color='r',ec='r')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,190,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)
	plt.show()

    def plotmeters_otw(self):
	""" Creates two images containing interesting plots

	x-axis is distance

	Used with OTW data (no Power plot)
	

	"""

	df = self.df

	# distance increments for bar chart
	dist_increments = -df.ix[:,'cum_dist'].diff()
	dist_increments[0] = dist_increments[1]
#	dist_increments = abs(dist_increments)+dist_increments

	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- HR / Pace / Rate / Power"

	# First panel, hr
	ax1 = fig1.add_subplot(3,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],
		width = dist_increments,align='edge',
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],
		width = dist_increments,align='edge',
		color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],
		width = dist_increments,align='edge',
		color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],
		width = dist_increments,align='edge',
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],
		width = dist_increments,align='edge',
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],
		width=dist_increments,align='edge',
		color='r',ec='r')

	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')

	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,100,1.1*self.rwr.max])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(3,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate=[85,190])
	
	ax2.axis([0,end_dist,yrange[1],yrange[0]])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(175,95,-10))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(3,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_xlabel('Distance (m)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)


	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- Stroke Metrics"
	
	# Top plot is pace
	ax5 = fig2.add_subplot(2,1,1)
	ax5.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,190])
	ax5.axis([0,end_dist,yrange[1],yrange[0]])
	ax5.set_xticks(range(1000,end_dist,1000))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(175,95,-10))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.yaxis.set_major_formatter(majorFormatter)
	
	# next we plot the stroke distance
	ax6 = fig2.add_subplot(2,1,2)
	ax6.plot(df.ix[:,'cum_dist'],df.ix[:,' StrokeDistance (meters)'])
	yrange = y_axis_range(df.ix[:,' StrokeDistance (meters)'],
			      ultimate = [5,15])
	ax6.axis([0,end_dist,yrange[0],yrange[1]])
	ax6.set_xlabel('Distance (m)')
	ax6.set_xticks(range(1000,end_dist,1000))
	ax6.set_ylabel('Stroke Distance (m)')
#	ax6.set_yticks(np.arange(5.5,11.5,0.5))
	grid(True)
	

	plt.subplots_adjust(hspace=0)

	plt.show()
	print "done"
    

    def plottime_otw(self):
	""" Creates two images containing interesting plots

	x-axis is time

	Used with OTW data (no Power plot)
	

	"""
	
	df = self.df

	# time increments for bar chart
	time_increments = df.ix[:,' ElapsedTime (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))


	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- HR / Pace / Rate "

	# First panel, hr
	ax1 = fig1.add_subplot(3,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],
		width=time_increments,
		color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],
		width=time_increments,
		color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],
		width=time_increments,
		color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],
		width=time_increments,
		color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],
		width=time_increments,
		color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],
		width=time_increments,
		color='r',ec='r')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rwr.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rwr.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rwr.at+1.5,"AT",size=8)
	ax1.text(5,self.rwr.tr+1.5,"TR",size=8)
	ax1.text(5,self.rwr.an+1.5,"AN",size=8)
	ax1.text(5,self.rwr.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax1.axis([0,end_time,100,1.1*self.rwr.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,190,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(3,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,190])
	ax2.axis([0,end_time,yrange[1],yrange[0]])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
#	ax2.set_yticks(range(175,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(3,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
#	rate_ewma = pd.ewma(df,span=20)
#	ax3.plot(rate_ewma.ix[:,'TimeStamp (sec)'],
#		 rate_ewma.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)


	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax3.set_xlabel('Time (h:m)')
	ax3.xaxis.set_major_formatter(majorTimeFormatter)
	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readfilename+" --- Stroke Metrics"

	# Top plot is pace
	ax5 = fig2.add_subplot(2,1,1)
	ax5.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	yrange = y_axis_range(df.ix[:,' Stroke500mPace (sec/500m)'],
			      ultimate = [85,190])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax5.axis([0,end_time,yrange[1],yrange[0]])
	ax5.set_xticks(range(0,end_time,300))
	ax5.set_ylabel('(sec/500)')
#	ax5.set_yticks(range(175,90,-5))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.xaxis.set_major_formatter(timeTickFormatter)
	ax5.yaxis.set_major_formatter(majorFormatter)

	# next we plot the drive length
	ax6 = fig2.add_subplot(2,1,2)
	ax6.plot(df.ix[:,'TimeStamp (sec)'],
		 df.ix[:,' StrokeDistance (meters)'])
	yrange = y_axis_range(df.ix[:,' StrokeDistance (meters)'],
			      ultimate = [5,15])

	ax6.axis([0,end_time,yrange[0],yrange[1]])
	ax6.set_xticks(range(0,end_time,300))
	ax6.set_xlabel('Time (sec)')
	ax6.set_ylabel('Stroke Distance (m)')
#	ax6.set_yticks(np.arange(5.5,11.5,0.5))
	ax6.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)


	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax6.set_xlabel('Time (h:m)')
	ax6.xaxis.set_major_formatter(majorTimeFormatter)
	plt.subplots_adjust(hspace=0)

	plt.show()

	self.piechart()
	
	print "done"

    def piechart(self):
	""" Figure 3 - Heart Rate Time in band.
	This is not as simple as just totalling up the
	hits for each band of HR.  Since each data point represents
	a different increment of time.  This loop scans through the
	HR data and adds that incremental time in each band

	"""

	df = self.df
#	df.sort_values(by=' ElapsedTime (sec)',ascending = 1)
	df.sort_values(by='TimeStamp (sec)',ascending = 1)
	number_of_rows = self.number_of_rows

	time_increments = df.ix[:,'TimeStamp (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	
	time_in_zone = np.zeros(6)
	for i in range(number_of_rows):
	    if df.ix[i,' HRCur (bpm)'] <= self.rwr.ut2:
		time_in_zone[0] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.ut1:
		time_in_zone[1] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.at:
		time_in_zone[2] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.tr:
		time_in_zone[3] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.an:
		time_in_zone[4] += time_increments[i]
	    else:
		time_in_zone[5] += time_increments[i]
		
	# print(time_in_zone)
	wedge_labels = ['<ut2','ut2','ut1','at','tr','an']
	totaltime = time_in_zone.sum()

        perc = 100.*time_in_zone/totaltime
        cutoff = 1.0
        if len(perc[perc<cutoff])>1:
            cutoff = 2.0
            if len(perc[perc<cutoff])>1:
                cutoff = 3.0
        
	for i in range(len(wedge_labels)):
	    min = int(time_in_zone[i]/60.)
	    sec = int(time_in_zone[i] - min*60.)
	    secstr=str(sec).zfill(2)
	    s = "%d:%s" % (min,secstr)
	    wedge_labels[i] = wedge_labels[i]+"\n"+s
	    perc = 100.*time_in_zone[i]/totaltime
	    if perc < cutoff:
		wedge_labels[i] = ''
	
	# print(wedge_labels)
	fig2 = plt.figure(figsize=(5,5))
	fig_title = "Input File:  "+self.readfilename+" --- HR Time in Zone"
	ax9 = fig2.add_subplot(1,1,1)
	ax9.pie(time_in_zone,
		labels=wedge_labels,
		colors=['gray','gold','limegreen','dodgerblue','m','r'],
		autopct=lambda x: my_autopct(x,cutoff=cutoff+2),
		pctdistance=0.8,
		counterclock=False,
		startangle=90.0)

	plt.show()
	return 1

    def power_piechart(self):
	""" Figure 3 - Heart Rate Time in band.
	This is not as simple as just totalling up the
	hits for each band of HR.  Since each data point represents
	a different increment of time.  This loop scans through the
	HR data and adds that incremental time in each band

	"""

	df = self.df
#	df.sort_values(by=' ElapsedTime (sec)',ascending = 1)
	df.sort_values(by='TimeStamp (sec)',ascending = 1)
	number_of_rows = self.number_of_rows

	time_increments = df.ix[:,'TimeStamp (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))

	ut2,ut1,at,tr,an = self.rwr.ftp*np.array(self.rwr.powerperc)/100.
	
	time_in_zone = np.zeros(6)
	for i in range(number_of_rows):
	    if df.ix[i,' Power (watts)'] <= ut2:
		time_in_zone[0] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= ut1:
		time_in_zone[1] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= at:
		time_in_zone[2] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= tr:
		time_in_zone[3] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= an:
		time_in_zone[4] += time_increments[i]
	    else:
		time_in_zone[5] += time_increments[i]
		
	# print(time_in_zone)
	wedge_labels = ['power<ut2','power ut2','power ut1','power at',
			'power tr','power an']

	totaltime = time_in_zone.sum()
        perc = 100.*time_in_zone/totaltime
        cutoff = 1.0
        if len(perc[perc<cutoff])>1:
            cutoff = 2.0
            if len(perc[perc<cutoff])>1:
                cutoff = 3.0
        
	for i in range(len(wedge_labels)):
	    min = int(time_in_zone[i]/60.)
	    sec = int(time_in_zone[i] - min*60.)
	    secstr=str(sec).zfill(2)
	    s = "%d:%s" % (min,secstr)
	    wedge_labels[i] = wedge_labels[i]+"\n"+s
	    perc = 100.*time_in_zone[i]/totaltime

	    if perc < cutoff:
		wedge_labels[i] = ''
	
	# print(wedge_labels)
	fig2 = plt.figure(figsize=(5,5))
	fig_title = "Input File:  "+self.readfilename+" --- Power Time in Zone"
	ax9 = fig2.add_subplot(1,1,1)
	ax9.pie(time_in_zone,
		labels=wedge_labels,
		colors=['gray','gold','limegreen','dodgerblue','m','r'],
		autopct=lambda x: my_autopct(x,cutoff=cutoff+2),
		pctdistance=0.8,
		counterclock=False,
		startangle=90.0)

	plt.show()
	return 1

    def get_power_piechart(self,title):
	""" Figure 3 - Heart Rate Time in band.
	This is not as simple as just totalling up the
	hits for each band of HR.  Since each data point represents
	a different increment of time.  This loop scans through the
	HR data and adds that incremental time in each band

	"""

	df = self.df
#	df.sort_values(by=' ElapsedTime (sec)',ascending = 1)
	df.sort_values(by='TimeStamp (sec)',ascending = 1)
	number_of_rows = self.number_of_rows

	time_increments = df.ix[:,'TimeStamp (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))

	ut2,ut1,at,tr,an = self.rwr.ftp*np.array(self.rwr.powerperc)/100.
	
	time_in_zone = np.zeros(6)
	for i in range(number_of_rows):
	    if df.ix[i,' Power (watts)'] <= ut2:
		time_in_zone[0] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= ut1:
		time_in_zone[1] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= at:
		time_in_zone[2] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= tr:
		time_in_zone[3] += time_increments[i]
	    elif df.ix[i,' Power (watts)'] <= an:
		time_in_zone[4] += time_increments[i]
	    else:
		time_in_zone[5] += time_increments[i]
		
	# print(time_in_zone)
	wedge_labels = ['power<ut2','power ut2','power ut1','power at',
			'power tr','power an']

	totaltime = time_in_zone.sum()
        perc = 100.*time_in_zone/totaltime
        cutoff = 1.0
        if len(perc[perc<cutoff])>1:
            cutoff = 2.0
            if len(perc[perc<cutoff])>1:
                cutoff = 3.0

	for i in range(len(wedge_labels)):
	    min = int(time_in_zone[i]/60.)
	    sec = int(time_in_zone[i] - min*60.)
	    secstr=str(sec).zfill(2)
	    s = "%d:%s" % (min,secstr)
	    wedge_labels[i] = wedge_labels[i]+"\n"+s
	    perc = 100.*time_in_zone[i]/totaltime
	    if perc < 5:
		wedge_labels[i] = ''
	
	# print(wedge_labels)
	fig2 = plt.figure(figsize=(5,5))
	fig_title = title
	ax9 = fig2.add_subplot(1,1,1)
	ax9.pie(time_in_zone,
		labels=wedge_labels,
		colors=['gray','gold','limegreen','dodgerblue','m','r'],
		autopct=lambda x: my_autopct(x,cutoff=cutoff+2),
		pctdistance=0.8,
		counterclock=False,
		startangle=90.0)

	return fig2


    def get_piechart(self,title):
	""" Figure 3 - Heart Rate Time in band.
	This is not as simple as just totalling up the
	hits for each band of HR.  Since each data point represents
	a different increment of time.  This loop scans through the
	HR data and adds that incremental time in each band

	"""

	df = self.df
	number_of_rows = self.number_of_rows

	time_increments = df.ix[:,'TimeStamp (sec)'].diff()
	time_increments[0] = time_increments[1]
	time_increments = 0.5*(abs(time_increments)+(time_increments))
	
	time_in_zone = np.zeros(6)
	for i in range(number_of_rows):
	    if df.ix[i,' HRCur (bpm)'] <= self.rwr.ut2:
		time_in_zone[0] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.ut1:
		time_in_zone[1] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.at:
		time_in_zone[2] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.tr:
		time_in_zone[3] += time_increments[i]
	    elif df.ix[i,' HRCur (bpm)'] <= self.rwr.an:
		time_in_zone[4] += time_increments[i]
	    else:
		time_in_zone[5] += time_increments[i]
		
	# print(time_in_zone)
	wedge_labels = ['<ut2','ut2','ut1','at','tr','an']
	totaltime = time_in_zone.sum()
        perc = 100.*time_in_zone/totaltime
        cutoff = 1.0
        if len(perc[perc<cutoff])>1:
            cutoff = 2.0
            if len(perc[perc<cutoff])>1:
                cutoff = 3.0

	for i in range(len(wedge_labels)):
	    min = int(time_in_zone[i]/60.)
	    sec = int(time_in_zone[i] - min*60.)
	    secstr=str(sec).zfill(2)
	    s = "%d:%s" % (min,secstr)
	    wedge_labels[i] = wedge_labels[i]+"\n"+s
	    perc = 100.*time_in_zone[i]/totaltime
	    if perc < 5:
		wedge_labels[i] = ''
	
	# print(wedge_labels)
#	fig2 = plt.figure(figsize=(5,5))
	fig2 = figure.Figure(figsize=(5,5))
	fig_title = title
	ax9 = fig2.add_subplot(1,1,1)
	ax9.pie(time_in_zone,
		labels=wedge_labels,
		colors=['gray','gold','limegreen','dodgerblue','m','r'],
		autopct=lambda x: my_autopct(x,cutoff=cutoff+2),
		pctdistance=0.8,
		counterclock=False,
		startangle=90.0)


	return fig2

    def uploadtoc2(self,
		   comment="uploaded by rowingdata tool\n",
		   rowerFile="defaultrower.txt"):
	""" Upload your row to the Concept2 logbook

	Will ask for username and password if not known
	Will offer to store username and password locally for you.
	This is not mandatory

	This just fills the online logbook form. It may break if Concept2
	changes their website. I am waiting for a Concept2 Logbook API

	"""

	comment+="version %s.\n" % __version__
	comment+=self.readfilename

	# prepare the needed data
	# Date
	datestring = "{mo:0>2}/{dd:0>2}/{yr}".format(
	    yr = self.rowdatetime.year,
	    mo = self.rowdatetime.month,
	    dd = self.rowdatetime.day
	    )

	rowtypenr = [1]
	weightselect = ["L"]

	# row type
	availabletypes = getrowtype()
	try:
	    rowtypenr = availabletypes[self.rowtype]
	except KeyError:
	    rowtypenr = [1]


	# weight
	if (self.rwr.weightcategory.lower()=="lwt"):
	    weightselect = ["L"]
	else:
	    weightselect = ["H"]

	df = self.df

	# total dist, total time, avg pace, avg hr, max hr, avg dps

	totaldist = df['cum_dist'].max()
	totaltime = df['TimeStamp (sec)'].max()
	avgpace = 500*totaltime/totaldist
	avghr = df[' HRCur (bpm)'].mean()
	maxhr = df[' HRCur (bpm)'].max()
	avgspm = df[' Cadence (stokes/min)'].mean()
	avgdps = totaldist/(totaltime*avgspm/60.)

	hour=int(totaltime/3600)
	min=int((totaltime-hour*3600.)/60)
	sec=int((totaltime-hour*3600.-min*60.))
	tenth=int(10*(totaltime-hour*3600.-min*60.-sec))

	# log in to concept2 log, ask for password if it isn't known
	print "login to concept2 log"
	save_user = "y"
	save_pass = "y"
	if self.rwr.c2username == "":
	    save_user = "n"
	    self.rwr.c2username = raw_input('C2 user name:')
	    save_user = raw_input('Would you like to save your username (y/n)? ')
	    
	if self.rwr.c2password == "":
	    save_pass = "n"
	    self.rwr.c2password = getpass.getpass('C2 password:')
	    save_pass = raw_input('Would you like to save your password (y/n)? ')

	# try to log in to logbook
	br = mechanize.Browser()
	loginpage = br.open("http://log.concept2.com/login")

	# the login is the first form
	br.select_form(nr=0)
	# set user name
	usercntrl = br.form.find_control("username")
	usercntrl.value = self.rwr.c2username

	pwcntrl = br.form.find_control("password")
	pwcntrl.value = self.rwr.c2password

	response = br.submit()
	if "Incorrect" in response.read():
	    print "Incorrect username/password combination"
	    print ""
	else:
	    # continue
	    print "login successful"
	    print ""
	    br.select_form(nr=0)

	    br.form['type'] = rowtypenr
	    print "setting type to "+self.rowtype

	    datecntrl = br.form.find_control("date")
	    datecntrl.value = datestring
	    print "setting date to "+datestring

	    distcntrl = br.form.find_control("distance")
	    distcntrl.value = str(int(totaldist))
	    print "setting distance to "+str(int(totaldist))

	    hrscntrl = br.form.find_control("hours")
	    hrscntrl.value = str(hour)
	    mincntrl = br.form.find_control("minutes")
	    mincntrl.value = str(min)
	    secscntrl = br.form.find_control("seconds")
	    secscntrl.value = str(sec)
	    tenthscntrl = br.form.find_control("tenths")
	    tenthscntrl.value = str(tenth)

	    print "setting duration to {hour} hours, {min} minutes, {sec} seconds, {tenth} tenths".format(
		hour = hour,
		min = min,
		sec  = sec,
		tenth = tenth
		)

	    br.form['weight_class'] = weightselect

	    print "Setting weight class to "+self.rwr.weightcategory+"("+weightselect[0]+")"

	    commentscontrol = br.form.find_control("comments")
	    commentscontrol.value = comment
	    print "Setting comment to:"
	    print comment

	    print ""

	    res = br.submit()

	    if "New workout added" in res.read():

		# workout added
		print "workout added"
	    else:
		print "something went wrong"

	if save_user == "n":
	    self.rwr.c2username = ''
	    print "forgetting user name"
	if save_pass == "n":
	    self.rwr.c2password = ''
	    print "forgetting password"


	if (save_user == "y" or save_pass == "y"):
	    self.rwr.write(rowerFile)
	    

	print "done"


def dorowall(readFile="testdata",window_size=20):
    """ Used if you have CrewNerd TCX and summary CSV with the same file name

    Creates all the plots and spits out a text summary (and copies it
    to the clipboard too!)

    """

    tcxFile = readFile+".TCX"
    csvsummary = readFile+".CSV"
    csvoutput = readFile+"_data.CSV"

    tcx = rowingdata.TCXParser(tcxFile)
    tcx.write_csv(csvoutput,window_size=window_size)

    res = rowingdata.rowingdata(csvoutput)
    res.plotmeters_otw()

    sumdata = rowingdata.summarydata(csvsummary)
    sumdata.shortstats()

    sumdata.allstats()
