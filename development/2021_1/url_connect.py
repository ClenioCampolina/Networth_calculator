import ssl

# Ignore SSL certificate errors
def context_with_no_certificate_check():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx