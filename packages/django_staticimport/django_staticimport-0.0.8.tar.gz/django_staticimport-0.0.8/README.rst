django_staticimport [![Build Status](https://travis-ci.org/leoxnidas/django_staticimport.svg?branch=master)](https://travis-ci.org/leoxnidas/django_staticimport) [![Dependency Status](https://dependencyci.com/github/leoxnidas/django_staticimport/badge)](https://dependencyci.com/github/leoxnidas/django_staticimport)
-------------------

Add static files never was so easy. This library allows you to include css, js and images files (static files) on a template faster than the old way.


Install
-------

```pip install django-staticimport```

or

```easy_install django-staticimport```


Usage.
------

####Add the app to settings.

```python
# installing the static_import application.
INSTALLED_APPS = [
		.
		.
		.

    'static_import',
]

# adding remote static file.
HOSTED_LIBS = [
	{
		'name': 'selectjs',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js'
	},
]
```

####Then.. on the templates.

```html
<!DOCTYPE html>
{% load staticimport %}
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Hi</title>
	<!-- including css files -->
	{% import 'main.css' %}
	{% import 'something.css' %}
	
	<!-- including js files with custom attributes -->
	{% import 'angularjs' %}
	{% import 'main.js' attrs='async' %}
</head>
<body>
	<!-- including images -->
	{% import 'image.jpg' css='image' id='image' attrs='width="100px" height="100px" data-city="picture"' %}
	<h1>hello world</h1>
</body>
</html>
```

####also you could downlaod static files with new django command, called
```python manage.py download_static_file angularjs https://cdnjs.cloudflare.com/ajax/libs/1140/2.0/1140.min.css```

Supported remote libraries
--------------------------

	* angularjs (lastest release)
	* angular material (lastest release)
	* dojo (lastest release)
	* ext-core (lastest release)
	* hammerjs (lastest release)
	* jquery 3 (lastest release)
	* jquery 2 (lastest release)
	* jquery 1 (lastest release)
	* jquery mobile (lastest release)
	* jquery ui (lastest release)
	* jquery color (lastest release)
	* mootools (lastest release)
	* prototype (lastest release)
	* scriptaculous (lastest release)
	* spf (lastest release)
	* swfobject (lastest release)
	* threejs (lastest release)
	* webfont (lastest release)
	* stringjs (lastest release)
	* zooming (lastest release)
	* angular qrcode (lastest release)
	* react (lastest release)
	* react-dom-server (lastest release)
	* react-dom (lastest release)
	* react-with-addons (lastest release)
	* materialize (lastest release)
	* bootstrap (lastest release)
	* bootstrap-theme (lastest release)
	* bulma (lastest release)
	* metro-UI (lastest release)
	* metro-UI-responsive (lastest release)
	* metro-UI-schemes (lastest release)
	* metro-UI-rtl (lastest release)
	* metro-UI-icons (lastest release)
	* font-awesome (lastest release)
	* select2 (lastest release)


LICENSE
-------

Copyright (c) 2016-2017 Leonardo Esparis and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, 
       this list of conditions and the following disclaimer.
    
    2. Redistributions in binary form must reproduce the above copyright 
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
