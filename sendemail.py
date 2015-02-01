#-*-coding:utf-8-*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib


def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr(( \
	Header(name, 'utf-8').encode(), \
	addr.encode('utf-8') if isinstance(addr, unicode) else addr))
	
	
from_addr = raw_input('From: ')
password = raw_input('Password: ')
smtp_server = raw_input('SMTP server: ')
to_addr = raw_input('To: ')

msg = MIMEMultipart('alternative')
msg['From'] = _format_addr(u'Python coder <%s>' % from_addr)
msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
msg['Subject'] = Header(u'来自SMTP(Python)的测试。。。', 'utf-8').encode()

msg.attach(MIMEText('hello', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +'<p><img src="cid:0"></p>'
'<p>send by <a href="http://www.python.org">Python</a>...</p>' +
'</body></html>', 'html', 'utf-8'))
with open('/users/xiao/test.jpg','rb') as f:
	mime = MIMEBase('image', 'jpg', filename='test.jpg')
	mime.add_header('Content-Disposition', 'attachment', filename='test.jpg')
	mime.add_header('Content-ID', '<0>')
	mime.add_header('X-Attachment-ID', '0')
	mime.set_payload(f.read())
	encoders.encode_base64(mime)
	msg.attach(mime)

server = smtplib.SMTP(smtp_server,25)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
