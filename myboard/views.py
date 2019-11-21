from django.shortcuts import render
from myboard.models import BoardTab
from django.http.response import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def Main(request):
    return render(request,'main.html')

def ListFunc(request):
    datas = BoardTab.objects.all().order_by('-gnum','onum')
    #return render(request,'board.html',{'data':datas})
    
    paginator = Paginator(datas,2) #페이징
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages())
        
    return render(request,'board.html',{'data':data})

def InsertFunc(request):
    return render(request,"insert.html")
def get_ipAddr(request): # client ip 얻기
    x_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_for:
        ip = x_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def InsertokFunc(request):
    if request.method == 'POST':
        try:
            gbun = 1
            datas = BoardTab.objects.all()
            if datas.count() != 0:
                gbun = BoardTab.objects.latest('id').id + 1
                
            BoardTab(
                name = request.POST.get('name'),
                passwd = request.POST.get('passwd'),
                mail = request.POST.get('mail'),
                title = request.POST.get('title'),
                cont = request.POST.get('cont'),
                bip = get_ipAddr(request),
                bdate = datetime.now(),
                readcnt = 0,
                gnum = gbun,
                onum = 0,
                nested = 0,
            ).save()
        except Exception as e:
            print('InsertokFunc err :',e)
            
    return HttpResponseRedirect('/board/list') #추가 후 목록보기

def UpdateFunc(request):
    try:
        data = BoardTab.objects.get(id=request.GET.get('id'))
        
    except Exception as e:
        print('UpdateFunc err : ', e)
    return render(request,'update.html',{'data_one':data})

def UpdateokFunc(request):
    if request.method=='POST':
        upRec = BoardTab.objects.get(id = request.POST.get('id'))
        if upRec.passwd == request.POST.get('up_passwd'):
            upRec.name = request.POST.get('name')
            upRec.mail = request.POST.get('mail')
            upRec.title = request.POST.get('title')
            upRec.cont = request.POST.get('cont')
            upRec.save()
        else:
            return render(request,'error.html')
        
    return HttpResponseRedirect('/board/list') # 수정 후 목록보기

def DeleteFunc(request):
    try:
        data = BoardTab.objects.get(id=request.GET.get('id'))
    except Exception as e:
        print('DeleteFunc err:',e)
    
    return render(request,'deleteok.html',{'data':data})

def DeleteokFunc(request):
    if request.method=='POST':
        delRec = BoardTab.objects.get(id = request.POST.get('id'))
        if delRec.passwd == request.POST.get('del_passwd'):
            delRec.delete()
            return HttpResponseRedirect('/board/list') # 삭제 후 목록보기
            
        else:
            return render(request,'error.html')
        
def SearchFunc(request): #검색용
    if request.method == "POST":
        s_type = request.POST.get('s_type')
        s_value = request.POST.get('s_value')
        if s_type == "title":
            datas = BoardTab.objects.filter(title__contains = s_value).order_by('-id')
        elif s_type == "name":
            datas = BoardTab.objects.filter(name__contains = s_value).order_by('-id').order_by('-id')
        
        
        paginator = Paginator(datas,1)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages())
        
    return render(request, 'board.html', {'data':data})

        def ContentFunc(request):
    data = BoardTab.objects.get(id=request.GET.get("id"))
    data.readcnt = data.readcnt + 1 #조회수 증가
    data.save()
    page = request.GET.get('page')
    return render(request,'content.html',{'data_one':data,'page':page})

def ReplyFunc(request): #댓글용
    try:
        data = BoardTab.objects.get(id=request.GET.get('id'))
    except Exception as e:
        print('ReplyFunc err:',e)
    
    return render(request,'reply.html',{'data_one':data})

def ReplyokFunc(request):
    if request.method == 'POST':
        try:
            regnum = int(request.POST.get('gnum')) 
            reonum = int(request.POST.get('onum'))
             
            temRec = BoardTab.objects.get(id=request.POST.get('id'))
            old_gnum = temRec.gnum
            old_onum = temRec.onum
            if old_onum >= reonum and old_gnum == regnum:
                old_onum = old_onum + 1  # onum 갱신
            
            # 댓글 저장
            BoardTab(
                name = request.POST.get('name'),
                passwd = request.POST.get('passwd'),
                mail = request.POST.get('mail'),
                title = request.POST.get('title'),
                cont = request.POST.get('cont'),
                bip = get_ipAddr(request),
                bdate = datetime.now(),
                readcnt = 0,
                gnum = regnum,
                onum = old_onum,
                nested = int(request.POST.get('nested')) + 1,
                ).save()
        except Exception as e:
            print('ReplyokFunc err',e)
            
    return HttpResponseRedirect('/board/list')
