import os
import re

import sys
sys.path.append('./postprocessors')

from doc2html import DocToHTMLPostProcessor


def convert(file_path, target_format, executable='libreoffice'):

    if not os.path.isfile(file_path):
        raise Exception('File not found')

    outdir = re.sub('^(.+)[/\\\\][^/\\\\]+$', '\\1', file_path)

    response = os.system(' '.join([
        executable, '--headless', '--invisible', '--convert-to', target_format, '--outdir', outdir, file_path
    ]))

    if target_format == 'html' and re.match('.*\.(docx?|odt)$', file_path, re.IGNORECASE):
        DocToHTMLPostProcessor(re.sub('^(.+)\.(docx?|odt)$', '\\1.html', file_path, re.IGNORECASE))

    return response == 0
