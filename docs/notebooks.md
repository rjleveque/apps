(notebooks_intro)=
# Jupyter notebooks

The Jupyter notebook is a very nice platform for illustrating Clawpack examples.

The links below will take you to static view of several notebooks
as html files. You can also play animations in them and interact
with some plots, but to actually run the code yourself you should
clone the apps repository.  Or you can download individual notebooks using
the download button at the top of the page.

**Version:** Most of these notebooks now work with Clawpack 5.14.0.

**Finding the notebooks:** The links below are to html rendered versions
of the notebooks. See the beginning of each notebook for information
on where to find the original `.ipynb` file. Many of them are in the
apps repository, in some subdirectory of `$CLAW/apps/notebooks`.

If you have used Clawpack with the Jupyter notebook and would like
to submit your notebook for inclusion, please send us a link or
submit a pull request to the apps repository.

:::{warning}
The notebooks are not rendering properly on Github, so the output will not
be seen.

You can run them locally via:
    
    git clone https://github.com/rjleveque/apps.git
    cd apps
    git fetch origin jupyter-book:jupyter-book
    git checkout jupyter-book
    jupyter book start --execute

but some of the visclaw notebooks throw errors due to sample data files not
being found.  Work in Progress.
:::

(notebooks_pyclaw)=
## Examples using PyClaw

(notebooks_amrclaw)=
## Examples using AMRClaw

- [`$CLAW/apps/notebooks/amrclaw/RuledRectangles.ipynb`](../notebooks/amrclaw/RuledRectangles.ipynb)

(notebooks_geoclaw)=
## Examples using GeoClaw

- [`$CLAW/apps/notebooks/geoclaw/topotools_examples.ipynb`](../notebooks/geoclaw/topotools_examples.ipynb)

(notebooks_visclaw)=
## Examples using VisClaw

- [`$CLAW/apps/notebooks/visclaw/gridtools.ipynb`](../notebooks/visclaw/gridtools.ipynb)
- [`$CLAW/apps/notebooks/visclaw/pcolorcells.ipynb`](../notebooks/visclaw/pcolorcells.ipynb)
- [`$CLAW/apps/notebooks/visclaw/animation_tools_demo.ipynb`](../notebooks/visclaw/animation_tools_demo.ipynb)

:::{note}
More to appear...
:::
