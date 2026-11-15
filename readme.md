> A perfect resume did not exi...

<p align="center">
	<img width="192" height="192" src="https://mustafatufan.de/images/icon_domain.svg">
</p>

---
# Printable Resume Website
[**`mustafatufan.de`**](https://mustafatufan.de) is my resume website in German and English, hosted on Github Pages.

## Languages
German is the primary language and lives at the root. English lives under `/en/`. Both share the same stylesheet, script, images and icons.

| Page | German (primary) | English |
|---|---|---|
| Resume | [`/index.html`](https://mustafatufan.de/) | [`/en/index.html`](https://mustafatufan.de/en/) |
| Beyond the Resume | [`/beyond.html`](https://mustafatufan.de/beyond.html) | [`/en/beyond.html`](https://mustafatufan.de/en/beyond.html) |
| PDF | `/pdf/Mustafa_Tufan_Software_Entwickler_Lebenslauf.pdf` | `/pdf/Mustafa_Tufan_Software_Engineer_Resume.pdf` |

- Every content change goes into both languages, and both PDFs are exported again afterwards.
- Each page names its counterpart in the `hreflang` links of its `<head>`, in the language buttons at the top, and in `/sitemap.xml`. `x-default` points to the German page.
- Pages under `/en/` reach the shared files with `../` (`../css/style.css`, `../images/me.jpeg`).
- Links that end up in the printed PDF are absolute (`https://mustafatufan.de/...`), because a PDF cannot resolve relative links.

## Tech Stack
- Bootstrap 5.3
- Font Awesome 6.7
- Vanilla JavaScript (no jQuery)

## Rules
- Printable
- Must represent whole career, experience and skills
- Clear & minimal
- Readable by applicant tracking systems (ATS)

## Usage
Fork and complete [Github Pages setup](https://help.github.com/en/articles/configuring-a-publishing-source-for-github-pages).

Change information as yours: `/index.html` and `/en/index.html`

Change website icon: `/images/icon.png`

Change resume photo: `/images/me.jpeg`

## Printing to PDF
Open the page in Chrome, press `Ctrl/Cmd + P` and save as PDF with the default settings:

- Margins: **Default**
- Scale: **Default** (100)
- Headers and footers: **off**

Or export both from the command line (macOS), which gives the same result:

```sh
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$chrome" --headless --no-pdf-header-footer --user-data-dir="$(mktemp -d)" \
  --print-to-pdf=pdf/Mustafa_Tufan_Software_Entwickler_Lebenslauf.pdf "file://$PWD/index.html"
"$chrome" --headless --no-pdf-header-footer --user-data-dir="$(mktemp -d)" \
  --print-to-pdf=pdf/Mustafa_Tufan_Software_Engineer_Resume.pdf "file://$PWD/en/index.html"
```

Each page prints on A4 in two pages. Replace the PDF of a language after every content change in that language.

German text runs longer than English, so the German page is the one that decides whether a change still fits on two pages. Check the page count with `pdfinfo` after exporting.

## ATS rules
The printed PDF is what applicant tracking systems parse, so the pages keep to these rules:

- One column of real headings (`h1`, `h2`, `h3`), paragraphs and lists. No tables for layout.
- Standard section names: Summary, Skills, Experience, Projects, Education (German: Profil, Kenntnisse, Berufserfahrung, Projekte, Ausbildung).
- Name on the first line, then contact details as plain text (address, phone, e-mail, LinkedIn, GitHub).
- Each job has its title and dates on one line, then company and location on the next. Dates are `Mon YYYY - Mon YYYY` in English and `MM/YYYY - MM/YYYY` in German, which is the usual form on German CVs and does not depend on a parser knowing German month names.
- Icons and other decoration are hidden in print (`d-print-none`), because icon fonts end up as unreadable characters in the PDF text.
- The photo is printed at the top right, as is customary on German CVs. It is a plain flex item, not a positioned element: Chrome writes positioned elements after the rest of the page, which would move the header text behind the Summary.
- No page numbers or other page margin content: Chrome writes it as the first text of the PDF, ahead of the name.
- No automatic hyphenation: a word split across two lines is split in the PDF text as well. A keyword with a hyphen that lands on a line end is kept together with `text-nowrap`.

To check what a parser reads, run `pdftotext -raw pdf/Mustafa_Tufan_Software_Entwickler_Lebenslauf.pdf - | head` (and the same for the English PDF). The first line must be the name, followed by the headline and the contact details.

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
