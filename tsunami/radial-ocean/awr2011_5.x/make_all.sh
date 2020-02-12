
make .exe

make data -f Makefile_220
make topo -f Makefile_220
make output -f Makefile_220
make plots -f Makefile_220

make data -f Makefile_260
make topo -f Makefile_260
make output -f Makefile_260
make plots -f Makefile_260

python compare_gauges.py

# To make other plots in paper:
python plot_ocean.py
python plot_xsec.py