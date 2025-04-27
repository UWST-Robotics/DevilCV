import grequests
import requests

BridgeType = str | int | float | bool | None

class Bridge:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.root_url = f"http://{self.host}:{self.port}/"
        self.set_url = lambda path,value: f"{self.root_url}/api/v1/values/?path={path}&value={value}"
    def set_value(self, key:str, value:BridgeType):
        
        response = requests.post(self.set_url(key, value))
        
        if response.status_code == 200:
            print(f"Value set successfully: {key} = {value}")
        else:
            print(f"Failed to set value: {response.status_code} - {response.text}")
    def set_values(self, values:dict[str, str]):
        print(f"Setting values: {values}")
        requests_list = []
        for key, value in values.items():
            requests_list.append(grequests.post(self.set_url(key, value)))
        responses = grequests.imap(requests_list)
        for response in responses:
            if response.status_code == 200:
                print(f"Value set successfully: {response.url} - {response.text}")
            else:
                print(f"Failed to set value: {response.status_code} - {response.text}")

    