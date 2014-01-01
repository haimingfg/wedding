#coding=utf-8
#!/usr/bin/python

import os,sys,json

def role_type(role_id):
	_role_type = ['客人','兄弟']	
	role_id = int(role_id)
	rlen = len(_role_type)
	if (rlen < role_id or 0 > role_id):
		return False
	return _role_type[role_id - 1]

def loop_input(_type='string', _len=5):
	_type_tips = {'string':u'字符', 'number':'数字', 'bool':'True/False'}
	while True:
		print u'请输入%s'% _type_tips[_type]
		line = sys.stdin.readline().strip()
		if 0 < len(line): return line

def is_check_unique(member_name, members):
	for member in members:
		if member['name'] == member_name.decode('utf-8'):
			return False
	return True

def write_to_json(data, file_name):
	f = open(file_name, 'w')
	if 0 < len(data):
		f.write(json.dumps(data))
		

def read_from_json(file_name):
	if os.path.isfile(file_name):f = open(file_name, 'r').read()
	return [] if 0 == len(f) else json.loads(f)

def create_member(name, role, is_note, is_come):
	if 0 == len(name): name = loop_input();
	name = name.decode('utf-8')
	return {'name':name, 'role':role, 'is_note':is_note, 'is_come':is_come}

def note_mode(members):
	print '通知模式见到人名打个电话,e个mail输入y来，n不来，0不确定';
	for member in members:
		if False == member['is_note']:
			print member['name']
			line = sys.stdin.readline().strip();
			if 'y' == line:
				member['is_note'] = True
				member['is_come'] = True
				print '来到做，' + role_type(member['role']);
				line = sys.stdin.readline().strip();
				if 'y' != line:
					member['role'] = 1 if 2 == member['role'] else 2

				print '是否有其他人过来,y:是 n:否'
				line = sys.stdin.readline().strip();
				if 'y' == line:
					add_mode(members, True)
			elif 'n' == line:
				member['is_note'] = True
				member['is_come'] = False
			elif 'done' == line:
				print '推出'
				break
			print '设定成功'
	print '全部设置完毕,请按help提示'

def add_mode(members, is_come=False):
	fst_come = True
	while True:
		tips = u'请输入' if fst_come else u'继续,如果完成请输入done'
		fst_come = False
		print tips

		name = sys.stdin.readline().strip()
		if 'done' == name: 
			break
		else:
			if is_check_unique(name, members):
				print '1：做客人食饭，2：做兄弟'
				role_id = int(sys.stdin.readline().strip())
				if False == is_come:
					is_note = False
				else:
					is_note = True
				member = create_member(name, role_id, is_note, is_come)
				members.append(member)
			else:
				print '已经有%s，或者输入一些标识标志这个是谁' % name;

def show_mode(members):
	id = 1
	for member in members:
		name = member['name']		
		role = role_type(member['role'])
		note_tips = '通知了' if member['is_note'] else '没有通知'
		if member['is_note']:
			come_tips = '确认来' if member['is_come'] else '确认不来'
		else:
			come_tips = '等通知'
		come_tips = come_tips + ',做' + role

		print '%d.%s,%s,%s' % (id, name, \
				note_tips.decode('utf-8'), come_tips.decode('utf-8')) 
		id += 1


def edit_member(members):
	mlen = len(members)
	if 0 == mlen:
		print '列表空'
		return False

	show_mode(members);
	print '输入序号,done结束'
	line = sys.stdin.readline().strip()
	if 'done' == line: return False
	_id = int(line);
	
	print _id > mlen
	print mlen
	if (_id > mlen) or (_id < 0) :
		print '请输入正确的序号'
		return False

	member_name = members[_id - 1]['name']

	print '你修改的人是 -> %s 请输入修改的信息' % member_name.encode('utf-8')
	print '修改信息，只输入回车不修改'

	order_type = 0

	while True:
		if 0 == order_type:
			print '输入名字'
			name = sys.stdin.readline().strip()
			if False == is_check_unique(name, members):
				print '已经有这个名字,如果同名请输入标识'
				order_type = 0;
			else:
				name = member_name.encode('utf-8')
		elif 1 == order_type: 
			print '输入角色 1:宾客 2:兄弟'
			role = sys.stdin.readline().strip()
		elif 2 == order_type: 
			print '输入是否通知 y:通知 n:没有'
			is_note = sys.stdin.readline().strip()
			is_note = True if 'y' == is_note else False
			if False == is_note:
				is_come = False
				order_type += 1
		elif 3 == order_type:
			print '输入是否来 y:来 n:不来'
			is_come = sys.stdin.readline().strip()
			is_come = True if 'y' == is_come else False
		else:
			print '输入回车重新输入一遍,输入done 保存结束'
			line = sys.stdin.readline().strip()
			if 'done' != line:
				order_type = 0
			else:
				order_type = -1
		if 0 > order_type:
			member = create_member(name, role, is_note, is_come)
			members[_id - 1] = member
			break;
		else:
			order_type+=1

