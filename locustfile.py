from locust import HttpUser, task, between
import random, string

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
        self.client.post("/api/user/register/", json=data, name="register")
