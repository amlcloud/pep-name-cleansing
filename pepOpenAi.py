# Need the following imports

import openai
import needed_vars
from needed_vars import repo_path
import csv
import re
# import nltk
# from nltk import ne_chunk, pos_tag, word_tokenize
# from nltk.tree import Tree
from time import sleep
import logging
from country_list import countries_for_language
from names_dataset import NameDataset

class PepOpenAi:

    # TODO: Add variables that you might need
    def __init__(self):
        self.names = []
        self.data = "Name;Date of Birth;Country;Current Position\n"
        self.logger = logging.getLogger('ftpuploader')
        # self.countries = [item[1] for item in countries_for_language('en')]
        # self.nd = NameDataset()
        with open(f'{repo_path}/names_list.txt', encoding='utf-8') as fp:
            self.namesList = fp.readlines()[0].split(";")
            # print(self.namesList)
        # self.nameCountries = filtered_countries
        return

    def getNames(self, url):
        # Promp that will be used to get the list of names of PEPs
        textPrompt = "Create a CSV of the given names (without their position) of Politically Exposed Persons (PEPs) in this URL in the format Index, Name: "
        
        try:
            # Extract the names 
            namesQuery = self.makeGPTQuery(textPrompt+url)
        
            # Need to format the csv file so that everything looks clean
            STARTING_CHAR = '1'
            while namesQuery[0] != STARTING_CHAR:
                namesQuery = namesQuery[1:]

            NAME_HEADER = "Index,Name\n"
            if namesQuery.split("\n")[0] != NAME_HEADER[:10]:
                namesQuery = NAME_HEADER + namesQuery

            namesQuery = re.sub(", ", ",", namesQuery)
        
            # Now get the names you want to add and return them
            return [item[2:] for item in namesQuery.split("\n")[1:]]
        
        except Exception as e:
            self.logger.error("Failed to make list "+str(e))
            return []

    # Just uses getNames() to return the longest possible list
    # created from the query
    def getLongestNamesList(self, url, iterations=50):
        # maxLen = -1
        # newList = []
        # returnText = ""
        for i in range(iterations):
            currResponse = self.getNames(url)
            # print("CurrResponse:" + str(currResponse))
            for item in currResponse:
                # print("Item: "+item)
                # item = item.strip(',').upper()
                item = item.strip(',')
                item = item.strip(' ')
                item = item.strip("\n")
                if not item in self.names:
                    self.names.append(item)
            print("Current Iteration: "+str(i))
            print(self.names)
        # Don't know if I need this yet
        # RIGHT NOW: Likely we only start adding names
        # to the class when we are getting longest list of names
        # self.names = self.names + currResponse
        # self.names = newList
        # return currResponse
        return
    
    # This gets a list of URLs and gets the longest
    # List of names of each and puts them in the names attribute
    def getUrlNames(self, urlList, iterations=50):
        for url in urlList:
            self.getLongestNamesList(url, iterations)
        return

    # Possible function to filter out only the names in
    # the text
    def filterNames(self):
        newNames = []
        # ONE METHOD TRIED: https://unbiased-coder.com/extract-names-python-nltk/
        # --> DID NOT WORK
        # Make the list of names that you want to regex

        # Here we check if we want to filter the names to anything,
        # otherwise we really don't know and look at every country for a name match
              
        # print("FIRST NAMES:")
        # print(first_names)
        # print("LAST NAMES:")
        # print(last_names)
            
        for name in self.names:
            try:
                def makeLastName(index, possible_name, text):
                    try:
                        currLast = text.split()[index+1]
                        # if currLast in last_names:
                        print("Testing: "+possible_name+' '+currLast)
                        print("In last name: "+str(currLast in self.namesList))
                        print("In first name: "+str(currLast in self.namesList))
                        if currLast in self.namesList:
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
                    if poss_name in self.namesList:
                        # print("Currently Testing this Name: "+poss_name)
                        currName = makeLastName(i, poss_name, name)
                    if currName != None:
                        # print("Appending this name: "+currName)
                        allNames.append(currName)
                """
                for name in allNames:
                    if len(name) >= len(addName):
                        # print("Current New Name: "+name)
                        addName = name
                """
                print(f'Current All Names: {allNames}')
                addName = allNames[len(allNames)-1]
                print(f'Chosen name: {addName}')
                
                newNames.append(addName)
            except Exception as e:
                self.logger.error("Failed to make name for "+name+" due to "+str(e))
                pass
            # sleep(3)

        self.names = list(set(newNames))
        # self.names = list(set(self.names))
        return
    
    # Possible function to test if name really is a PEP
    def verifyNames(self):
        instances = 0
        newNames = []
        textPrompt = " a Politically Exposed Person? Answer with 'Yes' or 'No'."
        for name in self.names:
            try:
                ans = self.makeGPTQuery("Is "+name+textPrompt).strip('\n')
                ans = ans.strip()
                print("Is " + name + " a PEP? Answer: "+ans)
                if ans == 'Yes':
                    newNames.append(name)
                instances = instances + 1
            except Exception as e:
                print("Unable to do request for "+name)
                self.logger.error('Error in request '+str(e))
                # Print reason why request did not work
                pass
            sleep(3)
        self.names = newNames
        self.names = [item for item in self.names if ' ' in item]
        self.names = list(set(self.names))
        print("Number of Instances: "+str(instances))
        return

    # Once you have the names covered, you should be able
    # to get the needed data 
    def getNamesData(self, loopWeight=1):
        dataPrompt = "Get the Name, Date of Birth, Country, Current Position of the following people and put in a semicolon delimited CSV format: "
        dobPrompt = "Get the Date of Birth of "
        dobPrompt2 = " and put in the format mm-dd-yyyy"
        posPrompt = "Get the current political position of "
        countryPrompt = "Get the country of origin of "
        # posPrompt2
        currList = self.names

        # Run through the list and get the data
        while currList:
            # Current round of additions,
            # Response from ai compromises when too many entries
            # at a time
            # currAdd = currList[:loopWeight]
            currAdd = currList[0]

            # Use regex to extract the actual country from the code
            country = self.makeGPTQuery(countryPrompt+currAdd+".")
            print("Country Query Response: "+str(country))
            try:
                country = re.findall(r"(?=("+'|'.join(self.countries)+r"))", country)[0][0]
            except:
                country = "Unknown"
            print("Country: "+str(country))

            # Query for the desired information individually
            try:
                birth = self.makeGPTQuery(dobPrompt+currAdd+dobPrompt2)
                birth = re.findall(r'\d\d-\d\d-\d\d\d\d', birth)[0]
            except:
                birth = "Unknown"
            print("Birth: "+str(birth))
            
            # Still don't know how to extract position properly from
            # chatGPT response
            try:
                position = self.makeGPTQuery(posPrompt+currAdd+".")
                print(position)
                position = position.split(" is ")
                print(position)
                position = position[len(position)-1].strip()
            except:
                position = "Unknown"
            
            # Put them together in the desired csv format
            dataText = currAdd + ";" + birth + ";" + country + ";" + position + "\n"
            print(dataText)
            self.data = self.data + dataText

            # dataText = self.makeGPTQuery(dataPrompt+str(currAdd)).strip('\n')
            # dataText = dataText.strip()
            # print(dataText)

            # Now append string to data attribute
            # self.data = self.data + dataText + '\n'
            currList = currList[loopWeight:]
            sleep(15)
        return

    # Helper function to make openai queries
    def makeGPTQuery(self, currPrompt):
        try:
            query = openai.Completion.create(
                model="text-davinci-002",
                prompt= currPrompt,
                temperature=0.7,
                max_tokens=700,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            currResponse = query['choices'][0]['text']
            currResponse = currResponse.strip('\n')
            currResponse = currResponse.strip() 
            return currResponse

        except Exception as e:
            self.logger.error("Query could not be processed because: "+str(e))
            return ""
    
    def savePepCsv(self, path):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            # First extract each row of the data
            dataList = self.data.split("\n")
            # Now put each row as a list into the csv
            for item in dataList:
                writer.writerow(item.split(";"))
        return
    
