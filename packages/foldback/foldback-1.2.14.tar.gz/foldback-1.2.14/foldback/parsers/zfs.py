"""
ZFS status
"""

from foldback.parsers import ShellCommandParser, ShellCommandParserError


class Pool(object):
    """ZFS pool

    """
    def __init__(self, name):
        self.name = name


class ZFSPools(ShellCommandParser):
    """ZFS zpools list

    """
    def update(self):
        """List of ZFS pools


        """
        cmd = ( 'zpool', 'list', '-Hp' )
        self.execute(cmd)

        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise ZFSError('Error running {0}: {1}'.format(' '.join(cmd), stderr))
