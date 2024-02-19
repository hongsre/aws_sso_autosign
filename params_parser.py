import os
import sys
import argparse


class PARAMS():
    def parse_cli_args(self, argv=None):
        ''' Command line argument processing '''
        parser = argparse.ArgumentParser(
            description='client config')
        parser.add_argument('-v', '--version', action='store', default=None,
                            help='client config set version')
        parser.add_argument('-n', '--gamecode', action='store', default=None,
                            help='game code')
        parser.add_argument('-c', '--version-code', action='store', default=None,
                            help='client config set version code')
        args = parser.parse_args(argv)
        self.version = args.version
        self.gamecode = args.gamecode
        self.version_code = args.version_code

    def __init__(self, version=None, gamecode=None, version_code=None):
        self.version = version
        self.gamecode = gamecode
        self.version_code = version_code


if __name__ == "__main__":
    params = PARAMS()
