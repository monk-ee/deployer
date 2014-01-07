#!/usr/bin/python

__author__ = 'monkee'
import boto.ec2
from datetime import date
import yaml, sys,logging
from subprocess import call


def main(argv):
    tag = ''
    checkout_dir = ''
    ssh_key = ''
    timestamp = str(date.today())

    #get configuration
    try:
        configStr = open('/opt/bin/config.yml','r')
        config = yaml.load(configStr)
    except (OSError, IOError), emsg:
        print('Cannot find or parse config file: ' + str(emsg))
        sys.exit(2)

    #logging for debug really you can set to logging.INFO to chill it out
    logging.basicConfig(filename=config['logfile'],level=logging.INFO)

    try:
        tag = argv[1]
        checkout_dir = argv[2]
        ssh_key = argv[3]
    except BaseException, emsg:
        logging.warning(timestamp + ': Missing Arguments: ' + str(emsg) + ' : '+str(argv))
        sys.exit(2)

    try:
        ec2 = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=config['s3']['aws_access_key'], aws_secret_access_key=config['s3']['aws_secret_key'])
        reservations = ec2.get_all_instances(filters={'tag-value' : tag})

        for reserve in reservations:
            server = reserve.instances[0].dns_name
            rsync = "/usr/bin/rsync -avzh --delete -e 'ssh -i "+ssh_key+"' "+checkout_dir+"/dist/ admin@"+server+":/var/www/"
            call(rsync,shell=True)

    except BaseException, emsg:
         logging.warning(timestamp + ': Cannot send message: ' + str(emsg))
         sys.exit(2)

    sys.exit()

if __name__ == "__main__":
   main(sys.argv)