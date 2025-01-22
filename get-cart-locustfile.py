from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    def __init__(self, environment):
        super().__init__(environment)
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
    def view_cart(self):
        with self.client.get(
            "/cart",
            headers={
                **self.default_headers,
                "Accept": "application/json",
                "Cookies": f"token={self.token}",
                "Host": "localhost:5000",
            },
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

if __name__ == "__main__":
    run_single_user(AddToCart)
