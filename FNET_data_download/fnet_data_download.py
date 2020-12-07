import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime as dt
import os, glob
import shutil
import requests
import zipfile
import warnings
warnings.filterwarnings("ignore")

from config import user,passwd

now = dt.now()

daylag = 1 #number of days of lag
# print(now.year,now.month,now.day - 1,now.hour)

## Data is obtained for 1 day0
starttime = now.strftime("%Y/%m/{},{}:%M:%S".format(now.day - (daylag+1),now.hour))
endtime = now.strftime("%Y/%m/{},{}:%M:%S".format(now.day - (daylag),now.hour))
print("Requesting data from {} to {}".format(starttime,endtime))


# Data location
datadir="./downloadDir"



def page_is_loaded(br):
    return br.find_element_by_tag_name("body") != None


## all available Fnet stations
fnet=pd.read_csv('F_net_stations.txt',delimiter='\s+',header=None,names=['Station','stn','Lat','Lon','Alt','tt1','tt2','tt3'])
nfnet=fnet.iloc[::2, 0:5]
nfnet.set_index('Station',inplace=True)
print(nfnet.head())

# logfile = open("logfile.txt",'w')

# comps=['BHZ','BHN','BHE']
# for i,ss in enumerate(nfnet['stn'].values):
#     i+=1
# # for i in range(3,len(nfnet)):
#     # ss=nfnet.iloc[i,0]
#     for j in range(len(comps)):
#         # datafilename_tocheck = "{}_{}_*".format(ss,comps[j])
#         # datafilename_tocheck_list = glob.glob(datafilename_tocheck)

#         # request data for last one day
#         command1='get {} {} {} {}'.format(ss,comps[j],starttime,endtime)
#         # command1='get {} {} 2017/10/17,12:00:00 2017/11/05,12:00:00'.format(ss,comps[j])
#         print('--> Working on File {}/{}, Station: {}, Component: {}'.format(i,nfnet.shape[0], ss,comps[j]))
#         logfile.write('--> Working on File {}/{}, Station: {}, Component: {}\n'.format(i,nfnet.shape[0], ss,comps[j]))
#         #open up firefox browser and navigate to web page
#         br=webdriver.Firefox() #or webdriver.Chrome() but needs chromedriver or geockodriver
#         br.get("http://{}:{}@www.fnet.bosai.go.jp/auth/dataget/?LANG=en".format(user,passwd))
#         timeout=20 #wait for 20 sec to load
#         try:
#             wait=WebDriverWait(br,timeout)
#             wait.until(page_is_loaded)
#         except TimeoutException:
#             print("The requested web page is taking long to load!")
#             br.quit()
#         assert "Retrieval of Waveforms" in br.title #look for the title on the page
#         br.find_element_by_xpath("/html/body/form/table[1]/tbody/tr[3]/td/ul[1]/label[1]").click() #select data format MSEED

#         elem=br.find_element_by_name('commands')
#         elem.clear()
#         elem.send_keys(command1)
#         # elem.send_keys(Keys.RETURN)

#         br.find_element_by_xpath("/html/body/form/table[1]/tbody/tr[3]/td/div[8]/button").click()


        
#         try:
#             # wait to make sure there are two windows open
#             WebDriverWait(br, 10).until(lambda d: len(d.window_handles) == 2)

#             # switch windows
#             br.switch_to_window(br.window_handles[1])

#             element = WebDriverWait(br, 40).until(EC.element_to_be_clickable((By.XPATH, "/html/body/a[1]")))
#             linktosave=element.get_attribute("href")
#             filename=linktosave.split("=")[1]
#             fileFormat = ".mseed"
#             fullfilename = os.path.join(datadir, filename)
#             # print(f"fullfilename is {fullfilename}")
#             # print(f"linktosave is {linktosave}")

#             response = requests.get(linktosave, stream=True, auth=(user, passwd))
#             with open(fullfilename, 'wb') as out_file:
#                 shutil.copyfileobj(response.raw, out_file)
#             del response
#             # element.click()
#             zip_ref = zipfile.ZipFile(fullfilename, 'r')
#             tmplistname = zip_ref.namelist()
#             zip_ref.extractall(datadir)
#             zip_ref.close()
#             os.remove(fullfilename)
#             extractFileName = datadir+"/"+tmplistname[0]
#             if os.path.exists(extractFileName):
#                 os.rename(extractFileName,extractFileName+".mseed")
#                 logfile.write("----> Successful download: {}\n".format(os.path.basename(extractFileName)+".mseed"))
#         except Exception as e:
#             # print(e)
#             print("----> TIMEOUT: Loading file is taking way too long for file {}, station {}, component {}!".format(ss,comps[j]))
#             logfile.write("----> Failed download\n")

#         print(br.current_url)
#         br.quit()


# logfile.close()