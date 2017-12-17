import os
import re


def convert(file_path, target_format, executable='libreoffice'):

    if not os.path.isfile(file_path):
        raise Exception('File not found')

    outdir = re.sub('^(.+)[/\\\\][^/\\\\]+$', '\\1', file_path)

    response = os.system(' '.join([
        executable, '--headless', '--invisible', '--convert-to', target_format, '--outdir', outdir, file_path
    ]))

    return response == 0
