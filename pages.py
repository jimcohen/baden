#!python3
import json
import os
import cgi

data = json.load(open("baden.json"))
incorporations = json.load(open("incorporations_by_name.json"))
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
    result.append('      <li><a href="https://github.com/cvzi/baden/issues">Are we wrong? Correct us!</a></li>')
    return "\n".join(result)


def get_incorporations(city):
    if not city in incorporations:
        return ""

    subs = incorporations[city]

    if city in subs:
        subs.remove(city)

    return cgi.escape(", ".join(subs))


for city in data:
    friendly = make_friendly(city)
    cityhtml = cgi.escape(city, True)
    title = cityhtml + (" ist badisch!" if data[city]["Baden"] else " ist nicht badisch!")
    question = "Ist " + cityhtml + " badisch?"
    answer = (("Ja! " + cityhtml + " liegt in Baden.") if data[city]["Baden"] else ("Nein! " + cityhtml + " liegt nicht in Baden."))
    color = "green" if data[city]["Baden"] else "red"
    incop_short = get_incorporations(city)
    if incop_short:
        incop_long = "  <h3>Stadtgliederung: " + incop_short + "</h3>"
    else:
        incop_long = ""
    with open(os.path.join("pages/",friendly+".html"), "wb") as f:
        html = template.replace("{$title}", title)
        html = html.replace("{$question}", question)
        html = html.replace("{$answer}", answer)  
        html = html.replace("{$script}", "")
        html = html.replace("{$list}", get_nearby(city))   
        html = html.replace("{$color}", color)
        html = html.replace("{$incorporationsshort}", incop_short) 
        html = html.replace("{$incorporationslong}", incop_long)
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
    html = html.replace("{$question}", u"Übersicht")
    html = html.replace("{$answer}", "")  
    html = html.replace("{$color}", "green")
    html = html.replace("{$incorporationsshort}", "") 
    html = html.replace("{$incorporationslong}", "")
    
    f.write(html.encode("utf8"))


print("Done!")
