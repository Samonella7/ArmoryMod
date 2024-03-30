import os
import re
from glob import glob

dirs = ['/mnt/c/Program Files (x86)/Steam/steamapps/common/wesnoth/data/']
savefile = 'weapon-types.txt'

def main ():
    files = []
    for rootDir in dirs:
        files += glob(rootDir + '**/units/**/*.cfg', recursive=True)
    
    attacks = set()
    attackRegex = re.compile('\\[attack\\](?:.|\n|\r)*?\\[\\/attack]')
    attackNameRegex = re.compile('(?:.|\n|\r)*name\s*=\s*_*\s*(.*)(?:.|\n|\r)*')
    for filename in files:
        text = ''
        with open(filename, 'r') as file:
            text = file.read()
        for attack in re.findall(attackRegex, text):
            matches = re.findall(attackNameRegex, attack)
            stripedMatches = [s.strip('"') for s in matches]
            attacks.update(stripedMatches)
            # if 'longsword' in stripedMatches:
            #     print (filename)

    data = readSave()

    for attack in attacks:
        if not any(attack in l for l in data.values()):
            data['unsorted'].append(attack)
    
    writeSave(data)
    
def readSave ():
    data = {}
    with open(savefile, 'r') as file:
        weapon_list = []
        weapon_type = ''
        for line in file:
            if line.isspace():
                continue

            elif ':' in line:
                # encountered a new weapon type. save the old one:
                if weapon_type != '':
                    data[weapon_type] = weapon_list
                # start a new one:
                weapon_type = line.strip().strip(':')
                weapon_list = []

            else:
                weapon_list.append(line.strip())
        
        data[weapon_type] = weapon_list
    
    return data

def writeSave (data):
    with open(savefile, 'w') as file:
        for weapon_type in data.keys():
            weapon_list = data[weapon_type]
            file.write(weapon_type + ':\n')
            file.writelines('\t' + w + '\n' for w in weapon_list)

def searchFolder (folder):
    return 

if __name__ == '__main__':
    main()
