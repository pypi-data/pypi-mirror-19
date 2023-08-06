List of available utilities
---------------------------

* it4ifree - Show some basic information from IT4I PBS accounting.
* motd_rss - A generic tool for extracting RSS feed(s) into formatted text or HTML page (using TAL / Zope Page Template).

Installation / upgrading
------------------------
```
$ pip install --upgrade it4i.portal.clients
```

Sample config file main.cfg
---------------------------
```
[main]

# uncomment and fill in your IT4I username
#it4i_username = <your_username_here>

# IT4I Extranet API
extranet_api_url = https://extranet.it4i.cz/
```

* System-wide config file path: ```/usr/local/etc/it4i-portal-clients/main.cfg```
* Local user's config file path: ```~/.it4i-portal-clients/main.cfg```

