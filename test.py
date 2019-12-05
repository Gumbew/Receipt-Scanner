# -*- encoding: utf-8 -*-

import re

text = 'РОТ мо ФА\n22.12.201'
#print(re.sub(r'(^.+?)(\d{2})', '\g<2>', text))


trim_trash_in_front = re.sub(r'.*(\d{2})', '\g<2>', text)
remove_new_line = re.sub(r'\\n', '', trim_trash_in_front)
print(remove_new_line)
