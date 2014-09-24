import matplotlib.pyplot as plt
import numpy as np
import datetime,time,os.path,xlrd
import matplotlib.gridspec as gridspec

class UnassignedGraphError(BaseException):
    pass

def metadata(fig,show,climates,files):
##  fig = the figure on which the metadata is drawn  ##
##  show = whether the plot will be show on the screen  ##
##  climates = what climate models are being used  ##
##  files = the data file names with paths  ##
    ax = fig.add_subplot(111,position=[0.125,0.165,0.001,0.001])
    textstr = 'Willamette Water 2100\nGraph generated on ' + str(datetime.date.today()) +'\n\n'+ climates[0] + ' data generated on ' + time.ctime(os.path.getctime(files[0])) +'\n'+ climates[1] + ' data generated on ' + time.ctime(os.path.getctime(files[1])) +'\n'+ climates[2] + ' data generated on ' + time.ctime(os.path.getctime(files[2])) +'\n'+ climates[3] + ' data generated on ' + time.ctime(os.path.getctime(files[3]))
    if show:
        props = dict(boxstyle='round', facecolor=(0.75,0.75,0.75), lw=0.)
    else:
        props = dict(boxstyle='round', facecolor='white', lw=0.)
    plt.text(-100, 15, textstr, transform=ax.transAxes, fontsize=6,verticalalignment='top',bbox = props)
    return

def day_average(data):
    '''
    Averages the same days across 90 years
    '''
    days = []
    step = 0
    for h in range(3):
        section = []
        for i in range(365):
            day = 0
            for j in range(30):
                day += data[(i*j)+step]
            section += [day/30]
        days += [section]
        step += 30
    return days



def multi_plot(data1,data2,data3,data4,climates,show,title,files):
    from matplotlib.font_manager import FontProperties
    fprops = FontProperties()
    fprops.set_size('small')
    averaging_window = 59
    window_raw = np.array([])
    window_raw = np.append(window_raw,[n_take_k(averaging_window-1,i) for i in range(averaging_window)])
    window = window_raw / np.sum(window_raw)
