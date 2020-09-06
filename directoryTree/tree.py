import os

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
        subs=os.listdir(path)
        #subs=os.walk(path)
        #subs= [f.path for f in os.scandir(path) if f.is_dir()]
        for sub in subs:
            if os.path.isdir(os.path.join(path, sub)):
                tempNode=Node(os.path.join(path, sub))
                self.children.append(tempNode)


def createDirectoryTree(rootNode, maxDepth=99999):
    if rootNode == None or maxDepth < 1:
        return None
    rootNode.findChildDirectories()
    for child in rootNode.children:
        createDirectoryTree(child, maxDepth - 1)

def printDirectoryTree(rootNode, maxDepth=99999, tabCount=1):
    if rootNode == None or maxDepth < 1:
        return None
    str="|    " * (tabCount-1)
    print("{}|----{}".format(str, rootNode.dirName))
    for child in rootNode.children:
        printDirectoryTree(child, maxDepth-1, tabCount+1)

rootDir="D:\\video_lecs_os"
rootNode=Node(rootDir)
createDirectoryTree(rootNode, maxDepth=30)
printDirectoryTree(rootNode)
