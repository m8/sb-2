
import os
import shutil
import mistune
import re
from datetime import datetime
from collections import OrderedDict

style_path = "/assets/style/"
blog_path = "/blog"

blog_check = False
blog_list={}

def iterate_folders(src, dst, symlinks=False, ignore=None):
    global blog_check
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if(item == "blog"):
            blog_check = True
        if os.path.isdir(s):
            if(blog_check and item!= "blog" and item.startswith('_') == False):
                blog_check = False
            iterate_folders(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                if(item.endswith('.md')):
                    htmlfile = rendermarkdown(s)
                    f = open(d.rsplit('/',1)[0]+ htmlfile[1], "w")
                    f.write(htmlfile[0])
                    f.close()
                else:
                    shutil.copy2(s, d)

def rendermarkdown(src):
    filesrc = open(src)
    filesrc = filesrc.readlines()
    # Escape for rendering HTML 
    markdown = mistune.Markdown(escape=False)

    title = filesrc[1].split(': ')[1].rstrip()
    layout = open("_templates/"+filesrc[2].split(': ')[1].rstrip()).read()
    stylesheet = filesrc[3].split(': ')[1].rstrip()
    date = filesrc[4].split(': ')[1].rstrip()
    permalink = filesrc[5].split(': ')[1].rstrip()

    md_content = ""
    for var in range(8,len(filesrc)):
      md_content += filesrc[var]
    layout = layout.replace('{{title}}',title)
    layout = layout.replace('{{content}}',  markdown(md_content))
    layout = layout.replace('{{stylesheet}}',style_path+stylesheet)
    if(blog_check):
        blog_list[date] =  [title,permalink]
    return [layout,permalink]

def createUrl(text):
    return re.sub(r'[\W_]+', '_', text.lower())

def renderblogpage():
    sorted_blogs = reversed(sorted(blog_list))
    line = ""
    for s in sorted_blogs:
        line += "\n <li>{} &ndash; <a href=/blog{}>{}</a></li>\n".format(s,blog_list[s][1],blog_list[s][0])
    layout = open("_templates/blogindex.html").read()
    layout = layout.replace('{{title}}',"Blog Sayfası")
    layout = layout.replace('{{content}}',  line)
    layout = layout.replace('{{stylesheet}}',style_path+"style.css")
    f = open("_site/{}/index.html".format(blog_path), "w")
    f.write(layout)
    f.close()

iterate_folders('_content','_site')
renderblogpage()
