# doc-converter

A Python CLI script for document conversion between various file formats with advanced postprocessing capabilities. Allows conversion between various office document formats (`doc`<->`docx`<->`odt`, `xls`<->`xlsx`<->`ods`, `ppt`<->`pptx`<->`odp`) and exporting to various standard formats (`pdf`,`html`,`png`, etc.). Constists of a Python wrapper around Libreoffice a custom-built postprocessors.

## Usage

```
python converter.py -s [FILE] -f [FORMAT] [-e [LIBREOFFICE_PATH]] [-l [FONTS_DIR]] [-a [FONT_ALTERNATIVES_FILE]] [-i]
```

Parameters:

 - `file` - path to file to convert
 - `format` - output format, given as a standard extension: `doc`, `pdf`, `html`, `png`, etc.
 - `libreoffice_path` - (optional) path to the Libreoffice executable (by default, calls `libreoffice`)
 - `fonts_dir` - (optional, only for html output) a directory containing ttf/otf/woff/woff2 fonts which should be included as base64 strings inside html; if this option is missing, no font files will be included
 - `font_alternatives_file` - (optional, only for html output) a file describing font fallbacks (e.g. `"Times New Roman", "Times", "Liberation Serif", serif`) which will try to replace all fonts inside the document with their corresponding callbacks located inside `fonts_dir`
 

Example of usage:

```
python converter.py -s ./~test/test1.docx -f html -e '"C:\\Program Files (x86)\\LibreOffice 5\\program\\soffice.exe"' -l ./fonts -a ./fonts/alternatives.list -i
```


 ## Requirements

 - python 2+
 - Libreoffice