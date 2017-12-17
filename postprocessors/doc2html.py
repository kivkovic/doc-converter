#from re import findall, match, sub, IGNORECASE
#from os import system, walk, path, makedirs
#from random import randint
#from base64 import b64encode

import tempfile, os

class DocToHTMLPostProcessor():

    def __init__(self, file_name):
        self.process_html(file_name)

    def process_html(self, file_name):

        temp_dir = tempfile.mkdtemp(prefix='doc2html_')
        temp_name = None

        with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as temporary, open(file_name, 'r') as source:
            temp_name = temporary.name
            source.seek(0)
            temporary.seek(0)

            line_context = dict(head=False, body=False, script=False, style=False)
            for line in source:
                temporary.write(line)

        os.remove(file_name)
        os.rename(temp_name, file_name)


        # detected_fonts = self.get_document_fonts(source)
        # available_fonts = self.get_physical_fonts('fonts/')
        # font_alternatives = self.get_font_alternatives('fonts/__alternatives.list')
        # (resolved_fonts, resolved_alternatives) = self.get_resolved_fonts(detected_fonts, available_fonts, font_alternatives)

        # line_context = dict(head=False, body=False, script=False, style=False)
        # for line in source:
        #     if match('.*<head[^>]*>.*', line, IGNORECASE):
        #         line_context['head'] = True
        #     if match('.*</head[^>]*>.*', line, IGNORECASE):
        #         self.write_document_style(temporary)
        #         self.write_font_imports(temporary, resolved_fonts)
        #         line_context['head'] = False
        #     if match('.*<body[^>]*>.*', line, IGNORECASE):
        #         line_context['body'] = True
        #     if match('.*</body[^>]*>.*', line, IGNORECASE):
        #         line_context['body'] = False
        #     if match('.*<script[^>]*>.*', line, IGNORECASE):
        #         line_context['script'] = True
        #     if match('.*</script[^>]*>.*', line, IGNORECASE):
        #         line_context['script'] = False
        #     if match('.*<style[^>]*>.*', line, IGNORECASE):
        #         line_context['style'] = True
        #     if match('.*</style[^>]*>.*', line, IGNORECASE):
        #         line_context['style'] = False
        #     temporary.write(self.replace_line_fonts(line, resolved_alternatives, line_context))

        # source.close()
        # temporary.close()

        # system(' '.join(['rm', file_path]))
        # system(' '.join(['mv', temp_file, file_path]))

    # def get_font_alternatives(self, path):
    #     font_alternatives = []

    #     with open(path, 'r') as fonts_file:
    #         for line in fonts_file:
    #             font_alternatives.append(
    #                 map(lambda name: name.strip().replace('"', '').replace("'", ""), line.rstrip().split(',')))

    #     return font_alternatives

    # def get_document_fonts(self, document_file):
    #     document_file.seek(0)
    #     fonts = []
    #     for line in document_file:
    #         if match('.*font(-family:|\\s+face\\s*=).*', line, IGNORECASE):
    #             fontfamily = findall('[{\\s;"](font-family:\\s*([^;}]+))["\\s;}]', line, IGNORECASE)
    #             fontface = findall('<\\s*(font[^>]+face\\s*=\\s*\"([^\"]+)\")\\s*>', line, IGNORECASE)
    #             for font in fontfamily + fontface:
    #                 if font and len(font) > 1:
    #                     fonts.append(
    #                         sub('^(.+)((, (sans|(sans-)?serif|mono(space)?))|( Fallback))$', '\\1',
    #                             font[1].replace('"', '').replace("'", ""),
    #                             IGNORECASE))

    #     return list(set(fonts))

    # def get_resolved_fonts(self, detected_fonts, available_fonts, font_alternatives):
    #     resolved_fonts = []
    #     resolved_names = []
    #     resolved_alternatives = dict()

    #     for document_font in detected_fonts:
    #         for physical_font in available_fonts:
    #             if physical_font['font_name'] == document_font and physical_font not in resolved_fonts:
    #                 resolved_fonts.append(physical_font)
    #                 if document_font not in resolved_names:
    #                     resolved_names.append(document_font)

    #     for document_font in detected_fonts:
    #         if document_font not in resolved_names:
    #             for alternative_font in font_alternatives:
    #                 if document_font == alternative_font[0]:
    #                     for physical_font in available_fonts:
    #                         for idx in range(1, len(alternative_font)):
    #                             if physical_font['font_name'] == alternative_font[idx]:
    #                                 if document_font not in resolved_alternatives:
    #                                     resolved_alternatives[document_font] =\
    #                                         ', '.join(map(lambda name: ' ' in name and '"' + name + '"' or name, alternative_font))
    #                                 resolved_fonts.append(physical_font)

    #     return (resolved_fonts, resolved_alternatives)

    # def get_physical_fonts(self, path):

    #     fonts = []
    #     font_files = []
    #     for (dirpath, dirnames, filenames) in walk(path):
    #         font_files.extend(filenames)
    #         break

    #     for filename in font_files:

    #         matches = match('^(.+)-(.+).ttf$', filename)
    #         if matches:
    #             families = matches.group(1).split(',')
    #             fonttype = matches.group(2).split(',')
    #             fontstyle = None

    #             common_name = families[0]
    #             weight = self.guess_weight(families[0])

    #             if len(families) > 1:
    #                 if match('.*cond', families[1]) and not match('.*cond', families[0]):
    #                     common_name = families[0] + ' ' + 'Condensed'
    #                 weight = self.guess_weight(families[1]) or weight

    #             for fstyle in matches.groups():
    #                 if not fontstyle and match('.*(ital(ic)?|obliq(ue)?)', fstyle, IGNORECASE):
    #                     fontstyle = 'italic'
    #                 if not match('.*cond', common_name, IGNORECASE) and match('.*Cond', fstyle):
    #                     common_name = common_name + ' ' + 'Condensed'

    #             if not weight:
    #                 for ftype in fonttype:
    #                     weight = self.guess_weight(ftype)
    #                     if weight:
    #                         break

    #             weight = weight or 400
    #             fontstyle = fontstyle or 'normal'
    #             fonts.append(dict(font_name=common_name, font_weight=weight, font_style=fontstyle, font_path=path + filename))

    #     return fonts

    # def replace_line_fonts(self, line, font_alternatives, line_context):
    #     if match('.*font(-family:|\\s+face\\s*=).*', line, IGNORECASE):
    #         for font in font_alternatives:
    #             if line_context['style'] and not line_context['script']:
    #                 line = sub('(font-family:)\\s*("?' + font + '"?[^;}]+)', '\\1 ' + font_alternatives[font], line, IGNORECASE)
    #             if line_context['body'] and not line_context['script'] and not line_context['head']:
    #                 line = sub('(<\\s*font[^>]+face\\s*=\\s*\")(' + font + '[^\"]+)(\"\\s*>)', '\\1' + font_alternatives[font].replace('"', '') + '\\3', line, IGNORECASE)

    #     return line

    # def write_document_style(self, target):
    #     target.write('<style type="text/css">\nhtml { width: 100%; height: 100%; margin: 0; padding: 0}\n' +
    #                  'body { width: 597px; margin: 76px; }\n</style>\n')

    # def write_font_imports(self, target, fonts):
    #     target.write('<style type="text/css">')
    #     for font in fonts:
    #         woff2file = open(font['font_path'].replace('.ttf', '.woff2'), 'r')
    #         ttffile = open(font['font_path'], 'r')

    #         target.write(
    #             """
    #             @font-face {
    #                 font-family: '%s',
    #                 src: url(data:application/font-woff;charset=utf-8;base64,%s) format('woff2'),
    #                      url(data:application/font-ttf;charset=utf-8;base64,%s) format('ttf');
    #                 font-weight: %d;
    #                 font-style: %s;
    #             }
    #             """ % (font['font_name'],
    #                    b64encode(woff2file.read()),
    #                    b64encode(ttffile.read()),
    #                    font['font_weight'],
    #                    font['font_style'])
    #         )

    #         woff2file.close()
    #         ttffile.close()

    #     target.write('</style>\n')

    # def guess_weight(self, name):
    #     suffix = '\\s*(cond(ensed)?|obliq(ue)?|ital(ic)?)?$'

    #     if match('(thin|hairline|ultra-?light|extra-?light)' + suffix, name, IGNORECASE):
    #         return 100
    #     if match('(light)' + suffix, name, IGNORECASE):
    #         return 200
    #     if match('(book)' + suffix, name, IGNORECASE):
    #         return 300
    #     if match('(regular|normal|plain|standard|roman)' + suffix, name, IGNORECASE):
    #         return 400
    #     if match('(medium)' + suffix, name, IGNORECASE):
    #         return 500
    #     if match('((s|d)emi-?bold)' + suffix, name, IGNORECASE):
    #         return 600
    #     if match('(bold)' + suffix, name, IGNORECASE):
    #         return 700
    #     if match('(heavy|black|extra-?bold)' + suffix, name, IGNORECASE):
    #         return 800
    #     if match('((ultra|heavy)-?(black|bold)|extra-?black|fat|poster)' + suffix, name, IGNORECASE):
    #         return 900
    #     return None
