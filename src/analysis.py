import nltk
import pickle
import random
import re

import scipy.stats as ss

from textblob import TextBlob, Word
from langdetect import detect

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
    personalRecipients = ["annika", "syyskuura", "kelly", "sofia", "ana",
                              "konst", "anoop", "floris", "nigel" ]
    @staticmethod
    def loadFromFile():
        f = open('mails_dump', 'r')
        mails = pickle.load(f)
        return mails
    def __init__(self, _allMails):
        self.allMails = _allMails
        self.allMails_raw = _allMails
        
        self.cleanupEmails()
        
        self.pMails = None
        self.wkMails = None
        
    
    def getRandomMail(self):
        return random.choice(self.allMails)
        
    def classifyEmails(self):
        "Classifies in personal and work emails"
        pMails = self.filterPersonalEmails()
        wkMails = self.filterWorkEmails()
        
        computLenghtAndSizeVocab(pMails)
        computLenghtAndSizeVocab(wkMails)
        
        self.pMails = pMails
        self.wkMails = wkMails
        return self.pMails, self.wkMails
        
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
        
    def filterWorkEmails(self):
        engMails = filter(lambda m: detectEmailLanguage(m) == "en",
                          self.allMails)
        wkMails = filter(lambda m: not Mails.isPersonal(m), engMails)
        wkMails = filter(lambda m: 'Call' not in m['labels'] , wkMails)
        return wkMails

    @staticmethod    
    def isPersonal(m):
        
        # NOTE: only english recipients for now
        recipientLowercase = m['to'].lower()
        found = any([recipientLowercase.find(r) != -1  
                        for r in Mails.personalRecipients])
        
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
    
def gimmeMails():
    allMails = DataLoading.loadDataFromArchive()
    mails = Mails(allMails)
    return mails

# computes English vocabulary
def computeVocabulary(tb):
    "return vocabulary in an email"
    
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

def computLenghtAndSizeVocab(ms):
    lens = getBodyLengths(ms)
    # XXX: Kinda too much code duplication around this
    tbs = mails2TBs(ms)
    vocabs = [computeVocabulary(tb) for tb in tbs]
    for i, m in enumerate(ms):
        m['len'] = lens[i]
        m['size_vocab'] = len(vocabs[i])
    
def summary(listofdata):
    desc = ss.describe(listofdata)
    names = ["length", "min", "max", "mean", "stdev"]	
    desc = [desc[0], desc[1][0],desc[1][1], desc[2],desc[3]]
    for i in range(5):
        print "%s: %d" % (names[i], desc[i])
        
def mails2TBs(ms):
    "Convert the emails' bodies into a list of TextBlob-s"
    bodies = [m['body'].decode("utf-8", "ignore") for m in ms]
    tbs = [TextBlob(b) for b in bodies]
    return tbs

# NOTE: length in number of words    
def getBodyLengths(ms):
    tbs = mails2TBs(ms)
    return [len(tb.words) for tb in tbs]
    
def detectEmailLanguage(m):
    b = m['body'].decode("utf-8", "ignore")
    s = m['subject']
    try:
        return detect(b)
    except:
        try:
            return detect(s)
        except:
            return "en"
            
