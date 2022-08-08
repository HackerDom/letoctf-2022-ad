from gornilo.http_clients import requests_with_retries


class Api:
    def __init__(self, host):
        self.host = host

    def get_cat_name(self, cat_id):
        return requests_with_retries().get(f"http://{self.host}:8888/cat/{cat_id}").headers["Name"]

    def add_cat(self, cat_id, cat_name, x, y):
        res = requests_with_retries().post(f"http://{self.host}:8888/cat/{cat_id}", headers={
            "Name": cat_name,
            "x": str(x),
            "y": str(y)
        })
        res.raise_for_status()

    def meow_meow(self, x, y):
        res = requests_with_retries().get(f"http://{self.host}:8888/meow-meow", headers={
            "x": str(x),
            "y": str(y)
        })

        return res.text.split(",")

    def get_farm(self, farm_id):
        res = requests_with_retries().get(f"http://{self.host}:8888/farm/", headers={
            "FarmId": farm_id
        })
        return res.text

    def create_farm(self, farm_id, farm_name, *cats):
        res = requests_with_retries().get(f"http://{self.host}:8888/farm/{farm_id}", headers={
            "Name": farm_name,
            "Cats": ",".join(cats)
        })
        res.raise_for_status()