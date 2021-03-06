#!/usr/bin/env python3

import os
import json
import errno
import sys
import argparse
import subprocess
import shutil

def hornetctl_node(args):
    if args.node == "on":
        # check if service is running
        if not os.system('systemctl is-active --quiet hornet'):  # will return 0 for active else inactive.
            print('Service is already running!')
            sys.exit(1)

        if not os.system('systemctl is-active --quiet goshimmer'):  # will return 0 for active else inactive.
            print('GoShimmer is already running! You cannot run both nodes at the same time.')
            sys.exit(1)

        print("Starting Hornet Systemd Service.")
        os.system('systemctl start hornet')
    else:
        print("Stopping Hornet Systemd Service. Please be patient and wait for graceful shutdown.")
        os.system('systemctl stop hornet')


def hornetctl_network(args):
    default_file = "/etc/default/hornet"
    comnet_string = "OPTIONS=\"--config config_comnet\"\n"

    # read default file
    lines = []
    try:
        f = open(default_file, "r")
        lines = f.readlines()
        f.close()

    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)

    if args.network == "mainnet":
        if comnet_string in lines:
            lines[:] = (value for value in lines if value != comnet_string)
    else:
        lines.append(comnet_string)

    # write default file
    try:
        f = open(default_file, "w")
        for line in lines:
            f.write(line)
        f.close()
        print('Network update successfull.')

    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)


def hornetctl_dashboard(config_file, args):
    lines = ""
    with open(config_file, "r") as f:
        for line in f.readlines():
            lines += line.replace("\n", "")

    config_json = json.loads(lines)

    if args.dashboard == "on":
        config_json["dashboard"]["bindAddress"] = "0.0.0.0:8081"
    else:
        config_json["dashboard"]["bindAddress"] = "localhost:8081"

    try:
        f = open(config_file, "w")
        f.write(json.dumps(config_json, indent=1))
        f.close()

        if args.dashboard == "on":
            if "comnet" in config_file:
                print("Hornet Comnet Dashboard was enabled.")
            else:
                print("Hornet Mainnet Dashboard was enabled.")
        else:
            if "comnet" in config_file:
                print("Hornet Comnet Dashboard was disabled.")
            else:
                print("Hornet Mainnet Dashboard was disabled.")

    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)

def set_snapshot_path(config, path):
    lines = ""
    with open(config, "r") as f:
        for line in f.readlines():
            lines += line.replace("\n", "")

    config_json = json.loads(lines)
    config_json["snapshots"]["local"]["path"] = path

    try:
        f = open(config, "w")
        f.write(json.dumps(config_json, indent=1))
        f.close()

    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)


def set_db_path(config, path):
    lines = ""
    with open(config, "r") as f:
        for line in f.readlines():
            lines += line.replace("\n", "")

    config_json = json.loads(lines)
    config_json["db"]["path"] = path

    try:
        f = open(config, "w")
        f.write(json.dumps(config_json, indent=1))
        f.close()

    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)

def hornetctl_usb(args):
    config_file = "/var/lib/hornet/config.json"
    config_comnet_file = "/var/lib/hornet/config_comnet.json"

    volume_path = "/dev/sda1"
    volume_exists = os.path.exists(volume_path)

    # switch to USB
    if args.usb == 'on':

        # check if partition exists
        if not volume_exists:
            print("USB is not connected or not properly partitioned.")
            sys.exit(1)

        # if volume is already mounted, unmount it
        if volume_path in subprocess.check_output("mount", shell=True).decode('ascii'):
            os.system('umount ' + volume_path)

        # if partition is not ext4, format it
        if 'ext4' not in subprocess.check_output("blkid " + volume_path, shell=True).decode('ascii'):
            print("Formatting the partition to ext4. Please be Patient!\n")
            os.system('mkfs.ext4 -F ' + volume_path)

        # mount on /mnt
        os.system('mount ' + volume_path + ' ' + '/mnt')

        # create /mnt/hornet
        if not os.path.isdir('/mnt/hornet'):
            os.mkdir('/mnt/hornet')

        # set ownership of /mnt/hornet to hornet user
        os.system('chown -R hornet:hornet /mnt/hornet')

        set_db_path(config_file, '/mnt/hornet/mainnetdb')
        set_db_path(config_comnet_file, '/mnt/hornet/comnetdb')

        set_snapshot_path(config_file, '/mnt/hornet/export.bin')
        set_snapshot_path(config_comnet_file, '/mnt/hornet/export_comnet.bin')

    # switch to SD
    else:
        # if volume is mounted, unmount it
        if volume_path in subprocess.check_output("mount", shell=True).decode('ascii'):
            os.system('umount ' + volume_path)

        set_db_path(config_file, 'mainnetdb')
        set_db_path(config_comnet_file, 'comnetdb')

        set_snapshot_path(config_file, 'export.bin')
        set_snapshot_path(config_comnet_file, 'export_comnet.bin')


