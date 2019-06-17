import os, subprocess, shutil, re, sys, glob, tempfile, time, logging

#sys.path.append('./postprocessors')
#from doc2html import DocToHTMLPostProcessor

def convert(file_path, target_format, output_path = None, executable = None, local_fonts = False, font_alternatives = False, inline_images = True, proc_timeout = 10000):

    if not os.path.isfile(file_path):
        raise Exception('File not found')

    if executable:
        executable_root = re.sub('[\\/][^\\/]*$', '', executable)
        executable_file = re.sub('^.*[\\/]*', '', executable)

    else:
        paths = glob.glob(os.environ['PROGRAMFILES'] + '\\LibreOffice*') + \
            glob.glob(os.environ['PROGRAMFILES(X86)'] + '\\LibreOffice*') + \
            glob.glob('/opt/libreoffice*') + \
            glob.glob('/usr/local/libreoffice*')

        for path in paths:
            for subdir in ['program', '']:
                for binary in ['soffice.exe', 'soffice.bin', 'soffice']:
                    if os.path.isfile(os.path.realpath(path + '/' + subdir + '/' + binary)):
                        executable_root = os.path.realpath(path + '/' + subdir)
                        executable_file = binary
                        break

    output_path = output_path or re.sub('^(.+)[/\\][^/\\]+$', '\\1', file_path)
    temp_profile_dir = tempfile.mkdtemp(prefix = 'doc-converter_').replace('\\', '/')
    env_override_user = '-env:UserInstallation=file:///' + temp_profile_dir

    arguments = [
        executable_file,
        env_override_user,
        '--headless',
        '--invisible',
        '--nocrashreport',
        '--nodefault',
        '--nofirststartwizard',
        '--nologo',
        '--norestore',
        '--convert-to', target_format,
        '--outdir', output_path,
        file_path
    ]

    log.info('Calling subprocess.Popen with arguments: ' + ' '.join(arguments))

    libreprocess = subprocess.Popen(arguments, executable = executable_root + '/' + executable_file, env = os.environ)
    timeout = 0

    while True:
        returncode = libreprocess.poll()

        if returncode != None:
            if returncode == 0:
                log.info('Return code: ' + str(returncode))
                libreprocess.wait()
                shutil.rmtree(temp_profile_dir)
                return True
            else:
                log.error('Return code: ' + str(returncode))
                break

        timeout += 1000
        if timeout <= proc_timeout:
            time.sleep(1)
        else:
            break

    log.error('Process timed out after ' + proc_timeout + 'ms')
    if libreprocess:
        try:
            libreprocess.kill()
            log.info('Sent kill to process')
        except AttributeError:
            os.kill(libreprocess.pid, 9)
            log.info('Sent kill 9 to process')

    time.sleep(3)
    shutil.rmtree(temp_profile_dir)

    return False


log = type('', (), {})()
log.log = log.debug = log.info = log.warning = log.error = log.exception = log.critical = lambda x: x

if __name__ == '__main__':

    import getopt

    def usage():
        print('python converter.py -i [INPUT_FILE] -o [OUTPUT_FILE] -f [FORMAT] [--executable=[LIBREOFFICE_PATH]]')
        #print('python converter.py -i [INPUT_FILE] -o [OUTPUT_FILE] -f [FORMAT] [--executable=[LIBREOFFICE_PATH]] [--local-fonts=[LOCAL_FONTS]] [-font-alternatives=[FONT_ALTERNATIVES]] [--inline-images]')

    log = logging.getLogger(__name__)
    logging.basicConfig(filename = 'doc-converter.log', level = logging.INFO, format = '%(asctime)-15s %(message)s')
    log.info('Started doc-converter with arguments: ' + ' '.join(sys.argv[1:]))

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:f:', ['executable=', 'local-fonts=', 'font-alternatives=', 'inline-images'])
    except getopt.GetoptError as e:
        log.error(e)
        usage()
        sys.exit(2)

    file_path = None
    target_format = None
    output_path = None
    executable = None
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

    convert(file_path, target_format, output_path, executable, local_fonts, font_alternatives, inline_images)
