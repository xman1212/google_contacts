# -*- coding: utf-8 -*-

import csv
import codecs

# 分组标签字段的名称
GROUP_FIELD = u'Group Membership'

def read(path):
	keys = []
	data = []
	key_group = -1
	content = open(path, 'rb').read()
	content = content.decode('utf-16')
	for line in content.split('\n'):
		words = line.split(",")
		if len(keys) <= 0:
			# 提取字段名
			keys = words
			for i,key in enumerate(keys):
				if key.find(GROUP_FIELD) >= 0:
					key_group = i
					break
			assert key_group >= 0, "无法找到分组标签字段:" + GROUP_FIELD
		elif len(words) == len(keys):
			# 默认清空现有标签
			words[key_group] = []
			data.append(words)

	# 添加标签
	filter(keys, data, u"Phone", key_group, u"Phone")
	filter(keys, data, u"mail", key_group, u"Email")
	filter(keys, data, u"mail", key_group, u"Gmail", u"@gmail")
	filter(keys, data, u"Address", key_group, u"Address")

	# 转换标签格式
	tags = set()
	for dat in data:
		dat[key_group] = u" ::: ".join(dat[key_group])
		tags.add(dat[key_group])
	output(keys, data, "out.csv")
	print "tags", tags
	return keys, data

def filter(keys, data, filter_str, key_group, group_tag, sub_filter=None):
	''' 匹配filter_str的字段，如果其有内容则加上分组标记group_tag'''
	keys_filter = [i for i, key in enumerate(keys) if key.find(filter_str) >=0]
	for dat in data:
		finded = False
		for key in keys_filter:
			num = dat[key]
			if len(num) > 0:
				if sub_filter:
					if num.find(sub_filter) >= 0:
						finded = True
						break
				else:
					finded = True
					break
		if finded:
			dat[key_group].append(group_tag)

def output(keys, data, path):
	f = codecs.open(path, "wb", 'utf-16')
	def write_line(f, dat):
		line = u",".join(dat) + u"\n"
		line.encode('utf-16')
		#print line
		try:
			f.write(line)
		except:
			print "error:", line
	write_line(f, keys)
	for dat in data:
		write_line(f, dat)
	f.close()



read("google.csv")


