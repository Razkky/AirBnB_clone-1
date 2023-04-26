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
        print("Packing web_static to {}".format(file))
        local("tar -czvf {} web_static/".format(file))
        file_size = os.getsize(file)
        print("web_static packed: {} -> {} Bytes".format(file, file_size))
    except Exception:
        file = None
    return file


def do_deploy(archive_path):
    """Deploy webstatic to remote server"""
    base_name = os.path.basename(archive_path)
    name_file = base_name.replace(".tgz", "")
    path = '/data/web_static/releases/{}'.format(name_file)
    if not os.path.exists(archive_path):
        return False
    else:
        try:
            put(archive_path, '/tmp/{}'.format(base_name))
            run('mkdir -p /data/web_static/releases/{}'.format(
                name_file))
            run("sudo tar -xzf /tmp/{} -C {}".format(base_name, path))
            run("rm -rf /tmp/{}".format(base_name))
            run("sudo mv {}/web_static/* {}".format(path, path))
            run("sudo rm -rf {}/web_static".format(path))
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
