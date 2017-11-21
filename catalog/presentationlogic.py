import pymysql.cursors
from pyramid.request import Request

def addproject():
	from catalog.connection_py import connection as conn
	s_id_list=list()
	conn=conn()
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="INSERT INTO presentation_project() values()"
			cursor.execute(sql)
			sql1="SELECT LAST_INSERT_ID()";
			cursor.execute(sql1)
			pro_id=cursor.fetchall()
			project_id=int(pro_id[0]['LAST_INSERT_ID()'])
			query_1='''insert into Presentation (pr_id) values ({p_id})'''.format(p_id=project_id)
			cursor.execute(query_1)
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		# conn.close_connection()
		connection.close()
	return project_id

def local_connector():
	from catalog.connection_py import connection as conn
	conn=conn()
	resp = dict(status=True,con='')
	
	s = conn.connect()
	if not s["status"]:
		print("conn fail")
		resp["status"]=False
		return resp
	else:
		connection=s["connection"]
		resp['con']=connection
	return resp

# def get_slide_elements(s_id):
# 	elements=[]
# 	resp = dict(status=True,elements=elements)
# 	s = local_connector()
# 	if not s.status:
# 		resp['status']=False
# 	connection=s["con"]
# 	try:
# 		with connection.cursor() as cursor:
# 			query="select * from Presentation where flag=0 and s_id={id};".format(id=int(s_id))
# 			cursor.execute(query)
# 			s_id_list=cursor.fetchall()
# 		resp["s_id"]=[i for i in s_id_list]
# 	except Exception as e:
# 		print(e)
# 		resp["status"]=False
# 	finally:
# 		connection.close()
# 	return resp

def get_all_slides_id(p_id):
	from catalog.connection_py import connection as conn
	s_id_list=list()
	conn=conn()
	s = conn.connect()
	resp = dict(status=True,s_id=s_id_list,pr_id=p_id)
	if not s["status"]:
		print("conn fail")
		resp["status"]=False
		return resp
	else:
		connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			query="select s_id from Presentation where flag=0 and pr_id={pr_id};".format(pr_id=int(p_id))
			cursor.execute(query)
			s_id_list=cursor.fetchall()
		resp["s_id"]=[i['s_id'] for i in s_id_list]
	except Exception as e:
		print(e)
		resp["status"]=False
	finally:
		connection.close()
	print(resp)
	return resp

def addslide(request):
	id_p=request.params['id']
	id_slide=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="INSERT INTO Presentation (pr_id) values(%s)"
			cursor.execute(sql,(int(id_p)))
			sql1="SELECT LAST_INSERT_ID()";
			cursor.execute(sql1)
			idslide=cursor.fetchall()
			id_slide=idslide[0]['LAST_INSERT_ID()']
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	return id_slide

def saveslide(request):
	resp_dict=dict(status=True)
	slide_id=request.params['s_id']
	id_cat=request.params['idcat']
	desc=request.params['desc']
	pos_x=request.params['pos_y']
	pos_y=request.params['pos_x']
	obj_len=request.params['height']
	obj_wid=request.params['width']
	if(id_cat!=""):
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql="INSERT INTO slide_elements (s_id,e_id, e_desc, position_x, position_y, object_length, object_breadth) values (%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql,(int(slide_id),int(id_cat),desc,int(pos_x),int(pos_y),int(obj_len),int(obj_wid)))
				sql1="SELECT LAST_INSERT_ID()";
				cursor.execute(sql1)
				idblock=cursor.fetchall()
				id_block=idblock[0]['LAST_INSERT_ID()']
				resp_dict['block_id']=id_block
				connection.commit()
		except Exception as e:
			print(e)
			resp_dict['status']=False
		finally:
			connection.close()
	else:
		tmp_url=request.params['url']
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql1="INSERT INTO slide_elements (s_id,position_x, position_y, object_length, object_breadth, temp_url) values (%s,%s,%s,%s,%s,%s) "
				cursor.execute(sql,(int(slide_id),int(pos_x),int(pos_y),int(obj_len),int(obj_wid),tmp_url))
				sql1="SELECT LAST_INSERT_ID()";
				cursor.execute(sql1)
				idblock=cursor.fetchall()
				id_block=idblock[0]['LAST_INSERT_ID()']
				resp_dict['block_id']=id_block
			connection.commit()
		except NameError:
			print('An exception')
			resp_dict['status']=False
		finally:
			connection.close()
	return resp_dict

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