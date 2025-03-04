import string
import random

from aiosmtplib import SMTP

from backend.modules.redis.redis_code_utils import add_code_to_redis
from backend.utils.settings import settings


class SendEmail:
    
    @staticmethod
    def get_random_code(k=6) -> str:
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
        return res

    @staticmethod
    async def post_mail(user_to, message) -> None:
        smt = SMTP(hostname='smtp.gmail.com', port=587, start_tls=True)
        await smt.connect()
        await smt.login(settings.email.login, settings.email.login)
        await smt.sendmail(settings.email.login, user_to, message.encode('utf-8'))
        await smt.quit()

    @staticmethod
    async def send_code_to_email(user) -> None:
        code = SendEmail.get_random_code()
        message = f'Ваш код {code}'
        await add_code_to_redis(user, code)
        await SendEmail.post_mail(user.email, message)
