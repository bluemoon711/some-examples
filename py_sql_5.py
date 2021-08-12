#!/usr/bin/env python3.6
import os
import pandas as pd
import csv
from shutil import copyfile
import datetime

test_dir_path = os.environ["WORKSPACE"] + '/' + os.environ["BUILD_NUMBER"] + "_LOG_DIR"
test_result_file = test_dir_path + "/pandas_multiple.xlsx"
template_file = test_dir_path + "/template.xlsx"
fvalue = os.environ["FirmwareVersion"]
rebootvalue = os.environ["ER Reboot Logs"]
powervalue = os.environ["ER Power Disconnect Logs"]
volvalue = os.environ["ER Battery Voltage"]
vehtype = os.environ["Vehicle Type"] 
mapver = os.environ["MapsVersion"]
lvsvalue = os.environ["LVS Enabled"] 
ecmconnect = os.environ["ECM Connection"] 
calstatus = os.environ["Calibration Status"]
calneed = os.environ["Calibration Needed - AV/ADAS Enabled"] 
card = os.environ["DvrSdCardRecordedFrame/DvrSdCardDvrActiveRunTimePercentage"]
count = os.environ["SDCardUNMOUNTEDCount"]
dropnum = os.environ["AdasDroppedFramesIncidentDroppedOver10Count"]
stamp = os.environ["AVGGpsStatsLargeTimestamps"]
gpsreset =os.environ["GpsStatsUbloxResets"]
gpssec = os.environ["AVGGpsStatsTimeToFirstValidPointSeconds"]
upload_file = "excel"

copyfile(upload_file, template_file)
os.chdir(test_dir_path)
files = [f for f in os.listdir('.') if os.path.isfile(f)]
print("All files found:\n"+";".join(files))

df = pd.read_csv(files[0])
df = df.iloc[1:] 
#prefilter with in service and ODD-0
df1 = df[(df["ERStatus"]=="In Service")&(df["Overdue for Download"]=="0")]
df2 = df1.loc[df["FirmwareVersion"] != fvalue]
df3 = df1.loc[df["ER Reboot Logs"] > rebootvalue]
df4 = df1.loc[df["ER Power Disconnect Logs"] > powervalue]
df5 = df1.loc[(df["ER Battery Voltage LOW"] == volvalue) | (df["ER Battery Voltage HIGH"] == volvalue)]
df6 = df1.loc[df["Vehicle Type"] == vehtype]
df7 = df1.loc[df["MapsVersion"] == mapver]
df8 = df1.loc[df["LVS Enabled"] == lvsvalue]
df9 = df1.loc[df["ECM Connection"] == ecmconnect]
df10 = df1.loc[(df["Calibration Status"] == calstatus) & (df["Calibration Needed - AV/ADAS Enabled"] == calneed)]
df801 = df1.loc[df["LVS Enabled"] == "1"]
df11 = df801.loc[(df["DvrSdCardRecordedFrame/DvrSdCardDvrActiveRunTimePercentage"] == card)]
df12 = df801.loc[df["SDCardUNMOUNTEDCount"] == count]
df13 = df1.loc[df["AdasDroppedFramesIncidentDroppedOver10Count"] > dropnum]
df14 = df1.loc[(df["AVGGpsStatsLargeTimestamps"] > stamp) | (df["GpsStatsUbloxResets"] > gpsreset) | (df["AVGGpsStatsTimeToFirstValidPointSeconds"] < gpssec)]
def highlight_cols(s, coldict):
	if s.name in coldict.keys():
		return ['background-color: {}'.format(coldict[s.name])] * len(s)
	return [''] * len(s)
coldict = {'ERStatus':'yellow', 'Overdue for Download': 'yellow'}
fwdict = {'FirmwareVersion':'yellow'}
rebootdict = {'ER Reboot Logs': 'yellow'}
powerdict = {'ER Power Disconnect Logs': 'yellow'}
batdict = {'ER Battery Voltage LOW': 'yellow', 'ER Battery Voltage HIGH': 'red'}
vehdict = {'Vehicle Type': 'yellow'}
mapdict ={'MapsVersion': 'yellow'}
lvsdict ={'LVS Enabled': 'yellow'}
ecmdict ={'ECM Connection': 'yellow'}
caldict = {'Calibration Status': 'yellow', 'Calibration Needed - AV/ADAS Enabled': 'red'}
streamdict = {'DvrSdCardRecordedFrame/DvrSdCardDvrActiveRunTimePercentage': 'yellow'}
sddict = {'SDCardUNMOUNTEDCount': 'yellow'}
dropdict = {'AdasDroppedFramesIncidentDroppedOver10Count': 'yellow'}
gpsdict = {'AVGGpsStatsLargeTimestamps': 'yellow', 'GpsStatsUbloxResets': 'red', 'AVGGpsStatsTimeToFirstValidPointSeconds': 'blue'}

