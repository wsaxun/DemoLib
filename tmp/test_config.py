from common.conf import (
    get_webApi_conf,
    get_amqp_conf,
    get_log_conf
)

amqpConf = get_amqp_conf()
logConf = get_log_conf()
webApiConf = get_webApi_conf()


print(amqpConf)
print(logConf)
print(webApiConf)

print(type(logConf))