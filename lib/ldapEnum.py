#!/usr/bin/env python3

import os
from sty import fg, bg, ef, rs
from lib import nmapParser
from subprocess import call
from utils import config_paths


class LdapEnum:
    def __init__(self, target):
        self.target = target
        self.processes = ""

    def ldapSearch(self):
        np = nmapParser.NmapParserFunk(self.target)
        np.openPorts()
        ldap_ports = np.ldap_ports
        if len(ldap_ports) == 0:
            pass
        else:
            ldap_enum = f"lib/ldap.sh {self.target}"
            call(ldap_enum, shell=True)

    def Scan(self):
        np = nmapParser.NmapParserFunk(self.target)
        np.openPorts()
        ldap_ports = np.ldap_ports
        if len(ldap_ports) == 0:
            pass
        else:
            c = config_paths.Configurator(self.target)
            c.createConfig()
            if not os.path.exists(f"""{c.getPath("ldapDir")}"""):
                os.makedirs(f"""{c.getPath("ldapDir")}""")
            c = (
                fg.cyan
                + "Enumerating LDAP: Lightweight Directory Access Protocol, Running the following commands:"
                + fg.rs
            )
            print(c)
            string_ldap_ports = ",".join(map(str, ldap_ports))
            commands = (
                f"""nmap -vv -Pn -sV -p {string_ldap_ports} --script='(ldap* or ssl*) and not (brute or broadcast or dos or external or fuzzer)' -oA {c.getPath("nmapLdap")} {self.target}""",
                f"""enum4linux -a -M -l -d {self.target} | tee {c.getPath("ldapEnum4linux")}""",
            )
            self.processes = commands
