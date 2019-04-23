#! /usr/bin/env python
# some code borrowed from Chunyang, thanks!

import os
import sys

user_name = 'qd212'
my_name = 'QINGYUN'
print '\n'*3
tot = float(os.popen("qstat -u '*' | grep ' r ' | wc -l").readline().strip())
tot_cuda = float(os.popen("qstat -u '*' | grep 'cuda-low' | wc -l").readline().strip())
tot_cuda_list = (os.popen("qstat -u '*' | grep 'cuda'")).readlines()
my = float(os.popen("qstat -u "+user_name+" | grep ' r ' | wc -l").readline().strip())
my_cuda = float(os.popen("qstat -u "+user_name+" | grep 'cuda' | wc -l").readline().strip())
my_cpu  = float(os.popen("qstat -u "+user_name+" | grep 'all-low' | wc -l").readline().strip())
my_wait = os.popen("qstat -u "+user_name+" | grep 'qw '").readlines()

num_gpu = {'air200': 2,'air201': 2,'air202': 2,'air203': 2,'air204': 4,'air205': 4,'air206': 4,'air207': 4,'air208': 4,'air209': 4}

print '\nCUDA Job list:'
with os.popen("qstat -u '*' | grep 'cuda-low'") as f:
  f_list = []
  for x in range(200,210):
    num_gpu_running = sum([('air'+str(x)) in i for i in tot_cuda_list])
    f_list.append('-'*25+' '*2+'Cuda jobs running @air'+str(x)+' '*2+'-'*40+'  air'+str(x)+'  '+str(num_gpu_running)+'   '+str(num_gpu['air'+str(x)]-num_gpu_running)+'.')
  f_list.extend(f.readlines())
  f_list.sort(key=lambda x: x.strip().split('@')[1][3:6])
  for f_line in f_list:
    if f_line.strip().split(' ')[3]==user_name:
      # print '-'*100
      print f_line.strip()[:-1]
      job_id = f_line.strip().split(' ')[0]
      str_temp = os.popen("qstat -j "+job_id+" | head -n15").readlines()[12].strip()
      print ' '*(110-len(str_temp))+str_temp+' '*2+job_id#*(86-len(os.popen("qstat -j "+job_id+" | head -n15").readlines()[12].strip()))+'*'*5
      # print '-'*100
    else:
      print f_line.strip()[:-1]
print '\nTOTAL_JOBS =', int(tot)
print my_name+'_JOBS =', int(my_cpu)
print '\n'
print 'TOTAL_CUDA_JOBS =', int(tot_cuda)
print my_name+'_CUDA_JOBS =', int(my_cuda)
# print 'RATE =', my / tot
if len(my_wait) > 0:
  print '\nMy waiting jobs are:'+' '*2+'_'*70
  for f_line in my_wait:
    print f_line.strip()[:-1]
    job_id = f_line.strip().split(' ')[0]
    print ' '*35+os.popen("qstat -j "+job_id+" | head -n15").readlines()[12].strip()+' '*2+'*'#*(86-len(os.popen("qstat -j "+job_id+" | head -n15").readlines()[12].strip()))
print '\n'

if my_cpu > 0:
  print '\nCPU Job list:'+' '*9+'_'*70
  with os.popen("qstat -u "+user_name+" | grep 'all-low'") as f:
    f_list = []
    f_list.extend(f.readlines())
    f_list.sort(key=lambda x: x.strip().split('@')[1][3:6])
    for f_line in f_list:
      print f_line.strip()[:-1]
      job_id = f_line.strip().split(' ')[0]
      str_temp = os.popen("qstat -j "+job_id+" | head -n15").readlines()[12].strip()
      print ' '*(100-len(str_temp))+str_temp+' '*2+'*'#
