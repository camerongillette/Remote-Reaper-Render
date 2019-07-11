import os
import math,time
import csv
from subprocess import check_output

reaperFileListPath = "C:\\Users\\Cam\\Dropbox\\reaper_file_list.txt"
start_path = "C:\\production\\music recording\\"

class FileDateMod:
	def __init__(self, file, dateMod):
		self.file = file
		self.dateMod = dateMod
	
	def __cmp__(self, other):
		if hasattr(other, 'dateMod'):
			return self.dateMod.__cmp__(other.dateMod)
	
def getFilesWithDateMod():
	filesWithDateMod = []

	#Traverse directory tree
	for (path,dirs,files) in os.walk(start_path):
		for file in files:
			if file.lower().endswith(".rpp"):
				fstat = os.stat(os.path.join(path,file))

				# Convert file size to MB, KB or Bytes
				if (fstat.st_size > 1024 * 1024):
					fsize = math.ceil(fstat.st_size / (1024 * 1024))
					unit = "MB"
				elif (fstat.st_size > 1024):
					fsize = math.ceil(fstat.st_size / 1024)
					unit = "KB"
				else:
					unit = "B"
				osfsize = fstat.st_size

				mtime = time.strftime("%X %x", time.gmtime(fstat.st_mtime))
				
				 # Print file attributes
				filesWithDateMod.append(FileDateMod(path+"\\"+file,fstat.st_mtime))
				#print('\t{:15.15s} {:2s} {:18s}'.format(file,unit,mtime))

	filesWithDateMod.sort(key=lambda x: x.dateMod, reverse=True)
	#for x in range(len(filesWithDateMod)): 
	#	print('\t{:2s} {:18f}'.format(filesWithDateMod[x].file,filesWithDateMod[x].dateMod))
	return filesWithDateMod

def updateFileList():
	fileList = getFilesWithDateMod()
	#empty the file
	#open(reaperFileListPath, 'w').close()
	#repopulate
	with open(reaperFileListPath, mode='wb') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for x in range(len(fileList)): 
			if(fileList[x].file != ""):
				csv_writer.writerow([fileList[x].file, 0])
	
def checkFileList():
	renderTookPlace = 0
	with open(reaperFileListPath) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if(row[1] == "1"):
				check_output("\"C:\\Program Files\\REAPER (x64)\\reaper.exe\" -renderproject \""+row[0]+"\"", shell=True)
				renderTookPlace = 1
			line_count += 1
	if renderTookPlace == 1:
		updateFileList()

while True:
	time.sleep(5)		
	checkFileList()