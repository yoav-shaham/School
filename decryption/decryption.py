__author__ = 'Cyber-01'
import hashlib
import multiprocessing
import myglobals
encrypted="EC9C0F7EDCC18A98B1F31853B1813301".lower()
flag=None

def init(args):
    global flag
    flag=args
def decryptor(info):
    print(encrypted)
    start=long(info[0])
    end=long(info[1])
    percentage=0
    jumps=(end-start)/100
    recorder=jumps
    global flag
    while start < end and flag.value == 0:
        md5format = hashlib.md5(str(start)).hexdigest()

        if md5format == encrypted:
            flag.value=1
            return str(start)
        start += 1
        if recorder<=0 :
            percentage+=1
            print percentage
            recorder=jumps
        recorder-=1
def divider(parts, start , end):
    jump= end- start
    jump=jump/parts
    sections=[]
    for times in range(parts):
        sections.append([start,start+jump])
        start=start+jump
    return sections

def main():
    myglobals.data=0
    print encrypted

    procecess=[]
    start = 1000000000
    end = 9999999999
    devision=divider(8,start,end,)
    pool= multiprocessing.Pool(initializer = init, initargs = (flag, ))
    x=pool.map_async(decryptor,devision,chunksize = 1)
    print x.wait()
    print x.get()

if __name__=="__main__":
    flag = multiprocessing.Value('i', 0)
    main()
