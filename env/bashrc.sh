# Python support
## Load a python script at interpreter startup
export PYTHONSTARTUP=$HOME/python_startup.py
## To debug with ipdb by default
export PYTHONBREAKPOINT=ipdb.set_trace
## To debug just by adding 'ipdb' in front of the program call
alias ipdb='ipdb3 -c continue'
