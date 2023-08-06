def infinite():
	n=0
	while 'n==5':
		yield n
		n=n+1

k=infinite()
print k.next()
print k.next()
print k.next()
print k.next()
print k.next()
print k.next()
print k.next()
print k.next()