#coding : utf-8
from django.http.response import JsonResponse


def C_Response(code,data,msg=None):
    if data:
        resp = {"code": 0, "data": data};
    else:
        resp = {"code": code, "errMsg": msg};
    return JsonResponse(resp);