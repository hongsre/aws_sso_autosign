import sys
import params_parser
import os
from multiprocessing import Process, freeze_support
from sso_sign import SSO_SIGN
from aws_configure import update_and_save_aws_config
import subprocess
import re
import time
import yaml

base = os.path.dirname(os.path.abspath(__file__))
config_path = f"{base}/config_llz.yaml"

def get_config(config_path):
    print(config_path)
    if os.path.isfile(config_path):
        print(f'{config_path} ok')
    else:
        print(f'{config_path} not found program shutdown')
        sys.exit(1)

    with open(config_path, 'r', encoding="UTF-8") as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
    return config

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

def execute_aws_cli():
    # AWS SSO 로그인 명령 실행
    log_file_path = f"{base}/aws_sso_login_llz.log"
    command = f"aws sso login --no-browser"
    print(f"llz sso login 명령 실행")
    with open(log_file_path, "w") as log_file:
        subprocess.run(command, shell=True, stdout=log_file, stderr=subprocess.STDOUT, text=True)
    print(f"llz sso login 명령 완료")

    return False

def monitor_log_and_execute_selenium(otp_key, username, passwd):
    log_file_path =  f"{base}/aws_sso_login_llz.log"  # 로그 파일 경로
    base_url = None
    user_code = None

    # 로그 파일에서 URL과 코드 추출
    while True:
        try:
            with open(log_file_path, "r") as log_file:
                contents = log_file.read()
                base_url_match = re.search(r'https://device.sso.us-east-1.amazonaws.com/', contents)
                user_code_match = re.search(r'Then enter the code:\s*\n\s*(\w+-\w+)', contents)
                if base_url_match and user_code_match:
                    base_url = base_url_match.group(0).strip()
                    user_code = user_code_match.group(1).strip()
                    break
            time.sleep(1)  # 로그 파일 업데이트 대기
        except:
            print("logfile not found")
            time.sleep(1)
    x = 0
    while x < 5:
        try:
            if base_url and user_code:
                final_url = f"{base_url}?user_code={user_code}"
                print(f"Final URL: {final_url}")
                
                # Selenium을 사용하여 최종 URL 열기
                selenium = SSO_SIGN()
                selenium.action(final_url, otp_key, username, passwd)
                print("selenium process is done")
                break
            else:
                print("URL or user code not found in the log file.")
        except Exception as E:
            print("selenium Exception 발생 재시도 필요")
            print(f"에러내용: {E} ")
            x += 1
            time.sleep(2)

def init_aws_config(config):
    init_infos = config['init']
    session_name = config['init']['profile_name']
    init_infos.pop('profile_name', None)
    for key in init_infos:
        update_and_save_aws_config(session_name, key, init_infos[key])

def create_profile_data(profile_infos):
    profile_data = {}
    for key, value in profile_infos.items():
        profile_name = f"{key}"
        # 생성된 프로필 이름을 키로 하고, 해당 내용을 값으로 하는 딕셔너리 업데이트
        profile_data[profile_name] = value
    return profile_data

def apply_profile_to_aws_config(profile_data):
    """YAML 파일에서 추출한 프로필 정보를 AWS config 파일에 적용하는 함수"""
    for env, details in profile_data.items():
        section = f"profile {details['name']}"
        for key, value in details.items():
            if key != 'name':
                # print(f'section: {section}, key: {key}, value: {value}')
                update_and_save_aws_config(section, key, str(value))

def main():
    config = get_config(config_path)
    # result = True
    otp_key = config['info']['otp_key']
    # profile_names = config['info']['profile_names']
    username = config['info']['id']
    passwd = config['info']['pw']
    profile_data = create_profile_data(config['info']['profile_infos'])
    if config['info']['profile_create']:
        init_aws_config(config)
        apply_profile_to_aws_config(profile_data)
    # AWS CLI 실행 프로세스 시작
    profile_name = details['name']
    log_file_path = f"{base}/aws_sso_login_llz.log"
    # 파일을 쓰기 모드로 열기
    with open(log_file_path, 'w') as file:
        pass  # 파일에 아무것도 쓰지 않음
    aws_cli_process = Process(target=execute_aws_cli, args=(profile_name,))
    aws_cli_process.start()

    # Selenium 작업 프로세스 시작
    selenium_process = Process(target=monitor_log_and_execute_selenium, args=(otp_key, username, passwd,))
    selenium_process.start()
    aws_cli_process.join()
    selenium_process.join()
    # time.sleep(10)


if __name__ == '__main__':
    if os.name == 'nt':
        freeze_support()
    main()
