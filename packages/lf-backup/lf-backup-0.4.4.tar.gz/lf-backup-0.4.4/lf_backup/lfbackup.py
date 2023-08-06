#!/usr/bin/env python3

import argparse
import csv
import pwd

import sys,os
import getpass

import multiprocessing

import logging
import logging.handlers

import time,datetime

import psycopg2

import lf_backup

owner_files_dict={}

# return list of files from db in same format as returned from csv file
def read_sql():
    items=[]

    dbhost=os.environ.get('PGHOST')
    dbport=os.environ.get('PGPORT')
    dbname=os.environ.get('PGDATABASE')
    dbuser=os.environ.get('PGUSER')
    dbpass=os.environ.get('PGPASSWORD')
    qry=os.environ.get('PGSQL')

    if dbhost and dbport and dbname and dbuser and dbpass:
        db_conn_param="dbname='{}' user='{}' password='{}' host='{}' port={}".format(dbname,dbuser,dbpass,dbhost,dbport)
        try:
            conn=psycopg2.connect(db_conn_param)
        except psycopg2.Error as e:
            print("Error: can't connect to database: %s" % e.pgerror)
            return items

        cur = conn.cursor()
        if not qry:
            qry = """select find_owner(filename) as owner,
                filename,
                to_timestamp(atime) as atime,
                to_timestamp(mtime) as mtime,
                to_timestamp(ctime) as ctime,
                st_size/1024.0/1024.0/1024.0 as size
             from file_metadata
             where
                st_size > 3.0*1024*1024*1024
                and (
                  mtime > (extract(epoch from now()) - 604800)
                  or
                  ctime > (extract(epoch from now()) - 604800)
                )"""

        cur.execute(qry)
        results = cur.fetchall()
        items=[row[1] for row in results]

    return items

# initialize logging to syslog - borrowed from leftover
def init_logging():
    crier=logging.getLogger('crybaby')
    crier.setLevel(logging.DEBUG)

    syslog=logging.handlers.SysLogHandler(address=('loghost',514))
    #syslog=logging.handlers.SysLogHandler(address='/dev/log',facility='daemon')
    crier.addHandler(syslog)

    crier.info('lf-backup starting')
    crier.debug('DEBUG: lf-backup syslog logging setup complete')

    return crier

# read csv file into list using field to pick, default to final field
def read_csv(csv_file,field=-1):
    csv_items=[]

    crier.info("lf-backup: backing up from csv %s" % csv_file)

    try:
        with open(csv_file) as f:
            for row in csv.reader(f):
                if field==-1 or (field>=0 and field<len(row)):
                    csv_items.append(row[field])
    except OSError:
        print("Error: missing CSV file",csv_file)
        crier.info("lf-backup: failed to find csv %s" % csv_file)

    return csv_items

# return true if object exists and size/mtime identical
# mtime comparison currently disabled due to format mismatch
def check_stored_object(name,container,container_dir,size,mtime):
    if name in container_dir:
       #if container_dir[name][0]==size and container_dir[name][1]==mtime:
       if container_dir[name][0]==size:
          return True

    return False

def generate_destname(prefix,filename):
    if prefix and filename.startswith(prefix):
       destname=filename[len(prefix):]
    else:
       destname=filename

    # elide leading / from destname
    if destname[0]=='/':
        destname=destname[1:]

    return destname

# file to backup, syslog object
def backup_file(filename,container,prefix,container_dir,crier):
    global owner_files_dict

    #print("considering file",filename)

    destname=generate_destname(prefix,filename)

    #print("container",container,"dest",destname)

    try:
        statinfo=os.stat(filename)
    except OSError:
        print("Error: missing file",filename)
        crier.info("lf-backup: failed to find %s" % filename)
        return

    if check_stored_object(destname,container,container_dir,statinfo.st_size,
        statinfo.st_mtime):
        print("file",filename,"is already current")
        crier.info("lf-backup: %s is already current" % filename)
    else:
        # append file to dict keyed to uid for later mailed report
        if statinfo.st_uid not in owner_files_dict:
            owner_files_dict[statinfo.st_uid]=[]
        owner_files_dict[statinfo.st_uid].append(filename)

        # upload file to swift to container:destname
        print("uploading file",filename)
        crier.info("lf-backup: uploading file %s" % filename)
        lf_backup.upload_to_swift(filename,destname,container)

