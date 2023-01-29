from pepNamesCheck import PepNamesCheck
import time
from needed_vars import repo_path

url_list = ["https://www.airforce.gov.au/about-us/"]
# url_list = []

# Just runs all the functions made in the PepOpenAi and PepNamesCheck classes
def makeNamesCheck():
    namesChecker = PepNamesCheck()
    namesChecker.makeUrlList(f'{repo_path}/pep_register.csv')
    namesChecker.createNameAccuracy(namesChecker.urls, 1)
    # namesChecker.createNameAccuracy(url_list, 1)
    # namesChecker.changeWords()
    namesChecker.inputNamesData()
    namesChecker.writeNameAccuracy(f'{repo_path}/names_accuracy.csv')
    print(f'Names Length: {len(namesChecker.namesData)-1}')
    namesChecker.showURLSPresent(f'{repo_path}/names_accuracy.csv')
    # Show results of getting words
    namesChecker.namesGen.makeWordFreq()
    namesChecker.namesGen.showWordFreq()
    return

if __name__ == "__main__":
    st = time.time()
    makeNamesCheck()
    et = time.time()
    print(f'Total Time Taken = {et-st}')