======
README
======

This package provides the core component for generate data used in the
xdashboard dashboard server. The anme p01.dashboard is choosen because this package
allows to generate the data for a given sample rate and send them to the
browser using web sockets. This package provides the core sample data
genaration, queue and processor implementation and also provides the
javascript library used for the xdashboard server.

You can use this library and implement your own kind of xdashboard server if
you like to provide a custom dasboard solution or you can inherit from the
xdashboard package and add your own sample data for your xdashboard dashboard.

Note; this package does not provide a running server and a working dashboard
it only provides the libraries for build one. Check the xdashboard package for a
fully working sample dashboard server. Anyway, p01.dashboard and xdashboard are only
packages for build your own custom dashboard. You will allways need to implement
what you like to display. But the default xdashboard server provides simple
samples for how to get easy started with.
