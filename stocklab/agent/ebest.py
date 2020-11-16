import configparser
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


class EBest:
    
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


        


