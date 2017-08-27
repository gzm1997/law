from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import random, string
from law import setting

def _format_addr(s):
    name, email_addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), email_addr))

def send_email(smtp_server, from_email, from_email_psd, to_email, subject, content, type_message):
	email_client = smtplib.SMTP(smtp_server)
	email_client.login(from_email, from_email_psd)

	message = MIMEText(content, type_message, "utf-8")
	message["subject"] = Header(subject)
	message["from"] = _format_addr('gzm <%s>' % from_email)
	message["to"] = _format_addr('注册用户 <%s>' % to_email)

	email_client.sendmail(from_email, [to_email], message.as_string())
	email_client.quit()


def send_vertify_email(signup_user_email):
	length = 16
	vertifycode = ''.join([random.choice(string.ascii_letters) for i in range(length)])
	send_email(setting.SMTP_SERVER, setting.SMTP_EMAIL, setting.SMTP_PASSWORD, signup_user_email, "gzm注册验证", 
		'<html>' +
		'<body>' + 
		'<a href=' + 
		'http://' + setting.IP_ADDRESS + '/vertify?vertifycode=' + vertifycode + 
		'>' + 
		'点击此处验证你的账户' + 
		'</a>'
		'</body>' + 
		'</html>', "html")
	return vertifycode

if __name__ == "__main__":
	print(send_vertify_email("1617899539@qq.com"))