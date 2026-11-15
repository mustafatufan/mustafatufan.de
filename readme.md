> A perfect resume did not exi...

<p align="center">
	<img width="192" height="192" src="https://mustafatufan.de/images/icon_domain.svg">
</p>

---
# Printable Resume Website
[**`mustafatufan.de`**](https://mustafatufan.de) is my resume website in 25 languages, hosted on Github Pages.

## Languages
German is the primary language and lives at the root. Every other language has its own folder, named after its language code.

| Page | German (primary) | English | Other languages |
|---|---|---|---|
| Resume | [`/`](https://mustafatufan.de/) | [`/en/`](https://mustafatufan.de/en/) | `/<code>/`, for example [`/fr/`](https://mustafatufan.de/fr/) |
| Beyond the Resume | [`/beyond.html`](https://mustafatufan.de/beyond.html) | [`/en/beyond.html`](https://mustafatufan.de/en/beyond.html) | `/<code>/beyond.html` |
| PDF | `/pdf/Mustafa_Tufan_Software_Entwickler_Lebenslauf.pdf` | `/pdf/Mustafa_Tufan_Software_Engineer_Resume.pdf` | `/pdf/Mustafa_Tufan_CV_<CODE>.pdf` |

The language menu shows German first, then English, then the other languages by number of speakers worldwide:

Spanish (`es`), French (`fr`), Portuguese (`pt`), Turkish (`tr`), Italian (`it`), Polish (`pl`), Dutch (`nl`), Romanian (`ro`), Greek (`el`), Hungarian (`hu`), Czech (`cs`), Swedish (`sv`), Bulgarian (`bg`), Danish (`da`), Finnish (`fi`), Slovak (`sk`), Croatian (`hr`), Lithuanian (`lt`), Slovene (`sl`), Latvian (`lv`), Estonian (`et`), Irish (`ga`), Maltese (`mt`).

- German and English each have a button of their own. The other languages are in the menu next to them.
- Each page names all its translations in the `hreflang` links of its `<head>`. `x-default` points to the German page.
- All languages share the same stylesheet, script, images and icons.
- Links that end up in the printed PDF are absolute (`https://mustafatufan.de/...`), because a PDF cannot resolve relative links.

## How the pages are built
The HTML pages are generated. Do not edit `index.html`, `beyond.html` or the files in the language folders by hand: the next build overwrites them.

| Source | Purpose |
|---|---|
| `src/resume.html`, `src/beyond.html` | Page templates, shared by all languages |
| `src/i18n/<code>.json` | The texts of one language |
| `src/i18n/common.json` | Texts that are the same in every language, such as the technology lists |
| `src/print.json` | Print font size per language, written by the PDF export |
| `build.py` | Writes every page and `sitemap.xml`. Needs Python 3 and nothing else |

```sh
python3 build.py            # write all pages and the sitemap
python3 build.py --pdf      # also export all resume PDFs (needs Google Chrome)
python3 build.py --pdf fr   # export only the French PDF
```

The generated pages are committed, so Github Pages serves them as plain static files.

### Changing content
1. Change the text in `src/i18n/en.json` and in every other language file. A key that is missing in a language stops the build with a message.
2. Run `python3 build.py --pdf` and commit the result.

A change to the structure of the page goes into the template once and reaches every language.

### Text markup
- `[[key|text]]` in a text becomes a link. The targets are listed under `LINKS` in `build.py`.
- `[[nowrap|text]]` keeps a term on one line.
- `[[beyond]]` becomes a link to the Beyond page of that language.

### Adding a language
1. Copy `src/i18n/en.json` to `src/i18n/<code>.json` and translate the values.
2. Add the language to `LANGS` in `build.py`. Its position there is its position in the menu.
3. Run `python3 build.py --pdf`.

## Tech Stack
- Bootstrap 5.3
- Font Awesome 6.7
- Vanilla JavaScript (no jQuery)
- Python 3 for the build (standard library only)

## Rules
- Printable
- Must represent whole career, experience and skills
- Clear & minimal
- Readable by applicant tracking systems (ATS)

## Usage
Fork and complete [Github Pages setup](https://help.github.com/en/articles/configuring-a-publishing-source-for-github-pages).

Change information as yours: `/src/i18n/*.json`, then run `python3 build.py --pdf`

Change website icon: `/images/icon.png`

Change resume photo: `/images/me.jpeg`

## Printing to PDF
`python3 build.py --pdf` exports every resume with headless Chrome. The result is the same as opening a page in Chrome, pressing `Ctrl/Cmd + P` and saving as PDF with the default settings:

- Margins: **Default**
- Scale: **Default** (100)
- Headers and footers: **off**

Every resume prints on A4 in two pages. German and English print at 9pt. A language whose text runs longer gets the largest smaller size with which it still fits, down to 8pt, and that size is stored in `src/print.json`. If a language does not fit even at 8pt, the export stops and names it: shorten its texts.

## ATS rules
The printed PDF is what applicant tracking systems parse, so the pages keep to these rules:

- One column of real headings (`h1`, `h2`, `h3`), paragraphs and lists. No tables for layout.
- Standard section names: Summary, Skills, Experience, Projects, Education (German: Profil, Kenntnisse, Berufserfahrung, Projekte, Ausbildung).
- Name on the first line, then contact details as plain text (address, phone, e-mail, LinkedIn, GitHub).
- Each job has its title and dates on one line, then company and location on the next. Dates are `Mon YYYY - Mon YYYY` in English and `MM/YYYY - MM/YYYY` in every other language, which does not depend on a parser knowing the month names of that language.
- Icons and other decoration are hidden in print (`d-print-none`), because icon fonts end up as unreadable characters in the PDF text.
- The photo is printed at the top right, as is customary on German CVs. It is a plain flex item, not a positioned element: Chrome writes positioned elements after the rest of the page, which would move the header text behind the Summary.
- No page numbers or other page margin content: Chrome writes it as the first text of the PDF, ahead of the name.
- No automatic hyphenation: a word split across two lines is split in the PDF text as well. A keyword with a hyphen that lands on a line end is kept together with `[[nowrap|...]]`.

To check what a parser reads, run `pdftotext -raw pdf/Mustafa_Tufan_Software_Entwickler_Lebenslauf.pdf - | head`. The first line must be the name, followed by the headline and the contact details.

---
##### Tech stack tag ordering convention
1. Industry, domain
2. Programming languages
3. Frameworks, libraries, etc. that are related with those programming languages
4. Development terms like *RESTful API*
5. Databases
6. Version control tools
7. Container tools
8. Other CI/CD tools
9. Servers like *Tomcat*
10. Third party services like *Admob* or *Google Play Game Services*

- *The order of the same types should be according to importance & experience.*
- *Typing of the all terms must be the same with title of its Wikipedia article. (For example, it should be Apache Ant, not Ant.)*

## Contributing
Pull requests are welcome without changing personal information.

## License
[MIT](https://choosealicense.com/licenses/mit/)
