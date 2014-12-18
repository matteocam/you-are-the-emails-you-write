#!/usr/bin/python

from gmail import Gmail
import pickle

class MailAnalytics:
  def __init__(self, loginFile = 'credentials.txt'):
    self.g = Gmail()
    self.loginFromCredentialsFile(loginFile)

  def loginFromCredentialsFile(self, loginFile = None):
    # XXX: currently file is not used
    try:
        # NOTE: your username andpassword here
        userName = None
        pwd = None 
      self.g.login(userName, pwd )
    except:
      print "Whoah! Not logged in"
  
  def getAllSentEmails(self):
      # Start date is 9 March 2007
  
      # 5. before=datetime.date(2013, 12, 20)
      # 6. before=datetime.date(2014, 5, 20),
      # 7. before=datetime.date(2014, 12, 15)
      
      # Your email here
      yourEmail = None
      mails = self.g.all_mail().mail(after=datetime.date(2014, 5, 20),
                         before=datetime.date(2014, 12, 15),
                         prefetch=True,
                         sender=yourEmail)
      return mails
      
  def email2dict(self, m):
      "Saves only some features of the emails as a dict"
      d = m.__dict__
      ret = {}
      savedFeatures = ['fr', 'to', 'subject', 'body', 'labels', 'sent_at', 'thread_id']
      for f in savedFeatures:
          ret[f] = d[f]
      return ret

  def dumpEmails(self, mails, fn = 'mail_archive'):
      f = open(fn, 'w')
      pickle.dump(mails, f)
  
  def retrieveSavedEmails(self, fn = 'mail_archive'):
      f = open(fn, 'r')
      mails = pickle.load(f)
      f.close()
      return mails
      
  def getAndDumpAllEmails(self, fn):
      mails = self.getAllSentEmails()
      print "Retrieved " + str(len(mails)) + " emails"
      mailsAsDicts = map(self.email2dict, mails)
      print "Converted to dicts"
      self.dumpEmails(mailsAsDicts, fn)
      print "Dumped.\nAll done."
            
 # Emails I sent
 #g.all_mail().mail(before=datetime.date(2014, 12, 9), after=datetime.date(2014, 10, 9), prefetch=True, attachment=True, sender="matteo.campanelli@gmail.com")

def mergeArchivesInOne():
    ma = MailAnalytics()
    nArchives = 7
    mail_archives = []
    for i in range(1,nArchives+1):
        filename = "mail_archive" + str(i)
        mails = ma.retrieveSavedEmails(filename)
        mail_archives.append(mails)
    all_mails = [m for ma in mail_archives for m in ma]
    print "Saving " + str(len(all_mails)) + " mails"
    f = open("all_mails_archive", 'w')
    pickle.dump(all_mails, f)
    
def loadAllMails():
    f = open("all_mails_archive", 'r')
    mails = pickle.load(f)
    f.close()
    return mails
    
    
 
