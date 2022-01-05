## INSTALLATION
**Windows**
```
cd <PROJECT_DIR>
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
**Linux**
```
cd <PROJECT_DIR>
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## CONFIGURATION
1. [Database connection](https://github.com/denisdenisi4/SiteUserStats/blob/main/app.py#L10-L13).
2. [Database table name](https://github.com/denisdenisi4/SiteUserStats/blob/main/visitors_stats/Constants.py#L23).
3. [Logs](https://github.com/denisdenisi4/SiteUserStats/blob/main/visitors_stats/Constants.py#L16-L21) (NOT YET IMPLEMENTED, only Python _print_ now).

## RUN
After configuration run the following commands:

**Windows**
```
cd <PROJECT_DIR>
venv\Scripts\activate
flask run
```
**Linux**
```
cd <PROJECT_DIR>
. venv/bin/activate
flask run
```
**Finally**, open [this page](http://127.0.0.1:5000/static/index.html) in the browser.