def hornetctl_clean(args):

    if args.clean == "db" or args.clean == "all":
        db_comnet = getLocal() + "/comnetdb"
        db_mainnet = getLocal() + "/mainnetdb"

        db_exists = os.path.isdir(db_comnet) or os.path.isdir(db_mainnet)

        if not db_exists:
            print("Hornet db is already clean. Nothing to do.")
        else:
            try:
                shutil.rmtree(db_mainnet)
                print("Hornet mainnet db has been cleaned.")
            except IOError as e:
                errorn, strerror = e.args
                if errorn == errno.EACCES:
                    print("You need root permissions to do this!")
                    sys.exit(1)
            try:
                shutil.rmtree(db_comnet)
                print("Hornet comnet db has been cleaned.")
            except IOError as e:
                errorn, strerror = e.args
                if errorn == errno.EACCES:
                    print("You need root permissions to do this!")
                    sys.exit(1)

    if args.clean == "snapshot" or args.clean == "all":

        snapshot_mainnet = getLocal() + "/export.bin"
        snapshot_mainnet_tmp = getLocal() + "/export.bin.tmp"
        snapshot_comnet = getLocal() + "/export_comnet.bin"

        snapshot_exists = os.path.isfile(snapshot_mainnet) or os.path.isfile(snapshot_mainnet_tmp) or os.path.isfile(snapshot_comnet)

        if not snapshot_exists:
            print("Hornet snapshots are already clean. Nothing to do.")
        else:
            try:
                os.remove(snapshot_mainnet)
                print("Hornet mainnet snapshot has been cleaned.")
            except IOError as e:
                errorn, strerror = e.args
                if errorn == errno.EACCES:
                    print("You need root permissions to do this!")
                    sys.exit(1)
            try:
                os.remove(snapshot_mainnet_tmp)
                print("Hornet mainnet tmp snapshot has been cleaned.")
            except IOError as e:
                errorn, strerror = e.args
                if errorn == errno.EACCES:
                    print("You need root permissions to do this!")
                    sys.exit(1)
            try:
                os.remove(snapshot_comnet)
                print("Hornet comnet snapshot has been cleaned.")
            except IOError as e:
                errorn, strerror = e.args
                if errorn == errno.EACCES:
                    print("You need root permissions to do this!")
                    sys.exit(1)

def hornetctl_log():
    os.system('journalctl -u hornet') #ToDo: improve this so it shows only the tail

def getHornetVersion():
    try:
        status, output = subprocess.getstatusoutput('hornet --version')
        if status != 0:
            return "unknown"
        else:
            return output
    except:
        return "unknown"


def getNodeStatus():
    try:
        cmd = 'systemctl status hornet'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        stdout_list = proc.communicate()[0].decode("utf-8").split('\n')
        for line in stdout_list:
            if 'Active:' in line:
                if '(running)' in line and 'since' in line:
                    return {
                        "status": 'running',
                        "since": line.split('since')[1].strip()
                    }
                elif 'inactive' in line:
                    return {
                        "status": 'inactive'
                    }
                elif 'since' in line:
                    return {
                        "status": 'not-running',
                        "since": line.split('since')[1].strip()
                    }
        return {
            "status": "unknown"
        }
    except:
        return {
            "status": "error"
        }


def getNetworkType():
    try:
        comnet_string = "OPTIONS=\"--config config_comnet\"\n"
        lines = []
        default_file = "/etc/default/hornet"
        if not os.path.isfile(default_file):
            return 'mainnet'

        f = open(default_file, "r")
        lines = f.readlines()
        f.close()
        if comnet_string in lines:
            return 'comnet'
        else:
            return 'mainnet'
    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)


def getDashboardStatus():
    try:
        networkType = getNetworkType()
        if networkType == "comnet":
            config_file = "/var/lib/hornet/config_comnet.json"
        else:
            config_file = "/var/lib/hornet/config.json"

        lines = ""
        with open(config_file, "r") as f:
            data = json.load(f)
            if '0.0.0.0' in data["dashboard"]["bindAddress"]:
                return 'enabled'
            else:
                return 'disabled'
    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)


