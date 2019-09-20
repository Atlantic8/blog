#encoding: utf8
import sys
import os

pwd = os.getcwd()
for filename in os.listdir('./'):
    fp = open('%s/%s' % (pwd, filename), encoding='utf8')
    data = fp.read()
    data = data.replace('\t','    ')
    fout = open('../new_post/%s' % filename, 'w', encoding='utf8')
    fout.write('%s' % data)


