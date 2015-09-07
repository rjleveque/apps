
.. _apps_parameter_sweep_advection_1d_example1:

Sample code to run parameter sweeps in parallel
================================================

Run the sample code from `$CLAW/classic/examples/advection_1d_example1` for
various parameter values, and create a separate `_output` and `_plots` 
directory for each.

The code in `parameter_sweep_mx.py` runs for 3 different grid resolutions 
denoted by `mx = clawdata.num_cells[0]`.  Run via:

```
    python parameter_sweep_mx.py N
```
where `N` is the number of processors to use.  If `N >= 3` and you have
sufficient cores, the 3 cases will run in parallel.  If `N < 3` they will be
distributed.  

The code in `parameter_sweep_beta.py` runs for 2 different values of the
user parameter `beta`, used in the initial conditions and also in plotting
the true solution.  Run via:

```
    python parameter_sweep_beta.py 2
```
for example.


The python module `parameter_sweep.py` is needed.
Currently this is in the directory `..` but should eventually be moved to
`clawutil`?

Version history:  
----------------

- Added 7 September 2015 by @rjleveque
- This version works with Clawpack 5.3.0 

