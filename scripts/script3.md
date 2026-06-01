# Pixhawk 6c & Jetson Nano setup with Ground station suing mavlink Protocol

Connecting flight controllers with companion computers can be annoying sometimes, because fiding the suitabe cable is abosolutely a hassle.
In this thread we are discussing how to conenct Pixhawk 6c with Jetson Nano to a Ground Control Station.

As you might know QGC requires UDP signal to make connection and get telemetry data from Flight Controllers. There have been options developed and improve over the years (mavproxy,mavros,...) but we will be using Mavlink-Anywhere which make the setup easy.

After isntallation setup from here:


here are the commands

sudo systemctl restart mavlink-router

journalctl -u mavlink-router -f
