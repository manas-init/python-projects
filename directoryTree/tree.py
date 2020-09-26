import os


# Python program to print 
# colored text and background 
class colors: 

    from platform import system
    if "win" in system().lower(): #works for Win7, 8, 10 ...
        from ctypes import windll
        k=windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11),7)
    
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


class Node:
    def __init__(self, baseDir):
        baseDir=os.path.split(baseDir)
        if len(baseDir) == 1:
            baseName=baseDir[0]
        else:
            baseName=baseDir[1]
        baseLoc=baseDir[0]
        self.dirName=baseName
        self.dirLoc=baseLoc
        self.children=[]

    def findChildDirectories(self):
        path=os.path.join(self.dirLoc, self.dirName)
        if not os.path.isdir(path):
            return
        subs=os.listdir(path)
        for sub in subs:
            tempNode=Node(os.path.join(path, sub))
            self.children.append(tempNode)


def createDirectoryTree(rootNode, maxDepth=99999):
    if rootNode == None or maxDepth < 1:
        return None
    rootNode.findChildDirectories()
    for child in rootNode.children:
        if os.path.isdir(os.path.join(rootNode.dirLoc, rootNode.dirName)):
            createDirectoryTree(child, maxDepth - 1)

def printDirectoryTree(rootNode, maxDepth=99999, tabCount=1):
    if rootNode == None or maxDepth < 1:
        return None
    str="|    " * (tabCount-1)
    fullPath=os.path.join(rootNode.dirLoc, rootNode.dirName)
    if os.path.isdir(fullPath):
        print("{}|----{}{}{}".format(str, colors.fg.blue, rootNode.dirName, colors.fg.lightgrey))
    else:
        extension=fullPath.split(".", -1)[-1]
        executables=["exe", "sh", "py", "cpp"]
        if extension in executables:
        #if os.access(fullPath, os.X_OK):
            print("{}|----{}{}{}".format(str, colors.fg.green, rootNode.dirName, colors.fg.lightgrey))
        else:
            print("{}|----{}{}{}".format(str, colors.fg.lightgrey, rootNode.dirName, colors.fg.lightgrey))
    for child in rootNode.children:
        printDirectoryTree(child, maxDepth-1, tabCount+1)

rootDir="D:\\video_lecs_os"
#rootDir="C:\Users\USER\Downloads"
rootNode=Node(rootDir)
createDirectoryTree(rootNode, maxDepth=5)
printDirectoryTree(rootNode)
