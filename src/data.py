# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 19:55:07 2014

@author: Matteo Campanelli
"""

import pickle

pMailsPerWeek = [273, 275, 288, 267, 232, 196, 160]
pMailsTotal = sum(pMailsPerWeek) # 1691

pMailsPerWeekByYear = {2012: [57, 65, 73, 63, 63, 47, 34],
                       2013: [127, 148, 121, 111, 103, 83, 80],
                       2014: [86, 58, 89, 90, 63, 60, 46] }

def normalize(l):
    return [float(x)/sum(l) for x in l ]

def getNormalizedWeekData():
    return normalize(pMailsPerWeek)

def getEmailsLensSizeVocab():
    f = open('mails_dump', 'r')
    mails = pickle.load(f)
    f.close()
    pMails = mails.pMails
    wkMails = mails.wkMails
    
    ret = { 'pMails' : {}, 'wkMails' : {} }

    ret['pMails']['lens'] = [ (m['len']/20)*20 for m in pMails ] # put a new bin every 20 units
    ret['pMails']['vsizes'] = [ m['size_vocab'] for m in pMails ]
    
    ret['wkMails']['lens'] = [ (m['len']/20)*20 for m in wkMails ] # put a new bin every 20 units
    ret['wkMails']['vsizes'] = [ m['size_vocab'] for m in wkMails ]
    
    return ret
    
def howManyMailsWithLengthBelowN(ms, N):
    belowN = lambda m: m['len'] <= N
    filteredMails = filter(belowN, ms) 
    
    return len(filteredMails)/float(len(ms))
    
def propertyByRecipient(ms, funOnMsg):
    "Returns a dictionary with how many mails I've written per person"
    rcpts = Mails.personalRecipients
    freq = {  r : {"abs" : 0, "rel" : 0 } for r in rcpts } 
    for m in ms:
        rcptLowercase  = m['to'].lower()
        # find right recipient.
        # If members of rcpts are "mutually exclusive" and 
        # we are dealing with the set of personal mails
        # a right recipient will be found
        for r in rcpts:
            if rcptLowercase.find(r) != -1:
                break
        freq[r]["abs"] += funOnMsg(m)
        
    total = sum([funOnMsg(m) for m in ms])
    for r in rcpts:
        freq[r]["rel"] = freq[r]["abs"]/float(total)
    return freq
    
def densityOfRecipients(ms):
    return propertyByRecipient(ms, lambda _: 1)
    
def printPropertyOfRecipients(ms, fun):
    d = fun(ms)    
    for r in d.keys():
        print "%s\t%d\t%f" % (r, d[r]["abs"], d[r]["rel"]*100)
        
def lengthDensityOfRecipients(ms):
    """ Compute absolute and average """
    return propertyByRecipient(ms, lambda m: m["len"])

# Old Version    
def __getPMailsLensSizeVocab():
    f = open('pMails_lens', 'r')
    pMails = pickle.load(f)
    f.close()
    lens = [ (m['len']/20)*20 for m in pMails ] # put a new bin every 20 units
    vsizes = [ m['size_vocab'] for m in pMails ]
    return lens, vsizes
    