# build db of container files by name
def build_container_dir(container):
    container_dir={}

    c_objs=lf_backup.get_sw_container(container)
    for obj in c_objs:
        container_dir[obj['name']]=[obj['bytes'],obj['last_modified']] 

    return container_dir

# shell to call backup_file with correct separate parameters
# each parameter is [filename,parse_args,container_dir,crier]
def backup_file_mp(x):
    backup_file(x[0],x[1].container,x[1].prefix,x[2],x[3])

# args from argparse, syslog object
def backup(parse_args,crier):
    input=[]

    if parse_args.csv:
        input=read_csv(parse_args.csv)
    elif parse_args.sql:
        input=read_sql()
    else:
        print("Error: no legal input type or parameter specified!")
        return

    container_dir=build_container_dir(parse_args.container)

    # build parallel parameter list
    segments=[[e,parse_args,container_dir,crier] for e in input]

    p=multiprocessing.Pool(parse_args.parallel)
    p.map(backup_file_mp,segments)

def restore_file(filename,container,prefix):
    if prefix:
       destname=os.path.join(prefix,filename)
    else:
       destname=filename

    print("restoring file",filename)
    #crier.info("lf-backup: restoring file %s" % filename)

    lflib.download_from_swift(filename,destname,container)

# shell to call restore_file with correct separate parameters
# each parameter is [filename,parse_args]
def restore_file_mp(x):
    restore_file(x[0],x[1].container,x[1].prefix)

def days_old(then,now):
    lm=time.strptime(then,'%Y-%m-%dT%H:%M:%S.%f')

    dt=datetime.datetime.fromtimestamp(time.mktime(lm))
    diff=now-dt

    return diff.days

def restore(parse_args,crier):
    if parse_args.restore<1:
       print("Error: minimum restore age is 1 day")
       return

    c_objs=lflib.get_sw_container(parse_args.container)
    print("restoring container",parse_args.container)
    #crier.info("lf-backup: restoring container %s" % parse_args.container)

    now=datetime.datetime.now()

    # build parallel parameter list
    r_files=[[obj['name'],parse_args] for obj in c_objs
        if days_old(obj['last_modified'],now)<=parse_args.restore]
    #print("r_files",r_files)

    p=multiprocessing.Pool(parse_args.parallel)
    p.map(restore_file_mp,r_files)

# send SMTP mail to username containing filelist
def mail_report(username,files):
    print("mailing report to",username)

    # pretty print python list to text list
    body=""
    for file in files:
       body+=(file+"\n")

    lf_backup.send_mail([username],"lf-backup: files uploaded",body)

# convert owner_files_dict into files by username and mail each
def mail_reports():
    global owner_files_dict

    for uid,files in owner_files_dict.items():
        mail_report(pwd.getpwuid(uid).pw_name,files)

# argparse config garbage
def parse_arguments():
    parser=argparse.ArgumentParser(
        description="Backup files to Swift from CSV or SQL")
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c","--csv",help="input from CSV file",
        type=str)
    group.add_argument("-s","--sql",help="input from SQL table",
        action="store_true")
    group.add_argument("-r","--restore",
        help="restore files newer than RESTORE days",type=int)
    parser.add_argument("-p","--prefix",help="strip from source filename",
        type=str)
    parser.add_argument("-C","--container",help="destination container",
        type=str,required=True)
    parser.add_argument("-P","--parallel",help="number of parallel workers",
        type=int,default=5)

    return parser.parse_args()

def main():
    crier=init_logging()

    parse_args=parse_arguments()
    if parse_args.restore:
        restore(parse_args,crier)
    else:
        backup(parse_args,crier)

    mail_reports()

if __name__ == '__main__':
    main()
