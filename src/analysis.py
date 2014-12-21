import nltk
import pickle
import random
import re

import scipy.stats as ss

from textblob import TextBlob, Word

# contains a list of all emails
#allMails = None

class DataLoading:
  @staticmethod
  def loadDataFromArchive():
    # Loads data from archives
    # XXX: currently only archive 3
    archiveName = "../archives/all_mails_archive"
    f = open(archiveName, 'r')
    mails = pickle.load(f)
    return mails

  @staticmethod
  def loadData():
    # filters data
    allMails = DataLoading.loadDataFromArchive()

    # XXX: No filtering for now
    res = allMails
    # filter by date

    # filter by language

    return res


class FrequencyAnalysis:
  def __init__(self, mails):
    self.mails = mails


class Mails:
    endlineSep = '\r\n'
    def __init__(self, _allMails):
        self.allMails = _allMails
        self.allMails_raw = _allMails
        
        self.cleanupEmails()
        
    
    def getRandomMail(self):
        return random.choice(self.allMails)
        
    def cleanupEmails(self):
        " Remove emails with None fields and filter bodies"
        
        # If some emails are drafts they may have None as rcpt
        rcptNotNone = lambda m: m['to'] is not None
        self.allMails = filter(rcptNotNone, self.allMails)
        
        self.allMails = map(Mails.removeQuotingFromBody, self.allMails)
        self.allMails = map(Mails.removeURLsFromBody, self.allMails)
        
        # filter emails sent to RTM
        self.allMails = [m for m in self.allMails if m['to'].find('RTM') == -1 ]
        
    def filterPersonalEmails(self):
        pMails = filter(Mails.isPersonal, self.allMails)
        return filter(lambda m: m['to'].find("Marco") == -1, pMails)

    @staticmethod    
    def isPersonal(m):
        
        # NOTE: only english recipients for now
        personalRecipients = ["annika", "kelly", "sofia", "ana",
                              "konst", "anoop", "floris", "nigel" ]
        recipientLowercase = m['to'].lower()
        found = any([recipientLowercase.find(r) != -1  
                        for r in personalRecipients])
        
        return found

    @staticmethod
    def removeQuotingFromBody(m):
        body = m['body']
        
        lines = body.split(Mails.endlineSep)
        notAQuoteLine = lambda l: l == '' or l[0] != '>'
        # remove quote lines
        onlyMyLines = filter(notAQuoteLine, lines)
        # remove lines of type "On  Thu, Nov 20, 2014 at 12:15 PM, xxx wrote:"
        notThatKindOfLine = lambda l: not re.search("^On.*20.*M.*", l)
        notThatKindOfLine_bis = lambda l: not re.search(".*@.*> wrote:", l)
        
        onlyMyLines = filter(notThatKindOfLine, onlyMyLines)
        onlyMyLines = filter(notThatKindOfLine_bis, onlyMyLines)
        # remove lines of type "2013/3/7 guy <guy@xxx>"
        notThatKindOfLine2 = lambda l: not re.search("^20..[/-].*[/-].*<.*@.*>", l)
        onlyMyLines = filter(notThatKindOfLine2, onlyMyLines)

        #remove =C2=A0= things in quotes
        notThatKindOfLine3 = lambda l: l.count('=') < 3
        onlyMyLines = filter(notThatKindOfLine3, onlyMyLines)
        
        m['body'] = Mails.endlineSep.join(onlyMyLines)
        return m
                
    @staticmethod
    def removeURLsFromBody(m):
        body = m['body']
        body = re.sub(r'\<http.+?\>', '', body, flags=re.S)
        body = re.sub(r'\http[^\s]+', '', body, flags=re.S)
        
        m['body'] = body
        return m
        
    @staticmethod
    def getAllBodiesFlat(ms):
        allBodies = [m['body'] for m in ms]
        allText = ' '.join(allBodies)
        #clean up odd characters
        allText = allText.decode("utf-8", "ignore")
        return allText
        
def personalMailsTB():
    allMails = DataLoading.loadDataFromArchive()
    mails = Mails(allMails)
    # filter personal mails
    pMails = mails.filterPersonalEmails()
    allText = Mails.getAllBodiesFlat(pMails)
    tb = TextBlob(allText)
    return tb

# computes English vocabulary
def computeVocabulary(tb):
    "return size of vocabulary in an email"
    
    wordSet = set([w.lower() for w in tb.words])
    
    #remove numbers
    noNumberInside = lambda w: not any([str(n) in w for n in range(0,10)])
    wordSet = filter(noNumberInside, wordSet)
    
    # break composed words
    # XXX: don't know how to do this yet
#    mkSplits = lambda w: [w1  in 
 #                           [ w.split('/'),
#                              w.split('-'),
#                              w.split('.')] ]
                              

#    splits = [mkSplits(s) ] 
   
    # TODO: spelling correction?
    
    # lemmatize words
    vocab = set([Word(w).lemmatize() for w in wordSet])
  
    # remove Italian words
    # XXX: too time consuming
    #vocab = filter([w for w in vocab 
    #                    if len(w) <= 2 or 
    #                        TextBlob(w).detect_language() != 'it' ])
    
    return vocab


def longestWord(vocab):
    #argmaxLen = lambda  w1, w2: 
    pass

    
def computeWeekdaysFreq(ms):
    for m in ms:
        m['wd'] = m['sent_at'].weekday()
    wdFreq = [0 for _ in range(7)]
    
    for m in ms:
        wdFreq[ m['wd'] ] += 1
    return wdFreq
    
def computeWeekdaysFreqBy(ms):
    sentInYear = lambda y: lambda m: m['sent_at'].year == y
    wdFreqByYear = {}
    for y in [2012, 2013, 2014]:
        ms_y = filter(sentInYear(y), ms)
        wdFreqByYear[y] = computeWeekdaysFreq(ms_y)
    return wdFreqByYear
    
def summary(listofdata):
    desc = ss.describe(listofdata)
    names = ["length", "min", "max", "mean", "stdev"]	
    desc = [desc[0], desc[1][0],desc[1][1], desc[2],desc[3]]
    for i in range(5):
        print "%s: %d" % (names[i], desc[i])
        
