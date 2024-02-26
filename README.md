[# sso autosign

# 필수 설치가 필요한 모듈

```toml
[tool.poetry]
name = "web_cron"
version = "0.1.0"
description = ""
authors = ["seongi.hong <seongi.hong@>"]

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

# config 셋팅법

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
