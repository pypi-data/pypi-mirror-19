#!/usr/bin/python3
# coding: utf-8
# zip_tools.py

import os
import zipfile
import gzip
import tarfile
import fnmatch

def extract_all(zipfile, dest_folder):
    """
    reads the zip file, determines compression
    and unzips recursively until source files 
    are extracted 
    """
    z = ZipFile(zipfile)
    print(z)
    z.extract(dest_folder)
    
def create_zip_from_file(zip_file, fname):
    """
    add a file to the archive
    """
    with zipfile.ZipFile(zip_file, 'w') as myzip:
        myzip.write(fname)

def create_gz_from_content(gz_file, binary_content):
    with gzip.open(gz_file, 'wb') as f:
        f.write(binary_content)
        
def create_tar_from_files(tar_file, fl):
    with  tarfile.open(tar_file, "w:gz") as tar:
        for name in fl:
            tar.add(name)
        
    
def create_zip_from_folder(zip_file, fldr, mode="r"):
    """
    add all the files from the folder fldr
    to the archive
    """
    #print('zip from folder - adding folder : ', fldr)
    zipf = zipfile.ZipFile(zip_file, 'w')
    for root, dirs, files in os.walk(fldr):
        for file in files:
            fullname = os.path.join(root, file)
            #print('zip - adding file : ', fullname)
            zipf.write(fullname)
    
    
    zipf.close()
    
class ZipFile(object):
    def __init__(self, fname):
        self.fname = fname
        self.type = self._determine_zip_type()
    
    def __str__(self):
        return self.fname + ' is type ' + self.type
        
    def _determine_zip_type(self):
        xtn = self.fname[-3:].upper()
        #print('_' + xtn + '_', self.fname)
        if xtn == 'ZIP':
            return 'ZIP'
        elif xtn == '.GZ':
            return 'GZ'
        elif xtn == 'TAR':
            return 'TAR'
        else:
            print('Unknown file type - TODO, examine header')
        return 'Unknown'
    
    def _extract_zip(self, fldr, password=''):
        z = zipfile.ZipFile(self.fname)
        z.extractall(fldr, pwd=password)  # must pass as bytes, eg b'SECRET'
        
    def _extract_gz(self, fldr, password=''):
        with gzip.open(self.get_file_named(fldr, '*.gz'), 'rb') as fip:
            file_content = fip.read()
            with open(fldr + os.sep + 'temp.tar', 'wb') as fop:
                fop.write(file_content)
        
    def _extract_tar(self, fldr, tar_file=''):
        if tar_file == '':
            fldr + os.sep + 'temp.tar'
        tar = tarfile.open(tar_file)
        for item in tar:
            tar.extract(item)
    
        #tar.extractall(path=fldr)
        tar.close()    
        
    
    
    def extract(self, dest_fldr, password=''):
        """
        unzip the file contents to the dest_folder
        (create if it doesn't exist)
        and then return the list of files extracted
        """
        #print('extracting to ' + dest_fldr)
        if self.type == 'ZIP':
            self._extract_zip(dest_fldr, password)
        elif self.type == 'GZ':
            self._extract_gz(dest_fldr, password)
        elif self.type == 'TAR':
            self._extract_tar(dest_fldr, self.fname)
        else:
            raise('Unknown archive file type')

    def get_file_named(self, fldr, xtn):
        """
        scans a directory for files like *.GZ or *.ZIP and returns
        the filename of the first one found (should only be one of
        each file here
        """
        res = []       # list of Sample objects
        for root, _, files in os.walk(fldr):
            for basename in files:
                if fnmatch.fnmatch(basename, xtn):
                    filename = os.path.join(root, basename)
                    res.append(filename)

        if len(res) > 0:   
            return res[0]
        else:
            return None

