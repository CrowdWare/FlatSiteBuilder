# FlatSiteBuilder

This desktop app is working as a content mangement system and is producing web content to use with github pages or any other service provider.
I have been inspired by Wordpress and the Divi - PageBuilder.

Have a look at our web site: https://artanidos.github.io/FlatSiteBuilder

![](FlatSiteBuilder.png)

## Prerequisits
In order to work with FlatSiteBuilder you have to install the following packages.  
```console
pip install --user PySide6
pip install --user PyQtWebEngine
pip install --user django
pip install --user dulwich
pip install --user jinja2
pip install --user markdown2
```

You also need to install the pyqt5 development tools.
```console
sudo apt install pyqt5-dev-tools
```  

Before you can run the program you have to build the resources.
```console
pyside6-rcc main.qrc -o main_rc.py
pyside6-rcc resources.qrc -o resources.py
pyside6-rcc plugins/carousel.qrc -o plugins/carousel_rc.py
pyside6-rcc plugins/imageeditor.qrc -o plugins/imageeditor_rc.py
pyside6-rcc plugins/revolution.qrc -o plugins/revolution_rc.py
pyside6-rcc plugins/texteditor.qrc -o plugins/texteditor_rc.py
pyside6-rcc plugins/github.qrc -o plugins/github_rc.py
pyside6-rcc plugins/shopify.qrc -o plugins/shopify_rc.py
pyside6-rcc plugins/markdowneditor.qrc -o plugins/markdowneditor_rc.py
```

## How to run
Open the terminal and download the source code using git.
```console
git clone https://github.com/Artanidos/FlatSiteBuilderPython.git
```
Then cd into FlatSiteBuilderPython
```console
cd FlatSiteBuilderPython
```
Then run python to execute the app.
```console
python3 main.py
```


# Atropos Theme
The atropos theme which is included in this package is only for demonstration.
I only have **one** license for this.
You can buy it here: https://wrapbootstrap.com/user/stepofweb

# Syntax
The syntax for the templates is based on [Django](https://www.djangoproject.com/start/). That also means that we render the HTML using [Jinja](https://palletsprojects.com/p/jinja/).

## Variable
```django
{{ varname }}
```

## Includes
```django
{% include "filename" %}
```

## Loop
```django
{% for page in pages %}
    {{ page.title }}
{% endfor %}
```

## Contitional
```django
{% if condition %}
    do something
{% endif %}
```

## Contact
If you have any feature requests then just send me an email with your ideas to artanidos@crowdware.at

## Donations
If you like to support my work on the FlatSiteBuilder you are invited to [become a patron](https://www.patreon.com/artananda) and/or you can also become a member of the [CrowdWare](https://www.crowdware.at) association. 



