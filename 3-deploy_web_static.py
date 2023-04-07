#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static
    folder of the AirBnB Clone repo using do_pack function
"""
from fabric.api import local, runs_once, put, run, env
from datetime import datetime
import os

env.hosts = ['54.160.113.7', '54.157.161.120']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


@runs_once
def do_pack():
    """Create a .tgz archive"""
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
        print(f"Packing web_static to {file}")
        local(f"tar -czvf {file} web_static/")
        file_size = os.getsize(file)
        print(f"web_static packed: {file} -> {file_size} Bytes")
    except Exception:
        file = None
    return file


def do_deploy(archive_path):
    """Deploy webstatic to remote server"""
    base_name = os.path.basename(archive_path)
    name_file = base_name.replace(".tgz", "")
    path = f'/data/web_static/releases/{name_file}'
    if not os.path.exists(archive_path):
        return False
    else:
        try:
            put(archive_path, '/tmp/{}'.format(base_name))
            run('mkdir -p /data/web_static/releases/{}'.format(
                name_file))
            run(f"sudo tar -xzf /tmp/{base_name} -C {path}")
            run(f"rm -rf /tmp/{base_name}")
            run(f"sudo mv {path}/web_static/* {path}")
            run(f"sudo rm -rf {path}/web_static")
            run('sudo rm -rf /data/web_static/current')
            run('ln -s {} /data/web_static/current'.format(
                path))
            print("New version deployed!")
        except Exception as err:
            return False
    return True

def deploy():
    """Archive a path and deploy it on remote server"""
    archive = do_pack()
    if archive:
        return do_deploy(archive)
    else:
        return False
