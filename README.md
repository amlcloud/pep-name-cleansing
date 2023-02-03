# pep-name-cleansing
Extract only the full names (First, Last) of Politically Exposed Persons (PEPs)

## Table of contents
*[Approach] (#approach)
* [Packages](#packages)
* [Setup](#setup)

## Approach
1) Run string through the dictionary to filter out words that are guaranteed to not match names (Mr. Mrs., Hon., etc.)
2) If 2 words, run through names dataset. IF good -> keep name, IF not -> requires manual check
3) If >2 words, get Chat GPT to filter words, then run through names dataset. IF good -> keep name, IF not -> requires manual check
	
## Technologies
Project is created with: 
* OpenAI version: 0.26.1
* country_list version: 1.0.0
	
## Setup
To setup this project, install the files in the txt files using npm/cmd:

```
$ pip install -r requirements.txt
```

Create a python file in the repository called needed_vars.py and write it as such:
![image](https://user-images.githubusercontent.com/101044075/215335146-00aebd92-8f9e-4aa3-9ac0-9a80e025b655.png)

To run the project, run the pepTest.py file. All the data will be stored in the test.csv file.
