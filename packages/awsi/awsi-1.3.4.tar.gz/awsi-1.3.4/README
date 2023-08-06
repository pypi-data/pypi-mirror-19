AWS Instance Information
========================


Summary
-------
awsi script can help search for a server in aws and connect to it.

It relies on you having boto installed and aws profiles set up containing your key and secret for each aws account.
it has its own config file which list the profiles to use and the regions to search.

It can generate a cache of all servers in the configured regions by calling <code>awsi refresh</code>

It can then connect to an instance using the instanceId, public ip address or name tag
If more than one server is found (maybe they have the same name) it will show you all of them and require you to use a different
piece of information. ID is unique so this is recommended.

Installation
------------

clone the repo and run
<code>pip install .</code>

OR 

pip install awsi

Configuration
-------------
In you home directory create a folder called '.awsi'  
In this folder create a config file called 'config.cfg'

The contents of the file should look like the following.

[main]  
profiles: default,work,work2  
regions: eu-west-1,eu-central-1,us-east-1,us-west-2,us-west-1
cache_file: /tmp/awsi_cache


Usage
-----
usage awsi [ refresh| i-12345 | 54.32.10.01 | Live Web Server | version ]


Todo
----
