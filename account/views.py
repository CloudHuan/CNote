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
post:127.0.0.1:8000/account/signin
body:username=xxx,password=xxx
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
POST 127.0.0.1:8000/account/signup
body:username=cloudhuan,password=1,phone=10010
{
    "data": {
        "uid": 3,
        "name": "cloudhuan",
        "phone": "10010"
    },
    "code": 0
}
*****返回码定义*****
0   注册成功
-1      method error,only support post
-100    params error,name or phone should not null
-101    password is null
-102    password must a 32 MD5 string
-103    username has been used
-104    phone has benn used
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
    if len(pwd) != 32:
        return C_Response(-102,'','password must a 32 MD5 string');
    r = User.objects.raw('SELECT * FROM account_user');
    for item in r:
        if phone == item.phone :
            return C_Response(-103, '', 'phone has been used');
        if name == item.name:
            return C_Response(-104, '', 'username has benn used');

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
调用方式 POST  
示例：
POST HTTP 127.0.0.1:8000/account/writenote
header：TOKEN:XXX    body:uid=1,content='我是文本哦'
{
    "data": {
        "uid": 1,
        "content": "我是文本哦",
        "name": "cz",
        "cid": 15
    },
    "code": 0
}

*****返回码*****
0   ok
-108    content is null
-109    token is invalid
'''
def writeNote(request):
    pass
    uid = request.POST.get('uid','');
    content = request.POST.get('content','');
    public = request.POST.get('public','');
    token = request.META.get('HTTP_TOKEN', '');

    if not content:
        return C_Response(-108,'','content is null');
    try:
        r = User.objects.get(token=token);
    except:
        return C_Response(-109, '', 'token is invalid');



    Note.objects.create(uuid=r.uid,content=content,public=False);
    r = Note.objects.get(cid=0);
    c_id = r.id;
    r.cid = c_id;
    r.save();
    query_shell = "SELECT a.id,a.name,b.uuid,b.content,b.cid FROM account_user a JOIN account_note b ON a.uid = b.uuid WHERE b.cid=%s"%c_id;
    rr = Note.objects.raw(query_shell)[0];
    return C_Response(0, {"name": rr.name, "uid": rr.uuid,"content":rr.content,"cid":rr.cid});

'''
*****读取用户笔记*****
调用方式 get 
示例：
get:127.0.0.1:8000/account/readnote?uid=2
header：TOKEN:XXXXXX
{
    "code": 0,
    "data": [
        {
            "cid:": 1,
            "content": "aabbcc"
        },
        {
            "cid:": 2,
            "content": "你们好"
        }
    ]
}
*****返回码*****
0   ok
-201    uid not found   
-203    no content  
-109    token is invalid
-500    id or token must hava at least one
'''
def readNotes(request):
    method = request.method;
    uid = request.GET.get('uid','');
    token = request.META.get('HTTP_TOKEN','');

    if not uid and not token:
        return C_Response(-500,'','uid or token must hava at least one')

    if uid:

        try:
            User.objects.get(uid=uid);
        except:
            return C_Response(-201, '', 'uid not found');

        items = Note.objects.filter(uuid=uid);
        resp = [];

        if not items:
            return C_Response(-203, '', 'no content');

        for o in items:
            if not o.public:
                continue;
            resp.append({"cid:": o.cid, "content": o.content,"public":o.public});
        if resp != []:
            return C_Response(0, resp);
        else:
            return C_Response(-203, '', 'no content');

    try:
        rrr = User.objects.get(token=token);
    except:
        return C_Response(-109, '', 'token is invalid');

    items = Note.objects.filter(uuid=rrr.uid);
    resp = [];

    if not items:
        return C_Response(-203,'','no content');

    for o in items:
        resp.append({"cid:":o.cid,"content":o.content,"public":o.public});

    return C_Response(0,resp);











