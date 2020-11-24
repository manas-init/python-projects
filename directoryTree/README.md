# Printing Directory Tree
This is a python project to print the directory structure of a machine in tree format. This can help us in visualizing the directory structure without having to scan the entire machine manually. The script is operating system independent.
<br><br>
## Getting started
This prints the directory structure using colour codes pretty much same as linux:<br>
- *Blue :* folder
- *Red :* zipped files
- *Green :* executable files
- *White :* files<br>
After every folder or file name their is size of that folder/file mentioned in human readable format inside parenthesis<br>
The folder size is calculated by counting the size of sub-folders and files.
<br><br>
## Prerequisistes
- Python 3.7.9
<br><br>
## Installing prerequisites
- *Python 3.7.9 :* Download python exe from https://www.python.org/downloads/windows/(download exe by checking python version and os).	Execute the exe file to install python
<br><br>
## Parameters to script
Call the python script with combination of following arguments <br>
`python tree.py [-h] -d PATH [-m MAXDEPTH] [--only-dir ONLYDIR] [-e EXTENSIONS] [-s SEARCH]`<br>

`-d | --dir <path of base directory>` required. The path from which the to explore the directory structure<br>
`-m | --max-depth <max-depth>` optional, default=999. The max-depth upto which we need to search from base-directory<br>
`--only-dir true/false`  optional, default=False. It tells whether to print only directories or print both directories and files in the output<br>
`-e | --extensions <extensions>` optional. It tells whether to print files of any particular extension<br>
`-s | --search <file-name>` optional. Prints the given filename in yellow colour if the file is found, no other file is printed<br>
`--no-colour true/false` optional, default=False. It prints the output in white colour only<br>
`-h | --help` optional. It prints the list of arguments that script accepts and their usage.
<br><br>
## Licence
Not licensed yet :see_no_evil:
<br><br>
## Authors
- manas https://github.com/manas-init :innocent:
