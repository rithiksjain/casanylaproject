import pymysql.cursors

def addproject():
	id_p=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			'''
			sql="SELECT * FROM presentation_project";
			cursor.execute(sql1)
			id_p1=cursor.fetchall()
			for a in id_p:
				id_p.append(b['id'])
			if(id_p==NULL):
			'''
			#else:
			sql="INSERT INTO presentation_project() values()"
			cursor.execute(sql)
			sql1="SELECT LAST_INSERT_ID()";
			cursor.execute(sql1)
			pro_id=cursor.fetchall()
			project_id=pro_id[0]['LAST_INSERT_ID()']
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
'''
def getslide():
	project_id=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="SELECT id from presentation_project"
			cursor.execute(sql)
			pro_id=cursor.fetchall()
			for a in pro_id:
				project_id.append(a)
			sql1="SELECT s_id from Presentation where pr_id=%d" %(int(project_id)
			cursor.execute(sql1)
			id_slide=cursor.fetchall()
			slide_id=id_slide[0]['s_id']
			sql2="SELECT * from slide_elements where s_id=%d" %(int(slide_id))
		connection.commit()
	except NameError:
		print('An exception flew by!')
	finally:
		connection.close()

'''
def addslide():
	id_p=request.params['id']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="INSERT INTO Presentation (pr_id) values(%d)"
			cursor.execute(sql,(int(id_p)))
			sql1="SELECT s_id from Presentation where pr_id=%d"
			cursor.execute(sql,(int(id_p)))
			project_id=cursor.fetchall()
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()

def saveslide():
	slide_id=request.params['idslide']
	id_cat=request.params['idcat']
	desc=request.params['desc']
	pos_x=request.params['pos_y']
	pos_y=request.params['pos_x']
	obj_len=request.params['height']
	obj_wid=request.params['width']
	tmp_url=request.params['url']
	if(id_cat!=NULL):
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql="INSERT INTO slide_elements (s_id,e_id, e_desc, position_x, position_y, object_length, object_breadth) values (%d,%d,%s,%d,%d,%d,%d)"
				cursor.execute(sql,(int(slide_id),int(id_cat),desc,int(pos_x),int(pos_y),int(obj_len),int(obj_wid)))
			connection.commit()
		except NameError:
			print('An exception')
		finally:
			connection.close()
	else:
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql1="INSERT INTO slide_elements (s_id,position_x, position_y, object_length, object_breadth, temp_url) values (%d,%d,%d,%d,%d,%s)"
				cursor.execute(sql,(int(slide_id),int(pos_x),int(pos_y),int(obj_len),int(obj_wid),tmp_url))
			connection.commit()
		except NameError:
			print('An exception')
		finally:
			connection.close()

def editslide():
	slide_id=request.params['idslide']
	id_cat=request.params['idcat']
	pos_x=request.params['pos_y']
	pos_y=request.params['pos_x']
	obj_len=request.params['height']
	obj_wid=request.params['width']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="UPDATE slide_elements SET position_x=%d, position_y=%d, object_length=%d, object_breadth=%d where s_id=%d"
			cursor.execute(sql,(int(pos_x),int(pos_y),int(obj_len),int(obj_wid),int(slide_id)))
		connection.commit()
	except NameError:
		print('An exception')
	finally:
		connection.close()

def deleteslide():
	slide_id=request.params['idslide']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="UPDATE presentation SET flag=1 where s_id=%d"
			cursor.execute(sql,(int(slide_id)))
		connection.commit()
	except NameError:
		print('An exception')
	finally:
		connection.close()
