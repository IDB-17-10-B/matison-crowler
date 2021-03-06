#yoink my code now
site='http://stankin.ru/university'
word='yeet'
import sys
import re
import requests
import time
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

pattern=re.compile(r'href="(?P<url>[a-zA-Z0-9:/&?=/.-]+)"')
body_pattern=re.compile(r'<body>([\s\S]+)</body>')
style_pattern=re.compile(r'<style[^>]*>[\s\S]*?</style>')
script_pattern=re.compile(r'<script[^>]*>[\s\S]*?</script>')
hook_pattern=re.compile(r'<.*?>')
space_pattern=re.compile(r'[\t\n\r\s]+')
symbol_pattern=re.compile(r'[,.:+;!&%|\()/©@"?/]+')

search_word = morph.parse(word)[0]  
search_word = search_word.normal_form
file = open('crawler.txt', 'w')
file.close()


def foo(search_word, addr, index):
  html=requests.get(addr).text
  links=pattern.findall(html)
  
  text=body_pattern.search(html).group()
  text=script_pattern.sub('',text)
  text=style_pattern.sub('',text)
  text=hook_pattern.sub('',text)
  text=re.sub(r'&nbsp;','',text)
  text=re.sub(r'&quot;','',text)
  text=space_pattern.sub(' ',text)
       
  rep = search_foo(search_word,text)
  file = open('crawler.txt', 'a')
  file.write(str(rep)+' '+addr+'\n')
  file.close()

  print ('На',addr,'\nСлово "'+word+'" повторяется',rep,'раз\n') 


  new_links=[]
  for item in links:
    if item.endswith(('.png','.css')):
      continue
    if item.startswith('/'):
      new_links.append (site+item)
    elif not item.startswith('/') and not item.startswith('http://'):
      new_links.append (addr+'/'+item) 
    elif 'stankin.ru' in item:
      new_links.append(item)
    if (index-1<0):
      return new_links
  all_links =[]
  for item in new_links:
    time.sleep(2)
    current_links = foo(search_word,item,index-1)
    all_links.extend(current_links)
  new_links.extend(all_links)

  return new_links


def search_foo(search_word,text):
  text=symbol_pattern.sub('',text)
  text=space_pattern.sub(' ',text)
  words=re.split(' ',text)

  morph_words = []
  for item in words:
    p = morph.parse(item)[0]  #разбор слова
    morph_words.append(p.normal_form) 

  rep=0
  for item in morph_words:
    if item==search_word:
      rep+=1

  return rep


foo(search_word,site,2)
list_sort={}
l=[]
file = open('crawler.txt', 'r')
for line in file:
  l=re.split(' ',line,1)
  list_sort[l[1]]=int(l[0])   
file.close()

for item in sorted(list_sort, key=list_sort.get, reverse=True):
  print (list_sort[item],item)
  
