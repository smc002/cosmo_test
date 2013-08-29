#! /usr/bin/env python  
#coding=utf-8  
## {{{ Recipe 193736 (r1): Clean up a directory tree   
""" removeall.py: 
 
   Clean up a directory tree from root. 
   The directory need not be empty. 
   The starting directory is not deleted. 
   Written by: Anand B Pillai <abpillai@lycos.com> """  
  
import sys, os  
  
ERROR_STR= """Cann't removing {}, error: {} """  
  
def rmgeneric(path, __func__):  
  
    try:  
        __func__(path)  
        print ('Removed ', path  )
    except OSError as err:  
        print (ERROR_STR.format(path, err))
              
def removeall(path):  
  
    if not os.path.isdir(path):  
        return  
      
    files=os.listdir(path)  
  
    for x in files:  
        fullpath=os.path.join(path, x)  
        if os.path.isfile(fullpath):  
            f=os.remove  
            rmgeneric(fullpath, f)  
        elif os.path.isdir(fullpath):  
            removeall(fullpath)  
            f=os.rmdir  
            rmgeneric(fullpath, f)  
## End of recipe 193736 }}}
