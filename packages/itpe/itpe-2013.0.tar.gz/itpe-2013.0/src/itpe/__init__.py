#!/usr/bin/python

import os
import csv

# Parameters
poddir = os.environ['HOME'] + '/Podfic/'
postfile = poddir + 'itpe-treats.html'
listfile = poddir + 'itpe-treats.csv'
imgwidth = '450px'



# Site names
dw_prefix_dict = {
  'ao3':  'archiveofourown.org',
  'blog': 'blogspot.com',
  'dj':   'deadjournal.com',
  'del':  'delicious.com',
  'dev':  'deviantart.com',
  'dw':   'dreamwidth.org',
  'da':   'da',
  'etsy': 'etsy.com',
  'ff':   'fanfiction.net',
  'ink':  'inksome.com',
  'ij':   'insanejournal.com',
  'jf':   'journalfen.com',
  'last': 'last.fm',
  'lj':   'livejournal.com',
  'pin':  'pinboard.in',
  'pk':   'plurk.com',
  'rvl':  'ravelry.com',
  'tw':   'twitter.com',
  'tum':  'tumblr.com',
  'wp':   'wordpress.com'
}

dw_prefix_dict_keys = dw_prefix_dict.keys()



# Create site link for Dreamwidth
def dw_user_link(username):
  if '/' in username:
    prefix,name = username.split('/')
    if prefix.lower() in dw_prefix_dict_keys:
      return '<user name=' + name + ' site=' + dw_prefix_dict[prefix.lower()] + '>'
    else:
      return '<a href="' + prefix + '">' + name + '</a>'
  else:
    if " " in username:
      return username
    else:
      return '<user name=' + username + '>'



# A function for splitting lists into nicely formatted strings
def list_split(my_list):
  if ',' in my_list:
    list_split = [x.lstrip() for x in my_list.split(',')]
    out_list = ''
    list_len = len(list_split)

    my_range = [i for i in range (list_len) if i+2 < list_len]

    for i in my_range:
      out_list = out_list + list_split[i] + ', '

    out_list = out_list + list_split[list_len-2] + ' and ' + list_split[list_len-1]

    return out_list
  else:
    return my_list



# An adaptation of list_split() that also applies DW user links
def list_split_dw(my_list):
  if ',' in my_list:
    list_split = [x.lstrip() for x in my_list.split(',')]
    out_list = ''
    list_len = len(list_split)

    my_range = [i for i in range (list_len) if i+2 < list_len]

    for i in my_range:
      out_list = out_list + dw_user_link(list_split[i]) + ', '

    out_list = out_list + dw_user_link(list_split[list_len-2]) + ' and ' + dw_user_link(list_split[list_len-1])

    return out_list
  else:
    return dw_user_link(my_list)



# Add any for/from information
def itpe_for_from(from_names,for_names):
  if {from_names,for_names} == {'',''}:
    return ''
  elif from_names == '':
    return '<h2><b>For ' + list_split_dw(for_names) + '!</h2></b>'
  elif for_names == '':
    return '<h2><b>From ' + list_split_dw(from_names) + '!</h2></b>'
  else:
    return '<h2><b>From ' + list_split_dw(from_names) + ', for ' + list_split_dw(for_names) + '!</h2></b>'



# Add any cover and editor details
def itpe_cover_art(artwork_link,artist,editor):
  if {artwork_link,artist,editor} == {'','',''}:
    return ''
  elif editor == '':
    if artist == '':
      return '<img src="' + artwork_link + '"><br /><br />'
    else:
      return '<font size="1"><div style="width:' + imgwidth + '"><img src="' + artwork_link + '"><br /> Cover artwork by ' + list_split_dw(artist) + '</font><br />'
  elif artwork_link == '':
    return '<font size="1">Edited by' + list_split_dw(editor) + '</font>'
  else:
    return '<font size="1"><div style="width:' + imgwidth + '"><img src="' + artwork_link + '"><br /> Cover artwork by ' + list_split_dw(artist) + '<br /> Edited by' + list_split_dw(editor) + '</font><br />'



