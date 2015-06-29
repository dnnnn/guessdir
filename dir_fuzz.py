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

			if r.status_code == 403:
				print colored("[-]403:"+testing_url,'yellow')
				times_403 = times_403+1
			if r.status_code == 302:
				print colored("[-]302:"+testing_url,'yellow')
				times_302 = times_302+1

			if (times_302>30)or(times_403>30)or(times_cant_connect>25):
				print colored("[!]Stop_Fuzz",'red')
				break

if __name__ == '__main__':

    times_403 = 0
    times_302 = 0
    times_cant_connect = 0

    url = 'http://www.wooyun.org'

    fd = open(os.getcwd()+'/dic/dir.txt','r')
    dir_fuzz_list = fd.readlines()
    fd.close()

    q = Queue.Queue(0)
    for i in dir_fuzz_list:
        i = i.strip('\r\n')
        q.put(i)

    Thread_number = 10
    Threads = []
    for i in xrange(0,Thread_number):
        t = Dir_fuzz(url)
        Threads.append(t)

    for i in Threads:
        i.start()

    for i in Threads:
        i.join()
    print "[^]Job Done!"



