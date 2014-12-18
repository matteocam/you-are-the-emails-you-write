import nltk
import pickle
import random
import re

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

def main():
    global allMails
    allMails = DataLoading.loadDataFromArchive()
    

class Mails:
    endlineSep = '\r\n'
    def __init__(self, _allMails):
        self.allMails = _allMails
        self.allMails_raw = allMails
        
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
        
    def filterPersonalEmails(self):
        return filter(Mails.isPersonal, self.allMails)

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
        m['body'] = Mails.endlineSep.join(onlyMyLines)
        return m
                
    @staticmethod
    def removeURLsFromBody(m):
        body = m['body']
        m['body'] = re.sub(r'\<http.+?\>', '', body, flags=re.S)
        return m
        
