import grequests
import requests

type BridgeType = str | int | float | bool | None

class Bridge:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.root_url = f"http://{self.host}:{self.port}/"
        self.set_url = f"{self.root_url}set/"
    def set_value(self, key:str, value:BridgeType):
        
        response = requests.post(self.set_url, data={"value": value, "path": key})
        
        if response.status_code == 200:
            print(f"Value set successfully: {key} = {value}")
        else:
            print(f"Failed to set value: {response.status_code} - {response.text}")
    async def set_values(self, values:dict[str, str]):
        requests_list = []
        for key, value in values.items():
            requests_list.append(grequests.post(self.set_url, data={"value": value, "path": key}))
        responses = grequests.imap(requests_list)
        for response in responses:
            if response.status_code == 200:
                print(f"Value set successfully: {response.url} - {response.text}")
            else:
                print(f"Failed to set value: {response.status_code} - {response.text}")

    