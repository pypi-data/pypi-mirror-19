import ftplib
import sys
import re
sqlfilelist=[]
binfilelist=[]
barebinfilelist=[]

def getuserinfo(macget_lib_position):
    authlib = CDLL(macget_lib_position)
    mac=create_string_buffer(288)
    authlib.authGetFingerprint(pointer(mac),sizeof(mac))
    mac=mac.value#this is macode
    username='u'+mac[0:6]
    password='p'+mac[-6:]
    return [username,password]

#-----------------via list to get bin and sql filename dir-----
def listfile(dirname):
    filenamedir=os.listdir(dirname)
    for filename in filenamedir:
        if "sql" in filename:
            sqlfilelist.append(dirname+filename)
            barebinfilelist.append(filename)
    return [sqlfilelist,binfilelist]
#your path format is below
#getdirfilelist=listfile('/var/lib/mysql/')

#print sys.argv[1]##python ftpupload.py -u     will print -u
try:
    from configparser import ConfigParser



# instantiate
config = ConfigParser()

# parse existing file
# read pos values from a section to finish upload
currentpos = config.get('pos', 'cupos')
#print currentpos

'''
username = config.get('server', 'user')
password = config.get('server','password')
ftp_connection = ftplib.FTP(server, username, password)
'''
userinfo=getuserinfo('/tmp/goodday/libauth.so')
server='192.168.1.211'
#ftp_connection = ftplib.FTP(server, userinfo[0], userinfo[1])

ftp_connection = ftplib.FTP(server, 'u123456', 'p654321')
uploadbinfile_list=listfile('/var/lib/mysql/')[1]
uploadbinfile_list=listfile('/var/lib/mysql/')[1]
uploadbinfile_path=(sorted(uploadbinfile_list))[-3]

print sorted(barebinfilelist)
detect_list=(sorted(barebinfilelist))
'''
if detect_list[-3]!=currentpos:
    oldpos=re.split(r'\.',currentpos)
    oldpos2= int(oldpos[1])
    uploadposition=re.split(r'\.',detect_list[-3])
    uploadposition2=int(uploadposition[1])
    while oldpos2!=uploadposition2:
        newposition=uploadposition[0]+"."+(str(oldpos2).zfill(6))
        print "i will upload %s"%newposition
        #ftp_connection.storbinary('STOR /tmp/goodday/purebackdata/%s'%newposition, fh)
        ftp_connection.storbinary('STOR %s'%newposition, fh)
        oldpos2=oldpos2+1
'''
ftp_connection.storbinary('STOR %s'%(sorted(barebinfilelist))[-3], fh)

uploadposition=re.split(r'\.',detect_list[-3])
uploadposition2=int(uploadposition[1])
uploadposition3=uploadposition2+1
finalposition=uploadposition[0]+"."+(str(uploadposition3).zfill(6))
config.set('pos', 'cupos',finalposition)
# save to a file
with open(u'/tmp/goodday/position.ini', 'w') as configfile:
    config.write(configfile)



#ftp_connection.storbinary('STOR /tmp/goodday/purebackdata/backupdir/%s'%(sorted(barebinfilelist))[-3], fh)
fh.close()

'''
#-------------------detect if client upload successlly------------------------
# update existing value
#yangming-bin.000515
oldpos=re.split(r'\.',currentpos)
oldpos2= int(oldpos[1])
newpos=oldpos2+1
newposition="yangming-bin."+str(newpos).zfill(6)
config.set('pos', 'cupos',newposition)
# save to a file
with open(u'/tmp/goodday/position.ini', 'w') as configfile:
    config.write(configfile)

#----------------------get /var/lib/mysql/ bin file----------------------
'''
