#!/usr/bin/env python3
import math, json, sys

def generacije(lsistem):
    niz = lsistem['aksiom']
    num = lsistem.get('generacije',4)
    pravila = lsistem['pravila']
    kljuci = pravila.keys()
    for _ in range(num):
        noviniz=[]
        for ch in niz:
            if ch in kljuci:
                noviniz.append(pravila[ch])
            else:
                noviniz.append(ch)
        niz=','.join(noviniz)
    return(niz)

def graf(niz, lsistem):
    korak= lsistem.get('korak',1)
    zasuk = lsistem['zasuki']
    zasuki = zasuk.keys()
    pomiki=lsistem['pomiki']
    angle = lsistem.get('kot',90)


    stack = []
    pointx = [0]
    pointy = [0]

    xs = []
    ys = []

    for ch in niz:
        if ch in pomiki:
            pointx.append(pointx[-1]+korak*math.cos(angle/180*math.pi))
            pointy.append(pointy[-1]+korak*math.sin(angle/180*math.pi))
        elif ch in zasuki:
            angle += zasuk[ch]
            angle %= 360
        else:
            if ch == '[':
               x = pointx[-1]
               y = pointy[-1]
               stack.append([x,y,angle])
               xs.append(pointx)
               ys.append(pointy)
               pointx = [x]
               pointy = [y]
            elif ch == ']':
               xs.append(pointx)
               ys.append(pointy)
               x, y, angle = stack.pop()
               pointx = [x]
               pointy = [y]
            else:
               pass
    xs.append(pointx)
    ys.append(pointy)
 
    return(xs, ys)

def main():
    from bokeh.plotting import figure, output_file, show
    from bokeh.io import export_svgs

    lsistem = {
      "ime": "hilbert",
      "barva": "#000000",
      "generacije": 3,
      "korak": 1,
      "aksiom": "l",
      "pravila": {"l":"+rF-lFl-Fr+","r":"-lF+rFr+Fl-"},
      "pomiki": ["F"],
      "zasuki": {"+":90,"-":90}
    }

    name = lsistem.get('ime','ls')
    color = lsistem.get('barva','blue')

    output_file(name + '.html')
    p = figure() 
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.xgrid.visible = False
    p.ygrid.visible = False
    niz = generacije(lsistem)
    pointx, pointy = graf(niz, lsistem)
    p.multi_line(pointx, pointy, color = color, line_width=2.5)
    show(p)

if __name__ == '__main__': 
   main()
