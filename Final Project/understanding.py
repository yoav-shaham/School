def createGenerator():
    yield 1
    yield 2
    yield 3
    yield 4

mygenerator = createGenerator() # create a generator
x=0
for i in mygenerator:
    print i
    if i==2:
        break
print "hey"
for i in mygenerator:
    print i
print "hello"