##  Plot preparation  ##
    clmt1 = climates[0]
    clmt2 = climates[1]
    clmt3 = climates[2]
    clmt4 = climates[3]
    fig = plt.figure(title, figsize=(10,7.5))
    first = fig.add_subplot(111, position = [0.08,0.37,0.4,0.25])
    first.plot(data1[0],movingaverage([np.mean(data1[1,i]) for i in range(365-(averaging_window/2) , 364)]+
                                      [np.mean(data1[1,i]) for i in range(365)]+
                                      [np.mean(data1[1,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.62')
    first.plot(data1[0],movingaverage([np.mean(data1[2,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data1[2,i]) for i in range(365)]+
                                      [np.mean(data1[2,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.32')
    first.plot(data1[0],movingaverage([np.mean(data1[3,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data1[3,i]) for i in range(365)]+
                                      [np.mean(data1[3,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0')
    first.legend(('Early century', 'Mid century', 'Late century'), bbox_to_anchor=(0.45,1.7),  fontsize=12)
    first.set_xlabel('$Month \, of \, Year$', fontsize=14)
    first.set_ylabel('$Discharge \,$ [m$^{\t{3}}$/s]',fontsize=14)
    month_labels(first)
    plt.xlim(273,640)
    plt.title(clmt1)
##  End of first plot code (the remainder is a repetition of it)  ##
    second = fig.add_subplot(111, position = [0.55,0.7,0.4,0.25])
    second.plot(data2[0],movingaverage([np.mean(data2[1,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data2[1,i]) for i in range(365)]+
                                      [np.mean(data2[1,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.62')
    second.plot(data2[0],movingaverage([np.mean(data2[2,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data2[2,i]) for i in range(365)]+
                                      [np.mean(data2[2,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.32')
    second.plot(data2[0],movingaverage([np.mean(data2[3,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data2[3,i]) for i in range(365)]+
                                      [np.mean(data2[3,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0')
    month_labels(second)
    plt.xlim(273,640)
    plt.title(clmt2+' minus '+clmt1)
    third = fig.add_subplot(111, position = [0.55,0.37,0.4,0.25])
    third.plot(data3[0],movingaverage([np.mean(data3[1,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data3[1,i]) for i in range(365)]+
                                      [np.mean(data3[1,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.62')
    third.plot(data2[0],movingaverage([np.mean(data3[2,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data3[2,i]) for i in range(365)]+
                                      [np.mean(data3[2,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.32')
    third.plot(data2[0],movingaverage([np.mean(data3[3,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data3[3,i]) for i in range(365)]+
                                      [np.mean(data3[3,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0')
    month_labels(third)
    plt.xlim(273,640)
    plt.title(clmt3+' minus '+clmt1)
    fourth = fig.add_subplot(111, position = [0.55,0.04,0.4,0.25])
    fourth.plot(data4[0],movingaverage([np.mean(data4[1,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data4[1,i]) for i in range(365)]+
                                      [np.mean(data4[1,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.62')
    fourth.plot(data4[0],movingaverage([np.mean(data4[2,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data4[2,i]) for i in range(365)]+
                                      [np.mean(data4[2,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0.32')
    fourth.plot(data4[0],movingaverage([np.mean(data4[3,i]) for i in range(365-averaging_window/2 , 364)]+
                                      [np.mean(data4[3,i]) for i in range(365)]+
                                      [np.mean(data4[3,i]) for i in range(0,averaging_window/2)],window)[averaging_window/2:365+averaging_window/2],color = '0')
    month_labels(fourth)
    plt.xlim(273,640)
    plt.title(clmt4+' minus '+clmt1)
##  Metadata and title  ##
    metadata(fig,show,climates,files)
    ttl = fig.add_subplot(111,position=[0.1,0.9,0.001,0.001])
    if show:
        props = dict(boxstyle='round', facecolor=(0.75,0.75,0.75), lw=0.)
    else:
        props = dict(boxstyle='round', facecolor='white', lw=0.)
    plt.text(-80, 8, title, transform=ttl.transAxes, fontsize=14, verticalalignment='top', bbox = props)
##  Plot generation  ##
    if show:
        plt.show(1)
    else:
        plt.savefig(title+'('+climates[0]+')'+'.png', format = 'png', dpi = 300.0)
    plt.close(1)
    return

def start():
    book = xlrd.open_workbook('Master File.xls')
    row0 = book.sheet_by_index(0).row_values(0)
    if 1.0 in(row0) and 2.0 in(row0) and 3.0 in(row0) and 4.0 in(row0):
        useless = True
    else:
        raise UnassignedGraphError()
    show = bool(book.sheet_by_index(0).col_values(0)[9])
    path = book.sheet_by_index(0).col_values(0)[5]
##  File name reading  ##
    graph = row0.index(1.0)
    files1 = book.sheet_by_index(0).col_values(graph)[2:]
    climate1 = book.sheet_by_index(0).col_values(graph)[1]
    graph = row0.index(2.0)
    files2 = book.sheet_by_index(0).col_values(graph)[2:]
    climate2 = book.sheet_by_index(0).col_values(graph)[1]
    graph = row0.index(3.0)
    files3 = book.sheet_by_index(0).col_values(graph)[2:]
    climate3 = book.sheet_by_index(0).col_values(graph)[1]
    graph = row0.index(4.0)
    files4 = book.sheet_by_index(0).col_values(graph)[2:]
    climate4 = book.sheet_by_index(0).col_values(graph)[1]
    titles = book.sheet_by_index(0).col_values(1)[2:]
    climates = [climate1,climate2,climate3,climate4]
    to_plot = book.sheet_by_index(0).col_values(2)[2:]
##  File reading + data handling  ##
    for i in range(len(files1)):
        if bool(to_plot[i]):
            file1 = np.array(np.genfromtxt(path+files1[i], delimiter=',',skip_header=1))
            file2 = np.array(np.genfromtxt(path+files2[i], delimiter=',',skip_header=1))
            file3 = np.array(np.genfromtxt(path+files3[i], delimiter=',',skip_header=1))
            file4 = np.array(np.genfromtxt(path+files4[i], delimiter=',',skip_header=1))
            title = str(titles[i])
            assert len(file1[1]) == len(file2[1]) and len(file1[1]) == len(file3[1]) and len(file1[1]) == len(file4[1])
            average = day_average(file1[:,1])
            data1 = np.array([range(274,639),average[0],average[1],average[2]])
            average = day_average(file2[:,1]-file1[:,1])
            data2 = np.array([range(274,639),average[0],average[1],average[2]])
            average = day_average(file3[:,1]-file1[:,1])
            data3 = np.array([range(274,639),average[0],average[1],average[2]])
            average = day_average(file4[:,1]-file1[:,1])
            data4 = np.array([range(274,639),average[0],average[1],average[2]])
##  Data transfer to the multi_plot function  ##
            multi_plot(data1,data2,data3,data4,climates,show,title,[path+files1[i],path+files2[i],path+files3[i],path+files4[i]])
    return

def month_labels (axys):
##    This function was pulled from Roy Haggerty's Cascade Plot code
    """
    Place month labels on horizontal axis.  This is a little tricky,
       so I found some code on the web and modified it.
    """
    from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
    import matplotlib.pyplot as plt
    import matplotlib.dates as dates
    import datetime
    import matplotlib.ticker as ticker

    axys.xaxis.set_major_locator(dates.MonthLocator())
    axys.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
    axys.xaxis.set_major_formatter(ticker.NullFormatter())
    axys.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
    for tick in axys.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')
    return

def n_take_k(n,k):
##    This function was pulled from Roy Haggerty's Cascade Plot code
    """Returns (n take k),
    the binomial coefficient.

    author: https://code.google.com/p/econpy/source/browse/trunk/pytrix/pytrix.py
    """
    n, k = int(n), int(k)
    assert (0<=k<=n), "n=%f, k=%f"%(n,k)
    k = min(k,n-k)
    c = 1
    if k>0:
        for i in xrange(k):
            c *= n-i
            c //= i+1
    return c

def movingaverage(interval, window):
##    This function was pulled from Roy Haggerty's Cascade Plot code
    """
    Calculate a moving average and return numpy array (dimension 1)
    """
    return np.convolve(interval, window, 'same')

start()
