import requests, json
import urllib.parse

#INPUT: 
copy_path_from = ["user","test"] #["space","folder"]
copy_path_to = ["user","test1"] #["space","folder"]

dremio_url = 'http://localhost:9047' # url dremio
user="usr" # user name in dremio
pwd="pwd" # password ame in dremio
verify_ssl=False # SSL enanled/disabled for REST calls

#######################


token = "_dremio"
content_type = "application/json"


def login():
    headers = {'Content-Type': content_type}
    data = '{"userName": "'+ user + '","password": "'+pwd+'" }'
    token_obj={}
    try:
        response = requests.post(dremio_url + '/apiv2/login', headers=headers, data=data, verify=verify_ssl)
        token = response.json()['token'] 
        token_obj={"res":True, "token":token}
        return token_obj
    except requests.exceptions.SSLError as e:
        print("SSLError")
        token_obj={"res":False, "token":None}
        return token_obj

def get_all_vdss_from_folder():
    headers = {'Content-Type': content_type, 'Authorization': token}
    tmp_path=""
    for one in copy_path_from:
        tmp_path=tmp_path+"/"+one 
    tmp_path=urllib.parse.quote(tmp_path)
    try:
        response = requests.get(dremio_url + '/api/v3/catalog/by-path'+tmp_path, headers=headers, verify=verify_ssl)
        return(response.json())
    except requests.exceptions.SSLError as e:
        return({"response":"SSLError"})
    
def get_vds(id):
    headers = {'Content-Type': content_type, 'Authorization': token}

    try:
        response = requests.get(dremio_url + '/api/v3/catalog/'+id, headers=headers, verify=verify_ssl)
        return(response.json())
    except requests.exceptions.SSLError as e:
        return({"response":"SSLError"})

def move_vds(vds):
    headers = {'Content-Type': content_type, 'Authorization': token}
    
    for name in vds["path"]:
        tmp_name=name
    print(copy_path_to)
    tmp_copy_to = copy_path_to.copy()
    tmp_copy_to.append(name)
    vds_new = {
        "entityType": "dataset",
        "path": tmp_copy_to,
        "type":  "VIRTUAL_DATASET",
        "fields": vds["fields"],
        "sql": vds["sql"] 
        }
    vds_new=json.dumps(vds_new)
    try:
        response = requests.post(dremio_url + '/api/v3/catalog', headers=headers,  data=vds_new ,verify=verify_ssl)
        return(response.json())
    except requests.exceptions.SSLError as e:
        return({"response":"SSLError"})




if __name__ == "__main__":
    token_obj=login()
    datasets=[]
    if (token_obj["res"]):
        token=token+token_obj["token"]
        object_response=get_all_vdss_from_folder()
        for vds in object_response["children"]:
            vds=get_vds(vds["id"])
            move_vds(vds)