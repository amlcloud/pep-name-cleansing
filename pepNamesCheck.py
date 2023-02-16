from pepOpenAi import PepOpenAi
from needed_vars import repo_path, path
import logging
import csv
import pandas as pd
from replace_dict import word_ref
import re
from time import sleep
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By

# NAME FIX: Take one name
# BATCH FIX: Supply list of names (csv)/array -> csv file/array, String -> String, array of json objects -> array of json objects
# JSON object : { in, out }

class PepNamesCheck(PepOpenAi):
    def __init__(self):
        PepOpenAi.__init__(self)
        # self.namesGen = PepOpenAi()
        # CSV Format of the Names Data, including the link they were taken from
        # self.namesData = ["Name;Chosen Name;OpenAi Possible Names;URL"]
        # self.namesData = ["Name;Chosen Name;OpenAi Possible Names;URL;GPT Chosen Name"]
        self.namesData = ['Name;Chosen Name;URL']
        self.logger = logging.getLogger('ftpuploader')
        self.urls = []
        self.scrapeDict = {}
        # Extract all the possible names included in the repository
        with open(f'{repo_path}/names_list.txt', encoding='utf-8') as fp:
            self.possibleNames = fp.readlines()[0].split(";")
        return
    
    def getNamesWebScrape(self, url):
        webQuery_1 = 'Please list the names of the people from this text: '
        webQuery_2 = 'Please list the names of Politically Exposed Persons (PEPs) from this text: '
        namePrompt = 'Check if the following string is a name and answer in Yes/No: '
        # csv_query = "Create a CSV of the given names (without their position) of Politically Exposed Persons (PEPs) in this URL in the format Index, Name: "
        csv_query = "Create a CSV of the names in this URL in the format Index, Name: "
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'ul']
        # tags = ['p']
        text = []
        namesList = []
        
        # First extract the text from the website
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            for sym in tags:
                # print(f'Curr Tag {sym}')
                currSym = driver.find_elements(By.TAG_NAME, sym)
                for element in currSym:
                    # text = text+ element.text.strip('\n ') + '\n'
                    # print(element.get_attribute("textContent").strip('\n ') )
                    text.append(element.get_attribute("textContent").strip('\n \t'))
            driver.close()
        # When you can't even extract from the website
        # just return nothing
        except Exception as e:
            self.logger.error(repr(e))
            return text
        
        # NOTE: Trying to check if we can filter names out using GPT
        for item in text:
            # Use GPT to check if the string is a name
            item = re.sub(r'\n+|\t+', '',item)
            try:
                print(f'Current Item: {item}')
                answer = self.makeGPTQuery('Check if the following string is a name and answer in Yes/No: '+item)
                answer = re.findall(r'Yes|yes|No|no', answer)[0]
                print(f'Answer: {answer}')
                if answer.lower() == 'yes':
                    namesList.append(item)
                self.scrapeDict[item] = answer.lower()
            except Exception as e:
                print(repr(e))
                self.scrapeDict[item] = 'error'
            sleep(2)
        
        with open(f'{repo_path}/scrape_test.csv', 'w', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['Name', 'Response'])
            for key in self.scrapeDict:
                writer.writerow([key, self.scrapeDict[key]])

        
        # print(text)

        # Then check if you can get the names
        # if text != '':
            # return self.makeGPTQuery(csv_query+'\n'+text)
            # return self.makeGPTQuery(webQuery_1+'\n'+text)
        return namesList

    # All this really does is call the name extraction function
    # from the PepOpenAi class
    def createNameAccuracy(self, urlList, numTimes):
        self.getUrlNames(urlList=urlList, iterations=numTimes)
        return
    
    # Helper Functions
    def inputNamesData(self):
        newNames = []
        print(self.urlDict)        
        for name in self.names:

            # Change the name immediately
            # changedName = self.changeWords(name)
            print(f'Mapped URL: {self.urlDict[name]}')
            # First just insert the name into the database
            cleansedName = self.namesCleanse(name)
            
            # Here we also test out if chatGPT can just clean the name for us
            # try:
            #    gptName = self.GPTchangeWords(name)
            # except Exception as e:
            #    self.logger.error(f'Failed to get GPT name because of {repr(e)}')

            # In this case, try the same thing for the URL
            try:
                addData = f'{name};{cleansedName};{self.urlDict[name]}'
            except Exception as e:
                self.logger.error(f'Failed to find the url of {name} due to: {repr(e)}')
                addData = f'{name};{cleansedName};Link not found'

            # Record what you added and append it to the new list 
            print(f'Added Name Data: {addData}')
            self.namesData.append(addData)
            newNames.append(cleansedName)

            # To prevent rate limit from reaching
            # ONLY APPLIES FOR GETTING NAMES USING GPT
            sleep(3)
        
        # Remove duplicates in the list of names present,
        # NOTE: This name generator does not assume names can be from different countries,
        # since ChatGPT may not know how to differentiate between PEPs with the same name
        self.names = list(set(newNames))
        # self.names = list(set(self.names))
        return
    
    # Function that puts together all the name cleaning functins together
    def namesCleanse(self, name):
        try:
            # First use the wordref dictionary to filter
            # words that would not be part of a name (Mr., Hon., Mrs., etc.)
            refName = self.changeWords(name)
            print(f'Without Titles: {refName}')

            # IF the name is at most 2 words, just run through
            # names dataset to filter the words
            if len(refName.split()) <= 2:
                print("Using Names Dataset")
                ndName = self.ndChangeWords(refName)
                return ndName
            
            # If it is still longer than 2 words, use GPT to
            # filter out the words more then run through names dataset
            else:
                print("Using GPT to filter words")
                gptName = self.GPTchangeWords(refName)
                if len(gptName.split()) > 2:
                    print("Using Names Dataset to Change the Name")
                    gptName = self.ndChangeWords(gptName)
                return gptName
        
        except:
            return name
    
    # Helper unction to use the names dataset
    # to filter out the word
    def ndChangeWords(self, name):
        # Local function just to match last names
        def makeLastName(index, possible_name, text):
            try:
                currLast = text.split()[index+1]
                if currLast in self.possibleNames:
                    # print("Testing: "+possible_name+' '+currLast)
                    # print("In last name: "+str(currLast in self.possibleNames))
                    # print("In first name: "+str(currLast in self.possibleNames))
                    return f'{possible_name} {currLast}'
            except:
                return None
            return None
        
        allNames = []
        currName = None

        # Loop through each word and check if word
        # and next word form a first name last name
        for i in range(len(name.split())):
            poss_name = name.split()[i]
            if poss_name in self.possibleNames:
                # print("Currently Testing this Name: "+poss_name)
                currName = makeLastName(i, poss_name, name)
            if currName != None:
                # print("Appending this name: "+currName)
                allNames.append(currName)
        
        # Then return the latest occurrence of a name match
        print(f'Current allNames: {allNames}')
        if allNames:
            return allNames[len(allNames)-1]
        else:
            return name

    
    # Function to help filter out filler words in name
    def changeWords(self, name):
        for key in word_ref:
            if re.search(key, name):
                name = re.sub(key, word_ref[key], name)
        return name
    
    # GPT cleanses data
    # NOTE: Trying to extract instead the first names and last names separately
    def GPTchangeWords(self, name):
        # In this case, we give chat GPT a string
        # and ask it to only give the first name and last name
        firstPrompt = f'Give only the first name in the format [First Name] of this string: {name}'
        secondPrompt = f'Give only last name in the format [Last Name] of this string: {name}'
        firstName = ""
        lastName = ""
        
        # Extract the first name
        while firstName == "":
            firstName = self.makeGPTQuery(firstPrompt)
            # print(f'Current Name: {cleaned}')
            firstName = re.sub('\n', ' ', firstName)
            firstName = re.sub(' ', '', firstName)
            sleep(1.5)
        
        # Extract the last name
        while lastName == "":
            lastName = self.makeGPTQuery(secondPrompt)
            lastName = re.sub('\n', '', lastName)
            lastName = re.sub(' ', '', lastName)
            sleep(1.5)

        returnName = f'{firstName} {lastName}'
        returnName = re.sub(r'[^a-zA-Z\s-]', '', returnName)
        return returnName
    
    # Writes into a file the data added in the
    # namesData attribute of this class
    def writeNameAccuracy(self, path):
        with open(path, 'w', encoding='utf-8', newline='') as fp:
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
    
    # Helper Functions to get Data from the Cleaned Names CSV

    def getCsvDf(self, names_path):
        df = pd.read_csv(names_path)
        return df

    def getNamesRetained(self, names_path):
        df = self.getCsvDf(names_path=names_path)
        namesList = list(df['Name'])
        cleanseList = list(df['Chosen Name'])
        num = 0

        for i in range(len(namesList)):
            name = namesList[i]
            cleanse = cleanseList[i]

            if name == cleanse:
                # print("Name: "+name)
                num = num + 1
        
        # print(f'Total Number of Names: {len(namesList)}')
        # print(f'Names Kept: {num}')
        # print(f'Percent Kept: {num/len(namesList)}.2f')

        return df[df['Name'] == df['Chosen Name']]