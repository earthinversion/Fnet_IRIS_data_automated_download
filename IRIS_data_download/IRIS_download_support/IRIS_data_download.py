from obspy.clients.fdsn import Client #import Client
from datetime import datetime as dt
from obspy.core import UTCDateTime
from obspy import read, read_inventory

client = Client("IRIS")
import matplotlib.pyplot as plt
plt.style.use("seaborn")

now = dt.now()

daylag = 0 #number of days of lag
hourdiff = 9 #greater than 1
# starttime = UTCDateTime(now-daylag)
# endtime = UTCDateTime(now)
starttime = UTCDateTime(now.strftime("%Y/%m/{},{}:%M:%S".format(now.day - (daylag),now.hour-hourdiff)))
endtime = UTCDateTime(now.strftime("%Y/%m/{},{}:%M:%S".format(now.day,now.hour-(hourdiff-1))))
print("current Time: {}".format(UTCDateTime(now.strftime("%Y/%m/{},{}:%M:%S".format(now.day,now.hour)))))
print(f"Hour lag: {hourdiff}")
print("starttime: {}; endtime: {}".format(starttime,endtime))

network = "IU"
station = "ANMO"
location = "00"
component = "BH?"
data_filename = f"{network}_{station}_{location}_{component}.mseed"
inventoryfile = f"{network}_{station}_{location}_{component}.xml"
try:
    ## retrieve data info
    stream = client.get_waveforms(network, station, location, component, starttime, endtime,attach_response=True)
    invt = client.get_stations(starttime = starttime, endtime=endtime, network=network, station=station, channel=component,level="response")
    invt.write(inventoryfile, 'STATIONXML')

    ## save data to MSEED file
    stream.write(data_filename, format="MSEED") 

    ## Read data
    st = read(data_filename) 
    inv = read_inventory(inventoryfile)
    st.remove_response(inventory=inv,output="DISP") #"VEL" #remove response
    st.detrend('linear') #detrend

    sps = st[0].stats.sampling_rate
    print(f"Sampling rate is {sps}")
    print(f"Length of stream is {len(st)}")


    plot_data = 1
    if plot_data:
        fig, ax = plt.subplots(3,1,figsize=(10,6),sharex=True)
        ax[0].plot(st[0].times("matplotlib"), st[0].data, "r-",lw=0.5,label=st[0].stats.channel)
        ax[0].legend(loc='best')

        ax[1].plot(st[1].times("matplotlib"), st[1].data, "r-",lw=0.5,label=st[1].stats.channel)
        ax[1].legend(loc='best')

        ax[2].plot(st[2].times("matplotlib"), st[2].data, "r-",lw=0.5,label=st[2].stats.channel)
        ax[2].legend(loc='best')

        ax[2].xaxis_date()
        fig.autofmt_xdate()
        plt_id = f"{st[0].stats.network}-{st[0].stats.station}"
        ax[0].set_title(plt_id)
        ax[2].set_xlabel("UTCDateTime")

        plt.savefig(f'{plt_id}_{starttime}-{endtime}.png',dpi=300,bbox_inches='tight')
        plt.close('all')
except Exception as e:
    print(e)