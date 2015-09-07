"""
Generic code to run a sequence of cases in parallel.

To try it out:
    $ python run_parallel.py nprocs
where nprocs is the number of processors to use.  This will run the
sample code below.  


To modify for your problem:

Define a function make_all_cases that returns a *caselist*, a list of 
dictionaries.  Each dictionary should define whatever parameters
are needed for one case.

Define a function run_one_case(case) that takes a dictionary *case* as input
and does whatever necessary to run that one case.

Import this module and call
    run_many_cases(caselist, nprocs, run_one_case)

This module contains templates run_one_case_sample and make_all_cases_sample.

"""

import os, time, sys
from multiprocessing import Process, current_process
import atexit    # Exit handling

def run_many_cases(caselist, nprocs, run_one_case):
    """
    Split up cases in *caselist* between the *nprocs* processors.
    Each case is a dictionary of parameters for that case.

    *run_one_case* should be a function with a single input *case*
    that runs a single case. 
    """

    # Split up cases between nprocs processors:
    # caseproc[i] will be a list of all cases to be handled by processor i
    caseproc = [[] for p in range(nprocs)]
    for i in range(len(caselist)):
        caseproc[i%nprocs].append(caselist[i])

    # for debugging:
    #print "+++ caseproc: ", caseproc

    print "\n%s cases will be run on %s processors" % (len(caselist),nprocs)

    ans = raw_input("OK to run? ")
    if ans.lower() not in ['y','yes']:
        raise Exception("*** Aborting")
    

    def run_cases(procnum):
        # loop over all cases assigned to one processor:
        p = current_process()
        message =  "\nProcess %s will run these cases:\n" % p.pid
        for case in caseproc[procnum]:
            message = message + "  %s \n" % case
        print message # constructed first to avoid interleaving prints
        time.sleep(1)

        for case in caseproc[procnum]:
            print "\nProcess %s now running this case: %s" % (p.pid, case)
            run_one_case(case)

    plist = [Process(target=run_cases, args=(p,)) for p in range(nprocs)]

    # Handle termination of subprocesses in case user terminates the main process
    def terminate_procs():
        for P in plist:
            if P.is_alive():
                P.terminate()
    atexit.register(terminate_procs)

    print "\n=========================================\n"
    for P in plist:
        P.start()
        print "Starting process: ",P.pid
    for P in plist:
        P.join()


#==================================
# Sample code below to illustrate:
#==================================

def make_all_cases_sample():
    """
    Output: *caselist*, a list of cases to be run.
    Each case should be dictionary of any parameters needed to set up an
    individual case.  These will be used by run_one_case.

    This is a sample where each case has a single parameter 'num'.
    Specialize this code to the problem at hand.
    """

    # Create a list of the cases to be run:
    caselist = []

    for num in range(7):
        case = {'num': num}
        caselist.append(case)

    return caselist



def run_one_case_sample(case):
    """
    Generic code, must be specialized to the problem at hand.
    Input *case* should be a dictionary with any parameters needed to set up
    and run a specific case.
    """

    # For this sample, case['num'] is just an identifying number.
    print 'Sample job... now running case ',case['num']
    
    # This part shows how to redirect stdout so output from any
    # print statements go to a unique file...
    import sys
    sys_stdout = sys.stdout
    sys.stdout = open('case%s.out' % case['num'], 'w')
    print 'Working on case ',case['num']
    time.sleep(1)
    print 'Still working on case ',case['num']
    time.sleep(1)
    print 'Done with case ',case['num']
    # Fix stdout again
    sys.stdout = sys_stdout




if __name__ == "__main__":
    
    # If executed at command line, run the sample code above...

    if len(sys.argv) > 1:
        nprocs = int(sys.argv[1])
    else:
        nprocs = 1

    caselist = make_all_cases_sample()
    run_many_cases(caselist, nprocs, run_one_case=run_one_case_sample)
    print "Done... See files caseN.out for python output from each case"
