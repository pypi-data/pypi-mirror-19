#coding=utf-8
import sys
import threading
from time import ctime,sleep
from httplib import HTTPConnection



#####################################################################
#coding=utf-8
HOST = "10.3.41.4"; #主机地址 例如192.168.1.101  
PORT = 90 #端口  
URI = "/" #相对地址,加参数防止缓存，否则可能会返回304  
TOTAL = 0 #总数  
SUCC = 0 #响应成功数  
FAIL = 0 #响应失败数  
EXCEPT = 0 #响应异常数  
MAXTIME=0 #最大响应时间  
MINTIME=100 #最小响应时间，初始值为100秒  
GT3=0 #统计3秒内响应的  
LT3=0 #统计大于3秒响应的 

max =9


list=[] 
for i in range(max): 
    list.append(i) 
print(list)



def move(func):
    for i in range(9):
        print "Thread %s! is running %s" %(func,ctime())
        try:  
            st = ctime()  
            conn = HTTPConnection(HOST, PORT, False)    
            conn.request('GET', URI)  
            res = conn.getresponse() 
            #print 'HOST', HOST
            #print 'URI', URI
            #print 'PORT', PORT   
            #print 'version:', res.version    
            #print 'reason:', res.reason    
            #print 'status:', res.status    
            #print 'msg:', res.msg    
            #print 'headers:', res.getheaders()                    
        except Exception,e:  
            print e  
        conn.close()  




threads = []
files = range(len(list))


#创建线程
for i in files:
    t = threading.Thread(target=move,args=(list[i],))
    threads.append(t)


if __name__ == '__main__': 
    for i in files:
        threads[i].start()

    #主线程
    print 'end:%s' %ctime()
