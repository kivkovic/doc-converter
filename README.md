# doc-converter

A Python CLI script for document conversion between various file formats with advanced postprocessing capabilities. Allows conversion between various office document formats (`doc`↔`docx`↔`odt`↔`rtf`, `xls`↔`xlsx`↔`ods`, `ppt`↔`pptx`↔`odp`, etc.) and exporting to various standard formats (`pdf`,`html`,`txt`,`png`,`jpg`, etc.). Constists of a Python wrapper around Libreoffice and some custom-built postprocessors.

## Usage

```
python converter.py -i [INPUT_FILE] -o [OUTPUT_DIR] -f [FORMAT] [--executable=[LIBREOFFICE_PATH]] [--local-fonts=[LOCAL_FONTS]] [-font-alternatives=[FONT_ALTERNATIVES]] [--inline-images]
```

Parameters:

 - `input_file` - path to the source file
 - `output_dir` - destination directory
 - `format` - output format, given as a standard extension: `doc`, `pdf`, `html`, etc. For a list of supported formats, see: [Libreoffice supported formats](https://en.wikipedia.org/wiki/LibreOffice#Supported_file_formats) 
 - `libreoffice_path` - (*optional*) path to the Libreoffice executable (by default, calls `libreoffice`)
 - `local_fonts` - (*optional, only for html output*) a directory containing ttf/otf/woff/woff2 fonts which should be included as base64 strings inside html. If this option is missing, no font files will be included
 - `font_alternatives` - (*optional, only for html output*) a file describing font fallbacks (e.g. `"Times New Roman", "Times", "Liberation Serif", serif`) which will try to replace all fonts inside the document with their corresponding callbacks located inside `fonts_dir`. See the file `fonts/alternatives.list` in this repository for an example
 - `inline_images` - (*optional, only for html output*) if argument is specified, all images will be converted to inline base64 strings. By default, images are stored in the same folder as the resulting html file

Example of usage:

```
python converter.py -i ./~test/test1.docx -o ./~test/1 -f html --executable='"C:\\Program Files (x86)\\LibreOffice 5\\program\\soffice.exe"' --local-fonts=./fonts --font-alternatives=./fonts/alternatives.list --inline-images
```


 ## Requirements

 - python 2+
 - Libreoffice