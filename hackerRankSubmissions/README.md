# Downloading hacker rank submissions
This is a python project to download all the accepted submissions by a user on hacker rank. It was created to that people can save all their accepted solutions locally in order to better track their progress or keep them as reference.
<br><br>
## Getting started
This script will create the a folder named "submissions" inside the script directory.<br>
According to the category of question new folders will be created inside submission folder. Ex: submissions/Practice/Algorithms/Dynamic Programming/Stock Maximize.cpp<br>
All the accepted solutions will be saved into respective folder.<br><br>
## Prerequisistes
- Python 3.7.9
- Python sub-dependencies
  - requests
  - BeautifulSoup
  - selenium
- Chrome Driver
<br><br>
## Installing prerequisites
- *Python 3.7.9 :* Download python exe from https://www.python.org/downloads/windows/(download exe by checking python version and os).	Execute the exe file to install python
- *requests :* python -m pip install requests (https://pypi.org/project/requests/)
- *BeautifulSoup :* pip install beautifulsoup4 (https://pypi.org/project/beautifulsoup4/)
- *selenium :* pip install selenium (https://pypi.org/project/selenium/)
- *Chrome Driver :* 
  - Open google chrome
  - goto menu -> help -> About Google Chrome
  - check chrome version
  - Download chrome driver for same version using link https://chromedriver.chromium.org/downloads
<br><br>
## Output of script
For each accepted solution
<br>*Sample output*<br>
```
Starting : https://www.hackerrank.com/challenges/stockmax/submissions/code/183693820
navigated to submissions page
File present : submissions/Practice/Algorithms/Dynamic Programming/Stock Maximize.cpp
Ended : https://www.hackerrank.com/challenges/stockmax/submissions/code/183693820
  ```
 <br>*Understanding the output*<br>
  `Starting : <url/>`  -> url to submitted code <to mark the start submission parsing and file creation><br>
	`navigated to submissions page` -> tells whether above url was opened successfully or not<br>
	`File present : <file-path>` -> file path relative to script location <"File present" is code is already downloaded before so skipping scrapping of code, "File created" is code downloaded during this execution><br>
	`Ended : <url>` -> url to submitted code <to mark the submission parsing and file creation is complete> <br>
<br><br>
## Licence
Not licensed yet :see_no_evil:
<br><br>
## Authors
- manas https://github.com/manas-init :innocent:
