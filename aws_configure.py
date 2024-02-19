import configparser
import os

def load_aws_config():
    """AWS config 파일을 불러오는 함수"""
    # 홈 디렉토리 경로 가져오기
    home_directory = os.path.expanduser('~')
    # .aws/config 파일 경로 설정
    aws_config_path = os.path.join(home_directory, '.aws', 'config')
    # ConfigParser 객체 생성
    config = configparser.ConfigParser()
    # .aws/config 파일 읽기
    config.read(aws_config_path)
    return config, aws_config_path

def update_and_save_aws_config(section, key, value):
    """AWS config 파일을 업데이트하고 저장하는 함수"""
    # 설정 불러오기
    config, aws_config_path = load_aws_config()
    
    # 섹션이 없으면 생성
    if not config.has_section(section):
        config.add_section(section)
    
    # 키-값 설정 업데이트
    config.set(section, key, value)
    
    # 변경 사항을 파일에 저장
    with open(aws_config_path, 'w') as configfile:
        config.write(configfile)
    
    print(f"Updated {section} section, set {key} to {value}.")

# # 예제: 'default' 섹션의 'region'을 'us-west-2'로 변경하고 저장
# update_and_save_aws_config('default', 'region', 'us-west-2')
