import requests
import jsonpath

def test_jsonpath():
    # 演练环境httpbin.ceshiren，请求什么，返回什么
    url = "https://httpbin.ceshiren.com/post"
    # 定义一个变量，存放请求体信息
    req_body = {"teacher": "ad", "school": "hogwarts"}
    # 通过json 关键字传递请求体信息
    r = requests.post(url, json=req_body)
    # print(r.text)
    # print(r.json()["headers"]["Content-Type"])
    # jsonpath 的返回值，如果没有找到，则返回False
    assert jsonpath.jsonpath(r.json(), "$..Content-Type1111") == False
    #  jsonpath 的返回值，如果找到的话，会返回结果列表，不管找到几个结果，最外层都是返回返回列表
    assert jsonpath.jsonpath(r.json(), "$..Content-Type")

