import allure
import jsonpath
import requests

from L2.utils.log_util import logger


@allure.feature("宠物管理业务场景接口测试")
class TestPetstorePetmanager:
    '''
    宠物商店接口业务测试
    '''

    def setup_class(self):
        # 准备测试数据
        self.base_url = "https://petstore.swagger.io/v2/pet"
        # 查询接口 url
        self.search_url = self.base_url + "/findByStatus"
        # 定义 pet id
        self.pet_id = 9223372000001084222
        # 删除接口 url
        self.delete_url = self.base_url + f"/{self.pet_id}"
        # 宠物状态
        self.pet_status = "available"
        # 新增宠物数据
        self.add_pet_info = {
          "id": self.pet_id,
          "category": {
            "id": 1,
            "name": "cat"
          },
          "name": "miao",
          "photoUrls": [
            "string"
          ],
          "tags": [
            {
              "id": 5,
              "name": "cute"
            }
          ],
          "status": self.pet_status
        }
        # 更新宠物数据
        self.update_name = "miao-hogwarts"
        self.update_pet_info = {
          "id": self.pet_id,
          "category": {
            "id": 1,
            "name": "cat"
          },
          "name": self.update_name,
          "photoUrls": [
            "string"
          ],
          "tags": [
            {
              "id": 5,
              "name": "cute"
            }
          ],
          "status": self.pet_status
        }
        # 查询宠物数据
        self.search_param = {
            "status": self.pet_status
        }
        self.proxy = {
            "http": "http://127.0.0.1:8888",
            "https": "http://127.0.0.1:8888"
        }

    @allure.story("宠物增删改查场景测试")
    def test_pet_manager(self):
        with allure.step("新增宠物"):
            # 新增宠物
            add_r = requests.post(self.base_url, json=self.add_pet_info, proxies=self.proxy, verify=False)
            logger.info(f"新增宠物接口响应为：{add_r.text}")
            # 断言
            assert add_r.status_code == 200
            # 查询新增宠物结果
            search_r = requests.get(self.search_url, params=self.search_param, proxies=self.proxy, verify=False)
            logger.info(f"查询宠物接口的响应为：{search_r.text}")
            assert search_r.status_code == 200
            # 新增宠物业务断言
            # 查询接口响应中是否包含新增宠物的 id
            assert self.pet_id in jsonpath.jsonpath(search_r.json(), "$..id")

        with allure.step("修改宠物"):
            # 修改宠物
            update_r = requests.put(self.base_url, json=self.update_pet_info, proxies=self.proxy, verify=False)
            logger.info(f"更新宠物接口的响应为：{update_r.text}")
            # 断言
            assert update_r.status_code == 200
            # 查询更新宠物结果
            search_r = requests.get(self.search_url, params=self.search_param, proxies=self.proxy, verify=False)
            logger.info(f"查询宠物接口的响应为：{search_r.text}")
            assert search_r.status_code == 200
            # 更新宠物业务断言
            # 查询接口响应中是否包含更新宠物的 name
            assert self.update_name in jsonpath.jsonpath(search_r.json(), "$..name")

        with allure.step("删除宠物"):
            # 删除宠物
            delete_r = requests.delete(self.delete_url, proxies=self.proxy, verify=False)
            logger.info(f"删除宠物接口的响应为：{delete_r.text}")
            # 断言
            assert delete_r.status_code == 200
            # 查询删除宠物结果
            search_r = requests.get(self.search_url, params=self.search_param, proxies=self.proxy, verify=False)
            logger.info(f"查询宠物接口的响应为：{search_r.text}")
            assert search_r.status_code == 200
            # 删除宠物业务断言
            # 查询接口响应中是否不包含已经宠物的 id
            assert self.pet_id not in jsonpath.jsonpath(search_r.json(), "$..id")
