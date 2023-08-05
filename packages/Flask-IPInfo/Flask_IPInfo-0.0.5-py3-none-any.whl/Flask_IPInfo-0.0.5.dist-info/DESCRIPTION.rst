Flask-IPInfo
======

This library get some useful information from flask's request object.Such as 
IP Address, ISP, Location, Web Browser, Operating System, etc.

Example
-------

::

    from flask import Flask
    from flask_ipinfo import IPInfo

    app = Flask(__name__)
    ipinfo = IPInfo()

    @app.route("/")
    def hello():
        return "Your IP Address is :" + ipinfo.ipaddress

    if __name__ == "__main__":
        app.run()



Supports
--------
Tested on Python 3.5


* Project:  https://github.com/borisliu/flask-ipinfo


