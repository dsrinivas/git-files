import configparser
import csv
import itertools

colodict={}
locationdict = {}
businessUnit = {}
env = {}
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = lambda option: option

with open('NewInventoryAWX.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for idx,row in enumerate(csvReader,1):
        if idx == 1:
            pass
        else:
            colodict[row[0].upper() + '  ansible_host']  = row[1].upper()
            locationdict[row[0].upper()] = row[2]
            businessUnit[row[0].upper()] = row[4]
            env[row[0].upper()] = row[5]

config['colo'] = colodict
# adding End of File to Dictionary to represent last record
locationdict['EOF'] = 'EOF'
businessUnit['EOF'] = 'EOF'

# writing location values
values_view = locationdict.values()
value_iterator = iter(values_view)
serverLocation = next(value_iterator)

serverNames = {}

for key in locationdict:
        if locationdict.get(key) == serverLocation:
            serverNames[key] = None
        else:
            config[serverLocation] = serverNames
            serverNames.clear()
            serverLocation = locationdict.get(key)
            serverNames[key] = None

# writing business units values
values_view = businessUnit.values()
value_iterator = iter(values_view)
serverLocation = next(value_iterator)

serverNames = {}

for key in businessUnit:
        if businessUnit.get(key) == serverLocation:
            serverNames[key] = None
        else:
            config[serverLocation] = serverNames
            serverNames.clear()
            serverLocation = businessUnit.get(key)
            serverNames[key] = None

# writing environments values
envConfigDic = {}
envConfigs = {}

for serverName,envName in env.items():
    try:
        envConfigs[envName].append(serverName)
    except KeyError:
        envConfigs[envName] = [serverName]

for envName,serverNames in envConfigs.items():
    for serverName in serverNames:
        envConfigDic[serverName] = None
    config[envName] = envConfigDic
    envConfigDic.clear()


with open('hosts', 'w') as configfile:
   config.write(configfile,space_around_delimiters=False)


