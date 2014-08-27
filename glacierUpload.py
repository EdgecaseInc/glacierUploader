#!/usr/bin/env python3
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
	print msg +":"+ str(err)
	print("-"*60)
	traceback.print_exc(file=sys.stdout)
	print("-"*60)
	print("")
	sys.exit(1)

def upload(awsKeyId,awsSecret,awsVault,fileName,description):

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
		vault = layer2.get_vault(awsVault)
	except Exception as err:
		try:
			print("ERROR: Failed to get vault.  trying to create [{}]".format(
																		awsVault
																	)
			)
			vault = connection.create_vault(awsVault)
		except Exception as err:
			showException("ERROR_CREATING_VAULT:",err)

	try:
		print("\n\nStarting upload [{}] at {}\n\n".format(
														fileName,
														datetime.datetime.now())
		)
		archive_id = vault.upload_archive(fileName)
	except Exception as err:
		showException("ERROR_UPLOADING",err)

	print("Done id:{} time:{}".format(archive_id,datetime.datetime.now()))

parser=argparse.ArgumentParser(description="uploader for Amazon AWS glacier")

parser.add_argument("--glacierVault",
	help="AWS Glacier Vault URI",
	dest="vault",
	type=str
)
parser.add_argument("--awsKeyId",
	help="AWS API Key Id (aws_awsKeyId)",
	dest="keyId",
	type=str
)
parser.add_argument("--secret",
	help="AWS secret (aws_secret_access_key)",
	dest="secret",
	type=str
)
parser.add_argument("--sourceFile",
	help="Source file to be uploaded.",
	dest="sourceFile",
	type=str
)
parser.add_argument("--description",
	help="optional description.",
	dest="desc",
	default="",
	type=str
)
args=parser.parse_args()
upload( args.keyId, args.secret, args.vault, args.sourceFile, args.desc )
