#!/usr/bin/env python
#
# glacerUpload.py
# (c) 2014 Compare Metrics, Inc.
#     Sam Caldwell (sam@edgecase.io)
#
# This is a quick and dirty script to upload files to glacier from 
# the local file system.  Use --help or -h for usage informaiton.
#

import sys,traceback
import os
import boto 
import argparse
import datetime

def showException(msg,err):
    print(msg +":"+ str(err))
    print("-"*60)
    traceback.print_exc(file=sys.stdout)
    print("-"*60)
    print("")
    sys.exit(1)

def upload(awsKeyId,awsSecret,awsVault,fileName,description=None):

    connection=None
    vault=None
    
    if not os.path.isfile(fileName) :
        print("File not found: {}".format(fileName))
        sys.exit(1);
    try:
        connection = boto.connect_glacier(
                                    aws_access_key_id=awsKeyId,
                                    aws_secret_access_key=awsSecret
        )
    except Exception as err:
        showException("ERROR_CONNECTING",err)

    try:
        vault = connection.get_vault(awsVault)
    except Exception as err:
        try:
            print("ERROR: Failed to get vault.  ERROR:{}".format(err))
            print("Attempting to create vaulte [{}]".format(awsVault))
            vault = connection.create_vault(awsVault)
        except Exception as err:
            showException("ERROR_CREATING_VAULT:",err)

    try:
        print(
            "\n\nStarting upload [{}] at {}\n\n"
            .format(fileName,datetime.datetime.now())
        )
        archive_id = vault.upload_archive(fileName)
    except Exception as err:
        showException("ERROR_UPLOADING",err)

    print("Done id:{} time:{}".format(archive_id,datetime.datetime.now()))
    return archive_id

if __name__ == "__main__":
    print("-"*60)
    print("Glacier Uploader Starting....")
    print("-"*60)
    print("")

    parser=argparse.ArgumentParser(
        description="uploader for Amazon AWS glacier"
    )
    parser.add_argument("--vault",
        help="AWS Glacier Vault (if it doesn't exist, we will create it.)",
        dest="vault",
        type=str
    )
    parser.add_argument("--key",
        help="AWS API Key Id (aws_awsKeyId)",
        dest="key",
        type=str
    )
    parser.add_argument("--secret",
        help="AWS secret (aws_secret_access_key)",
        dest="secret",
        type=str
    )
    parser.add_argument("--file",
        help="Path and filename (upload source)",
        dest="file",
        type=str
    )
    parser.add_argument("--description",
        help="Optional description.",
        dest="desc",
        default="",
        type=str
    )
    args=parser.parse_args()

    try:
        if args.key=="":
            raise Exception("key")
        if args.vault=="":
            raise Exception("vault")
        if args.secret=="":
            raise Exception("secret")
        if args.file=="":
            raise exception("file")
    except Exception as err:
        print("Missing Argument: {}".format(err))
        sys.exit(1)

    try:
        with open(args.file,'r') as f:
            print("source file is valid and readable.")
    except Exception as err:
        print("Could not find or open file [{}]".format(args.file))
        sys.exit(1)

    try:
        id=upload( args.key, args.secret, args.vault, args.file, args.desc )
    except Exception as err:
        print("upload failed.  ERROR:{}".format(err))
        sys.exit(1)
        
    print("File Successfully uploaded.")
    print("\nFileId: {}".format(id))
    print("-"*60)