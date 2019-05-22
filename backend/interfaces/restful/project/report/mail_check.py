import re


def check_waykichain_mail(mail):
    return True if re.match(r'^[0-9a-zA-Z_.]{0,19}@waykichainhk.com$', mail) else False


def check_all_mail(mail):
    return True if re.match(r'^[0-9a-zA-Z_.]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', mail) else False


if __name__ == '__main__':
    ret = check_waykichain_mail("linxin.jiang@waykichainhk.com")
    print(ret)
    ret = check_all_mail("linxin.jiang@waykichainhk.com")
    print(ret)
