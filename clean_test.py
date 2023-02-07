from pepNamesCheck import PepNamesCheck
from pepOpenAi import PepOpenAi
import pandas as pd
import time
import json
from needed_vars import repo_path

test_names = [
    # 'Olaf Scholz', 
    # 'Annegret Kramp-Karrenbauer',
    # 'HE Mr Andrew Parker',
    # 'HE Mr Phillip Ellis',
    # 'HE Mr Paul Grigson',
    'The Honourable Bardish Chagger',
    'Deborahrumsey'
    ]

def main():
    testCheck = PepNamesCheck()
    namesDf = pd.read_csv(f'{repo_path}/names_accuracy.csv')
    # namesList = list(namesDf['Name'])
    namesList = test_names
    jsonArray = []
    for name in namesList:
        print(f'Current Name: {name}')
        cleansed = testCheck.namesCleanse(name)
        jsonArray.append({
            'In': name,
            'Out': cleansed
        })
        print(f'Old Name: {name} ; New Name: {cleansed}')
        print()
        time.sleep(1)
    
    # Save as JSON file
    with open(f'{repo_path}/names_json_test.json', 'w') as fp:
        json.dump(jsonArray, fp)
    return

if __name__ == '__main__':
    st = time.time()
    main()
    et = time.time()
    print(f'Time Taken: {et-st}')