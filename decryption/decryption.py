__author__ = 'Cyber-01'
import md5
import multiprocessing
import numba
encrypted="EC9C0F7EDCC18A98B1F31853B1813301".lower()
flag=0

def decryptor(info):
    start=info[0]
    end=info[1]
    global flag
    percentage=0
    jumps=(end-start)/100
    recorder=jumps
    while start < end and flag == 0:

        md5format = md5.md5(str(start)).hexdigest()

        if md5format == encrypted:
            print str(start)+"hello"
            flag=1
            return str(start)
            exit()
        start += 1
        if recorder<=0 :
            percentage+=1
            print percentage
            recorder=jumps
        recorder-=1
        start += 1
def divider(parts, start , end):
    jump= end- start
    jump=jump/parts
    sections=[]
    for times in range(parts):
        sections.append([start,start+jump])
        start=start+jump
    #if start != end:
        #sections.append([start,end])
    #print sections
    return sections

@numba.jit
def main():
    print encrypted
    procecess=[]
    start = 10000000000
    end = 99999999999
    devision=divider(8,start,end)
    pool= multiprocessing.Pool()

    x=[pool.map_async(decryptor,devision)]
    print x[0].get()
    #for mission in devision:
      #  procecess.append(multiprocessing.Process(target=decryptor,args=(mission[0],mission[1])))

    #for proce in procecess:
     #   proce.start()


if __name__=="__main__":
    main()