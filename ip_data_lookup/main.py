from requests import get

ip = "8.8.8.8"

object_list = []
data = get(f"http://ip-api.com/json/{ip}").json()

print(data)