from django.shortcuts import render
from django.http import Http404
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Substr, Length
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime 

from .models import RequestLog


@login_required
def AnalyticsHomeView(request, filter=None, date=None, **kwargs):
    if not request.user.is_superuser:
        raise Http404
    
    # base_url = 'http://computermuseum.ir/'
    # base_url_length = len(base_url)
        
    # logs = RequestLog.objects.annotate(
    #     stripped_url=Substr('requested_url', base_url_length + 1, Length('requested_url')  - base_url_length)
    # )
    device = kwargs.get('device', None)
    base = kwargs.get('base', None)
    logs = RequestLog.objects.all()
    if date not in (None, 'None'):
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            logs = logs.filter(datetime__date=date_obj.date())
        except:
            pass
    # Queryset to get distinct requested_url or IP and count occurrences
    if base in ('None', None):
        logs = (
            logs
            .values('requested_url')  # Group by requested_url
            .annotate(url_count=Count('requested_url'))  # Count occurrences of each requested_url
            .order_by('-url_count')  # Optional: Order by count descending
        )
    elif base == 'ip':
        logs = (
            logs
            .values('ip_address')  # Group by requested_url
            .annotate(ip_count=Count('ip_address'))  # Count occurrences of each requested_url
            .order_by('-ip_count')  # Optional: Order by count descending
        )
        
    
        

    
    if filter == 'home' :
        logs = logs.filter(
            Q(requested_url__exact='http://computermuseum.ir/') | 
            Q(requested_url__exact='https://computermuseum.ir/') | 
            Q(requested_url__exact='http://www.computermuseum.ir/') | 
            Q(requested_url__exact='https://www.computermuseum.ir/')
        )
    
    if filter == 'qr':
        logs = logs.filter(requested_url__startswith='http://computermuseum.ir/qr/')    
        
    if filter in ( 'crowdsourcing' , 'tickets', 'tickets-landing', 'ganjoor', 'qr-0a3c528e', 'nowruz-1404'):
        query = filter.replace('-', '/')
        if filter == 'nowruz-1404':
            query = filter
        print(query)
        # 'https://computermuseum.ir/qr/0a3c528e-e1ec-4e44-a2ea-2359d848eb61/'
        logs = logs.filter(requested_url__icontains=query)
        
    if device and device != 'None':
        try:
            logs = logs.filter(device_type=device)
        except:
            pass

    if base in ('None', None):
        logs_stat = logs.aggregate(count=Sum('url_count'))['count']
    elif base == 'ip':
        logs_stat = logs.aggregate(count=Sum('ip_count'))['count']
    
    # logs = logs[:20]
    page=None
    if logs.count() > 100:
        # pagination
        paginator = Paginator(logs, 25)  # 20 order in each page
        page = request.GET.get('page')
        try:
            logs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            logs = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            logs = paginator.page(paginator.num_pages)
    
    context = dict(
        page_title=_("Analytics"),
        logs=logs,
        logs_stat=logs_stat,
        page=page,
        date=date,
        filter=filter,
        device=device,
        base=base
    )
    return render(
        request, 
        'analytics/analytics_home.html', 
        context
    )
