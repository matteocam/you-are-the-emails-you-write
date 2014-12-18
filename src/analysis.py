import nltk
import pickle
import random

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
    def __init__(self, _allMails):
        self.allMails = _allMails
    
    def getRandomMail(self):
        return random.choice(self.allMails)
        
    def filterPersonalEmails(self):
        pass



