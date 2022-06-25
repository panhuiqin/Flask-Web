# -*- coding: utf-8 -*-
import redis
import CommonMethod.ReadConfig as Rf
import json


class ConnectRedis :
    """
    连接数据库，操作数据库
    """
    def __init__(self) :
        host, port, password, db = Rf.Read_config().Read_redis()
        self.POOL = redis.ConnectionPool(host=host, password=password,
                                    port=port, max_connections=100, db=db)  # 创造连接池,最多能放多少链接
        print(self.POOL)

    def Read_redis(self, name):
        r = redis.Redis(connection_pool=self.POOL)
        data = r.get(name)
        return data

    def Write_redis(self, name, data):
        r = redis.Redis(connection_pool=self.POOL)
        r.set(name, data)

    def Del_redis(self, name):
        r = redis.Redis(connection_pool=self.POOL)
        r.delete(name)

# Name = 'token'
# data1 = {"config": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InRlc3RhZG1pbiIsInN1YiI6InRlc3RhZG1pbiIsInNjb3BlIjoiZG9jdG9yLGRhdGFiYXNlLGFwcHNlcnZpY2UsY29uZmlnLHRoaXJkcGFydHksbWdyLHNmc3lzLGxvYWRtaW4sY2FwaSxvbGRvcGVuYXBpLExpYW5PdUlNLGRvY3N0dWRpbyxsb25vdGlmeSxsb2NtcyxzaG9wYWduZXQsU2VhcmNoV2ViLGF1dGgsYmFzZWFwaSxJbnFTZXJ2aWNlLFB1c2hTZXJ2aWNlLENBU2VydmljZSxsb2F1dGhvcml0eSxycHQsdGlja2V0LEZ6SW0sZG9jbGl2ZSxkb2Nncm91cCxCdXNpbmVzc0NlbnRlcixjaGF0cmVjb3JkLHVjLExvamcsbG9hcixjbXNldGwsbXNnLGZ6d2luLGJpZG9jLG1lZGlhLGJpZG9jYW5hLGxvc2NybSxsb2FjdGl2aXR5LGRpc2NlbnRlcixkd3osYmktYWN0dWFsLXRpbWUsb3BlbnN2YyxwdXNoc3ZjLGJhc2VkYXRhYXBpLG1lZGljYWxhc3Npc3RhbnQsSGVhbHRoQ2xvdWQsb3JkZXJmaWxlLGl0b20iLCJleHQiOiIiLCJyb2xlIjoiQXBpIiwianRpIjoiMjliYTA0NDktZjFkNS00MzhmLWFlMmUtYzRjOGViYmNkOTgwIiwiaWF0IjoiMDMvMDgvMjAyMiAwODo1MDoyOCIsImV4cCI6MTY0NjczMzAyOCwibmJmIjoxNjQ2NzI5MjQ4LCJpc3MiOiJodHRwczovL2F1dGgubGlhbi1vdS5jb20iLCJhdWQiOiJodHRwczovL2F1dGgubGlhbi1vdS5jb20vMTAvMTAifQ.XN0Cfipku1QQawjeVNjahfdS2e-8OkVwIqHHC9fR1M0", "doctor": "{\"code\":9998,\"msg\":\"\u624b\u673a\u9a8c\u8bc1\u7801\u9519\u8bef\",\"data\":{}}"}
# ConnectRedis().Write_redis(Name, json.dumps(data1))

# print(str(ConnectRedis().Read_redis(Name), encoding='utf-8'))


