'''
Created on 5. 1. 2017

@author: ppavlu
'''

class specList:
    '''
    classdocs
    '''

    def distinctItemsNumber(self):
        # Returns number of distinct items included in the list, no change to the original list
        count=0
        l=self.origlist.copy()
        if l != []:
            while l != []:
                item = l[0]
                count=count+1
                while item in l:
                    l.pop(l.index(item))
        return count
    
    def distinctItemsList(self):
        # Returns number of distinct items included in the list, no change to the original list
        ulist=[]
        l=self.origlist.copy()
        if l != []:
            while l != []:
                item = l[0]
                ulist.append(item)
                while item in l:
                    l.pop(l.index(item))
        return ulist
    
    def cleanList(self, unwanted):
        # removes any item in unwanted list from the original list (modifies the list by removing any instance of the unwanted item from it)
        for item in unwanted:
            while item in self.origlist:
                self.origlist.pop(self.origlist.index(item))
            

    def __init__(self, origlist):
        '''
        Constructor
        '''
        self.origlist=origlist