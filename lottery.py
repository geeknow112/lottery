#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
from pprint import pprint
import random
import os
import json


'''TSV読み込み'''
with open('./data/sales_data.tsv') as f:
	reader = csv.reader(f, delimiter = '\t')
	sales = [row for row in reader]
sales.pop(0)
#pprint(sales)

with open('./data/sales_0_data.tsv') as f:
	reader = csv.reader(f, delimiter = '\t')
	sales0 = [row for row in reader]
sales0.pop(0)
#pprint(sales0)

json_open = open('./data/config.json', 'r')
jconf = json.load(json_open)
conf = jconf['award']
sconf = jconf['sorry']

'''対象情報の整形,番号採番'''
obj_list = list()
def makeNumber(lists):
	objList = list()
	num_kuchi = 0
	for i in lists:
		num_kuchi = num_kuchi+1
		objList.append([num_kuchi, i[0], i[1], i[2], i[3]])
	return objList

obj_list = makeNumber(sales)

'''賞の抽選'''
def reChusen(lists, preTousenList):
	reChusenList = list()
	for obj in lists:
		tousen = obj[0] in [int(i[0]) for i in preTousenList]
		if tousen == False:
			reChusenList.append(obj)
	return reChusenList

award = {}
reList = {}
for i in range(len(conf)):
	award.update({i: random.sample(obj_list, k=int(conf[i]))})
	reList = reChusen(obj_list, award[i])
	obj_list.clear()
	obj_list = reList

'''当選者 出力'''
def toTsv(obj):
	return str(obj).replace(',', '\t').replace('[', '').replace(']', '').replace('\'', '')

def outputTsvAward(lists):
	with open('./data/winners.tsv', mode='w') as f:
		for i in range(len(lists)):
			f.write('# award ' + str(i) + '賞\n')
			for l in lists[i]:
				f.write(toTsv(l))
				f.write('\n')
			f.write('\n')

def outputTsvSorry(lists):
	with open('./data/winners.tsv', mode='a') as f:
		for i in range(len(lists)):
			f.write('# sorry ' + str(i) + '賞\n')
			for l in lists[i]:
				f.write(toTsv(l))
				f.write('\n')
			f.write('\n')


outputTsvAward(award)
#os.system('cat ./data/winners.tsv')
#pprint(obj_list)
#exit()

'''残念賞対象者(未当選者+購入なし者、整形、採番'''
sorrys = list()
for i in obj_list:
	sorrys.append([i[1], i[2], i[3], i[4]])

sorry_lists = makeNumber(sorrys + sales0)

'''賞の回数を算出'''
def checkUpopoi(sconf, sorry_lists):
	cnt_l = int(len(sorry_lists))
	limits = list()
	chLims = list()
	#pprint(sconf.pop(len(sconf) - 1))
	#pprint(sum(sconf))
	for i in range(len(sconf)):
		cnt_w = sum(sconf)
		if cnt_w > cnt_l:
			idx = len(sconf) -1
			lim = sconf.pop(idx)
			chLims.insert(0, idx)
		else:
			limits = sconf

	# 当選枠より注文者数が多い場合の処理
	if len(chLims) != 0:
		#pprint(chLims)
		for i in range(len(chLims)):
			if i == 0:
				limits.append(cnt_l - sum(sconf) - (len(chLims) - 1))
			else:
				limits.append(1)
	return limits

limits = checkUpopoi(sconf, sorry_lists)
#pprint(limits)
#exit()

'''残念賞の抽選'''
sorry = {}
reList = {}
for i in range(len(limits)):
	sorry.update({i: random.sample(sorry_lists, k=int(limits[i]))})
	reList = reChusen(sorry_lists, sorry[i])
	sorry_lists.clear()
	sorry_lists = reList

#pprint(sorry)
outputTsvSorry(sorry)
#os.system('cat ./data/winners.tsv')

