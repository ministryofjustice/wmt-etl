# Workload Management Tool - Data Import application

### Set-up Python Dev environment
Python development uses [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/index.html) to provide dependency isolation.

To set up Python and VirtualEnv install as follows:

`brew install python`
`pip install virtualenvwrapper`

Add the following lines to your `~/.bash_profile`:

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Run `source ~/.bash_profile` in order for these changes to take immediate effect

From the base project directory execute the following command to set up your environment:

`mkvirtualenv -a wmt-etl -r requirements.txt wmt-etl` 

All subsequent times you want to work on this project you should just need to type:

`workon wmt-etl`

And it will switch to this virtualenv and take you to the ./wmt-etl directory.

### Running the ETL Job

To run the example ETL file, first ensure that the local development DB is running and execute the following script to submit it for execution:

`python etl.py`
