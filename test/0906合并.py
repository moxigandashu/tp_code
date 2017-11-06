#-*-coding:utf-8-*-
'''
Created on 2017年9月6日

@author: Administrator
'''
import subprocess
from datetime import datetime
import os, re, sys
import time, os, sched, shlex, threading

devices=(sys.argv[1])
pkg_name=(sys.argv[2])
totaltime=int(sys.argv[3]) #总时间，单位秒
def getProcessId(ProcessName):
    pid = subprocess.Popen("adb shell ps | grep " + ProcessName, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE).stdout.readlines()

    for item in pid:
        if item.split()[8].decode() == ProcessName:
            #print item.split()[1].decode()
            return item.split()[1].decode()
    
#Get process user ID input parameter is process ID    
def getProcessUid(ProcessId):
    getUidcmd='adb shell cat /proc/'+ProcessId+'/status|grep Uid'
    p=subprocess.Popen(getUidcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    content_Uid=p.stdout.readlines()        
    try:
        UidList=content_Uid[0].strip().split('\t')
        #print UidList
        ProcessUid=UidList[1]
        return ProcessUid
    except TypeError:
        return 

#Get process uplink and downlink traffic
def getProcessTraffic(ProcessName):
    try:
        ProcessId=getProcessId(ProcessName)
        ProcessUid=getProcessUid(ProcessId)
        rxTraffic=[]
        txTraffic=[]
        #Traffic_list=[]
        #Traffic=''
        getProcessTrafficcmd='adb shell cat /proc/net/xt_qtaguid/stats | grep ' + ProcessUid
        p=subprocess.Popen(getProcessTrafficcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        try:
            #/proc/net/xt_qyaguid/stats the 5th column is downlink (receive) traffic, the 7th column is the uplink(transmit)
            for line in p.stdout.readlines():
                rx_bytes=line.split()[5]
                rxTraffic.append(int(rx_bytes))
                tx_bytes=line.split()[7]
                txTraffic.append(int(tx_bytes))
            T=1024 #Unit transferred, from bytes to Kb
            Traffic_info=str(sum(rxTraffic)/T)+','+str(sum(txTraffic)/T)
            #print Traffic_info
            return Traffic_info
        except ValueError:
            return "Process not found!"
    except (UnboundLocalError,TypeError):
        return

def get_cpu_kel(devices):
    cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
    output = subprocess.check_output(cmd,shell=True).split()
    sitem = ".".join([x.decode() for x in output])  # 杞崲涓簊tring
    return len(re.findall("processor", sitem))



def totalCpuTime(devices):
    user=nice=system=idle=iowait=irq=softirq= 0
    cmd = "adb -s " + devices +" shell cat /proc/stat"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()

    for info in res:
        if info.decode() == "cpu":
            user = res[1].decode()
            nice = res[2].decode()
            system = res[3].decode()
            idle = res[4].decode()
            iowait = res[5].decode()
            irq = res[6].decode()
            softirq = res[7].decode()
            result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
            return result


def processCpuTime(pid, devices):
    # pid = str(pid)
    # pid=get_pid(pkg_name)
    utime=stime=cutime=cstime = 0
    cmd = "adb -s "+ devices + " shell cat /proc/" + pid +"/stat"
    # print(cmd)
    # pid = int(pid)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    res = output.split()
    utime = res[13].decode()
    stime = res[14].decode()
    cutime = res[15].decode()
    cstime = res[16].decode()

    result1 = int(utime) + int(stime) + int(cutime) + int(cstime)

    return result1

def cpu_rate(pid, cpukel, devices,totaltime):
    num=0
    cpu=0.0
    list_cpu=[]

    for num in range(0, totaltime):
        totalCpuTime1 = totalCpuTime(devices)
        processCpuTime1 = processCpuTime(pid, devices)

        time.sleep(1)#闂撮殧鏃堕棿锛屽崟浣嶇

        totalCpuTime2 = totalCpuTime(devices)
        totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)*cpukel
        processCpuTime2 = processCpuTime(pid, devices)
        processCpuTime3 = processCpuTime2 - processCpuTime1
        cpu = '%.3f' % float(100.000 * (processCpuTime3) * get_cpu_kel(devices) / (totalCpuTime3))
#         print cpu
        traffic=getProcessTraffic(pkg_name)
        ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        listcpu = str(ts) + ' ' + str(sys.argv[2]) + ' ' + cpu+' '+traffic
        # cpu_mean = str(ts) + ' ' + cpu_mean
        result3 = "./list_cpu0907.txt"
        f = open(result3, 'a')
        f.write(listcpu + '\n')
        f.close()
        list_cpu.append(cpu)
        num += 1
    print num
    list_cpu = map(eval, list_cpu)
    print list_cpu
    cpu_mean='%.3f' % float(sum(list_cpu)/num)
    return  list_cpu, cpu_mean

if __name__ == "__main__":     
    devices=(sys.argv[1])
    pkg_name=(sys.argv[2])
    totaltime=int(sys.argv[3]) 
    pid=getProcessId(sys.argv[2])
    Traffic_start=getProcessTraffic(sys.argv[2])
    #print "Traffic_start:"+Traffic_start
    cpukel=get_cpu_kel(sys.argv[1])
    list_cpu, cpu_mean = cpu_rate(pid, cpukel, devices,totaltime)
    Traffic_end=getProcessTraffic(sys.argv[2])
    print "Traffic_end:"+Traffic_end
    print cpu_mean
    
    
    
    ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    cpu_mean = str(ts) + ' ' + str(sys.argv[2]) + ' ' + cpu_mean+'Traffic_start: '+Traffic_start+' Traffic_end: '+Traffic_end
    # cpu_mean = str(ts) + ' ' + cpu_mean
    result2 = "./0907CPU+Traffic.txt"
    f = open(result2, 'a')
    f.write(cpu_mean + '\n')
    f.close()

#             
#main function, set which process need to detect, set how long output the traffic information once. 
# def main():
#     #ProcessName="com.cootek.smartdialer"  #Set the need detect Process Name
#     ProcessName="com.cootek.smartdialer_oem_all_module"  #Set the need detect Process Name
#     #ProcessName="com.skype.rover"  #Set the need detect Process Name
#     #ProcessName="com.tencent.mm"  #Set the need detect Process Name
#     #filename='TrafiicAndCpu_3G4G.txt'                       #Save information to file
#     #ProcessName="swift.free.phone.call.wifi.chat"
#     filename='0906Test.txt' 
#     try:
#         starttime=datetime.now() 
#         while 1: #loop until interrupt
#             Traffic=getProcessTraffic(ProcessName)#call the traffic calculate function
#             #print Traffic
#             currentTime=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
#             Info=currentTime+'  '+ProcessName+'  3G/4G'+'  '+Traffic
#             print Info                     #display the information in cmd or not
#             File=open(filename,'a')
#             File.write(str(Info))
#             File.write('\n')
#             File.close()                               
#             time.sleep(5)   
#             endtime=datetime.now()
#             if (endtime-starttime).seconds>=300:
#                 File=open(filename,'a')
#                 File.write('\n\n\n')
#                 File.close()           
#                 break                    #how long seconds print the information once
#     except TypeError:
#         return 
#         print "Process is not running."                  
    
  
          
