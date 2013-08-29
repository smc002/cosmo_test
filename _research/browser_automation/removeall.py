#! /usr/bin/env python  
#coding=utf-8  
## {{{ Recipe 193736 (r1): Clean up a directory tree   
""" removeall.py: 
 
   Clean up a directory tree from root. 
   The directory need not be empty. 
   The starting directory is not deleted. 
   Written by: Anand B Pillai <abpillai@lycos.com> """  
  
import sys, os, logging
  
ERROR_STR= """Cann't removing {}, error: {} """  
  
def rmgeneric(path, __func__):  
  
    logger = logging.getLogger("COSMO")

    try:  
        __func__(path)  
        logger.info('Removed: {}'.format(path))
        ##print ('Removed ', path  )
    except OSError as err:  
        logger.info('Remove failed: {}'.format(path))
        logger.info(str(err))
        ##print (ERROR_STR.format(path, err))
        pass
              
def removeall(path):  
  
    if not os.path.isdir(path):  
        if os.path.exists(path):
            f=os.remove  
            rmgeneric(path, f)  
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
