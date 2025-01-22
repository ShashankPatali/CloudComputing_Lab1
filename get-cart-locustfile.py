from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class add_to_cart(FastHttpUser):
    def _init_(self, environment):
        super()._init_(environment)
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
    
    host = "http://localhost:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        with self.client.get(
            "/cart",
            headers={
                "Accept": "application/json",
                "Cookies": f"token={self.token}",
                "Host": "localhost:5000",
            },
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed with status code {resp.status_code}")

if _name_ == "_main_":
    run_single_user(add_to_cart)
