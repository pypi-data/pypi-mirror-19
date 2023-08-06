#!/usr/bin/python2.7

import log
import logging_subprocess

class NFSShare(object):
    def __init__(self, path, ip, options):
        self.logger = log.get(__name__)
        self.export = "{0} {1}/255.255.255.0({2}) # Added by noderoot".format(path, ip, options)
        self.exports_path = "/etc/exports"

    def bringup(self):
        with open(self.exports_path, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in lines:
                if self.export != line:
                    f.write(line)
                else:
                    self.logger.debug("Removing old export: {0}".format(line))

            self.logger.debug("Adding export: {0}".format(self.export))
            f.write(self.export)

        self.logger.info("Updating NFS exports")
        logging_subprocess.call(['export', '-a'], self.logger, shell=True)

    def bringdown(self):
        with open(self.exports_path, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in lines:
                if self.export != line:
                    f.write(line)
                else:
                    self.logger.info("Removing export: {0}".format(line))

        self.logger.info("Updating NFS exports")
        logging_subprocess.call(['export', '-a'], self.logger, shell=True)
