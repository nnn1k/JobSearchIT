import string
import random

from aiosmtplib import SMTP
from backend.utils.other.redis_func import add_code_to_redis

class SendEmail:
    
    @staticmethod
    def get_random_code(k=6) -> str:
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
        return res

    @staticmethod
    async def post_mail(user_to, message) -> None:
        mail_data = {
            'login': 'testemailsendnnn1k@gmail.com',
            'password': 'znwt bffc blls fpqp',
        }
        smt = SMTP(hostname='smtp.gmail.com', port=587, start_tls=True)
        await smt.connect()
        await smt.login(mail_data['login'], mail_data['password'])
        await smt.sendmail(mail_data['login'], user_to, message.encode('utf-8'))
        await smt.quit()

    @staticmethod
    async def send_code_to_email(user) -> None:
        code = SendEmail.get_random_code()
        message = f'Ваш код {code}'
        await add_code_to_redis(user, code)
        await SendEmail.post_mail(user.email, message)
