# drive code for your project
def get_fee_params():
    return [
        { "fee": 1},
        { "fee": 2},
        { "fee": 3},
    ]
    
print(get_fee_params())

def get_fee_publickey_params1():
    return [
        { "fee": 1, "publickey": "11" },
        { "fee": 2, "publickey": "22" },
        { "fee": 3, "publickey": "33" },
    ]
print(get_fee_publickey_params1())


def get_fee_publickey_params2():
    return [
        {"data": { "fee": 1, "publickey": "11" }},
        {"data": { "fee": 1, "publickey": "11" }},
        {"data": { "fee": 1, "publickey": "11" }},
    ]
print(get_fee_publickey_params2())


def validate_str_in_msg(check, expect):
    assert expect in check


base_url = "https://baas-test.wiccdev.org/v2/api"
