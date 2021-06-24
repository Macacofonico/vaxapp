import os
import requests



access_token=os.getenv("GIT_ACCESS_TOKEN")
headers={"Accept":"application/json","PRIVATE-TOKEN":access_token}
json={"name":"my new project","visibility":"internal"}
#data=requests.get(os.getenv("gitlab_url")+"v4/projects",auth=(os.getenv("gitlab_user"), os.getenv("gitlab_password")))
#print(data.json())
#print(os.getenv("gitlab_url")+"/v4/search?scope=projects&search=flight")
data=requests.get(os.getenv("gitlab_url")+"/v4/search?scope=projects&search=framework&per_page=2000",headers=headers)
while(data.links.get("next",None) != None):
    print(data.links["next"]["url"])
    data = requests.get(data.links["next"]["url"],
                        headers=headers)
    print(len(data.json()))

