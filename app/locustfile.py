from locust import HttpUser, task, between

class ShortenerUser(HttpUser):
    wait_time = between(0.1, 0.5)
    code = None

    def on_start(self):
        r = self.client.post("/shorten", json={"original_url": "https://example.com"})
        self.code = r.json()["short_url"].split("/")[-1]

    @task(9)
    def redirect(self):
        self.client.get(f"/{self.code}", allow_redirects=False)

    @task(1)
    def analytics(self):
        self.client.get(f"/analytics/{self.code}")