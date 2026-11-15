#!/usr/bin/env python3
"""Builds the static pages of mustafatufan.de.

    python3 build.py              write every HTML page and sitemap.xml
    python3 build.py --pdf        also export every resume PDF (needs Google Chrome)
    python3 build.py --pdf fr it  export only the PDFs of these languages

Sources
    src/resume.html, src/beyond.html   page templates, shared by all languages
    src/i18n/<code>.json               the texts of one language
    src/i18n/common.json               texts that are the same in every language
    src/print.json                     print font size per language (written by --pdf)

The first language in LANGS is the primary one and is written to the site
root. Every other language gets its own folder: /en/, /fr/, ...

Only the Python standard library is used.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
SITE = 'https://mustafatufan.de/'

# code, name in its own language, flag, Open Graph locale, PDF file name.
# The order is the order of the language menu: the primary language, then
# English, then the rest by number of speakers worldwide.
LANGS = [
    ('de', 'Deutsch', '🇩🇪', 'de_DE', 'Mustafa_Tufan_Software_Entwickler_Lebenslauf.pdf'),
    ('en', 'English', '🇬🇧', 'en_GB', 'Mustafa_Tufan_Software_Engineer_Resume.pdf'),
    ('es', 'Español', '🇪🇸', 'es_ES', 'Mustafa_Tufan_CV_ES.pdf'),
    ('fr', 'Français', '🇫🇷', 'fr_FR', 'Mustafa_Tufan_CV_FR.pdf'),
    ('pt', 'Português', '🇵🇹', 'pt_PT', 'Mustafa_Tufan_CV_PT.pdf'),
    ('tr', 'Türkçe', '🇹🇷', 'tr_TR', 'Mustafa_Tufan_CV_TR.pdf'),
    ('it', 'Italiano', '🇮🇹', 'it_IT', 'Mustafa_Tufan_CV_IT.pdf'),
    ('pl', 'Polski', '🇵🇱', 'pl_PL', 'Mustafa_Tufan_CV_PL.pdf'),
    ('nl', 'Nederlands', '🇳🇱', 'nl_NL', 'Mustafa_Tufan_CV_NL.pdf'),
    ('ro', 'Română', '🇷🇴', 'ro_RO', 'Mustafa_Tufan_CV_RO.pdf'),
    ('el', 'Ελληνικά', '🇬🇷', 'el_GR', 'Mustafa_Tufan_CV_EL.pdf'),
    ('hu', 'Magyar', '🇭🇺', 'hu_HU', 'Mustafa_Tufan_CV_HU.pdf'),
    ('cs', 'Čeština', '🇨🇿', 'cs_CZ', 'Mustafa_Tufan_CV_CS.pdf'),
    ('sv', 'Svenska', '🇸🇪', 'sv_SE', 'Mustafa_Tufan_CV_SV.pdf'),
    ('bg', 'Български', '🇧🇬', 'bg_BG', 'Mustafa_Tufan_CV_BG.pdf'),
    ('da', 'Dansk', '🇩🇰', 'da_DK', 'Mustafa_Tufan_CV_DA.pdf'),
    ('fi', 'Suomi', '🇫🇮', 'fi_FI', 'Mustafa_Tufan_CV_FI.pdf'),
    ('sk', 'Slovenčina', '🇸🇰', 'sk_SK', 'Mustafa_Tufan_CV_SK.pdf'),
    ('hr', 'Hrvatski', '🇭🇷', 'hr_HR', 'Mustafa_Tufan_CV_HR.pdf'),
    ('lt', 'Lietuvių', '🇱🇹', 'lt_LT', 'Mustafa_Tufan_CV_LT.pdf'),
    ('sl', 'Slovenščina', '🇸🇮', 'sl_SI', 'Mustafa_Tufan_CV_SL.pdf'),
    ('lv', 'Latviešu', '🇱🇻', 'lv_LV', 'Mustafa_Tufan_CV_LV.pdf'),
    ('et', 'Eesti', '🇪🇪', 'et_EE', 'Mustafa_Tufan_CV_ET.pdf'),
    ('ga', 'Gaeilge', '🇮🇪', 'ga_IE', 'Mustafa_Tufan_CV_GA.pdf'),
    ('mt', 'Malti', '🇲🇹', 'mt_MT', 'Mustafa_Tufan_CV_MT.pdf'),
]
PRIMARY = LANGS[0][0]
# Languages with their own button. The rest go into the "more languages" menu.
PINNED = 2

# Targets of the [[key|text]] links inside the texts.
LINKS = {
    'video': 'https://www.youtube.com/watch?v=4i90WbdHafo',
    'youtube': 'https://www.youtube.com/results?search_query=%22solochance.org%22',
    'infleks_trade': 'https://www.infina.com.tr/infleks-trade-en.html',
    'infleks_operation': 'https://www.infina.com.tr/infleks-operasyon-en.html',
    'infleks_wealth': 'https://www.infina.com.tr/infleks-varlik-en.html',
    'anabin': SITE + 'pdf/Anabin_Marmara_University_Master_Capital_Markets_Stock_Exchange.pdf',
    'solochance': 'https://SoloChance.org',
}

# Start and end of each job as (year, month).
JOB_DATES = {
    'j1': ((2023, 2), (2026, 8)),
    'j2': ((2019, 9), (2022, 12)),
    'j3': ((2019, 5), (2019, 8)),
    'j4': ((2018, 7), (2019, 4)),
    'j5': ((2016, 3), (2018, 6)),
}
EN_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Markup that only one page gets, inserted at the top of its <head>.
HEAD_EXTRA = {
    ('de', 'index'): '\n\t<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6507588368884912"\n'
                     '     crossorigin="anonymous"></script>\n',
}

PAGES = {'index': 'resume.html', 'beyond': 'beyond.html'}

# Print: every resume has to fit on two A4 pages. Languages that run longer
# than English get a slightly smaller print font, found by --pdf.
PRINT_SIZE = 9.0
PRINT_SIZE_MIN = 8.0
MAX_PAGES = 2

TOKEN = re.compile(r'\{\{\s*([a-z0-9_]+)(?:\|(attr|text|json))?\s*\}\}')
LINK = re.compile(r'\[\[([a-z_]+)(?:\|([^\]]*))?\]\]')


def lang_dir(code):
    return '' if code == PRIMARY else code + '/'


def page_file(page):
    return 'index.html' if page == 'index' else page + '.html'


def url(code, page):
    """Public address of a page."""
    return SITE + lang_dir(code) + ('' if page == 'index' else page_file(page))


def rel(from_code, to_code, page):
    """Relative link from a page of one language to the same page of another."""
    if from_code == to_code:
        return './' if page == 'index' else page_file(page)
    up = '' if from_code == PRIMARY else '../'
    path = up + lang_dir(to_code) + ('' if page == 'index' else page_file(page))
    return path or './'


def read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_texts():
    """Texts of every language, checked against the English key set."""
    common = read_json(os.path.join(SRC, 'i18n', 'common.json'))
    texts = {}
    for code, *_ in LANGS:
        path = os.path.join(SRC, 'i18n', code + '.json')
        if not os.path.exists(path):
            sys.exit('Missing language file: src/i18n/%s.json' % code)
        texts[code] = read_json(path)
    required = set(texts['en']) - set(common)
    problems = []
    for code, strings in texts.items():
        missing = sorted(required - set(strings))
        unknown = sorted(set(strings) - required - set(common))
        empty = sorted(k for k, v in strings.items() if not str(v).strip())
        for name, keys in (('missing', missing), ('unknown', unknown), ('empty', empty)):
            if keys:
                problems.append('%s.json: %s keys: %s' % (code, name, ', '.join(keys)))
    if problems:
        sys.exit('\n'.join(problems))
    return {code: dict(common, **strings) for code, strings in texts.items()}


def expand_links(value, code):
    """[[key|text]] becomes a link, [[nowrap|text]] a non-breaking span."""
    def link(match):
        key, text = match.group(1), match.group(2)
        if key == 'nowrap':
            return '<span class="text-nowrap">%s</span>' % text
        if key == 'beyond':
            target = url(code, 'beyond')
            return '<a href="%s">%s</a>' % (target, target.split('//', 1)[1])
        if key not in LINKS:
            sys.exit('%s.json: unknown link [[%s]]' % (code, key))
        return '<a href="%s">%s</a>' % (LINKS[key], text)
    return LINK.sub(link, value)


def as_markup(value, code):
    value = expand_links(value, code)
    return re.sub(r'&(?!#?\w+;)', '&amp;', value)


def as_plain(value, code):
    def text(match):
        if match.group(1) == 'beyond':
            return url(code, 'beyond').split('//', 1)[1]
        return match.group(2) or ''
    return html.unescape(re.sub(r'<[^>]+>', '', LINK.sub(text, value)))


def render(template, values, code):
    def token(match):
        key, how = match.group(1), match.group(2)
        if key not in values:
            sys.exit('Template uses {{%s}}, which %s.json does not define' % (key, code))
        value = str(values[key])
        if how == 'attr':
            return html.escape(as_plain(value, code), quote=True)
        if how == 'text':
            return html.escape(as_plain(value, code), quote=False)
        if how == 'json':
            return json.dumps(as_plain(value, code), ensure_ascii=False)[1:-1]
        return as_markup(value, code)
    return TOKEN.sub(token, template)


def job_date(code, key):
    def one(year, month):
        if code == 'en':
            return '%s %d' % (EN_MONTHS[month - 1], year)
        return '%02d/%d' % (month, year)
    start, end = JOB_DATES[key]
    return '%s - %s' % (one(*start), one(*end))


def hreflang_links(page):
    lines = ['    <link rel="alternate" hreflang="%s" href="%s"/>' % (code, url(code, page)) for code, *_ in LANGS]
    lines.append('    <link rel="alternate" hreflang="x-default" href="%s"/>' % url(PRIMARY, page))
    return '\n'.join(lines)


def lang_switch(current, page, label):
    """Buttons for the pinned languages and a menu with all the others."""
    on = 'btn btn-sm btn-dark'
    off = 'btn btn-sm btn-outline-secondary border border-dark'
    out = ['        <div class="d-flex gap-1 ms-auto">']
    for code, name, flag, *_ in LANGS[:PINNED]:
        out.append('            <a href="%s" class="%s" style="width:70px" lang="%s" hreflang="%s">%s %s</a>' % (
            rel(current, code, page), on if code == current else off, code, code, flag, code.upper()))
    more = LANGS[PINNED:]
    chosen = [lang for lang in more if lang[0] == current]
    face = '%s %s' % (chosen[0][2], current.upper()) if chosen else '<i class="fas fa-globe fa-fw"></i>'
    out.append('            <div class="dropdown">')
    out.append('                <button class="%s dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" aria-label="%s">%s</button>' % (
        on if chosen else off, html.escape(label, quote=True), face))
    out.append('                <ul class="dropdown-menu dropdown-menu-end lang-menu">')
    for code, name, flag, *_ in more:
        active = ' active" aria-current="page' if code == current else ''
        out.append('                    <li><a class="dropdown-item%s" href="%s" lang="%s" hreflang="%s">%s %s</a></li>' % (
            active, rel(current, code, page), code, code, flag, name))
    out.append('                </ul>')
    out.append('            </div>')
    out.append('        </div>')
    return '\n'.join(out)


def build_page(lang, page, texts, templates, sizes):
    code, _name, _flag, locale, pdf_file = lang
    size = sizes.get(code, PRINT_SIZE)
    values = dict(texts[code])
    values.update({
        'lang': code,
        'root': '' if code == PRIMARY else '../',
        'canonical': url(code, page),
        'site_short': url(code, 'index').split('//', 1)[1].rstrip('/'),
        'og_locale': locale,
        'pdf_file': pdf_file,
        'head_extra': HEAD_EXTRA.get((code, page), ''),
        'html_attrs': '' if size == PRINT_SIZE else ' style="--print-font-size:%.1fpt"' % size,
        'hreflang_links': hreflang_links(page),
        'lang_switch': lang_switch(code, page, texts[code]['ui_more_languages']),
    })
    for key in JOB_DATES:
        values['date_' + key] = job_date(code, key)
    return render(templates[page], values, code)


def write(path, content):
    """Writes a file only when its content changed. Returns True if it did."""
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            if f.read() == content:
                return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def build_sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in PAGES:
        for index, (code, *_rest) in enumerate(LANGS):
            if page == 'index':
                priority = '1.0' if index == 0 else '0.9' if index == 1 else '0.8'
            else:
                priority = '0.5'
            out += ['    <url>',
                    '        <loc>%s</loc>' % url(code, page),
                    '        <changefreq>monthly</changefreq>',
                    '        <priority>%s</priority>' % priority,
                    '    </url>']
    out.append('</urlset>')
    return '\n'.join(out) + '\n'


def find_chrome():
    candidates = [os.environ.get('CHROME'),
                  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                  shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chromium-browser')]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    sys.exit('Google Chrome not found. Set the CHROME environment variable to its path.')


def print_pdf(chrome, profile, html_path, pdf_path):
    subprocess.run([chrome, '--headless', '--no-pdf-header-footer', '--user-data-dir=' + profile,
                    '--print-to-pdf=' + pdf_path, 'file://' + html_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(pdf_path, 'rb') as f:
        return len(re.findall(rb'/Type\s*/Page\b', f.read()))


def export_pdfs(codes, texts, templates, sizes):
    """Exports the resume PDFs. A language that needs more than two pages
    gets the largest print font size with which it fits."""
    chrome = find_chrome()
    profile = tempfile.mkdtemp(prefix='resume-chrome-')
    steps = [round(PRINT_SIZE - i / 10, 1) for i in range(int(round((PRINT_SIZE - PRINT_SIZE_MIN) * 10)) + 1)]
    failed = []
    try:
        for lang in LANGS:
            code, pdf_file = lang[0], lang[4]
            if codes and code not in codes:
                continue
            html_path = os.path.join(ROOT, lang_dir(code), 'index.html')
            pdf_path = os.path.join(ROOT, 'pdf', pdf_file)

            def pages_at(size):
                sizes[code] = size
                write(html_path, build_page(lang, 'index', texts, templates, sizes))
                return print_pdf(chrome, profile, html_path, pdf_path)

            # Largest size that fits: binary search over the steps.
            low, high, best = 0, len(steps) - 1, None
            if pages_at(steps[0]) <= MAX_PAGES:
                best = 0
            else:
                low = 1
                while low <= high:
                    middle = (low + high) // 2
                    if pages_at(steps[middle]) <= MAX_PAGES:
                        best, high = middle, middle - 1
                    else:
                        low = middle + 1
            if best is None:
                failed.append(code)
                sizes.pop(code, None)
                write(html_path, build_page(lang, 'index', texts, templates, sizes))
                print('%s  does NOT fit on %d pages even at %.1fpt: shorten its texts' % (code, MAX_PAGES, PRINT_SIZE_MIN))
                continue
            if sizes[code] != steps[best]:
                pages_at(steps[best])
            if sizes[code] == PRINT_SIZE:
                del sizes[code]
            print('%s  %.1fpt  %s' % (code, steps[best], pdf_file))
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    write(os.path.join(SRC, 'print.json'), json.dumps(sizes, indent=4, sort_keys=True) + '\n')
    if failed:
        sys.exit('Not exported: ' + ', '.join(failed))


def main():
    args = sys.argv[1:]
    pdf = '--pdf' in args
    codes = [a for a in args if not a.startswith('--')]
    known = [lang[0] for lang in LANGS]
    for code in codes:
        if code not in known:
            sys.exit('Unknown language: ' + code)

    texts = load_texts()
    templates = {}
    for page, name in PAGES.items():
        with open(os.path.join(SRC, name), encoding='utf-8') as f:
            templates[page] = f.read()
    sizes_path = os.path.join(SRC, 'print.json')
    sizes = read_json(sizes_path) if os.path.exists(sizes_path) else {}

    changed = 0
    for lang in LANGS:
        for page in PAGES:
            path = os.path.join(ROOT, lang_dir(lang[0]), page_file(page))
            changed += write(path, build_page(lang, page, texts, templates, sizes))
    changed += write(os.path.join(ROOT, 'sitemap.xml'), build_sitemap())
    print('%d languages, %d pages, %d files changed' % (len(LANGS), len(LANGS) * len(PAGES), changed))

    if pdf:
        export_pdfs(codes, texts, templates, sizes)


if __name__ == '__main__':
    main()
