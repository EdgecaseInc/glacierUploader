#!/usr/bin/env python
#
# glacerUpload.py
#
# Copyright (c) 2014 Sam Caldwell (sam@edgecase.io), Edge Case, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, 
# USA.


import sys,traceback
import os
import boto 
import argparse
import time



def upload(awsKeyId,awsSecret,awsVault,file,inventory,description=None):

    connection=None
    vault=None
    
    try:
        with open(inventory,'a') as f:
            print("Verified inventory file is writable.")
    except Exception as err:
        raise Exception(
            "Could not verify write access to inventory file.  " + \
            "ERROR: {}".format(err)
        )

    try:
        with open(file,'rb') as f:
            print("source file readability verified.")
    except Exception as err:
        raise Exception(
            "Could not verify readability of source file." + \
            "ERROR: {}".format(err)
        )

    print("Connecting to glacier")
    try:
        connection = boto.connect_glacier(
                                    aws_access_key_id=awsKeyId,
                                    aws_secret_access_key=awsSecret
        )
    except Exception as err:
        showException("ERROR_CONNECTING",err)

    print("Connected.  Getting handle for glacier vault.")
    try:
        vault = connection.get_vault(awsVault)
    except Exception as err:
        try:
            print("ERROR: Failed to get vault.  ERROR:{}".format(err))
            print("Attempting to create vaulte [{}]".format(awsVault))
            vault = connection.create_vault(awsVault)
        except Exception as err:
            showException("ERROR_CREATING_VAULT:",err)

    start=time.time()
    try:
        print("\n\nStarting upload [{}] at {}\n\n".format(file,start))
        id = vault.upload_archive(file)
    except Exception as err:
        showException("ERROR_UPLOADING",err)
    stop=time.time()

    print("Done id:{} time:{}".format(id,stop))
    
    with open(inventory,'a') as f:
        f.write("'{}','{}','{}','{}'\n".format(file,start,stop,id))
    
    return id



def showException(msg,err):
    print(msg +":"+ str(err))
    print("-"*60)
    traceback.print_exc(file=sys.stdout)
    print("-"*60)
    print("")
    sys.exit(1)



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
    parser.add_argument("--inventory",
        help="Inventory file where we will track what is uploaded.",
        dest="inventory",
        default="inventory.csv",
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
        id=upload(
            args.key,
            args.secret,
            args.vault,
            args.file,
            args.inventory,
            args.desc
        )
    except Exception as err:
        print("upload failed.  ERROR:{}".format(err))
        sys.exit(1)

    print("")
    print("-"*60)
    print("Glacier Uploader Done.")
    print("Please make sure to keep your inventory file somewhere safe.")
    print("\nInventory File: {}".format(args.inventory))
    print("-"*60)
    print("")
    sys.exit(0)