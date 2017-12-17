import os, shutil, re, sys, tempfile

sys.path.append('./postprocessors')

from doc2html import DocToHTMLPostProcessor


def convert(file_path, target_format, executable='libreoffice', local_fonts = False, font_alternatives = False, inline_images = True):

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
        DocToHTMLPostProcessor(re.sub('^(.+)\.(docx?|odt)$', '\\1.html', file_path, re.IGNORECASE), local_fonts = local_fonts, font_alternatives = font_alternatives, inline_images = inline_images)

    shutil.rmtree(temp_profile_dir)

    return response == 0


if __name__ == '__main__':

    import getopt

    def usage():
        print('python converter.py -s [FILE] -f [FORMAT] [-e [LIBREOFFICE_PATH]] [-l [FONTS_DIR]] [-a [FONT_ALTERNATIVES_FILE]] [-i]')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:f:e:l:a:ih')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    file_path = None
    target_format = None
    executable='libreoffice'
    local_fonts = False
    font_alternatives = False
    inline_images = False

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(2)
        elif opt == '-s':
            file_path = arg
        elif opt == '-f':
            target_format = arg
        elif opt == '-e':
            executable = arg
        elif opt == '-l':
            local_fonts = arg
            if not local_fonts[-1] in ['/','\\']:
                local_fonts += '/'
        elif opt == '-a':
            font_alternatives = arg
        elif opt == '-i':
            inline_images = True

        else:
            usage()
            sys.exit(2)

    if not file_path:
        usage()
        raise Exception('Source file not specified')

    if not target_format:
        usage()
        raise Exception('Target format not specified')

    result = convert(file_path, target_format, executable, local_fonts, font_alternatives, inline_images)
    print(result and 'OK' or 'UNSPECIFIED ERROR')
