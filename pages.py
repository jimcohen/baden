#!python3
import json
import os
import cgi

data = json.load(open("baden.json"))
template = open("template.html").read()
script = open("script.html").read()
friendlies = {}

def make_friendly(city):
    if city in friendlies:
        return friendlies[city]

    s = city
    
    if ", " in s:
        one,two = s.split(", ",1)
        s = two + " " + one
    
    s = s.replace(" ","_")
    s = s.replace(u"ä","ae").replace(u"ü","ue").replace(u"ö","oe")
    s = s.replace(u"ß","ss").replace("/","--")

    friendlies[city] = s
    return s

def get_nearby(city):
    zipcode = data[city]["zip"]
    result = []
    for name in data:
        if data[name]["zip"] == zipcode and name != city:
            result.append('      <li><a href="' + make_friendly(name) + '.html">' + cgi.escape(name, True) + '</a></li>')
    result.sort()
    result.append('      <li><a href="index.html">Startseite</a></li>')
    return "\n".join(result)



for city in data:
    friendly = make_friendly(city)
    title = cgi.escape(city, True) + (" ist badisch!" if data[city]["Baden"] else " ist nicht badisch!")
    with open(os.path.join("pages/",friendly+".html"), "wb") as f:
        html = template.replace("{$title}", title)
        html = html.replace("{$list}", get_nearby(city))
        html = html.replace("{$script}", "")
        f.write(html.encode("utf8"))
    print(city)

# index
with open("pages/index.html", "wb") as f:


    allpages = []
    for name in friendlies:
        allpages.append(u'<li data-name="' + cgi.escape(name, True).lower() + '" data-zip="' + str(data[name]["zip"]) + '"><a href="' + friendlies[name] + '.html">' + cgi.escape(name, True) + '</a></li>')
    allpages.sort()

    html = template.replace("{$title}", u"Städte")
    html = html.replace("{$list}", u"".join(allpages))
    html = html.replace("{$script}", script)
    f.write(html.encode("utf8"))


print("Done!")
