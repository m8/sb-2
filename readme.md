# sb-2
different version of sb which is simple python script for creating markdown & html websites. this script allows you to prepare templates and write the website as markdown. it also creates a blog index page. If you write with markdown, these pages are converted to html. If you wrote it in html, it is directly copied. However, it is possible to define variables in markdown pages. these are replaced in the html template.

## Folders
**src**
```
-blog
--example1.md
--example2.md
-index.html
-contact.md
```

**dest**
```
-blog
--example1.html
--example2.html
-index.html
-contact.html
```

## features
- md support
- rss generating

## to-do
- create a simple _template folder
- create a project structure 

### dependencies
- mistune for rendering markdown pages