# Add the title
def itpe_title(title,title_link):
  if {title,title_link} == {'',''}:
    return ''
  elif title == '':
    return '<tr><td><b>Title:</b></td> <td> <a href="' + title_link + '">' + title_link + '</a></td></tr>'
  elif title_link == '':
    return '<tr><td><b>Title:</b></td> <td> ' + title + '</td></tr>'
  else:
    return '<tr><td><b>Title:</b></td> <td> <a href="' + title_link + '">' + title + '</a></td></tr>'



# Add the author(s)
def itpe_author(authors):
  if authors == '':
    return ''
  else:
    if ',' in authors:
      return '<tr><td><b>Authors:</b></td><td>' + list_split_dw(authors) + '</td></tr>'
    else:
      return '<tr><td><b>Author:</b></td><td>' + dw_user_link(authors) + '</td></tr>'



# List of fandoms with slashes in the name, when split

fandom_slash_exceptions = [
  ['.hack', '', 'sign'],
]



# Add the fandom(s)

def itpe_fandom(fandoms):
  if fandoms == '':
    return ''
  else:
    if '/' in fandoms:
      fan_split = fandoms.split('/')
      if [x.lower() for x in fan_split] in fandom_slash_exceptions:
        return '<tr><td><b>Fandom:</b></td><td>' + fandoms + '</td></tr>'
      else:
        return '<tr><td><b>Fandoms:</b></td><td>' + fandoms + '</td></tr>'
    else:
      return '<tr><td><b>Fandom:</b></td><td>' + fandoms + '</td></tr>'



# Add the pairing(s)

def itpe_pairing(pairings):
  if pairings == '':
    return ''
  else:
    if ',' in pairings:
      return '<tr><td><b>Pairings:</b></td><td>' + list_split(pairings) + '</td></tr>'
    else:
      return '<tr><td><b>Pairing:</b></td><td>' + pairings + '</td></tr>'



# Add the length
def itpe_length(length):
  if length == '':
    return ''
  else:
    return '<tr><td><b>Length:</b></td><td>' + length + '</td></tr>'



# Add some download links
def itpe_download_links(mp3_link,m4b_link):
  if {mp3_link,m4b_link} == {'',''}:
    return ''
  elif mp3_link == '':
    return '<tr><td><b>Download:</b></td><td><a href="' + m4b_link + '">Podbook</a></td></tr>'
  elif m4b_link == '':
    return '<tr><td><b>Download:</b></td><td><a href="' + mp3_link + '">MP3</a></td></tr>'
  else:
    return '<tr><td><b>Download:</b></td><td><a href="' + mp3_link + '">MP3</a> | <a href="' + m4b_link + '">Podbook</a></td></tr>'



def main():
  # Wipe the itpe-post.html file for new compile
  open(postfile, 'w').close()

  # A very primitive debugger to identify problems in the CSV (if they exist)
  i = 0

  # Write the new stuff
  with open(listfile) as csvfile:
    my_spreadsheet = csv.DictReader(csvfile, delimiter=",")
    for row in my_spreadsheet:

      i += 1
      print "Processing row " + str(i)

      with open(postfile, 'a') as f:
        lines = ['',
                 itpe_for_from(row['from'], row['for']),
                 itpe_cover_art(row['cover_art'], row['cover_artist'], row['editor']),
                 '<table>',
                 itpe_title(row['title'], row['title_link']),
                 itpe_author(row['authors']),
                 itpe_fandom(row['fandom']),
                 itpe_pairing(row['pairing']),
                 itpe_length(row['length']),
                 itpe_download_links(row['mp3_link'], row['m4b_link']),
                 '</table>',
                 '',
                 '']
        f.write('\n'.join(lines).encode('utf8'))
