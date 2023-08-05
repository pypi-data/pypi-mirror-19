API
===

RESTful API

Documentation on how to use the RESTful API provided by the application

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Examples
--------

### Curl

	$ curl http://127.0.0.1:80/api/statistics

### Python Requests

	import requests

	requests.get('http://127.0.0.1:80/api/statistics').json()

The result of these examples is as follows:

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Version
-------

### GET

Returns the version of the application

	{
	  "version": "0.1.0"
	}

/api/version

Statistics
----------

### GET

Returns statistics about the application and the Python interpreter

	{
	  "libenable": {
	    "version": "0.1.0",
	    "status": "RUNNING",
	    "running_tasks": 0,
	    "total_tasks": 0,
	    "status_code": 0
	  },
		"python": {
	    "platform": "linux",
	    "version": "3.5.2"
	  },
	  "time": {
	    "running": 123,
	    "start": 1483303416,
	    "current": 1483303539
	  }
	}

/api/statistics
