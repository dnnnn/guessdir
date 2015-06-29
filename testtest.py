import Queue

q = Queue.Queue()


list_test = ['abc','bcd','cde','dede']
for i in list_test:
	q.put(i)


print q.qsize()
print q.empty()

print q.get()

