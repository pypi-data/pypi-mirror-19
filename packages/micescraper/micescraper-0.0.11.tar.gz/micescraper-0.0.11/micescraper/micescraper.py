import os
import pdb
import re
import click
import requests
import pyquery
import unicodedata
import os.path as path
from collections import defaultdict
from pyquery.pyquery import PyQuery as pq



def url2name(url):
  idx = url.rindex('/')
  return url[idx+1:]

def scrape_name(html):
  """
  Get applicant name from applicant page
  """
  name = pq(pq(html)('#applicantName')[0]).text()
  name = '_'.join(name.split()[1:])
  name = name.encode('ascii', 'ignore')
  return name

def get_applicant_urls(html):
  p = re.compile("showApplicant\.php\?c_eff=\d+")
  return p.findall(html)

def links_from_app_page(html):
  c = defaultdict(lambda: 0)
  for typ, link in links_from_app_page_helper(html):
    c[typ] += 1
    link = "https://mice.cs.columbia.edu/recruit/%s" % link
    yield typ, '%s_%d' % (typ, c[typ]), link

def links_from_app_page_helper(html):
  return links_from_page(html, doc="showDoc", rec="showRec")

def links_from_page(html, **linktypes):
  """
  linktypes is a dict of shortname -> text to match in the link HREF
  """
  doc = pq(html)
  for a in doc('a'):
    a = pq(a)
    link = a.attr('href')
    if not link: continue
    for key, text in linktypes.items():
      if text in link:
        yield key, link


def scrape_links(html, username, password):
  for typ, name, link in links_from_app_page(html):
    if typ == 'doc':
      for r in dl_doc(link, username, password):
        yield name, r
    if typ == 'rec':
      for r in dl_rec(link, username, password):
        yield name, r

def dl_doc(url, username, password, cache=True):
  """
  """
  try:
    r = requests.post(url, data={'username':username, 'password': password})
    yield r
  except Exception as e:
    print e
    pass

def dl_rec(url, username, password):
  """
  """
  for r in dl_doc(url, username, password):
    for typ, name, link in links_from_app_page(r.content):
      if typ == 'doc':
        for ret in dl_doc(link, username, password):
          yield ret


def scrape_applicant(url, username, password, outdir, **kwargs):
  """
  Scrape applicant based on their showApplicant URL
  """
  for r in dl_doc(url, username, password ,False):
    appname = scrape_name(r.content)
    print appname

    if kwargs.get("skipifexists") == True:
        f_name = "./%s/%s.pdf" % (outdir, appname)
        if path.isfile(f_name):
            print "found, skipping"
            return True

    fulldocurl = "%s&%s" % (url.strip().strip("&"), "pdf=1&all=1&noheader=1&reviews=1")
    docs = dl_doc(fulldocurl, username, password)
    for doc in docs:
      if doc.content.strip():
        with file("./%s/%s.pdf" % (outdir, appname), "wb") as f:
          f.write(doc.content)
          if kwargs.get("apponly") == True:
              return True
          break

    # consolidated pdf doesn't include rec letters.  
    # right now, resort to scraping all documents individually

    prefix = './%s/%s' % (outdir, appname)
    try:
        os.makedirs(prefix)
    except:
        pass
    for name, resp in scrape_links(r.content, username, password):
      with file('%s/%s.pdf' % (prefix, name), 'wb') as f:
        f.write(resp.content)

    return False

def scrape_applicant_id(id, username, password, outdir, **kwargs):
  """
  Scrape applicant document based on candidate MICE ID
  """
  url = "https://mice.cs.columbia.edu/recruit/showApplicant.php?c_eff=%s&pdf=1&all=1&noheader=1&" % id
  url = "https://mice.cs.columbia.edu/recruit/showApplicant.php?c_eff=%s" % id
  return scrape_applicant(url, username, password, outdir)


def scrape_listApplicants(url, username, password, outdir, **kwargs):
  """
  Find links to each applicant from the list Applicants page and scrape them 
  """
  for r in dl_doc(url, username, password, 0):
    for appurl in get_applicant_urls(r.content):
      appurl = "https://mice.cs.columbia.edu/recruit/%s"  % appurl
      scrape_applicant(appurl, username, password, outdir, **kwargs)


