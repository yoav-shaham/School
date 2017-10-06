__author__ = 'Cyber-01'
import md5

encrypted="EC9C0F7EDCC18A98B1F31853B1813301"



def main():
    flag=0
    start=10000000000
    end=99999999999
    while start < end and flag==0:
        md5format=md5.md5(str(start)).hexdigest()
        if md5format==encrypted:
            print start
            exit()
        start+=1


if __name__=="__main__":
    main()