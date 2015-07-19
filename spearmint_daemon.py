#!/usr/bin/env python
import json,os,sys,time
import numpy as np
from optparse import OptionParser

#custom modules
from spearmint_shunt import Experiment

def main():
    usage = '%prog [options]'
    parser = OptionParser(usage)
    parser.add_option("-n","--niter",type="int",default=10,\
        help="number of optimization steps")
    parser.add_option("-l","--limit",type="int",default=5,\
        help="limit for checking whether a job has finished")
    parser.add_option("-s","--sleep",type="int",default=60,\
        help="sleep time between job checks in seconds")
    parser.add_option("--path",type="string",default=os.getcwd(),\
        help="path to experiment directory")
    (options, args) = parser.parse_args()
    global path
    path = options.path
    run(options.niter,options.limit,options.sleep)

def run(niter,limit,sleep):
    paramsJson = open('%s/spearmint_params.json'%path).read()
    params = json.loads(paramsJson)
    scientist = Experiment(name         = params['experiment']['name'],
                           description  = params['experiment']['description'],
                           parameters   = params['parameters'],
                           outcome      = params['outcome'],
                           path         = '%s/%s.json'%(path,\
                                                        params['database_name']))
    for i in xrange(niter):
        jobFinished = False
        count = 0
        job = scientist.suggest()
        job = parseValues(job,params)
        submit_job(job)
        print "\nJob status:"
        print "-----------"
        print ""
        while not jobFinished and count<=limit:
            jobId = getJobId()
            jobFinished,info = checkJobStatus(jobId)
            if not jobFinished:
                print "%i: \n%s"%(count,str(info))
                time.sleep(sleep)
                count+=1
        print "\nJob done!"
        print "---------"
        print ""
        try:
            accuracy = getAccuracy(job)
            print 'Accuracy: %s'%str(accuracy)
            scientist.update(job,accuracy)
        except IOError:
            os.system('python %s/sendEmail.py'%path)
            print "Unable to read last accuracy file with params: %s!"%str(job)


def submit_job(job):
    filename = 'Opt_job'
    for key in job.keys():
        filename+='_%s_%s'%(key,str(job[key]))
    filename+=".jdf"
    jdfFile = "%s/jobs/%s"%(path,filename)
    f = open(jdfFile,'w')
    content = [
        '#!/bin/bash',
        '\n#PBS -d %s'%path,
        '\n#PBS -j oe',
        '\n#PBS -l mppwidth=1',
        '\n#PBS -N opt_daemon',
        '\n#PBS -o %s/output'%path,
        '\n#PBS -q premium',
        '\n#PBS -l walltime=00:10:00',
        '\n#PBS -V',
        '\nmodule load python/2.7-anaconda'
        '\ncd $PBS_O_WORKDIR',
        '\npython %s/runSVM.py -C %s --degree %s'%(path,str(job["C"]),str(job["degree"]))
        ]
    f.writelines(content)
    f.close()
    os.system('qsub %s > %s/jobId.txt'%(jdfFile,path))

def parseValues(job,params):
    p = params["parameters"]
    for key in job.keys():
        if p[key]['type']=='integer':
            job[key] = int(job[key])
        elif p[key]['type']=='float':
            job[key] = float(job[key])
    return job

def getAccuracy(job):
    filename = '%s/results/Accuracy'%path
    for key in job.keys():
        filename+='_%s_%s'%(key,str(job[key]))
    filename+=".txt"
    f = open(str(filename),'r')
    accuracy = f.readlines()[0]
    f.close()
    return float(accuracy)

def checkJobStatus(jobId):
    statusFile = '%s/status.txt'%path
    os.system('qstat -u %s | grep %s > %s'%(os.getlogin(),jobId,statusFile))
    f = open(statusFile,'r')
    line = f.read()
    if line=='':
        return True,line
    else:    
        status = line.split()[-2]
        if status=='C':
            return True,line
        else:
            return False,line

def getJobId():
    jobIdFile = '%s/jobId.txt'%path
    f = open(jobIdFile,'r')
    line = f.read()
    jobId = line.split('.')[0]
    return jobId 

if __name__=='__main__':
    main()
