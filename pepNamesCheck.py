from pepOpenAi import PepOpenAi
from needed_vars import repo_path, path
import logging
import csv
import pandas as pd

class PepNamesCheck:
    def __init__(self):
        self.namesGen = PepOpenAi()
        self.namesData = ["Name;Chosen Name;OpenAi Possible Names"]
        self.logger = logging.getLogger('ftpuploader')
        self.urls = []
        with open(f'{repo_path}/names_list.txt', encoding='utf-8') as fp:
            self.possibleNames = fp.readlines()[0].split(";")
        return
    
    def createNameAccuracy(self, urlList, numTimes):
        self.namesGen.getUrlNames(urlList=urlList, iterations=numTimes)
        return
    
    # Helper Functions
    def inputNamesData(self):
        newNames = []            
        for name in self.namesGen.names:
            try:
                def makeLastName(index, possible_name, text):
                    try:
                        currLast = text.split()[index+1]
                        # if currLast in last_names:
                        print("Testing: "+possible_name+' '+currLast)
                        print("In last name: "+str(currLast in self.possibleNames))
                        print("In first name: "+str(currLast in self.possibleNames))
                        if currLast in self.possibleNames:
                            # print("Returned: "+possible_name+' '+currLast)
                            return possible_name+' '+currLast
                        else:
                            return None
                    except:
                        return None

                allNames = []
                currName = ""
                addName = ""
                for i in range(len(name.split())):
                    poss_name = name.split()[i]
                    # if (poss_name in first_names):
                    if poss_name in self.possibleNames:
                        print("Currently Testing this Name: "+poss_name)
                        currName = makeLastName(i, poss_name, name)
                    if currName != None:
                        print("Appending this name: "+currName)
                        allNames.append(currName)

                # print(f'Current All Names: {allNames}')
                addName = allNames[len(allNames)-1]
                # print(f'Chosen name: {addName}')

                addData = f'{name};{addName};{str(allNames)}'
                print(f'Added Name Data: {addData}')
                self.namesData.append(addData)
                
                newNames.append(addName)
            except Exception as e:
                self.logger.error("Failed to make name for "+name+" due to "+str(e))
                pass
        
        self.names = list(set(newNames))
        # self.names = list(set(self.names))
        return
    
    def writeNameAccuracy(self, path):
        with open(path, 'w', encoding='utf-8') as fp:
            writer = csv.writer(fp)
            for row in self.namesData:
                writer.writerow(row.split(";"))
        return
    
    def makeUrlList(self, csv_path):
        # Create dataframe and then extract needed columns
        df = pd.read_csv(csv_path)
        # print(list(df.columns))
        self.urls = list(df['actual list url'])
        print(self.urls)
        return