import time
import hashlib

'''产生随机的token'''
def randomTokens():
    unix_time = str(time.time()).encode("utf-8")
    return hashlib.md5(unix_time).hexdigest()

if __name__ == '__main__':
    print(userToken('cz'))