def getDashboardPort():
    try:
        networkType = getNetworkType()
        if networkType == "mainnet":
            config_file = "/var/lib/hornet/config.json"
        elif networkType == "comnet":
            config_file = "/var/lib/hornet/config_comnet.json"
        lines = ""
        with open(config_file, "r") as f:
            data = json.load(f)
            if '0.0.0.0' in data["dashboard"]["bindAddress"]:
                # split port
                return data["dashboard"]["bindAddress"].split(':')[1]
            else:
                return False
    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)

def getLocal():
    try:
        networkType = getNetworkType()
        if networkType == "comnet":
            config_file = "/var/lib/hornet/config_comnet.json"
        else:
            config_file = "/var/lib/hornet/config.json"

        lines = ""
        with open(config_file, "r") as f:
            data = json.load(f)
            if '/mnt' in data["snapshots"]["local"]["path"]:
                return '/mnt/hornet'
            else:
                return '/var/lib/hornet'
    except IOError as e:
        errorn, strerror = e.args
        if errorn == errno.EACCES:
            print("You need root permissions to do this!")
            sys.exit(1)

def getStatus():
    local = getLocal()
    if local == "/var/lib/hornet":
        local = "/var/lib/hornet (SD Card)"
    elif local == "/mnt/hornet":
        local = "/mnt/hornet (USB Volume)"

    status = {
        "version": getHornetVersion(),
        "node": getNodeStatus(),
        "networkType": getNetworkType(),
        "local": local,
        "dashboardStatus": getDashboardStatus(),
        "dashboardPort": getDashboardPort()
    }
    return json.dumps(status, indent=1)


def main():
    # check for sudo
    if os.geteuid() != 0:
        print("You need root permissions to do this!")
        sys.exit(1)

    # bootstrap parsers
    parser = argparse.ArgumentParser(prog='hornetctl')
    subparsers = parser.add_subparsers(help='hornetctl subcommands', dest='cmd')

    parser_node = subparsers.add_parser('node', help='start/stop node')
    parser_node.add_argument('node', choices=['on', 'off'], help='on starts, off stops')

    parser_status = subparsers.add_parser('status', help='show node status')

    parser_network = subparsers.add_parser('network', help='set mainnet/comnet')
    parser_network.add_argument('network', choices=['mainnet', 'comnet'], help='mainnet or comnet')

    parser_dashboard = subparsers.add_parser('dashboard', help='enable/disable dashboard')
    parser_dashboard.add_argument('dashboard', choices=['on', 'off'], help='on enables, off disables')

    parser_usb = subparsers.add_parser('usb', help='enable/disable USB for db and snapshot')
    parser_usb.add_argument('usb', choices=['on', 'off'], help='on enables, off disables')

    parser_clean = subparsers.add_parser('clean', help='clean db/snapshot')
    parser_clean.add_argument('clean', choices=['db', 'snapshot', 'all'], help='db, snapshot or all')

    parser_log = subparsers.add_parser('log', help='show log')

    args = parser.parse_args()

    # check if service is running
    status = os.system('systemctl is-active --quiet hornet') # will return 0 for active else inactive.
    if not status and args.cmd != 'node' and args.cmd != 'status' and args.cmd != 'log':
        try:
            print("Stopping hornet.service.")
            os.system("systemctl stop hornet")
        except:
            print("Error while stopping hornet systemd service.")

    comnet_config_file = "/var/lib/hornet/config_comnet.json"
    config_file = "/var/lib/hornet/config.json"

    # no cmd?
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # start/stop node?
    if args.cmd == 'node':
        hornetctl_node(args)

    if args.cmd == 'status':
        print(getStatus())

    # set mainnet/comnet?
    if args.cmd == 'network':
        hornetctl_network(args)

    # enable/disable dashboard?
    if args.cmd == 'dashboard':
        hornetctl_dashboard(comnet_config_file, args)
        hornetctl_dashboard(config_file, args)

    # enable/disable USB for db and snapshot?
    if args.cmd == 'usb':
        hornetctl_usb(args)

    if args.cmd == 'clean':
        hornetctl_clean(args)

    if args.cmd == 'log':
        hornetctl_log()

    # if service was running, restart it
    if not status and args.cmd != 'node' and args.cmd != 'status' and args.cmd != 'log':
        print(
            "Restarting hornet.service.\nIf you note systemd errors, stop the service, run \'hornetctl clean all\' and restart the service.")
        os.system('systemctl start hornet')


if __name__ == "__main__":
    main()
