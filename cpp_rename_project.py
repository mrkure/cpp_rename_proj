# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 11:25:37 2023

@author: CAZ2BJ
"""
import os, sys

def get_files(root_dir, ext = [], con = [], exc = [], rec = False, _print = False):
    result_files =[]
    for dirpath, dirnames, filenames in os.walk(root_dir):
        files = [os.path.normpath(f'{dirpath}\{filename}') for filename in filenames]   
        for file in files:  
            if ext:
                if not any([os.path.splitext(file)[-1] == f'.{i}'  for i in ext]): continue
            if con:
                if not all([i in os.path.basename(file) for i in con]): continue
            if exc:
                if any([i in os.path.basename(file) for i in exc]): continue            
            if _print: print(file)
            result_files.append(file)    
        if not rec: break       
    result_files.sort()  
    return result_files

def get_dirs(root_dir,  ext = [], con = [], exc = [], rec = False, _print = False):
    result_files =[]
    for dirpath, dirnames, filenames in os.walk(root_dir):
        files = [os.path.normpath(f'{dirpath}\{dirname}') for dirname in dirnames]   
        for file in files:  
            if con:
                if not all([i in os.path.basename(file) for i in con]): continue
            if exc:
                if any([i in os.path.basename(file) for i in exc]): continue            
            if _print: print(file)
            result_files.append(file)    
        if not rec: break       
    result_files.sort()  
    return result_files

def replace_in_file(filename, old_val, new_val):
    # Read in the file
    with open(filename, 'r') as file :
        filedata = file.read()
    
    # Replace the target string
    filedata = filedata.replace(old_val, new_val)
    
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)   
  
#%% MAIN
old_name = input("Insert name of project to rename : ")
new_name = input("Insert new name for project : ")

# old_name = "myproj"
# new_name = "newproj"

dirs = get_dirs(os.path.dirname(__file__),  ext = [], con = [old_name], exc = [], rec = False, _print = True)
if len(dirs) != 1:
    print("project not found ...\n")
    input("Press enter to exit .. ")
else:
    old_proj_dir               = dirs[0]
    sol_dir, old_proj_name     = os.path.split(dirs[0])
    
    old_file_sln               = get_files(sol_dir, ext = ["sln"], con = [], exc = [], rec = False, _print = False)[0]
    
    old_file_vcxproj           = get_files(old_proj_dir, ext = ["vcxproj"], con = [], exc = [], rec = False, _print = False)[0]
    old_file_vcxproj_basename  = os.path.split(old_file_vcxproj)[1]
   
    old_file_user              = get_files(old_proj_dir, ext = ["user"], con = [], exc = [], rec = False, _print = False)[0] 
    old_file_user_basename     = os.path.split(old_file_user)[1]    

    old_file_filters           = get_files(old_proj_dir, ext = ["filters"], con = [], exc = [], rec = False, _print = False)[0] 
    old_file_filters_basename  = os.path.split(old_file_filters)[1]   


    new_proj_dir = sol_dir + '\\' + new_name
    
    # replace in files
    replace_in_file(old_file_sln, old_name, new_name)
    replace_in_file(old_file_vcxproj, old_name, new_name)    
    replace_in_file(old_file_user, old_name, new_name)   
    
    # rename files
    os.rename(old_file_vcxproj,  old_proj_dir + '\\' + old_file_vcxproj_basename.replace(old_name, new_name))   
    os.rename(old_file_user,     old_proj_dir + '\\' + old_file_user_basename.replace(old_name, new_name))
    os.rename(old_file_filters,  old_proj_dir + '\\' + old_file_filters_basename.replace(old_name, new_name))
    
    # rename folder
    os.rename(old_proj_dir, new_proj_dir)
    