xl = pd.ExcelFile(template_file)
df00 = xl.parse('summary')
df00.columns= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
df00.at[0, 'B'] = f"{datetime.datetime.now():%Y-%m-%d}"
df00.at[1, 'B'] = len(df1.index)
df00.at[2, 'B'] = fvalue
#7: er reboots
df00.at[7, 'D'] = len(df1.index)
df00.at[7, 'E'] = len(df3.index)
df00.at[7, 'F'] = "{:.2%}".format(df00.loc[7, 'E']/df00.loc[7,'D'])
df00.at[7, 'G'] = df3["SerialNumber"].tolist()
df00.at[7, 'H'] = df3["CompanyName"].tolist()
#8: battery
df00.at[8, 'D'] = len(df1.index)
df00.at[8, 'E'] = len(df5.index)
df00.at[8, 'F'] = "{:.2%}".format(df00.loc[8, 'E']/df00.loc[8,'D'])
df00.at[8, 'G'] = df5["SerialNumber"].tolist()
df00.at[8, 'H'] = df5["CompanyName"].tolist()
#11: missing maps
df00.at[11, 'D'] = len(df1.index)
df00.at[11, 'E'] = len(df7.index)
df00.at[11, 'F'] = "{:.2%}".format(df00.loc[11, 'E']/df00.loc[11,'D'])
df00.at[11, 'G'] = df7["SerialNumber"].tolist()
df00.at[11, 'H'] = df7["CompanyName"].tolist()
#14: power disconnects
df00.at[14, 'D'] = len(df1.index)
df00.at[14, 'E'] = len(df4.index)
df00.at[14, 'F'] = "{:.2%}".format(df00.loc[14, 'E']/df00.loc[14,'D'])
df00.at[14, 'G'] = df4["SerialNumber"].tolist()
df00.at[14, 'H'] = df4["CompanyName"].tolist()
#15: fw_upgrade:
df00.at[15, 'D'] = len(df1.index)
df00.at[15, 'E'] = len(df2.index)
df00.at[15, 'F'] = "{:.2%}".format(df00.loc[15, 'E']/df00.loc[15,'D'])
df00.at[15, 'G'] = df2["SerialNumber"].tolist()
df00.at[15, 'H'] = df2["CompanyName"].tolist()
#17: Over Due for Download:
def remove(listA, listB):
	for item in listB:
		listA.remove(item)
	return listA
df00.at[17, 'D'] = len(df1.index)
df00.at[17, 'E'] = len(df.index)-len(df1.index)
df00.at[17, 'F'] = "{:.2%}".format(df00.loc[17, 'E']/df00.loc[17,'D'])
df00.at[17, 'G'] = [item for item in df["SerialNumber"].tolist() if item not in df1["SerialNumber"].tolist()]
df00.at[17, 'H'] = remove(df["CompanyName"].tolist(), df1["CompanyName"].tolist())
#4:
df00.at[4, 'B'] = df00.loc[17, 'F']
df00.at[4, 'C'] = df00.loc[11, 'F']
df00.at[4, 'D'] = df00.loc[8, 'F']
df00.at[4, 'E'] = "{:.2%}".format(len(df10.index)/len(df1.index))
df00.at[4, 'F'] = "{:.2%}".format(len(df11.index)/len(df1.index))
df00.at[4, 'G'] = "{:.2%}".format(len(df12.index)/len(df1.index))
df00.at[4, 'H'] = df00.loc[7, 'F']
df00.at[4, 'I'] = df00.loc[15, 'F']
df00.at[4, 'J'] = df00.loc[14, 'F']


writer = pd.ExcelWriter(test_result_file, engine='xlsxwriter')

def color_red(val):     
	color = 'black'
	try:
		if not val.endswith('%'): 
			pass
		elif float(val.rstrip('%')) > 5:
			color ='red'
		else:
			color = 'green'
	except:
		pass		
	return 'color: %s' % color

df00.style.apply(lambda x: ['background-color:#a9b2bc' if i < 3 else '' for i,_ in x. iteritems()])\
.apply(lambda x: ['background-color:#8c99a6' if 2 < i < 5 else '' for i,_ in x. iteritems()])\
.apply(lambda x: ['background-color:#c5ccd2'  if x.name == 'A' else '' for i,_ in x. iteritems()])\
.apply(lambda x: ['font-weight: bold' if x.name == 'A' or i < 6 else '' for i,_ in x. iteritems()])\
.applymap(color_red).to_excel(writer, sheet_name='summary', index=False)
df.to_excel(writer, sheet_name='fleet_data', index=False)
df1.style.apply(highlight_cols, coldict=coldict).to_excel(writer, sheet_name='prefilter_data', index=False)
df2.style.apply(highlight_cols, coldict=fwdict).to_excel(writer, sheet_name='fw_failures', index=False)
df3.style.apply(highlight_cols, coldict=rebootdict).to_excel(writer, sheet_name='er_reboots', index=False)
df4.style.apply(highlight_cols, coldict=powerdict).to_excel(writer, sheet_name='er_power_disconnect', index=False)
df5.style.apply(highlight_cols, coldict=batdict).to_excel(writer, sheet_name='bad_battery', index=False)
df6.style.apply(highlight_cols, coldict=vehdict).to_excel(writer, sheet_name='vehicle_unassigned', index=False)
df7.style.apply(highlight_cols, coldict=mapdict).to_excel(writer, sheet_name='badmaps', index=False)
df8.style.apply(highlight_cols, coldict=lvsdict).to_excel(writer, sheet_name='LVS_not_enabled', index=False)
df9.style.apply(highlight_cols, coldict=ecmdict).to_excel(writer, sheet_name='ECM_not_detected', index=False)
df10.style.apply(highlight_cols, coldict=caldict).to_excel(writer, sheet_name='notcalibrated', index=False)
df11.style.apply(highlight_cols, coldict=streamdict).to_excel(writer, sheet_name='LVSstreaming_failures', index=False)
df12.style.apply(highlight_cols, coldict=sddict).to_excel(writer, sheet_name='SDCard_failures', index=False)
df13.style.apply(highlight_cols, coldict=dropdict).to_excel(writer, sheet_name='ADASframedrops', index=False)
df14.style.apply(highlight_cols, coldict=gpsdict).to_excel(writer, sheet_name='GPSerros', index=False)

writer.save()

os.chdir(test_dir_path)
fis = [f for f in os.listdir('.') if os.path.isfile(f)]
print("All files found:\n"+";".join(fis))

try:
	os.remove(fis[0])
	os.remove(fis[1])
except OSError:
	pass

