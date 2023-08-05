========
ar_too
========

Artifactory configuration tool

Features
--------

* Update Artifactory LDAP settings
* Add or update repositories to Artifactory
* Set the 'admin' password

Usage
-----

* Update repositories
To update or create repositories, you must have a directory with individual
json files for each desired repository. Then, point the tool at the directory,
and it will create all the repos therein. Each json file should be set up as
per https://www.jfrog.com/confluence/display/RTF/Repository+Configuration+JSON

i.e:
`ar_too --url http://artifactory.company.com --username admin --password password configure --repos_dir /tmp/repos`

* Update LDAP settings
To update the LDAP settings, you'll need to create an ldap file
(see examples/ldap.json). Then, simply run the command and pass the file location.

i.e.:
`ar_too --url http://artifactory.company.com --username admin --password password configure --ldap_json /tmp/ldap.json`

The LDAP settings json is basically a json implementation of the ldap portion
of this xml doc:  https://www.jfrog.com/public/xsd/artifactory-v1_4_5.xsd.
The way this application works is download the current xml, compare the ldap
settings to the desired ldap settings, and send an update (which is the whole
system config) if they're different.

* Update the admin password
Updating the admin password is staight-forward. Simply pass the string you want
to update the password to. Note this will be visible in your command line history.

`ar_too --url http://artifactory.company.com --username admin --password password configure --admin_pass newpassword`

