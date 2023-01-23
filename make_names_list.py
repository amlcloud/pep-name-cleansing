from names_dataset import NameDataset
from needed_vars import repo_path

def create_names_txt():
    nd = NameDataset()
    names = []
    codes = [item.alpha_2 for item in nd.get_country_codes()]

    # First extract all the names and put it in the list
    for country_code in codes:
        male_first = nd.get_top_names(1000000, True, country_code)[country_code]['M']
        female_first = nd.get_top_names(1000000, True, country_code)[country_code]['F']
        last = nd.get_top_names(1000000, False, country_code)[country_code]

        for name in male_first:
            names.append(name)
        for name in female_first:
            names.append(name)
        for name in last:
            names.append(name)
    
    # Then join all the names together and write it in a string
    with open(f'{repo_path}/names_list.txt'):
