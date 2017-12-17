import os, shutil, re, sys, tempfile

sys.path.append('./postprocessors')

from doc2html import DocToHTMLPostProcessor


def convert(file_path, target_format, executable='libreoffice', local_fonts = False, font_alternatives = False):

    if not os.path.isfile(file_path):
        raise Exception('File not found')

    outdir = re.sub('^(.+)[/\\\\][^/\\\\]+$', '\\1', file_path)
    temp_profile_dir = tempfile.mkdtemp(prefix='doc-converter_').replace('\\', '/')
    env_override_user = '-env:UserInstallation=file:///' + temp_profile_dir + ''

    command = ' '.join([
        executable, env_override_user, '--headless', '--invisible', '--convert-to', target_format, '--outdir', outdir, file_path
    ])

    response = os.system(command)

    if target_format == 'html' and re.match('.*\.(docx?|odt)$', file_path, re.IGNORECASE):
        DocToHTMLPostProcessor(re.sub('^(.+)\.(docx?|odt)$', '\\1.html', file_path, re.IGNORECASE), local_fonts = local_fonts, font_alternatives = font_alternatives)

    shutil.rmtree(temp_profile_dir)

    return response == 0
