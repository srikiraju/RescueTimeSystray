import datetime
import socket
import pprint
import os
import thread
import time
import objc
import system_tray_icon
import pdb
import ConfigParser
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

from rescuetime.api.service.Service import Service
from rescuetime.api.access.AnalyticApiKey import AnalyticApiKey
from rescuetime.api.model.ResponseData import ResponseData

_timer = None;
apiKey = "";

def get_current_productivity():
	# get today's productivity scores from the service
    s = Service()
    key = AnalyticApiKey(apiKey, s)
    params = {'op': 'select',
	          'vn': 0,
			  'pv': 'interval',
			  'rs': 'hour',
			  'rb': (datetime.date.today() - datetime.timedelta(days = 1)).strftime('%Y-%m-%d'),
			  're': datetime.date.today().strftime('%Y-%m-%d'),
			  'rk': 'efficiency'}
    r = ResponseData(key, **params)
    r.sync()

    res = r.object['rows']
    prod_graph = []

    #Pull data for last 5 hours
    for i in range(6):
        rec_seconds = 0
        rec_prod = 0
        for ro in reversed(res):
            if ro[0] == (datetime.datetime.today() - datetime.timedelta(hours = i)).strftime('%Y-%m-%dT%H:00:00'):
                prod_graph.insert(0, ro[4])
        if len(prod_graph) < i + 1:
            prod_graph.insert(0,50)

    mins = datetime.datetime.today().time().minute
    cur_prod = (60-mins) * prod_graph[4] + mins * prod_graph[5]
    cur_prod = cur_prod/60
    prod_graph[5] = cur_prod

    return prod_graph

def show_current_productivity(app):
    try:
        # get current productivity and update system tray icon
        productivity = get_current_productivity()
        #icon_filename = "digits/" + str(productivity) + '.ico'
        app.set_image(productivity)
    except:
        pass

def _timer_action():
    show_current_productivity(_timer)

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read("key.cfg")
    apiKey = config.get("rescuetime","apikey")
    socket.setdefaulttimeout(20)
    app = NSApplication.sharedApplication()
    _timer = system_tray_icon.Timer.alloc().init()
    _timer.set_timer_method(_timer_action)
    app.setDelegate_(_timer)
    AppHelper.runEventLoop()
