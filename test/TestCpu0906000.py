# -*- coding: utf-8 -*-
import os, re, sys
import subprocess
import time, os, sched, shlex, threading
# import numpy as np
import datetime

# devices=(sys.argv[1])
# pkg_name=(sys.argv[2])
totaltime=int(sys.argv[3]) #总时间，单位秒
def get_pid(pkg_name):
    pid = subprocess.Popen("adb shell ps | findstr " + pkg_name, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE).stdout.readlines()

    for item in pid:
        if item.split()[8].decode() == pkg_name:
            print item.split()[1].decode()
            return item.split()[1].decode()




def get_cpu_kel(devices):
    cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
    output = subprocess.check_output(cmd).split()
    sitem = ".".join([x.decode() for x in output])  # 转换为string
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

'''
计算某进程的cpu使用率
100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
cpukel cpu几核
pid 进程id
'''
def cpu_rate(pid, cpukel, devices,totaltime):
    num=0
    cpu=0.0
    list_cpu=[]

    for num in range(0, totaltime):
        totalCpuTime1 = totalCpuTime(devices)
        processCpuTime1 = processCpuTime(pid, devices)

        time.sleep(1)#间隔时间，单位秒

        totalCpuTime2 = totalCpuTime(devices)
        totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)*cpukel
        processCpuTime2 = processCpuTime(pid, devices)
        processCpuTime3 = processCpuTime2 - processCpuTime1
        cpu = '%.3f' % float(100.000 * (processCpuTime3) * get_cpu_kel(devices) / (totalCpuTime3))
        print cpu
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        listcpu = str(ts) + ' ' + str(sys.argv[2]) + ' ' + cpu
        # cpu_mean = str(ts) + ' ' + cpu_mean
        result3 = "./list_cpu.txt"
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
    pid=get_pid(sys.argv[2])
    # print pid
    cpukel=get_cpu_kel(sys.argv[1])
    devices=sys.argv[1]
    list_cpu, cpu_mean = cpu_rate(pid, cpukel, devices,totaltime)
    print cpu_mean

    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    cpu_mean = str(ts) + ' ' + str(sys.argv[2]) + ' ' + cpu_mean
    # cpu_mean = str(ts) + ' ' + cpu_mean
    result2 = "./cpu_mean.txt"
    f = open(result2, 'a')
    f.write(cpu_mean + '\n')
    f.close()
