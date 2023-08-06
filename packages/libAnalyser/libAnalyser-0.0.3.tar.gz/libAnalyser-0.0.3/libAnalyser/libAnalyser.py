#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
import os
import site
import re


'''
    libAnalyser - Analy modules and detect a module is standard python library or not
'''
class libAnalyser(object):
    """docstring for libAnalyser"""
    def __init__(self): 
        super(libAnalyser, self).__init__()
        self.sitepackage_list = site.getsitepackages()
        self.sitepackage_list.append(site.getusersitepackages())

    # detect a python module/package exists or not
    def exists(self, module_name):
        try:
            __import__(module_name)
        except ImportError as e:
            return False
        return True

    # detect a thirdparty python package
    def thirdPartyPackage(self, module_name):
        if not self.sitepackage_list:
            raise ImportError('No getsitepackages found in site module')
            return False

        if not self.exists(module_name):
            return False

        for sitepackage in self.sitepackage_list:
            package_dir     = os.path.join(sitepackage, module_name)
            package_file    = os.path.join(sitepackage, module_name + '.py')

            if os.path.exists(package_dir) or os.path.exists(package_file):
                return True

        return False

    # detect a standard python package
    def standardPackage(self, module_name):
        if not self.sitepackage_list:
            raise ImportError('No getsitepackages found in site module')
            return False

        if not self.exists(module_name):
            return False

        for sitepackage in self.sitepackage_list:
            package_dir     = os.path.join(sitepackage, module_name)
            package_file    = os.path.join(sitepackage, module_name + '.py')

            if os.path.exists(package_dir) or os.path.exists(package_file):
                return False
                
        return True

    # extra all python packages from the path
    def getPackages(self, path, ignore_file_list = True, ignore_local_module = True, ignore_standard_package = True):
        src_file_package_dict = {}
        package_list = []
        source_file_list = []

        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    if '.py' != f[-3:]:
                        continue
                    source_file_list.append(os.path.splitext(f)[0])

                    src_file = os.path.join(root, f)
                    plist = self.__getpackage(src_file, ignore_standard_package)
                    if plist:
                        src_file_package_dict[os.path.relpath(src_file, path)] = plist
                        [ package_list.append(x) for x in plist if x not in package_list ]

        # remove local modules
        if ignore_local_module:
            for f in source_file_list:
                if f in package_list:
                    package_list.remove(f)
                for key in src_file_package_dict:
                    plist = src_file_package_dict[key]
                    if f in plist:
                        plist.remove(f)

        # for debug
        #self.__debugOutput(src_file_package_dict)

        if ignore_file_list:
            return package_list
        else:
            return src_file_package_dict

    # install all python thirdparty packages from the path
    def installPackages(self, path, *params):
        package_list = self.getPackages(path)

        if package_list:
            print('Installing python package from pip ... ')
            for package in package_list:
                prompt = '  > Package <%s> installing    - ' % package
                cmd = 'pip install %s' % package
                for argv in params:
                    cmd += ' %s' % argv
                
                try:
                    print('command: %s' % cmd)
                    os.system(cmd)
                    prompt += 'OK'
                except OSError as e:
                    print(e)
                    prompt += 'FAILED'
                except IOError as e:
                    print(e)
                    prompt += 'FAILED'
                print(prompt)
        return

    def __debugOutput(self, src_file_package_dict):
        for file in src_file_package_dict:
            print('Find module from file: %s' % file)
            print('  %s' % str(src_file_package_dict[file]))
        return

    def __getpackage(self, file, ignore_standard_package = True):
        package_list = []
        if not os.path.exists(file):
            return package_list

        with open(file) as f:
            for line in f:
                if not line:
                    continue

                modules = []
                line = line.strip()
                if 'import ' == line[:7]:
                    modules = line[7:].split(',')
                elif 'from ' == line[:5]:
                    line = line[5:]
                    pos = line.find(' import ')
                    if -1 != pos:
                        line = line[:pos]
                    modules = line.split(',')

                for md in modules:
                    md = md.strip()
                    pos = md.find(' as ')
                    if -1 != pos:
                        md = md[:pos]

                    if ignore_standard_package and self.standardPackage(md):
                        continue
                    package_list.append(md)

        return package_list
