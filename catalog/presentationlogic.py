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
	resp_dict=dict(status=True)
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
			resp_dict['slide_id']=id_slide
		connection.commit()
	except Exception as e:
	    print(e)
	    resp_dict['status']=False
	finally:
		connection.close()
	return resp_dict

def saveslide(request):
	resp_dict=dict(status=True)
	slide_id=request.params['s_id']
	'''
	try:
		id_cat=int(request.params['idcat'])
	except:
		id_cat=0
	'''
	id_cat=request.params['idcat']
	desc=request.params['desc']
	pos_x=request.params['pos_y']
	pos_y=request.params['pos_x']
	obj_len=request.params['height']
	obj_wid=request.params['width']
	block_id=request.params['id']
	#print("{},{},{},{},{},{},{},{}".format(slide_id,id_cat,desc,pos_x,pos_y,obj_len,obj_wid,block_id))
	id_list=[]
	connection = pymysql.connect(host='127.0.0.1',
                           	 user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="SELECT id from slide_elements where flag=0;"
			cursor.execute(sql)
			id_list1=cursor.fetchall()
			for a in id_list1:
				id_list2=a['id']
				id_list.append(id_list2)
			if (int(block_id)!=0):
				sql1="UPDATE slide_elements SET s_id=%d, e_desc='%s', position_x=%d, position_y=%d, object_length=%d, object_breadth=%d where id=%d"%(int(slide_id),desc,int(pos_x),int(pos_y),int(obj_len),int(obj_wid),int(block_id))
				#print(sql1)
				cursor.execute(sql1)
				resp_dict['block_id']=block_id
			else:
 				if(id_cat!=""):
 					sql2="INSERT INTO slide_elements (s_id,e_id, e_desc, position_x, position_y, object_length, object_breadth) values (%s,%s,%s,%s,%s,%s,%s)"
 					cursor.execute(sql2,(int(slide_id),int(id_cat),desc,int(pos_x),int(pos_y),int(obj_len),int(obj_wid)))
 					sql3="SELECT LAST_INSERT_ID()";
 					cursor.execute(sql3)
 					idblock=cursor.fetchall()
 					id_block=idblock[0]['LAST_INSERT_ID()']
 					resp_dict['block_id']=id_block
 				else:
 					tmp_url=request.params['url']
 					sql4="INSERT INTO slide_elements (s_id,position_x, position_y, object_length, object_breadth, temp_url) values (%s,%s,%s,%s,%s,%s) "
 					cursor.execute(sql4,(int(slide_id),int(pos_x),int(pos_y),int(obj_len),int(obj_wid),tmp_url))
 					sql5="SELECT LAST_INSERT_ID()";
 					cursor.execute(sql5)
 					idblock=cursor.fetchall()
 					id_block=idblock[0]['LAST_INSERT_ID()']
 					resp_dict['block_id']=id_block
		connection.commit()
	except Exception as e:
		print(e)
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

def delete_element(request):
	resp_dict=dict(status=True)
	id=request.params['id']
	print(id)
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="UPDATE slide_elements SET flag=1 where id=%d"%(int(id))
			cursor.execute(sql)
		connection.commit()
	except Exception as e:
		print(e)
		resp_dict['status']=False
	finally:
		connection.close()
	return resp_dict
'''	
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
'''