def tongji_member(members):
	come_num = not_note_num = note_num = 0
	for member in members:
		come_num += 1 if member['is_note'] and member['is_come'] else 0
		note_num += 1 if member['is_note'] else 0
		not_note_num += 1 if False == member['is_note'] else 0
	
	print '有%d通知了，有%d没有通知，有%d确认来' % (note_num, not_note_num, come_num)

def come_list(members):
	come_num = 0
	id = 0
	for member in members:
		is_come = member['is_note'] and member['is_come']
		if is_come: 
			come_num += 1 	
			id += 1
			print '%d.%s' % (id, member['name'])
	print '共%d' % come_num


def not_come_list(members):
	come_num = 0
	id = 0
	for member in members:
		not_come = (member['is_note'] and False == member['is_come'])
		if not_come:
			come_num += 1
			id += 1
			print '%d.%s' % (id, member['name'])
	print '共%d' % come_num

def not_note_mode(members):
	num = 0
	id = 0
	for member in members:
		not_note = False == member['is_note']	
		if not_note:
			num += 1
			id += 1
			print '%d.%s' % (id, member['name'])
	print '共%d' % num

def role_list(members, role_id):
	num = 0
	id = 0
	for member in members:
		_member_type = int(member['role'])
		if (True == member['is_come'] and role_id == _member_type):
			num +=1
			id += 1
			print '%d.%s' % (id, member['name'])
	print '共%d' % num


def del_all(members):
	return []

def del_mode(members):
	mlen = len(members)
	if 0 == mlen:
		print '列表空'
		return False

	show_mode(members);
	print '输入序号可以多个操作，英文的,隔开'
	_ids = sys.stdin.readline().strip().split(',')
	
	line = ''
	del_members_name = []
	for _id in _ids:
		_id = int(_id) - 1
		if (_id > mlen) or (_id < 0) :
			print '请输入正确的序号'
			return False
		member_name = members[_id]['name'].encode('utf-8')
		del_members_name.append(member_name)

	print del_members_name
	if [] == del_members_name: 
		print '没有删除的名单'
		return False
	new_member = []
	for i,member in enumerate(members):	
		member_name = member['name'].encode('utf-8')		
		if member_name in del_members_name:
		
			print '你删除的人是 -> %s ' % member_name
			print '删除请按y, Y每个确认直接删除'
			if 'Y' != line:
				line = sys.stdin.readline().strip()
			
			print '已删除%s' % member_name
		else:
			new_member.append(members[i])
	members = new_member
	#print new_member
	#print members
	#del new_member
	print  '删除结束'
	return new_member




def show_tips():
	print """
add: 进入名单输入
del: 进入删除名字
del_all: 删除全部
edit: 进入修改人信息
show: 查看名单
done: 返回返回上级/退出
tongji: 人数统计
come_list: 来的人数列表
not_come_list: 没有来的人
guest_list:客人列表
brother_list: 兄弟列表
not_note: 没有通知
note: 通知模式
help: 帮助
"""

file_name = 'members.json'
# members
members = read_from_json(file_name)

fst = True
while True:
	if [] == members:
		print "名单是空的是否添加,添加请按add, 结束请按done";
	else:
		if fst:show_tips()
		fst = False
		
	line = sys.stdin.readline().strip()
	if 'help' == line:
		show_tips()

	if 'done' == line: write_to_json(members, file_name);break

	if 'add' == line:
		add_mode(members)

	if 'show' == line:
		show_mode(members)
		
	if 'edit' == line:
		edit_member(members)

	if 'tongji' == line:
		tongji_member(members)

	if 'come_list' == line:
		come_list(members)

	if 'not_come_list' == line:
		not_come_list(members)

	if 'guest_list' == line:
		role_list(members, 1)

	if 'brother_list' == line:
		role_list(members, 2)

	if 'note' == line:
		note_mode(members)

	if 'not_note' == line:
		not_note_mode(members)

	if 'del_all' == line:
		members = del_all(members)
	if 'del' == line:
		members = del_mode(members)
