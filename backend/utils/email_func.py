import string
import random
import smtplib

class SendEmail:
    
    @staticmethod
    def get_random_code():
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return res

    @staticmethod
    def post_mail(user_to, message):
        mail_data = {
            'login': 'testemailsendnnn1k@gmail.com',
            'password': 'znwt bffc blls fpqp',
        }
        smt = smtplib.SMTP('smtp.gmail.com', 587)
        smt.starttls()
        smt.login(mail_data['login'], mail_data['password'])
        smt.sendmail(mail_data['login'], user_to, message.encode('utf-8'))
        smt.quit()

def send_code_to_email(user, user_type):
    code = SendEmail.get_random_code()
    message = f'Ваш код {code}'
    from backend.utils.redis_func import create_redis_client
    redis_client = create_redis_client()
    redis_client.hset(f'{user_type}:{user.id}', 'code', code)
    SendEmail.post_mail(user.email, message)
