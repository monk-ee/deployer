deployer
========

Team City Deployer into AWS

Introduction
========
Just a quick python script to find autoscaling instances (by tagname) and rsync the latest build to them.

You can then add a build task that deploys the code:

    Command Line
    Command: /opt/bin/deploy.py %autoscaling.group.name% %teamcity.build.checkoutDir% %ssh_key_location%
    Execute: If all previous steps finished successfully (zero exit code)


Requirements
========

+ python
+ boto
+ PyYAML


Assumptions
========
You can modify this script to copy to and from the correct directories.