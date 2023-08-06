"""
Jens Jørgen Mortensen <smoerhul> = JJM(smoerhul)
from, to(s), time, size, attachments?, title, summary, replied?, forwarded?
"""
import imaplib
import os.path as op
from email.header import decode_header

from spelltinkle.color import NoColor
from spelltinkle.config import configure
from spelltinkle.document import Document
from spelltinkle.i18n import _
from spelltinkle.input import Input
from spelltinkle.text import TextDocument
from spelltinkle.utils import f
            

def read_password(host):
    with open(op.expanduser('~/.spelltinkle/secrets.py')) as fd:
        dct = {}
        exec(fd.read(), dct)
    return dct['secrets'][host]
    
    
class MailDocument(Document):
    def __init__(self):
        Document.__init__(self)
        self.color = NoColor()
        config = configure().mail[0]
        host = config['host']
        M = self.connection = imaplib.IMAP4_SSL(host)
        self.connection.login(config['user'], read_password(host))
        #a, b = self.connection.list('INBOX')
        a, b = self.connection.list()
        print(a)
        for c in b[:4]:
            d, e = c.decode().split(')')
            assert d[0] == '('
            flags = d[1:].split()
            f, g = e.strip().split(' ', 1)
            assert f == '"/"'
            print('{:20} {}'.format(g, flags))
        print(M.select())
        a, b = M.fetch('8', '(UID BODY[HEADER])')
        print(a)
        from email.parser import HeaderParser
        p = HeaderParser()
        for x in b:
            print('--------')
            print(len(x))
            print('..........')
            if len(x) == 2:
                print(x[0])
                m = p.parsestr(x[1].decode())
                print(m['Subject'])
                print(m['Content-Type'])
            else:
                print(x)
        M.close()
        M.logout()
        
    def set_session(self, session):
        Document.set_session(self, session)
        #self.list()
        self.changes = 42
        
    def list(self):
        self.color.colors = colors = []
            
        self.change(0, 0, len(self.lines) - 1, 0, lines2)
        self.view.move(0, 0)

    def enter(self):
        for i, doc in enumerate(self.session.docs):
            if doc.filename == self.conf.calender_file:
                self.session.docs.append(self.session.docs.pop(i))
                return
        doc = TextDocument()
        doc.read(self.conf.calender_file, self.session.read())
        return doc
        

def check_mail():
    newdone = set()
    for c in b:
        if isinstance(c, tuple):
            txt = ''.join(s if isinstance(s, str) else s.decode(e or 'ascii')
                          for s, e in decode_header(c[1].decode()))
            txt = txt.strip().split('Subject:', 1)[1].strip()
            if txt.startswith('Cal: '):
                txt = txt[5:]
                if txt not in done:
                    event = str2event(txt, datetime.datetime.now())
                    c = Calender()
                    c.read(repeat=False)
                    c.events.append(event)
                    c.write()
                newdone.add(txt)
    if newdone != done:
        with open('/home/jensj/.spelltinkle/calender-email-seen.txt',
                  'w') as fd:
            for line in newdone:
                print(line, file=fd)
            

    
def mail(event):
    import smtplib
    from email.mime.text import MIMEText
    subject = '{}: {}'.format(event.start, event.text)
    msg = MIMEText('bla')
    msg['Subject'] = subject
    to = 'jensj@fysik.dtu.dk'
    msg['From'] = to
    msg['To'] = to
    s = smtplib.SMTP('mail.fysik.dtu.dk')
    s.sendmail(msg['From'], [to], msg.as_string())
    s.quit()
