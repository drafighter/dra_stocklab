import requests
import configparser
import xml.etree.ElementTree as ET


class Data:
    CORP_CODE_URL = "http://api.seibro.or.kr/openapi/service/CorpSvc/getIssucoCustnoByNm"

    def __init__(self):
        config = configparser.RawConfigParser()
        config.read('conf/config.ini')
        self.api_key = config['DATA']['api_key']
        if self.api_key is None:
            raise Exception("Need to api key")

    def get_corp_code(self, name=None):
        """
        한국예탁결재원에서 제공하는 기업코드를 회사명칭으로 검색
        :param name: str 회사명칭
        :return: dict 회사코드와 명칭
        """

        query_params = {
            "serviceKey": self.api_key,
            "issucoNm": name,
            "numOfRows": str(5000)
        }

        request_url = self.CORP_CODE_URL + "?"
        for k, v in query_params.items():
            request_url = request_url + k + "=" + v + "&"

        print(request_url)
        res = requests.get(request_url[:-1])

        """
        1. 내장함수이용 : xml.etree.ElemnetTree
         - ElementTree.fromstring(xml.text) -> 문자열에서 XML 파싱
        """

        root = ET.fromstring(res.text)
        from_tags = root.iter("items")
        result = {}
        for items in from_tags:
            for item in items.iter("item"):
                if name in item.find("issucoNm").text.split():
                    result["issucoCustno"] = item.find("issucoCustno").text
                    result["issucoNm"] = item.find("issucoNm").text
        return result




