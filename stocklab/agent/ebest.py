import configparser
import time
from datetime import datetime
import win32com.client
import pythoncom


class XASession:

    # 로그인 상태를 확인하기 위한 클래스 변수
    login_state = 0

    def OnLogin(self, code, msg):
        """
        로그인 시도 후 호출되는 이벤트
        :param code: 서버에서 받은 메시지 코드
        :param msg: 서버에서 받은 메시지
        :return:
        """
        if code == "0000":
            print(code, msg)
            XASession.login_state = 1
        else:
            print(code, msg)

    def OnDisconnect(self):
        """
        서버와 연결이 끊어지면 발생하는 이벤트
        :return:
        """
        print("Session disconnected")
        XASession.login_state = 0


class XAQuery:
    RES_PATH = "C:\\eBEST\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData", code)
        XAQuery.tr_run_state = 1

    def OnReceiveMessage(self, error, code, message):
        print("OnReceiveMessage", error, code, message, XAQuery.tr_run_state)


class EBest:
    QUERY_LIMIT_10MIN = 200 # 10분에 200건 조회 제한
    LIMIT_SECONDS = 600 # 10min

    def __init__(self, mode=None):
        """
        config.ini 파일을 로드해 사용자, 서버 정보 저장
        query_cnt 는 10분당 200개의 TR 수행을 관리하기 위한 리스트
        xa_session_client 는 XASession 객체
        :param mode: 모의서버는 DEMO, 실서버는 PROD 로 구분
        """

        if mode not in ("PROD", "DEMO", "ACE"):
            raise Exception("Need to run_mode(PROD or DEMO or ACE)")

        run_mode = "EBEST_" + mode
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.user = config[run_mode]['user']
        self.passwd = config[run_mode]['password']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        # 이벤트 방식으로 동작하는 COM 클래스에 대한 인스턴스 생성을 위해 DispatchWithEvents 사용
        # 파라미터로 연결할 이벤트 클래스 지정 (여기는 로그인 이벤트 클래스인 XASession 지정)
        self.xa_session_clinet = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)

        self.query_cnt = []

    def login(self):
        self.xa_session_clinet.ConnectServer(self.host, self.port)
        self.xa_session_clinet.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()

    def logout(self):
        XASession.login_state = 0
        self.xa_session_clinet.DisconnectServer()

    def _execute_query(self, res, in_block_name, out_block_name, *out_fields, **set_fields):
        """
        TR 코드를 실행하기 위한 메소드 입니다.
        :param res: str 리소스명(TR)
        :param in_block_name: str 인블록명
        :param out_block_name: str 아웃블록명
        :param out_fields: list 출력필드 리스트
        :param set_fields: dict 인블록에 설정한 필드 딕셔너리
        :return: list 결과 리스트
        """

        time.sleep(1)
        print("current query cnt:", len(self.query_cnt))
        print(res, in_block_name, out_block_name)
        while len(self.query_cnt) >= EBest.QUERY_LIMIT_10MIN:
            time.sleep(1)
            print("waiting for execute query... current query cnt:", len(self.query_cnt))
            
            # lambda 인자리스트 : 표현식
            # filter() : filter 에 인자로 사용되는 lambda 식은 각각의 iterable 요소에 대해 Boolean 값을 반환함
            # -> True 를 반환하면 그 요소는 남고, False 를 반환한 요소는 삭제됨

            # query_cnt 에 저장된 TR 코드 실행 시간이 600초 지난 것은 저장 TR 리스트에서 삭제하는 로직
            self.query_cnt = list(filter(lambda x: (datetime.today() - x).total_seconds() < EBest.LIMIT_SECONDS, self.query_cnt)())

        xa_query = win32com.client.DispatchWithEvents("XA_Session.XAQuery", XAQuery)
        xa_query.LoadFromResFile(XAQuery.RES_PATH + res + ".res")

        # in_block_name 셋팅
        for key, value in set_fields.items():
            xa_query.SetFieldData(in_block_name, key, 0, value)
        errorCode = xa_query.Request(0)









        


