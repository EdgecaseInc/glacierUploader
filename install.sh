#!/bin/bash
#
# install.sh (for glacierUpload.py)
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Edge Case, Inc.
# Author: Sam Caldwell (sam@edgecase.io)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS # IN THE SOFTWARE.
#
# This is a quick and dirty script to upload files to glacier from 
# the local file system.  Use --help or -h for usage informaiton.
#

export RAW_URL=https://raw.githubusercontent.com/EdgecaseInc/glacierUploader/master/glacierUpload.py

[ "$(whoami)" != "root" ] && {
    echo "This script must be run with root permissions."
    exit 1
}

apt-get install wget python python-dev python-pip -y || {
    echo "one or more dependencies failed to install."
    exit 2
}
pip install boto || {
    echo "failed to install boto (python package)"
    exit 3
}
wget $RAW_URL --output-file /usr/bin/glacierUpload.py || {
    echo "failed to download glacierUpload.py"
    exit 4
}
[ ! -x /usr/bin/glacierUpload.py ] && {
    chmod +x /usr/bin/glacierUpload.py
}
echo "glacierUpload.py is installed."
exit 0