import tempfile, os, shutil, re, base64

class DocToHTMLPostProcessor():

    def __init__(self, file_name, output_path, local_fonts = False, font_alternatives = False, inline_images = True):
        if not output_path[-1] in ['/','\\']:
            output_path += '/'

        self.file_name = output_path + os.path.basename(file_name)
        self.output_path = output_path
        self.local_fonts = local_fonts
        self.inline_images = inline_images
        self.font_alternatives = font_alternatives
        self.images_to_delete = []

        self.process_html()

    def process_html(self):


        self.temp_dir = tempfile.mkdtemp(prefix='doc2html_')
        self.temp_name = None

        with tempfile.NamedTemporaryFile(dir=self.temp_dir, delete=False, mode='w') as temporary, open(self.file_name, 'r') as source:
            self.temp_name = temporary.name

            if self.local_fonts:
                detected_fonts = self.get_document_fonts(source)
                available_fonts = self.get_physical_fonts(self.local_fonts)

                if self.font_alternatives:
                    font_alternatives = self.get_font_alternatives()
                else:
                    font_alternatives = []

                (resolved_fonts, resolved_alternatives) = self.get_resolved_fonts(detected_fonts, available_fonts, font_alternatives)

            line_context = dict(head=False, body=False, script=False, style=False)

            source.seek(0)
            temporary.seek(0)

            for line in source:
                if re.search('<head[^>]*>', line, re.IGNORECASE):
                    line_context['head'] = True

                if re.search('</head[^>]*>', line, re.IGNORECASE):
                    if self.local_fonts:
                        self.write_font_imports(temporary, resolved_fonts)
                    line_context['head'] = False

                if re.search('<body[^>]*>', line, re.IGNORECASE):
                    line_context['body'] = True

                if re.search('</body[^>]*>', line, re.IGNORECASE):
                    line_context['body'] = False

                if re.search('<script[^>]*>', line, re.IGNORECASE):
                    line_context['script'] = True

                if re.search('</script[^>]*>', line, re.IGNORECASE):
                    line_context['script'] = False

                if re.search('<style[^>]*>', line, re.IGNORECASE):
                    line_context['style'] = True

                if re.search('</style[^>]*>', line, re.IGNORECASE):
                    line_context['style'] = False

                if self.local_fonts and re.search('font(-family:|\\s+face\\s*=)', line, re.IGNORECASE):
                    line = self.replace_line_fonts(line, resolved_alternatives, line_context)

                if self.inline_images and re.search('<img[^<>]+>', line, re.IGNORECASE):
                    line = self.replace_images(line)

                temporary.write(line)

        os.remove(self.file_name)
        os.rename(self.temp_name, self.file_name)
        shutil.rmtree(self.temp_dir)

        for image in set(self.images_to_delete):
            os.remove(image)

    def replace_images(self, line):
        for image in re.finditer('<img[^<>]+src="([^"]+)"', line, re.IGNORECASE):

            image_path = self.output_path + '/' + image.group(1)

            with open(image_path, 'rb') as image_file:
                extension = os.path.splitext(image_path)[1][1:]
                encoded_string = base64.b64encode(image_file.read())
                line = line[:image.start(1)] + 'data:image/' + extension + ';base64,' + str(encoded_string) + line[image.end(1):]

            self.images_to_delete.append(image_path)

        return line

    def get_font_alternatives(self):
        font_alternatives = []

        with open(self.font_alternatives, 'r') as fonts_file:
            for line in fonts_file:
                font_alternatives.append(
                    list(map(lambda name: name.strip().replace('"', '').replace("'", ""), line.rstrip().split(','))))

        return font_alternatives

    def get_document_fonts(self, document_file):
        document_file.seek(0)
        fonts = []
        for line in document_file:
            if re.search('font(-family:|\\s+face\\s*=)', line, re.IGNORECASE):
                fontfamily = re.findall('[{\\s;"](font-family:\\s*([^;}]+))["\\s;}]', line, re.IGNORECASE)
                fontface = re.findall('<\\s*(font[^>]+face\\s*=\\s*\"([^\"]+)\")\\s*>', line, re.IGNORECASE)
                for font in fontfamily + fontface:
                    if font and len(font) > 1:
                        fonts.append(
                            re.sub('^(.+)((, (sans|(sans-)?serif|mono(space)?))|( Fallback))$', '\\1',
                                font[1].replace('"', '').replace("'", ""),
                                re.IGNORECASE))

        return list(set(fonts))

    def get_resolved_fonts(self, detected_fonts, available_fonts, font_alternatives):
        resolved_fonts = []
        resolved_names = []
        resolved_alternatives = dict()

        for document_font in detected_fonts:
            for physical_font in available_fonts:
                if physical_font['font_name'] == document_font and physical_font not in resolved_fonts:
                    resolved_fonts.append(physical_font)
                    if document_font not in resolved_names:
                        resolved_names.append(document_font)

        for document_font in detected_fonts:
            if document_font not in resolved_names:
                for alternative_font in font_alternatives:
                    if document_font == alternative_font[0]:
                        for physical_font in available_fonts:
                            for idx in range(1, len(alternative_font)):
                                if physical_font['font_name'] == alternative_font[idx]:
                                    if document_font not in resolved_alternatives:
                                        resolved_alternatives[document_font] =\
                                            ', '.join(map(lambda name: ' ' in name and '"' + name + '"' or name, alternative_font))
                                    resolved_fonts.append(physical_font)

        return (resolved_fonts, resolved_alternatives)

    def get_physical_fonts(self, path):

        fonts = []
        font_files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            font_files.extend(filenames)
            break

        for filename in font_files:

            re.matches = re.match('^(.+)-(.+).ttf$', filename)
            if re.matches:
                families = re.matches.group(1).split(',')
                fonttype = re.matches.group(2).split(',')
                fontstyle = None

                common_name = families[0]
                weight = self.guess_weight(families[0])

                if len(families) > 1:
                    if re.match('.*cond', families[1]) and not re.match('.*cond', families[0]):
                        common_name = families[0] + ' ' + 'Condensed'
                    weight = self.guess_weight(families[1]) or weight

                for fstyle in re.matches.groups():
                    if not fontstyle and re.match('.*(ital(ic)?|obliq(ue)?)', fstyle, re.IGNORECASE):
                        fontstyle = 'italic'
                    if not re.match('.*cond', common_name, re.IGNORECASE) and re.match('.*Cond', fstyle):
                        common_name = common_name + ' ' + 'Condensed'

                if not weight:
                    for ftype in fonttype:
                        weight = self.guess_weight(ftype)
                        if weight:
                            break

                weight = weight or 400
                fontstyle = fontstyle or 'normal'
                fonts.append(dict(font_name=common_name, font_weight=weight, font_style=fontstyle, font_path=path + filename))

        return fonts

    def replace_line_fonts(self, line, font_alternatives, line_context):
        for font in font_alternatives:
            if line_context['style'] and not line_context['script']:
                line = re.sub('(font-family:)\\s*("?' + font + '"?[^;}]+)', '\\1 ' + font_alternatives[font], line, re.IGNORECASE)
            if line_context['body'] and not line_context['script'] and not line_context['head']:
                line = re.sub('(<\\s*font[^>]+face\\s*=\\s*\")(' + font + '[^\"]+)(\"\\s*>)', '\\1' + font_alternatives[font].replace('"', '') + '\\3', line, re.IGNORECASE)

        return line

    def write_font_imports(self, target, fonts):
        target.write('<style type="text/css">')
        for font in fonts:
            woff2file = open(font['font_path'].replace('.ttf', '.woff2'), 'r')
            ttffile = open(font['font_path'], 'r')

            target.write(
                """
                @font-face {
                    font-family: '%s',
                    src: url(data:application/font-woff;charset=utf-8;base64,%s) format('woff2'),
                         url(data:application/font-ttf;charset=utf-8;base64,%s) format('ttf');
                    font-weight: %d;
                    font-style: %s;
                }
                """ % (font['font_name'],
                       base64.b64encode(woff2file.read()),
                       base64.b64encode(ttffile.read()),
                       font['font_weight'],
                       font['font_style'])
            )

            woff2file.close()
            ttffile.close()

        target.write('</style>\n')

    def guess_weight(self, name):
        suffix = '\\s*(cond(ensed)?|obliq(ue)?|ital(ic)?)?$'
        # try larger regexes first
        if re.search('^((ultra|heavy)-?(black|bold)|extra-?black|fat|poster)' + suffix, name, re.IGNORECASE):
            return 900
        if re.search('^(heavy|black|extra-?bold)' + suffix, name, re.IGNORECASE):
            return 800
        if re.search('^((s|d)emi-?bold)' + suffix, name, re.IGNORECASE):
            return 600
        if re.search('^(bold)' + suffix, name, re.IGNORECASE):
            return 700
        if re.search('^(thin|hairline|(ultra|extra)-?light)' + suffix, name, re.IGNORECASE):
            return 100
        if re.search('^(light)' + suffix, name, re.IGNORECASE):
            return 200
        if re.search('^(medium)' + suffix, name, re.IGNORECASE):
            return 500
        if re.search('^(book)' + suffix, name, re.IGNORECASE):
            return 300
        if re.search('^(regular|normal|plain|standard|roman)' + suffix, name, re.IGNORECASE):
            return 400
        return None
