from needed_vars import path, repo_path
from pepOpenAi import PepOpenAi
import time

testUrl = "https://www.airforce.gov.au/about-us/"

def cleanse_test():
    test_pep = PepOpenAi()
    test_pep.getLongestNamesList(testUrl, iterations=3)
    test_pep.filterNames()
    print(test_pep.names)
    # test_pep.verifyNames()
    # test_pep.getNamesData()
    # test_pep.savePepCsv(path=f'{repo_path}/test.csv')
    return

if __name__ == "__main__":
    st = time.time()
    cleanse_test()
    et = time.time()
    print(f'Total Elapsed Time: {et-st}')