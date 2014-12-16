import nltk
import pickle

class DataLoading:
  @staticmethod
  def loadDataFromArchive():
    # Loads data from archives
    # XXX: currently only archive 3
    f = open("mail_archive3", 'r')
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




