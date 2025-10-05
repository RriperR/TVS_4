from locust import HttpUser, task, between
import random, string

URLS = [
    "/api/user/register/",            # baseline
    "/api/user/register/?slow=1",     # искусственная задержка
    "/api/user/register/?boom=1",     # необработанное исключение
    "/api/user/register/?qspam=1",    # N+1 или избыточные запросы
]

class RegistrationUser(HttpUser):
    wait_time = between(0.3, 1.0)

    def random_email(self):
        return "user_" + "".join(random.choices(string.ascii_lowercase, k=8)) + "@test.local"

    def random_password(self):
        return "".join(random.choices(string.ascii_letters + string.digits, k=12))

    @task
    def register(self):
        data = {
            "email": self.random_email(),
            "password": self.random_password(),
        }
        url = random.choice(URLS)
        # имя задачи = сам URL без домена (для удобного отображения в CSV/отчётах)
        self.client.post(url, json=data, name=url)
