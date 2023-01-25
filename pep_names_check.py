from pepNamesCheck import PepNamesCheck
import time
from needed_vars import repo_path

url_list = ["https://www.airforce.gov.au/about-us/"]
# url_list = []

def makeNamesCheck():
    namesChecker = PepNamesCheck()
    namesChecker.makeUrlList(f'{repo_path}/pep_register.csv')
    # namesChecker.createNameAccuracy(url_list, 1)
    namesChecker.createNameAccuracy(namesChecker.urls, 1)
    namesChecker.inputNamesData()
    namesChecker.writeNameAccuracy(f'{repo_path}/names_accuracy.csv')
    return

if __name__ == "__main__":
    st = time.time()
    makeNamesCheck()
    et = time.time()
    print(f'Total Time Taken = {et-st}')