from django.shortcuts import render
from django.http import Http404
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Substr, Length
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.utils import timezone 

from .models import RequestLog


@login_required
def AnalyticsHomeView(request, filter=None, date=None, **kwargs):
    if not request.user.is_superuser:
        raise Http404
    
    # base_url = 'http://inex-design.com/'
    # base_url_length = len(base_url)
        
    # logs = RequestLog.objects.annotate(
    #     stripped_url=Substr('requested_url', base_url_length + 1, Length('requested_url')  - base_url_length)
    # )
    device = kwargs.get('device', None)
    base = kwargs.get('base', None)
    lan = kwargs.get('lan', 'all') # language
    lan_q = lan + '/' if lan in ('en', 'fa') else ''
    
    HTTP_DOMAIN = 'http://inex-design.com/'
    HTTP_W_DOMAIN = 'http://www.inex-design.com/'
    HTTPS_DOMAIN = 'https://inex-design.com/'
    HTTPS_W_DOMAIN = 'https://www.inex-design.com/'
    
    # HTTP_DOMAIN = 'http://127.0.0.1:8000/'
    # HTTPS_DOMAIN = 'https://127.0.0.1:8000/'
    
    
    
    logs = RequestLog.objects.exclude(requested_url__icontains='/analytics/')
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
    
    if lan in ('en', 'fa'):
        logs = logs.filter(
            Q(requested_url__startswith=f"{HTTP_DOMAIN}{lan_q}") | 
            Q(requested_url__startswith=f"{HTTPS_DOMAIN}{lan_q}") | 
            Q(requested_url__startswith=f"{HTTP_W_DOMAIN}{lan_q}") | 
            Q(requested_url__startswith=f"{HTTPS_W_DOMAIN}{lan_q}")
        )
    
    if filter == 'home' :
        logs = logs.filter(
            Q(requested_url__exact=f"{HTTP_DOMAIN}") |  Q(requested_url__exact=f"{HTTP_DOMAIN}en/") | Q(requested_url__exact=f"{HTTP_DOMAIN}fa/") |
            Q(requested_url__exact=f"{HTTPS_DOMAIN}") |  Q(requested_url__exact=f"{HTTPS_DOMAIN}en/") | Q(requested_url__exact=f"{HTTPS_DOMAIN}fa/") |
            Q(requested_url__exact=f"{HTTP_W_DOMAIN}") |  Q(requested_url__exact=f"{HTTP_W_DOMAIN}en/") | Q(requested_url__exact=f"{HTTP_W_DOMAIN}fa/") |
            Q(requested_url__exact=f"{HTTPS_W_DOMAIN}") | Q(requested_url__exact=f"{HTTPS_W_DOMAIN}en/") | Q(requested_url__exact=f"{HTTPS_W_DOMAIN}fa/")
        )

            
    
    if filter == 'projects':
        logs = logs.filter(
            Q(requested_url__icontains=f"/projects/")
        )
        
    if filter in ('store', 'office', 'restaurant', 'residential', 'exhibition', 'yektanet'):
        logs = logs.filter(
            requested_url__icontains=f"/projects/categories/{filter}/"
            )
        
    if device and device != 'None':
        try:
            logs = logs.filter(device_type=device)
        except:
            pass

    if base in ('None', None):
        logs_stat = logs.aggregate(count=Sum('url_count'))['count']
    elif base == 'ip':
        logs_stat = logs.aggregate(count=Sum('ip_count'))['count']
    
    today = timezone.now()
    # Create a list of date strings from today until 10 days ago
    dates_list = [
        (today - timedelta(days=i)).strftime('%Y-%m-%d') 
        for i in range(11)  # Include today and the 10 days before
    ]
    # logs = logs[:20]
    # page=None
    # if logs.count() > 100:
    #     # pagination
    #     paginator = Paginator(logs, 25)  # 20 order in each page
    #     page = request.GET.get('page')
    #     try:
    #         logs = paginator.page(page)
    #     except PageNotAnInteger:
    #         # If page is not an integer deliver the first page
    #         logs = paginator.page(1)
    #     except EmptyPage:
    #         # If page is out of range deliver last page of results
    #         logs = paginator.page(paginator.num_pages)
    
    context = dict(
        page_title=_("Analytics"),
        logs=logs,
        logs_stat=logs_stat,
        # page=page,
        date=date,
        filter=filter,
        device=device,
        base=base,
        lan=lan,
        dates_list=dates_list,
    )
    return render(
        request, 
        'analytics/analytics_home.html', 
        context
    )
