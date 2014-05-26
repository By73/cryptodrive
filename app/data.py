import os.path
import configparser


class DataConf(object):
    '''
    A container object that finds, reads and generates metadata
    '''
    def __init__(self, files=[]):
        self.files = files
        self.conf_files = self.fetch_config_files(self.files)

    config = configparser.ConfigParser(allow_no_value=True)

    def __str__(self):
        pass

    def fetch_config_files(self, files):
        '''Fetches config paths'''
        delim = {'posix': '/',
                 'nt': '\\'}

        if os.name == 'posix':
            default_config_files = ['/etc/cryptodrive/server.conf',
                                    '/etc/cryptodrive/client.conf',
                                    'ROOT/config/server.conf',
                                    'ROOT/client.conf',
                                    '~/.cryptodrive/server.conf',
                                    '~/.cryptodrive/client.conf']
        elif os.name == 'nt':
            default_config_files = ['ROOT\\config\\server.conf',
                                    'ROOT\\client.conf',
                                    '~\\.cryptodrive\\server.conf',
                                    '~\\.cryptodrive\\client.conf']

        for file in files:
            default_config_files.append(file)

        config_files = []

        for i in default_config_files:
            dir = i.split(delim[os.name])

            if dir[0] == 'ROOT':
                path = i[4:]
                root = ''
                for dir in os.getcwd().split('/'):
                    if dir == '':
                        continue
                    root = root + '/' + dir
                    if dir == 'cryptodrive':
                        break
                path = root + path
                exist = os.path.exists(path)
                file_data = [exist, path]
                config_files.append(file_data)

            elif dir[0] == '~':
                path = os.path.expanduser(i)
                exist = os.path.exists(path)
                file_data = [exist, path]
                config_files.append(file_data)

            else:
                exist = os.path.exists(i)
                file_data = [exist, i]
                config_files.append(file_data)

        return config_files

if __name__ == '__main__':
    files = ['/etc/testfile1', '/etc/testfile2']
    data = Data(files).fetch_config_files(files)
    for i in data:
        print(i)
