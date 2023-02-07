from pepNamesCheck import PepNamesCheck
import time
from needed_vars import repo_path
import pandas as pd

dfUrls = pd.read_csv(f'{repo_path}/pep_register.csv')

url_list = [
    "https://www.airforce.gov.au/about-us/",
    "https://www.dfat.gov.au/about-us/our-people/homs/australian-ambassadors-and-other-representatives",
    "https://japan.kantei.go.jp/100_kishida/meibo/sourihosakan/index_e.html",
    "https://www.mofa.go.jp/about/hq/list2.html",
    "https://overseas.mofa.go.kr/au-en/wpge/m_3301/contents.do",
    "https://korea.assembly.go.kr:447/cha/spro.jsp",
    "http://english.www.gov.cn/statecouncil/",
    "https://www.fmprc.gov.cn/mfa_eng/ziliao_665539/wjrw_665549/3607_665555/",
    "https://www.rbnz.govt.nz/about-us/our-people/our-leadership-team",
    "https://www.mfat.govt.nz/en/about-us/our-people/our-heads-of-mission/",
    "https://au.int/en/high-representatives",
    "https://www.badea.org/board-of-governor.htm",
    "https://iccwbo.org/about-us/governance/executive-board/"
    ]

# Use this to filter the countries present in the csv
url_list = list(dfUrls[dfUrls['country'] == 'International']['actual list url'])
url_list = [item for item in url_list if item == item]
print(url_list)

# Just runs all the functions made in the PepOpenAi and PepNamesCheck classes
def makeNamesCheck():
    namesChecker = PepNamesCheck()
    # namesChecker.makeUrlList(f'{repo_path}/pep_register.csv')
    # namesChecker.createNameAccuracy(namesChecker.urls, 1)
    namesChecker.createNameAccuracy(url_list, 1)
    # namesChecker.changeWords()
    namesChecker.inputNamesData()
    namesChecker.writeNameAccuracy(f'{repo_path}/names_accuracy.csv')
    print(f'Names Length: {len(namesChecker.namesData)-1}')
    namesChecker.showURLSPresent(f'{repo_path}/names_accuracy.csv')
    # Show results of getting words
    # namesChecker.namesGen.makeWordFreq()
    # namesChecker.namesGen.showWordFreq()
    # namesChecker.namesGen.showWordFreq()
    print(set(list(dfUrls['country'])))
    return

if __name__ == "__main__":
    st = time.time()
    makeNamesCheck()
    et = time.time()
    print(f'Total Time Taken = {et-st}')