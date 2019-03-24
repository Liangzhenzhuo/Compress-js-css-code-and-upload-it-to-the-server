from os import listdir, remove
from os.path import dirname
from paramiko.sftp_client import SFTPClient
from paramiko import Transport
from warnings import filterwarnings
from jsmin import jsmin
from cssmin import cssmin
filterwarnings(action='ignore', module='.*paramiko.*')
cur_path = dirname(__file__) + '/'


def cssmini(code):
    new_css = cssmin(code, wrap=None)
    return new_css


def jsmini(code):
    jsmini = jsmin(code)
    return jsmini


def upload_file(host, port, usr, psw, local_path, remote_path):
    file_count = 0
    print('-' * 50 + '\n')
    print('Start uploading files')
    transport = Transport((host, port))
    transport.connect(username=usr, password=psw)
    sftp = SFTPClient.from_transport(transport)
    for file_name in listdir(local_path):
        local_file = local_path + '\\' + file_name
        remote_file = remote_path + '/' + file_name
        if file_name.split('.')[-1] == 'css':
            new_css = cssmini(open(local_file, 'r').read())
            with open('tmp.css', 'w') as tmp_css:
                tmp_css.write(new_css)
                tmp_css.close()
                sftp.put(cur_path + tmp_css.name, remote_file)
                remove(cur_path + tmp_css.name)
        elif file_name.split('.')[-1] == 'js':
            new_js = jsmini(open(local_file, 'r', encoding='utf-8').read())
            with open('tmp.js', 'w', encoding='utf-8') as tmp_js:
                tmp_js.write(new_js)
                tmp_js.close()
                sftp.put(cur_path + tmp_js.name, remote_file)
                remove(cur_path + tmp_js.name)
        else:
            sftp.put(local_file, remote_file)
        print(file_name + 'Upload completed')
        file_count += 1
    transport.close()
    print('All files have been uploaded, Connection has been closed, Number of files：{}'.format(file_count))
    print('-' * 50 + '\n')


if __name__ == '__main__':
    upload_file(host='192.168.100.43', port=22, usr='root', psw='password',
                local_path=r'C:\test', remote_path='/home/test')
