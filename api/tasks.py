from celery import shared_task
import time
from django.core.cache import cache

@shared_task
def mul(a,b):
    # time.sleep(5)
    return a*b

# increase count using cache value stored into redis 
@shared_task
def visit_cache():
    count = cache.get('visits',0)
    count +=1
    cache.set('visits',count,timeout=None)
    time.sleep(50)
    return count