import re
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from multiprocessing.dummy import Pool as ThreadPool

from premailer import Premailer
import ujson


class Parser:
    _servers = {
        'gmail': {'host': 'smtp.gmail.com', 'port': '587'},
        'mailru': {'host': 'smtp.mail.ru', 'port': '465'},
        'yandex': {'host': 'smtp.yandex.ua', 'port': '465'},
        'outlook': {'host': 'smtp-mail.outlook.com', 'port': '587'},
    }

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def parser(self) -> list:
        _pattern = '(@)([a-zA-Z]+)((.com))'
        with open(self.config, 'r') as f:
            _conf_dict = ujson.loads(f.read())
        _get_smtp = _conf_dict['sender']['email']
        _conf_dict['sender']['password'] = self._password_encoder(_conf_dict['sender']['password'])
        smtp = re.findall(_pattern, _get_smtp)[0][1]
        server = self._servers.get(smtp, 'Not supported')
        return [server, _conf_dict]

    @staticmethod
    def _password_encoder(pwd: str):
        return base64.b64encode(str.encode(pwd))

    @staticmethod
    def _password_decoder(pwd: bytes):
        return bytes.decode(base64.b64decode(pwd))

    def __repr__(self):
        return Parser.__name__


class Sender(Parser):
    def __init__(self, pool=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smtp, self.user_dict = self.parser()
        self.pools = pool

    def send_mail(self):
        if self.pools:
            pool = ThreadPool(self.pools)
            pool.map(self._sender, self._get_email_list())
            pool.join()
            pool.close()
        else:
            for to_addr in self._get_email_list():
                self._sender(to_addr)

    def _get_email_list(self):
        return [line.strip() for line in open(self.user_dict['to_list']['users'])]

    def _compress_html(self):
        with open(self.user_dict['to_list']['letter'], 'r', encoding='utf-8') as f:
            new_html = Premailer(f.read())
            html = new_html.transform()
        return html

    def _sender(self, to_addr):
        self._send_mail(to_addr, self._form_message(to_addr))

    def _send_mail(self, to_addrs, msg):
        server = smtplib.SMTP(**self.smtp)
        server.ehlo()
        server.starttls()
        server.ehlo()
        __pwd__ = self._password_decoder(self.user_dict['sender']['password'])
        _log = self.user_dict['sender']['email']
        server.login(_log, __pwd__)
        server.sendmail(_log, to_addrs, msg.as_string())
        print("Email successfully sent to", to_addrs)
        server.quit()

    def _form_message(self, to_addrs):
        msg = MIMEMultipart()
        msg['Subject'] = self.user_dict['to_list']['subject']
        msg['From'] = self.user_dict['to_list']
        msg['To'] = to_addrs
        body = MIMEText(self._compress_html(), 'html')
        msg.attach(body)
        try:
            return msg
        except smtplib.SMTPAuthenticationError:
            print('SMTPAuthenticationError')
            print("Email not sent to", to_addrs)
