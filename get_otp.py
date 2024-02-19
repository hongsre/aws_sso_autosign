def get_otp_code(otp_key):
    import pyotp
    # Google Authenticator의 시크릿 키
    totp = pyotp.TOTP(otp_key)
    otp_code = totp.now()
    return otp_code