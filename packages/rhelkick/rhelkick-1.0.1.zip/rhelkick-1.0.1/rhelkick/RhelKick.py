"""Prepare the current machine to build other hosts.

This module allows for command line or programtic generation of kickstart files
and serving other necessary items for rhel-like distros.
-Ryan Birmingham
"""
import os
import time
import datetime
import socket
import pyftpdlib

class RhelKick(object):
    """An object to keep track of server options and hosted items.

    Args:
        folder: Folder to put files in and host.
        services: A list, file, or file path containing a list of services.
        options: A list, file, or file path containing a list of options.
    """

    def __init__(self, folder="kickstart", services=["web"], options={"ext_host": "8.8.8.8"}):
        """initalize, trying to normalize input."""
        # get ready for kickstart file creation
        self.kickfile = open(folder+'rhelkick-ks.cfg', 'w+')
        # start time
        starttime = datetime.datetime.fromtimestamp(time.time())
        self.starttime = starttime.strftime('%Y-%m-%d %H:%M:%S')
        # if services looks like a list, then use it
        if not os.path.isdir(folder):
            os.mkdir(folder)
        self.folder = folder
        self.kickfile = open(folder+'/anaconda-ks.cfg', 'w+')
        self.services = services
        if type(services) is not list:
            if type(services) is not file:
                try:
                    services = open(services)
                except IOError:
                    raise IOError('Services file interpreted as path,'
                                  'not found')
                except TypeError:
                    raise TypeError('services input type not understood')
            self.services = services.read().splitlines()
        # if options is not a dictionary, avoid it
        self.options = options
        if type(options) is not dict:
            if type(options) is not file:
                try:
                    options = open(options)
                except IOError:
                    raise IOError('Options file interpreted as path,'
                                  'not found')
                except TypeError:
                    raise TypeError('options input type not understood')
            try:
                self.options = {x.split(":")[0]: x.split(":")[1]
                                for x in options.read().splitlines()}
            except IndexError:
                raise IOError('Option file should have key:value per line.')
        self.port = 8080
        self.myip = self.get_ip(self.options.get("ext_host", "8.8.8.8"))

    def __str__(self):
        """Return a string for command line invoke."""
        return "RhelKick instance, started at " + self.starttime

    def touch(self):
        """Update create time."""
        starttime = datetime.datetime.fromtimestamp(time.time())
        self.starttime = starttime.strftime('%Y-%m-%d %H:%M:%S')

    def get_ip(self, to="8.8.8.8"):
        """Get external ip address."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((to, 80))
        return s.getsockname()[0]

    def get_services(self):
        """create a port openings for firewall for services."""
        serv_map = {"web": "80:tls,",
                    "ssh": "ssh:tls,",
                    "ftp": "ftp:tls,",
                    "mysql": "3306:tcp,3306:udp,"}
        return "".join(serv_map[line] for line in self.services)[:-1]

    def partition_scheme(self):
        """Write partition rules."""
        # Partition management, within install
        partscheme = self.options.get("partition", "standard")
        drivesize = self.options.get("drivesize", "200000")  # 20gb
        swap = self.options.get("swap", "4096")  # 4gb
        formattyype = self.options.get("formattype", "ext3")
        if partscheme == "nochange":
            pass
        elif partscheme == "standard":
            self.kickfile.write("clearpart --all\n")
            self.kickfile.write("part /boot --fstype " + formattyype +
                                "--size=512\npart swap --size=" + swap + "\n")
            self.kickfile.write("part /home --fstype " + formattyype +
                                "--size="+(drivesize-(512+int(swap))/2)+"\n")
            self.kickfile.write("part / --fstype " + formattyype +
                                "--size="+(drivesize-(512+int(swap))/2)+"\n")
        elif partscheme == "nethome":
            self.kickfile.write("clearpart --all\n")
            self.kickfile.write("part /boot --fstype " + formattyype +
                                "--size=512\npart swap --size=" + swap + "\n")
            self.kickfile.write("part / --fstype " + formattyype +
                                "--size=1 --grow\n")
        elif partscheme == "defined":
            self.kickfile.write("clearpart --all\n")
            self.kickfile.write("part /boot --fstype " + formattyype +
                                "--size=512\npart swap --size=" + swap + "\n")
            self.kickfile.write("part /home --fstype " + formattyype +
                                "--size="+(drivesize-(512+int(swap))/3)+"\n")
            self.kickfile.write("part /var --fstype " + formattyype +
                                "--size="+(drivesize-(512+int(swap))/6)+"\n")
            self.kickfile.write("part /usr --fstype " + formattyype +
                                "--size="+(drivesize-(512+int(swap))/6)+"\n")
            self.kickfile.write("part /tmp --fstype " + formattyype +
                                "--size="+(drivesize-(512+int(swap))/6)+"\n")
            self.kickfile.write("part / --fstype " + formattyype +
                                "--size=1 --gr\n")
        else:
            self.kickfile.write("clearpart --all\n")
            boot = self.options.get("boot", "250")
            self.kickfile.write("part /boot --fstype " + formattyype +
                                "--size=" + boot + "\n")
            self.kickfile.write("part swap --size=" + swap + "\n")
            home = self.options.get("home", "100")
            self.kickfile.write("part /home --fstype " + formattyype +
                                "--size=" + home)
            home = self.options.get("root", "800")
            self.kickfile.write("part / --fstype " + formattyype +
                                "--size=" + home + "--grow\n")
        self.kickfile.write("\n")

    def writeNextHostTool(self):
        """Add the tool to automatically name the host."""
        hpatt = self.options.get("hostpattern", "build")
        self.kickfile.write("AVAIL=FALSE\nnewhn=" + hpatt + "0\nCOUNTER=1")
        self.kickfile.write('\nwhile [ "$avail" = "FALSE" ]; do\n')
        self.kickfile.write(" let newhn=build$COUNTER\n  ping -c1 -W1 " +
                            "$newhn || AVAIL=TRUE\n" +
                            "let COUNTER=COUNTER+1\n\n")
        self.kickfile.write("""echo setting hostname to $newhn
        awk '!/HOSTNAME:*/' /etc/sysconfig/network > tempnetwork
        awk '!/127.0.0.1*/' /etc/hosts > tmphosts
        echo 127.0.0.1       $newhn $newhn.""")
        self.kickfile.write(self.options.get("hostdomain", "localnet.com"))
        self.kickfile.write(""" localhost >> tmphosts
        mv tmphosts /etc/hosts
        echo HOSTNAME: $newhn >> tempnetwork
        mv tempnetwork /etc/sysconfig/network\n""")
        if (self.options.get("dhcp", "no").upper() == "YES"):
            self.kickfile.write("""echo setting up for dhcp
            echo DEVICE=eth0 > /etc/sysconfig/network-scripts/ifcfg-eth0
            echo BOOTPROTO=dhcp >> /etc/sysconfig/network-scripts/ifcfg-eth0
            echo ONBOOT=yes >> /etc/sysconfig/network-scripts/ifcfg-eth0
            echo DHCP_HOSTNAME=$newhn >> /etc/sysconfig/network-scripts/ifcfg-eth0
            """)

    def unpackAnsible(self):
        """unpack and run ansible items."""
        self.kickfile.write("""echo Installing ansible
        sudo easy_install pip
        pip install ansible
        echo installing ansible playbooks""")
        self.kickfile.write("wget http://" + self.get_ip(
            self.options.get("ext_host", "8.8.8.8")))
        self.kickfile.write("/" + self.options.get("ansible_tar", "no"))
        self.kickfile.write("tar -xvf -C /root/ansible/n")
        self.kickfile.write("""for f in ls /root/ansible/*.yml
        do
          ansible-playbook -i "localhost," -c local $f
        done""")

    def genKick(self):
        """Use input services and options to create a kickstart file."""
        # install section
        self.kickfile.write("install\n")
        myip = self.myip
        webpath = "url --url http://" + myip + ":" + self.port
        self.kickfile.write(webpath + "\n")
        lang = self.options.get("lang", "en_US.UTF-8")
        self.kickfile.write("lang " + lang + "\n")
        self.kickfile.write("langsupport --default " + lang + " " + lang)
        self.kickfile.write("keyboard " + self.options.get("keyboard", "us"))
        nameserver = self.options.get("nameserver", "192.168.0.1")
        netdevice = self.options.get("netdevice", "eth0")
        netline = "network --device " + netdevice + "--bootproto "
        if (self.options.get("dhcp", "NO").upper() == "YES"):
            netline = netline + ("dhcp --nameserver " + nameserver)
        elif (self.options.get("static", "YES").upper() == "YES"):
            ipaddr = self.options.get("ipaddr", "192.168.0.4")
            netmask = self.options.get("netmask", "255.255.255.0")
            gateway = self.options.get("gateway", "192.168.0.1")
            netline = netline + ("static --ip="+ipaddr)
            netline = netline + (" --netmask="+netmask)
            netline = netline + (" --gateway="+gateway)
            netline = netline + (" --nameserver="+nameserver)
        self.kickfile.write(netline+"\n")
        self.kickfile.write("rootpw "+self.options.get("rootpw", "toor"))
        if (self.options.get("firewall", "YES").upper() == "YES"):
            self.kickfile.write("firewall --enabled --port=" +
                                self.get_services() + "\n")
        self.kickfile.write("authconfig --enableshadow --enablemd5")
        if (self.options.get("ldap", "YES").upper() == "YES"):
            ldaphost = self.options.get("ldapserver", "192.168.0.1")
            lddn = self.options.get("ldapbasedn", "DC=build,DC=local")
            self.kickfile.write(" --enableldap --ldapserver=" + ldaphost +
                                "--ldapbasedn=" + lddn)
        self.kickfile.write("\n")
        self.kickfile.write("timezone " +
                            self.options.get("timezone", "America/New_York\n"))
        self.kickfile.write("bootloader --location=mbr\n")

        # Partition management, within install
        self.partition_scheme()

        # packages
        self.kickfile.write("%packages\n")
        self.kickfile.write("@ core\n")
        if "web" in self.services:
            self.kickfile.write("@ web-server\n")
        if "mysql" in self.services:
            self.kickfile.write("@ sql-server\n")
            self.kickfile.write("mysql-server\n")
        self.kickfile.write("\n")
        self.kickfile.write("%post --log=/root/my-post-log")

        # post-install
        if not (self.options.get("hostpattern", "no").upper() == "NO"):
            self.writeNextHostTool()

        if not (self.options.get("ansible_tar", "no").upper() == "NO"):
                    self.unpackAnsible()

    def hostFiles(self):
        """host the image and files required for kickstart install/config."""
        os.chdir(self.folder)
        address = ("0.0.0.0", self.port)
        server = pyftpdlib.servers.FTPServer(address, pyftpdlib.FTPHandler)
        server.serve_forever()

    def preparePxe(self, install=False, config=False):
        """run commands to get pxe ready. RHEL-like only."""
        # TODO add dhcpd
        "https://www.unixmen.com/install-pxe-server-and-configure-pxe-client-on-centos-7/"
        if install:
            os.system("yum install dhcpd")
            os.system("yum install syslinux")
        if config:
            adddhcpd = "\nallow booting;\nallow bootp;"
            adddhcpd = adddhcpd + "\noption option-128 code 128 = string;"
            adddhcpd = adddhcpd + "\noption option-129 code 129 = text;"
            adddhcpd = adddhcpd + "\nnext-server " + self.myip + ";"
            adddhcpd = adddhcpd + '\nfilename "pxelinux.0";'
            os.system("echo '" + adddhcpd + "' >> /etc/dhcp/dhcpd.conf")
        if install:
            os.system("systemctl restart dhcpd")
            os.system("systemctl enable dhcpd")
        os.system("cp -r /usr/share/syslinux/* " + self.folder)
        self.pxeMenu()

    def prepareImage(self, url="http://mirrors.xservers.ro/centos/7.0.1406/" +
                     "isos/x86_64/CentOS-7.0-1406-x86_64-DVD.iso"):
        """Get and prepare iso image."""
        os.chdir(self.folder)
        os.system("wget " + url)
        os.system("mount -o loop " + url.split("/")[-1] + " /mnt/")
        os.system("cp -fr /mnt/* " + self.folder + "/image/")

    def pxeMenu(self):
        menufile = "default menu.c32\nprompt 0\ntimeout 30"
        menufile = menufile + "\nMENU TITLE RhelKick"
        menufile = menufile + "\nLABEL PXE from RHELKICK"
        menufile = menufile + "\nMENU LABEL Rhellike as configured"
        menufile = menufile + "\nKERNEL " + self.folder + "/image/"
        menufile = menufile + "\nAPPEND  initrd=/netboot/initrd.img"
        menufile = menufile + "  inst.repo=ftp://" + self.myip
        menufile = menufile + " ks=ftp://" + self.myip + "/pub/rhelkick-ks.cfg"
        os.system("echo '" + menufile + "' > " + self.folder +
                  "/pxelinux.cfg/default")

if __name__ == "__main__":
    import sys
    args = ["this", "/root/rhelkick", "/root/rhelkick/options.cfg",
            "/root/rhelkick/services.cfg"]
    for x in range(1, len(sys.argv)):
        args[x] = sys.argv[x]
    rk = RhelKick(args[1], args[2], args[3])
    rk.genKick()
    if not (rk.options.get("srcurl", "NO") == "NO"):
        rk.prepareImage(rk.options.get("srcurl", "NO"))
    rk.preparePxe()
    rk.hostFiles()
