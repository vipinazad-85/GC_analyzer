#!/usr/bin/python
import os
import datetime
import fnmatch
import shutil


path = sys.argv[1]
log_dir = "/tmp/slowness"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

servers = [t for t in os.listdir(path)]

l = len(servers)

print ("\n")


def gc(f):
    cnt = G = 0
    l = []
    for line in f:
        if fnmatch.fnmatch(line, '*[Full*'):
            s = line.split(" ")
            if len(s) > 15 and len(s) < 20:
                st = str(s[0])
                if int(float(s[11])) > 6:
                    cnt += 1
                    l.append(st[:16])
                if int(float(s[11])) > 10:
                    G += 1

    ll = len(l)
    ls = len(set(l))
    return cnt,  G, ll,ls

for i in range(l):
    pathgc = path + str(servers[i]) + '/logs/'
    tf = [t for t in os.listdir(pathgc) if fnmatch.fnmatch(t, '*.out*')]
    tf = sorted(tf, key=lambda tf: os.path.getmtime(os.path.join(pathgc, tf)), reverse=True)
    tf = tf[:3]
    for k in range(3):
 		File = pathgc + str(tf[k])
        with open(File, 'r') as f:
            cnt, G, ll,ls = gc(f)
            a = File.split("/")
            if cnt > 100 or ll > ls:
                shutil.copy(File, log_dir)
                print ("High Heap pressure found on Server  = {0}".format(a[7]))
                print ("Please check file {0} for GC details".format(File))
                print ("Total no of Full GC took more than 6 sec : {0}".format(cnt))
                print ("Total no of Full GC took more than 10 sec : {0}".format(G))
                print ("\n")
