from pathlib import PurePath
from ftplib import FTP
from .filewrapbase import FileWrapBase


class FileWrapFtp(FileWrapBase):
    def __init__(self, uri, type=None, user='anonymous', password=''):
        super(FileWrapFtp, self).__init__(uri, type)
        self.user = user
        self.password = password

    def readdir(self):
        if not self.is_dir:
            raise NotADirectoryError
        with FTP(self.hostname, self.user, self.password) as ftp:
            ftp.cwd(self.path)
            for (name, t) in ftp.mlsd(facts=['type']):
                if t['type'] in ('dir', 'file'):
                    yield FileWrapFtp(PurePath(self.uri).joinpath(name), type=t['type'], user=self.user, password=self.password)
                else:
                    continue

    def _get_type(self):
        """ TODO """
        return 'dir'

    def _get_parent(self):
        return FileWrapFtp(PurePath(self.uri).parent.as_posix(), user=self.user, password=self.password)