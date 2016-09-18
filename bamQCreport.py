#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys

def main():
    path = sys.argv[1]
    os.chdir(path)
    info = []
    for line in open("mapInfo.csv"):
        info = line.strip().split(',')
    for cov in open("covInfo.csv"):
        mean_depth = cov.strip().split(',')[1]
        info.append(mean_depth)
#        cov_1x = cov.strip().split(',')[2]
#        info.append(cov_1x)
#        cov_20x = cov.strip().split(',')[4]
#        info.append(cov_20x)
#        cov_200x = cov.strip().split(',')[7]
#        info.append(cov_200x)
#        cov_1000x = cov.strip().split(',')[9]
#        info.append(cov_1000x)
    captures = sorted(filter(lambda x: x.endswith('capture_stat.txt'), os.listdir('./')))
    #cfdna_mark_capture, cfdna_sort_capture, gdna_mark_capture, gdna_sort_capture
    for capture in captures:
        for line in open(capture):
            value = line.strip().split('\t')[1]
            info.append(value)
    files = filter(lambda x:x.endswith('.png'), os.listdir('./'))
    fs = []
    for fil in files:
        title = fil.split('.')[0]
        figure = fil
        fs.append((title,figure))

    print "<html>"
    print "<head>"
    css()
    print "</head>"
    print "<body>"
    content(fs,info)
    print "</body>"
    print "</html>"

def css():
    print "<style type=\"text/css\">"
    print "#backtop a {position:fixed; bottom:0px; right:50px; color:#333; z-index:1000; background:#cfcfcf; padding:10px; border-radius:4px; -moz-border-radius:4px; -webkit-border-radius:4px; font-weight:normal; text-decoration:none;}"
    print "#backtop a:hover {background:#333; color:#fff;}"
    print "#menu {text-align:left;}"
    print ".menu-item{font-size:20px; padding:5px;}"
    print "#container {text-align:center;}"
    print ".figure-title {color:#003399; font-weight:bold; font-size:30px; padding:10px;}"
    print ".figure-div {margin-top:40px;}"
    print ".table-title {color:#003399; font-weight:bold; font-size:30px; padding:10px;}"
    print ".table-div {margin-top:40px; padding:10px;}"
    print "li {color:#666666; font-size:15px; border:0px;}"
    print "table,th,td {border:1px solid black; border-collapse:collapse; background-color: silver; text-align:center;}"
    print "th {color: white; background-color: gray;}"
    print "</style>"

def content(fs,info):
    print "<div id='backtop'><a href='#'>TOP</a></div>"
    print "<div id='container'>"
    print "<div id='menu'>"
    print "<ul>"
    print "<li class='menu-item'><a href='#mapping information'>mapping information</a></li>"
    for f in fs:
        print "<li class='menu-item'>"
        print "<a href='#" + f[0].replace('_',' ') + "'>" + f[0].replace('_',' ')
        print "</a>"
        print "</li>"
    print "</ul>"
    print "</div>"
    print "<div id='figures'>"
    print "<div class='table-div'>"
    print "<div class='table-title'><a name='mapping information'>mapping information</a></div>"
    print "<table cellpadding='10px' width='1080' align='center'>"
    print "<tr><th>&nbsp;</th><th><b>cfdna</b></th><th><b>gdna</b></th></tr>"
    print "<tr><td><b>Total clean reads</b></td><td>" + info[3] + "</td><td>" + info[0] + "</td></tr>"
    print "<tr><td><b>Mapping rate</b></td><td>" + info[4] + "</td><td>" + info[1] + "</td></tr>"
    print "<tr><td><b>Duplication rate</b></td><td>" + info[5] + "</td><td>" + info[2] + "</td></tr>"
    print "<tr><td><b>Mean depth(raw)</b></td><td>" + info[8] + "</td><td>" + info[6] + "</td></tr>"
    print "<tr><td><b>Mean depth(deduplication)</b></td><td>" + info[9] + "</td><td>" + info[7] + "</td></tr>"
    print "<tr><td><b>Capture percentage</b></td><td>" + info[11] + "</td><td>" + info[13] + "</td></tr>"
    print "<tr><td><b>Capture percentage(deduplication)</b></td><td>" + info[10] + "</td><td>" + info[12] + "</td></tr>"
    print "</table>"
    print "</div>"
    for f in fs:
        print "<div class='figure-div'>"
        print "<div class='figure-title'><a name='" + f[0].replace('_',' ') + "'>" + f[0].replace('_',' ') + "</a></div>"
        print "<div class='figure'><img src='" + f[1] + "'></div>"
        print "</div>"
    print "</div>"
    print "</div>"

if __name__ == "__main__":
    main()
