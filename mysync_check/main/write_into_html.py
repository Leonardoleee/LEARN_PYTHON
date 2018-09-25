#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from main.sql_exec_out import *
from jinja2 import PackageLoader, Environment
import datetime

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def fill_html(zk3_info, rdsm_info, rdss_info, now, stat1, stat2):
    env = Environment(loader=PackageLoader('mysync_check', 'templates'))
    template = env.get_template('sync_info.html')
    END_TIME =  datetime.datetime.now()
    fill_html_result = template.render(zk3_info=zk3_info, rdsm_info=rdsm_info, rdss_info=rdss_info, now=now, stat1=stat1, stat2=stat2)
    return fill_html_result

def create_html(filename,start_time):
    fname = filename

    with open(fname, 'w') as f:
        html = fill_html(zk3_info, rdsm_info, rdss_info, now, stat1, stat2)
        f.write(html)
