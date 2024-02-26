# sso autosign

```
sso login을 자동화를 위한 스크립트입니다.
sso session을 로그인하고, 해당 세션을 이용하도록 profile을 등록해주면 
설정한 profile 계정에 대해서도 인증 세션을 사용하는 것으로 확인 됨.

Config 의 profile create 설정을 true로 설정하면
Config 의 [init][sso_session_name] 값을 불러와
init 함수를 실행하여 sso session login 설정을 추가하고, 
해당 세션을 이용하는 profile 데이터를 추가 함.

데이터는 Config의 profile_infos에 포함된 데이터를 사용
```
 

# 필수 설치가 필요한 모듈

```toml
[tool.poetry]
name = "web_cron"
version = "0.1.0"
description = ""
authors = ["seongi.hong <seongi.hong@line.games>"]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.28.1"
flake8 = "^4.0.1"
PyAutoGUI = "^0.9.53"
selenium = "^4.3.0"
webdriver-manager = "^3.7.1"
PyYAML = ">=6.0"
pyotp = "^2.8.0"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

# config 셋팅 방법

```yaml
# sso 로그인 프로파일 생성
init:
  sso_session_name: sso_session_name
  sso_start_url: sso_login_url
  sso_region: us-east-1
  # 아래 내용은 수정하지 않음.
  sso_registration_scopes: sso:account:access

# 로그인 정보 및 생성이 필요한 profile 정보
info:
  # aws profile 및 sso 설정이 되어있다면 sso_id, sso_pw, otp_key 값만 입력
  sso_id: 
  sso_pw: 
  otp_key:
  # aws profile 생성이 필요없다면 아래 값을 false로 설정
  profile_create: true
  profile_infos:
    real:
      name: profile_name
      sso_session: llz
      sso_account_id: AWS Account ID
      sso_role_name: custom_sso_role_name
      region: ap-northeast-2
      output: json  
    qa:
      name: profile_name
      sso_session: llz
      sso_account_id: AWS Account ID
      sso_role_name: custom_sso_role_name
      region: ap-northeast-2
      output: json
```

# 실행 방법
```bash
poetry run python sso_setting.py
```
