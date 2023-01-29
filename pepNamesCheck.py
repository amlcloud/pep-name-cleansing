from pepOpenAi import PepOpenAi
from needed_vars import repo_path, path
import logging
import csv
import pandas as pd
from replace_dict import word_ref
import re
from time import sleep

class PepNamesCheck:
    def __init__(self):
        self.namesGen = PepOpenAi()
        # CSV Format of the Names Data, including the link they were taken from
        # self.namesData = ["Name;Chosen Name;OpenAi Possible Names;URL"]
        self.namesData = ["Name;Chosen Name;OpenAi Possible Names;URL;GPT Chosen Name"]
        self.logger = logging.getLogger('ftpuploader')
        self.urls = []
        # Extract all the possible names included in the repository
        with open(f'{repo_path}/names_list.txt', encoding='utf-8') as fp:
            self.possibleNames = fp.readlines()[0].split(";")
        return
    
    # All this really does is call the name extraction function
    # from the PepOpenAi class
    def createNameAccuracy(self, urlList, numTimes):
        self.namesGen.getUrlNames(urlList=urlList, iterations=numTimes)
        return
    
    # Helper Functions
    def inputNamesData(self):
        newNames = []            
        for name in self.namesGen.names:

            # Change the name immediately
            changedName = self.changeWords(name)

            try:
                # This helper function checks if the immediately proceeding
                # word in the string is also in the possibleNames attribute
                # if so, returns the first and last name
                def makeLastName(index, possible_name, text):
                    try:
                        currLast = text.split()[index+1]
                        # if currLast in last_names:
                        # print("Testing: "+possible_name+' '+currLast)
                        # print("In last name: "+str(currLast in self.possibleNames))
                        # print("In first name: "+str(currLast in self.possibleNames))
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
                # Run through each word in the name
                # to check for possible first and last name combinations
                for i in range(len(changedName.split())):
                    poss_name = changedName.split()[i]
                    # if (poss_name in first_names):
                    if poss_name in self.possibleNames:
                        # print("Currently Testing this Name: "+poss_name)
                        currName = makeLastName(i, poss_name, name)
                    if currName != None:
                        # print("Appending this name: "+currName)
                        allNames.append(currName)

                # print(f'Current All Names: {allNames}')

                # If there were possible candidates,
                # we can take the name that occurred the latest;
                # assumes that preceeding combinations included titles (Mr, Ms, Hon., etc.)
                if allNames:
                    addName = allNames[len(allNames)-1]
                else:
                    addName = changedName

                # print(f'Chosen name: {addName}')

                # addData = f'{name};{addName};{str(allNames)};{self.namesGen.urlDict[name]}'
                # addData = f'{name};{addName};{str(allNames)};{nameUrl}'
                # addData = f'{name};{addName};{str(allNames)}'
            
            # This exception catches when the name's link cannot be found
            # NOTE: Do not know why yet this is the case, when all of the names'
            # urls should have been recorded
            except Exception as e:
                self.logger.error("Failed to make name for "+name+" due to "+repr(e))
                # newNames.append(addName)
                addName = self.changeWords(name)
                #allNames = []
                # addData = f'{name};{addName};[];Link not found'
            
            # Here we also test out if chatGPT can just clean the name for us
            try:
                gptName = self.GPTchangeWords(name)
            except Exception as e:
                self.logger.error(f'Failed to get GPT name because of {repr(e)}')

            # In this case, try the same thing for the URL
            try:
                addData = f'{name};{addName};{str(allNames)};{self.namesGen.urlDict[name]};{gptName}'
            except Exception as e:
                self.logger.error(f'Failed to find the url of {name} due to: {repr(e)}')
                addData = f'{name};{changedName};[];Link not found;{gptName}'

            # Record what you added and append it to the new list 
            print(f'Added Name Data: {addData}')
            self.namesData.append(addData)
            newNames.append(addName)

            # To prevent rate limit from reaching
            sleep(5)
        
        # Remove duplicates in the list of names present,
        # NOTE: This name generator does not assume names can be from different countries,
        # since ChatGPT may not know how to differentiate between PEPs with the same name
        self.namesGen.names = list(set(newNames))
        # self.names = list(set(self.names))
        return
    
    # Function to help filter out filler words in name
    def changeWords(self, name):
        for key in word_ref:
            if re.search(key, name):
                name = re.sub(key, word_ref[key], name)
        return name
    
    # GPT cleanses data
    def GPTchangeWords(self, name):
        # In this case, we give chat GPT a string
        # and ask it to only give the first name and last name
        cleanPrompt = f'Give only the first and last name in the format First Name, Last Name of this string: {name}'
        cleaned = self.namesGen.makeGPTQuery(cleanPrompt)
        return cleaned
    
    # Writes into a file the data added in the
    # namesData attribute of this class
    def writeNameAccuracy(self, path):
        with open(path, 'w', encoding='utf-8') as fp:
            writer = csv.writer(fp)
            for row in self.namesData:
                writer.writerow(row.split(";"))
        return
    
    # This returns all the URLs used to make the 
    # names database
    def makeUrlList(self, csv_path):
        # Create dataframe and then extract needed columns
        df = pd.read_csv(csv_path)
        # print(list(df.columns))
        self.urls = list(df['actual list url'])
        # print(self.urls)
        return
    
    # Uses the CSV from makeUrlList() to show the number
    # of CSVs present in the names_accuracy.csv vs
    # what was used from pep_register.csv
    def showURLSPresent(self, names_path):
        df = pd.read_csv(names_path)
        urlsPresent = list(df['URL'])
        # Compare URLs in CSV vs URLs stored in pepOpenAi from all the names
        inCsv = [link for link in self.urls if link in urlsPresent]
        # Now Print these results
        print(f'Links in CSV: (total count: {len(inCsv)})')
        #for link in inCsv:
        #    print(link)
        print(f'total count in csv: {len(inCsv)}')
        print(f'total count of all URLS: {len(self.urls)}')
        return