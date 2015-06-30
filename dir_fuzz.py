#!/usr/bin/env python
# encoding: utf-8

import requests,threading
from urllib import quote
from termcolor import colored
import os,sys
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')

class Dir_fuzz(threading.Thread):
	def __init__(self,fuzz_init_url=''):
		threading.Thread.__init__(self)
		self.fuzz_init_url = fuzz_init_url

	def run(self):

		while q.empty() == False:

			global times_403
			global times_302
			global times_200
			global times_cant_connect

			testing_path = q.get()
			dir_fuzz_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		    'Accept':'text/html;q=0.9,*/*;q=0.8',
		    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		    'Accept-Encoding':'gzip',
		    'Connection':'close',
		    'Referer':self.fuzz_init_url}

			testing_url = self.fuzz_init_url+quote(testing_path)
			print "[-]Test:"+testing_url

			try:
				r = requests.get(testing_url,headers=dir_fuzz_header,timeout=10,verify=False)
			except Exception, e:
				print colored("[!]Can't Connect!",'yellow')
				times_cant_connect = times_cant_connect+1

			if r.status_code == 200:
				print colored("[+]200:"+testing_url,'green')
				rcode200_url.append(testing_url)
				times_200 = times_200+1

			if r.status_code == 403:
				print colored("[-]403:"+testing_url,'yellow')
				rcode403_url.append(testing_url)
				times_403 = times_403+1

			if r.status_code == 302:
				print colored("[-]302:"+testing_url,'yellow')
				rcode302_url.append(testing_url)
				times_302 = times_302+1

			if (times_302>35)or(times_403>35)or(times_cant_connect>35)or(times_200>45):
				print colored("[!]Stop_Fuzz!",'red')
				break

if __name__ == '__main__':

    times_403 = 0
    times_302 = 0
    times_200 = 0
    times_cant_connect = 0

    rcode200_url = []
    rcode302_url = []
    rcode403_url = []

    url = 'http://www.gongzhengcar.net/'

    fd = open(os.getcwd()+'/dic/dir.txt','r')
    dir_fuzz_list = fd.readlines()
    fd.close()

    q = Queue.Queue(0)
    for i in dir_fuzz_list:
        i = i.strip('\r\n')
        q.put(i)

    Thread_number = 15
    Threads = []
    for i in xrange(0,Thread_number):
        t = Dir_fuzz(url)
        Threads.append(t)

    for i in Threads:
        i.start()

    for i in Threads:
        i.join()

    for i in rcode200_url:
        print colored("[+]response code 200||"+i,'green')
    for i in rcode302_url:
        print colored("[+]response code 302||"+i,'yellow')
    for i in rcode403_url:
        print colored("[+]response code 403||"+i,'yellow')

    print "[^]Job Done!"



