from builtins import Exception

from django.contrib.gis import geometry
from django.core.handlers import exception
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from MyTools.RespnseTools import C_Response
from MyTools.TokenTools import randomTokens
from account.models import *

'''
*****登录*****
post:
username
password
响应
{
    "code":0,
    "data"{
        "username":"cz",
        "phone":"13246634313",
        "uid":105
    }
}
*****返回码*****
0   登录成功
-105    密码错误，password wrong
-106    帐号不存在  ，account not found
-107    帐号密码不能为空，account or password not be null
'''
def signin(request):
    method = request.method;
    name = request.POST.get('username', '');
    pwd = request.POST.get('password', '');
    if not name or not pwd:
        return C_Response(-107,'','account or password not be null');
    infos = User.objects.filter(name=name);
    if not infos:
        return C_Response(-106,'','account not found');
    infos = infos[0];
    if not infos.pwd == pwd:
        return C_Response(-105,'','password wrong');

    # 生成认证token
    token = randomTokens();
    infos.token = token;
    infos.save();

    return C_Response(0,{"name":infos.name,"phone":infos.phone,"uid":infos.uid,"token":token});

'''
*****注册*****
method：post请求
必要信息：name、phone(唯一)、pwd密码
返回，json字段，包含name、phone
*****返回码定义*****
0   注册成功
-1      请求方式错误
-100    传入参数错误，传入name、phone为空
-101    传入密码pwd为空
-102    传入密码pwd没有32位 md5加密
-103    帐号已经被已经被注册phone唯一
'''
def signup(request):
    method = request.method;
    name = request.POST.get('username','');
    phone = request.POST.get('phone', '');
    pwd = request.POST.get('password', '');
    #一堆异常
    if method == 'GET':
        return C_Response(-1,'','method error,only support get');
    if not name or not phone:
        return C_Response(-100,'','params error,name or phone should not null');
    if not pwd:
        return C_Response(-101,'','password is null')
    if len(pwd) != 1:
        return C_Response(-102,'','password must a MD5 string');
    r = User.objects.raw('SELECT * FROM account_user');
    for item in r:
        if phone == item.phone or name == item.name:
            return C_Response(-103, '', 'account has benn regist!');

    #创建账户
    User.objects.create(name=name,phone=phone,pwd=pwd);
    m_id = User.objects.get(phone=phone);
    m_id.uid = m_id.id;
    m_id.save();
    #查询并返回数据
    resp = User.objects.get(phone=phone);


    return C_Response(0,{"name":resp.name,"phone":resp.phone,"uid":resp.uid});

'''
*****写入笔记*****
*****返回码*****
0   ok
-108    uid or content is null
-109    uid not found
'''
def writeNote(request):
    pass
    uid = request.POST.get('uid','');
    content = request.POST.get('content','');
    public = request.POST.get('public','');
    token = request.META.get('HTTP_TOKEN', '');



    if not uid or not content:
        return C_Response(-108,'','uid or content is null');
    try:
        User.objects.get(uid=uid);
    except:
        return C_Response(-109,'','uid not found');

    r = User.objects.get(uid=uid);
    if token != r.token:
        return C_Response(-202, '', 'no permission');

    Note.objects.create(uuid=uid,content=content,public=False);
    r = Note.objects.get(cid=0);
    c_id = r.id;
    r.cid = c_id;
    r.save();
    query_shell = "SELECT a.id,a.name,b.uuid,b.content,b.cid FROM account_user a JOIN account_note b ON a.uid = b.uuid WHERE b.cid=%s"%c_id;
    rr = Note.objects.raw(query_shell)[0];
    return C_Response(0, {"name": rr.name, "uid": rr.uuid,"content":rr.content,"cid":rr.cid});

'''
*****读取用户笔记*****
*****返回码*****
0   ok
-200    please input user id
-201    uid not found
-202    no permission

'''
def readNote(request):
    method = request.method;
    uid = request.GET.get('uid','');
    token = request.META.get('HTTP_TOKEN','');

    if not uid:
        return C_Response(-200,'','please input user id');
    try:
        User.objects.get(uid=uid);
    except:
        return C_Response(-201,'','uid not found');

    r = User.objects.get(uid=uid);
    if not token == r.token:
        return C_Response(-202, '', 'no permission');

    items = Note.objects.filter(uuid=uid);
    resp = [];

    for o in items:
        resp.append({"cid:":o.cid,"content":o.content});

    return C_Response(0,resp);











