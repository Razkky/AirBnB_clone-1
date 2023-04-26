#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static
    folder of the AirBnB Clone repo using do_pack function
    """
from fabric.api import local, runs_once
from datetime import datetime
import os


@runs_once
def do_pack():
    """Create a .tgz archive
        ready to be deployed"""
    if os.path.isdir('versions'):
        pass
    else:
        os.mkdir('versions')
    try:
        time = datetime.now()
        file = "versions/web_static{}{}{}{}{}{}.tgz".format(
                time.year,
                time.month,
                time.day,
                time.hour,
                time.minute,
                time.second
                )
        print("Packing web_static to {}".format(file))
        local("tar -czvf {} web_static/".format(file))
        file_size = os.stat(file).st_size
        print("web_static packed: {} -> {} Bytes".format(file, file_size))
    except Exception:
        file = None
    return file
