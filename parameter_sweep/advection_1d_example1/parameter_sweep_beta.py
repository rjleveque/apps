"""
Sample code to run many instances of clawpack in parallel for a
parameter study.

In this example the parameter `beta` specifying the initial conditions
(width of Gaussian) is varied, illustrating how to sweep over a parameter
that is not one of the standard clawpack setrun parameters.  Note that
it is still specified in setrun.py however, as `rundata.probdata.beta`.

The parameter `beta` is also used in plotting the true solution for each 
frame, so notice that the code for calling `plotclaw` has been modified
accordingly below.

The function make_all_cases returns *caselist*, a list of 
dictionaries.  Each dictionary should define whatever parameters
are needed for one case.

The function run_one_case(case) takes a dictionary *case* as input
and does what's necessary to run Clawpack for that one case.

The function run_all is the one called by executing at the command line.
    $ python parameter_sweep_beta.py

You can specify the number of processors to use on the command line,
    $ python parameter_sweep_beta.py 2
If not specified on the command line, the environment variable CLAW_NPROCS
is used, if this is set.  If not, 1 processor is used.

If modifying for a different problem, see in particular the lines starting
with ###.

"""

from numpy import *
import os, time, shutil, sys
from clawpack.clawutil.runclaw import runclaw 

sys.path.insert(0,'..')
from parameter_sweep import run_many_cases
del sys.path[0]
# should eventually move to clawutil and then simplify the above to:
# from clawpack.clawutil.parameter_sweep import run_many_cases

### Specify what should be done...
run_clawpack = True   # True ==> run clawpack for each
make_plots = True  # True ==> will also create _plots directories

# Name of executable:
xclawcmd = 'xclaw'

# Location of setrun function to use for all parameters except
# those changing for each case:
setrun_file = 'setrun.py' 

# Location of setplot file for plotting:
setplot_file = 'setplot.py'
    


if run_clawpack:
    # compile code if necessary
    os.system('make .exe')

if make_plots:
    from clawpack.visclaw.plotclaw import plotclaw


print "run_clawpack = ",run_clawpack
print "make_plots = ",make_plots


def make_all_cases():
    """
    Output: *caselist*, a list of cases to be run.
    Each case should be dictionary of any parameters needed to set up an
    individual case.  These will be used by run_one_case.

    """

    # Create a list of the cases to be run:
    caselist = []

    ### Construct the list of cases with parameters you want to vary.
    ### Also specify the desired name of each outdir and plotdir, 
    ### and where to send python output.

    for beta in [20,1000]:

        # Create all directories needed first, in case there's a problem:
        outdir = '_output_beta%s' % beta
        plotdir = '_plots_beta%s' % beta
        if run_clawpack:
            make_dir(outdir)  # checks before clobbering
        if make_plots:
            make_dir(plotdir)  # checks before clobbering
        # Where to redirect python output:
        python_out = 'python_beta%s.output' % beta

        # Define a dictionary of the parameters needed for this case:
        case = {'beta':beta, \
               'outdir':outdir, 'plotdir':plotdir, 'python_out':python_out}
        caselist.append(case)

    return caselist



def run_one_case(case):
    """
    Input *case* should be a dictionary with any parameters needed to set up
    and run a specific case.
    """

    ### Modify as needed...
    # unpack the dictionary:
    beta = case['beta']
    outdir = case['outdir']
    plotdir = case['plotdir']
    python_out = case['python_out']

    message = ""
    stdout_fname = python_out
    try:
        stdout_file = open(stdout_fname, 'w')
        message = message +  "Python output from this run will go to %s\n" \
                            % stdout_fname
    except:
        raise Exception("Cannot open file %s" % stdout_fname)

    if run_clawpack:
        message = message +  "Fortran output from this run will go to %s\n" \
                            % (outdir+'/nohup.out')
    print message

    # Redirect stdout,stderr so any print statements go to a unique file...
    import sys
    sys_stdout = sys.stdout
    sys.stdout = stdout_file
    sys_stderr = sys.stderr
    sys.stderr = stdout_file


    if run_clawpack:

        setrun_module = os.path.splitext(setrun_file)[0]
        try:
            exec('from %s import setrun' % setrun_module)
        except:
            raise Exception('*** Error importing setrun from %s\n Executing: %s' \
                            % (setrun_file,setrun_module))
    
    
        # initialize rundata using setrun but then change some things for each run:
        rundata = setrun()
    
        ### Modify as needed...
        rundata.probdata.beta = beta
    
        topdir = os.getcwd()
    
        try:
            os.chdir(outdir)
        except:
            raise Exception("*** Cannot chdir into %s" % outdir)
    
        rundata.write()
        os.chdir(topdir)
    
        # Run the executable code in nohup mode.
        # Use data from rundir=outdir, which was just written above...
        runclaw(xclawcmd = xclawcmd, outdir=outdir, rundir=outdir, nohup=True)

    if make_plots:
        print "Plotting using ",setplot_file
        ### we need to import setplot module and modify beta here too
        ### since it is used to plot the true solution in each frame:
        exec('import %s as setplot_module' % os.path.splitext(setplot_file)[0])
        setplot_module.beta = beta
        setplot = setplot_module.setplot
        plotclaw(outdir, plotdir, setplot)  # pass function rather than filename

    # Fix stdout again
    sys.stdout = sys_stdout
    sys.stderr = sys_stderr


def run_all(nprocs):
    """
    Run all cases, splitting between *nprocs* processes.
    """
    caselist = make_all_cases()
    run_many_cases(caselist, nprocs, run_one_case)
    

#------------------
# Utility routines


def make_dir(dir_name):
    """
    Check whether a directory already exists and if so ask before clobbering.
    Then create fresh directory.
    """

    if os.path.exists(dir_name):
        ans = raw_input('\n%s already exists, ok to overwrite? ' \
                        % os.path.abspath(dir_name))
        if ans.lower() not in ['y','yes']:
            raise Exception('*** Aborting')
        else:
            shutil.rmtree(dir_name)
    try:
        os.mkdir(dir_name)
        print "Created directory ",dir_name
    except:
        raise Exception('*** Problem creating directory %s' % dir_name)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use nprocs from command line, if specified
        nprocs = int(sys.argv[1])
    else:
        # Look for environment variable CLAW_NPROCS and if this is not set, use
        # default
        nprocs_default = 1
        nprocs = int(os.environ.get('CLAW_NPROCS', nprocs_default))

    run_all(nprocs)

