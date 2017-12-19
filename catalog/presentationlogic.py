import pymysql.cursors
from pyramid.request import Request
from pyramid.security import unauthenticated_userid
from pyramid.httpexceptions import HTTPFound

def is_loggedin(is_loggedin_flag=0):
	def deco_func(original):
		def sub_func(*args,**kwargs):
			try:
				user_id = unauthenticated_userid(args[1])
			except Exception as e:
				user_id=None
			if is_loggedin_flag:
				if user_id is None:
					return original(args[1],0)
				else:
					return original(args[1],1)
					
			if user_id is None:
				url="/login"
				return HTTPFound(location=url)
			return original(args[1])
		return sub_func
	return deco_func


def addproject(request):
	pname = request.params['p_name']
	style = request.params['s_name']
	apartment = request.params['a_name']
	client = request.params['c_name']
	from catalog.connection_py import connection as conn
	s_id_list=list()
	conn=conn()
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="INSERT INTO presentation_project(presentation_name,apartment_name,style_name,client_name) values(%s,%s,%s,%s)"
			cursor.execute(sql,(pname,apartment,style,client))
			sql1="SELECT LAST_INSERT_ID()";
			cursor.execute(sql1)
			pro_id=cursor.fetchall()
			project_id=int(pro_id[0]['LAST_INSERT_ID()'])
			query_1='''insert into Presentation (pr_id) values (%s)'''
			cursor.execute(query_1,(project_id))
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
	resp = dict(status=True,s_id=s_id_list,pr_id=p_id,p_name="")
	if not s["status"]:
		print("conn fail")
		resp["status"]=False
		return resp
	else:
		connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			query="select s_id from Presentation where flag=0 and pr_id={pr_id};".format(pr_id=int(p_id))
			query_name="select presentation_name, apartment_name, style_name, client_name from presentation_project where id={pr_id};".format(pr_id=int(p_id))
			cursor.execute(query)
			s_id_list=cursor.fetchall()
			cursor.execute(query_name)
			res=cursor.fetchall()
			p_name = res[0]["presentation_name"]
			a_name = res[0]["apartment_name"]
			s_name = res[0]["style_name"]
			c_name = res[0]["client_name"]
		resp["s_id"]=[i['s_id'] for i in s_id_list]
		resp["p_name"]=p_name
		resp["a_name"]=a_name
		resp["s_name"]=s_name
		resp["c_name"]=c_name
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
	id_cat=int(request.params['idcat'])
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
				cursor.execute(sql1)
				resp_dict['block_id']=block_id
			else:
				if((id_cat!=0) and (id_cat!=-1)):
					sql2="INSERT INTO slide_elements (s_id,e_id, position_x, position_y, object_length, object_breadth) values (%s,%s,%s,%s,%s,%s)"
					cursor.execute(sql2,(int(slide_id),int(id_cat),int(pos_x),int(pos_y),int(obj_len),int(obj_wid)))
					sql3="SELECT LAST_INSERT_ID()";
					cursor.execute(sql3)
					idblock=cursor.fetchall()
					id_block=idblock[0]['LAST_INSERT_ID()']
					resp_dict['block_id']=id_block
				elif(id_cat==-1):
					sql2="INSERT INTO slide_elements (s_id,e_id,e_desc, position_x, position_y, object_length, object_breadth) values (%s,%s,%s,%s,%s,%s,%s)"
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

def getprice_quote(request):
	pr_id=request.params['pr_id']
	from catalog.connection_py import connection as conn
	conn=conn()
	s = conn.connect()
	connection=s["connection"]
	sum_val=0
	try:
		with connection.cursor() as cursor:
			sql="select c.ItemName, ca.CategoryName, coalesce(v.`Quotation(Exc Taxes)`,0) as `Quotation(Exc Taxes)` from  Presentation p inner join slide_elements s on p.s_id=s.s_id and s.flag=0 inner join Catalog c  on c.idCatalog=s.e_id inner join Category ca on ca.idCategory=c.idCategory left join VendorPieceQuotation v on c.idCatalog=v.idCatalog where p.pr_id={pr_id};".format(pr_id=int(pr_id)) 
			cursor.execute(sql)
			res=cursor.fetchall()
			if res:
				for i in res:
					sum_val+=int(i["Quotation(Exc Taxes)"])
		# connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return dict(price = res,sum_val=sum_val)