import os, shutil, re, sys, tempfile

sys.path.append('./postprocessors')

from doc2html import DocToHTMLPostProcessor


def convert(file_path, target_format, output_path = None, executable='libreoffice', local_fonts = False, font_alternatives = False, inline_images = True):

    if not os.path.isfile(file_path):
        raise Exception('File not found')

    output_path = output_path or re.sub('^(.+)[/\\\\][^/\\\\]+$', '\\1', file_path)
    temp_profile_dir = tempfile.mkdtemp(prefix='doc-converter_').replace('\\', '/')
    env_override_user = '-env:UserInstallation=file:///' + temp_profile_dir + ''

    command = ' '.join([
        executable, env_override_user, '--headless', '--invisible', '--convert-to', target_format, '--outdir', output_path, file_path
    ])

    response = os.system(command)

    if target_format == 'html' and re.match('.*\.(docx?|odt)$', file_path, re.IGNORECASE):
        DocToHTMLPostProcessor(re.sub('^(.+)\.(docx?|odt)$', '\\1.html', file_path, re.IGNORECASE), output_path, local_fonts = local_fonts, font_alternatives = font_alternatives, inline_images = inline_images)

    shutil.rmtree(temp_profile_dir)

    return response == 0


if __name__ == '__main__':

    import getopt

    def usage():
        print('python converter.py -i [INPUT_FILE] -o [OUTPUT_FILE] -f [FORMAT] [--executable=[LIBREOFFICE_PATH]] [--local-fonts=[LOCAL_FONTS]] [-font-alternatives=[FONT_ALTERNATIVES]] [--inline-images]')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:f:', ['executable=', 'local-fonts=', 'font-alternatives=', 'inline-images'])
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(2)

    file_path = None
    target_format = None
    output_path = None
    executable='libreoffice'
    local_fonts = False
    font_alternatives = False
    inline_images = False

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(2)
        elif opt == '-i':
            file_path = arg
        elif opt == '-o':
            output_path = arg
        elif opt == '-f':
            target_format = arg
        elif opt == '--executable':
            executable = arg
        elif opt == '--local-fonts':
            local_fonts = arg
            if not local_fonts[-1] in ['/','\\']:
                local_fonts += '/'
        elif opt == '--font-alternatives':
            font_alternatives = arg
        elif opt == '--inline-images':
            inline_images = True

        else:
            usage()
            raise Exception('Invalid parameter: ' + arg)

    if not file_path:
        usage()
        raise Exception('Source file not specified')

    if not target_format:
        usage()
        raise Exception('Target format not specified')

    result = convert(file_path, target_format, output_path, executable, local_fonts, font_alternatives, inline_images)
    print(result and 'OK' or 'UNSPECIFIED ERROR')
