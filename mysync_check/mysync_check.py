#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os, time, datetime, traceback
from main import write_into_html, sql_exec_out, sendmail

time_stamp = time.strftime("%Y-%m-%d", time.localtime())
START_TIME = datetime.datetime.now()
(APP_PATH, APP_NAME) = os.path.split(os.path.realpath(__file__))

def sync_stat():
    fname = APP_PATH + "/sync_info_" + time_stamp + ".html"
    try:
        write_into_html.create_html(filename=fname, start_time=START_TIME)
        sendmail.send_mail()
    except Exception as e:
        print("ERROR:\t", e)
        traceback.print_exc()

if __name__ == "__main__":
    try:
        sync_stat()
    except Exception as e:
        print(e)
