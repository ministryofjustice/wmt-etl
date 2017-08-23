# Workload Management Tool - Data Import application

![Build Status](https://travis-ci.org/ministryofjustice/wmt-etl.svg?branch=master)

### Set-up Python Dev environment
Python development uses [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/index.html) to provide dependency isolation.

To set up Python and VirtualEnv install as follows:

```
brew install python
pip install virtualenvwrapper
brew install unixodbc
```

Install the ODBC Driver and SQLCMD utility for Mac:

```
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
ACCEPT_EULA=y brew install --no-sandbox msodbcsql mssql-tools
```

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

### Linting & Testing

In the base directory run the following command to execute pylint:

`pylint wmt_etl/`

In the base directory run the following command to execute unit tests (ignoring those marked integration):

`python -m pytest wmt_etl/`

To include integration tests in the run, specify the following addtional command line arg:

`python -m pytest --integration wmt_etl/`

### Running the ETL Job

This job is dependant on the creation of the application database with staging schema.

This is defined in the [WMT Worker](https://github.com/ministryofjustice/wmt-worker) repository which includes information on running the required migration scripts.

To run the example ETL file, first ensure that the local development DB is running and execute the following script to submit it for execution:

`python start.py`

### Troubleshooting

Ensure that your python directory points to `/usr/local/bin`. To disocver this, run `which python`.

If you get the following error message when running the virtualenvwrapper:

`/usr/local/bin : permission denied`

Run the following command and that should resolve it:

`sudo chown -R $(whoami) /usr/local/bin`

If you make a change to the path variable in your relative .rc file, then open a new terminal tab as these tend to be cached.