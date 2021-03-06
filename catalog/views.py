from pyramid.view import (view_config, view_defaults)
from pyramid.renderers import render_to_response
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.response import FileIter
from pyramid.response import FileResponse
from pyramid_flash_message import MessageQueue
from pyramid.view import render_view_to_response
from pyramid.request import Request
from catalog.presentationlogic import *
from pyramid.httpexceptions import HTTPFound
from catalog.connection_py import connection as conn
import tempfile
import pymysql.cursors
import ast
import zipfile
import glob
import shutil
import os
import json
from pyramid.security import (
	remember,
	forget,
	unauthenticated_userid,
)
conn=conn()
src_dir = "catalog/catalog/images"
dst_dir = "catalog/catalog/listimages"
dst_dir1 = "catalog/catalog/listimages/*"

'''@view_config(renderer='templates/home1.jinja2')
class Login:
	def __init__(self, request):
		self.request = request
		self.logged_in = request.authenticated_userid

	@view_config(route_name='home')
	def home(self):
		return {'name': 'Home View'}

	@view_config(route_name='hello')
	def hello(self):
		return {'name': 'Hello View'}


	@view_config(route_name='login',renderer='templates/login.jinja2')
	def login(self):
	        request = self.request
	        login_url = request.route_url('login')
	        referrer = request.url
	        if referrer == login_url:
	        	referrer = '/home1'  
	        came_from = request.params.get('came_from', referrer)
	        message = ''
	        login = ''
	        password = ''
	        if 'form.submitted' in request.params:
	        	print("1")
	        	login = request.params['uname']
	        	password = request.params['password']
	        	hashed_pw = USERS.get(login)
	        	print(hashed_pw)
	        	if hashed_pw and check_password(password, hashed_pw):
	        		print("2")
	        		headers = remember(request, login)
	        		return HTTPFound(location=came_from,headers=headers)
	        	message = 'Failed login'

	        return dict(
	            name='Login',
	            message=message,
	            url=request.application_url + '/login',
	            came_from=came_from,
	            login=login,
	            password=password,
	        )

	@view_config(route_name='logout')
	def logout(self):
	    request = self.request
	    headers = forget(request)
	    url = request.route_url('home')
	    return HTTPFound(location=url,headers=headers)

@view_config(route_name='home1',renderer='templates/home1.jinja2')
def home(request):
	return {}
'''


@view_config(route_name='login',renderer='templates/login.jinja2')
@is_loggedin(1)
def login(request,is_loggedin):
	message=''
	if is_loggedin:
		return HTTPFound(location="/submitlogin")

	if request.method=="POST":
		name=request.params['uname']
		password=request.params['password']
		s = conn.connect()
		connection=s["connection"]
		try:
			with connection.cursor() as cursor:
				sql="SELECT * FROM `User`"
				cursor.execute(sql)
				result=cursor.fetchall()
				for res in result:
					user=res['UserName']
					pwd=res['Password']
					if name==user and password==pwd:
						headers = remember(request, res['idUser'])
						return HTTPFound(location='/submitlogin',headers=headers)
					else:
						message="wrong creds"
		except Exception as e:
			message="something went wrong"
			print (e)
		connection.close()
	came_from = request.params.get('came_from', request.url)
	return dict(name='Login',message=message,came_from=came_from)

@view_config(route_name='submitlogin')
@is_loggedin()
def submitlogin(request):
	return render_to_response('templates/home.jinja2',{},request=request)

@view_config(route_name='logout')
@is_loggedin()
def logout(request):
    headers = forget(request)
    url = request.route_url('login')
    return HTTPFound(location=url,headers=headers)

@view_config(route_name='addpre')
@is_loggedin()
def addpre(request):
	id1=addproject(request)
	url=request.application_url+'/presentation/'+str(id1)
	return Response(status_int=302, location=url)

@view_config(route_name='clientdet')
@is_loggedin()
def clientdet(request):
	return render_to_response('templates/clientdetails.jinja2',{},request=request)


@view_config(route_name='editclient')
@is_loggedin()
def editclient(request):
	pr_id=request.params['prid']
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT apartment_name, presentation_name, style_name, client_name from presentation_project where id='%s'" %(pr_id)
			cursor.execute(sql)
			res=cursor.fetchall();
			print(res)
			a_name=res[0]['apartment_name']
			p_name=res[0]['presentation_name']
			s_name=res[0]['style_name']
			c_name=res[0]['client_name']
			connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/editclient.jinja2',{'pr_id':pr_id, 'p_name':p_name, 'a_name':a_name, 's_name':s_name, 'c_name':c_name}, request=request)

@view_config(route_name='subclient')
@is_loggedin()
def subclient(request):
	pr_id = request.params['prid']
	p_name = request.params['p_name']
	a_name = request.params['a_name']
	s_name = request.params['s_name']
	c_name = request.params['c_name']
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="UPDATE presentation_project set presentation_name=%s, style_name=%s, apartment_name=%s, client_name=%s where id=%s"
			cursor.execute(sql,(p_name,s_name,a_name,c_name,pr_id))
			connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	from pyramid.httpexceptions import HTTPFound
	url=request.application_url+'/presentation/'+str(pr_id)
	return Response(status_int=302, location=url)


@view_config(route_name='addslide', renderer='json')
@is_loggedin()
def add_slide(request):
	add=addslide(request)
	print(add)
	return add

@view_config(route_name='getprice')
@is_loggedin()
def getprice(request):
	price=getprice_quote(request)
	return render_to_response('templates/pricelist.jinja2',price,request=request)

@view_config(route_name='saveslide' ,renderer='json')
@is_loggedin()
def save_slide(request):
	s = saveslide(request)
	print (s)
	return s

@view_config(route_name='delete_ele', renderer='json')
@is_loggedin()
def delete(request):
	d = delete_element(request)
	print(d)
	return d

@view_config(route_name='vendor',renderer='templates/vendorform.jinja2')
@is_loggedin()
def vendor(request):
	return {}

@view_config(route_name='category',renderer='templates/category.jinja2')
@is_loggedin()
def category(request):
	return {}

@view_config(route_name='material',renderer='templates/material.jinja2')
@is_loggedin()
def material(request):
	return {}

@view_config(route_name='fabric',renderer='templates/fabric.jinja2')
@is_loggedin()
def fabric(request):
	return {}

@view_config(route_name='itemtype',renderer='templates/itemtype.jinja2')
@is_loggedin()
def itemtype(request):
	return {}

@view_config(route_name='createlist')
@is_loggedin()
def createlist(request):
	userid=request.params['id']
	return render_to_response('templates/addlist.jinja2',{'id':userid},request=request)

@view_config(route_name='itemadded')
@is_loggedin()
def itemadded(request):
	listid=request.params['idlist']
	catalogid=request.params['id']
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="INSERT INTO `ListItems` (`idList`,`idCatalog`) VALUES (%s,%s)"
			cursor.execute(sql, (listid,catalogid))
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Item added to List!')
	return render_to_response('templates/submitlist.jinja2',{},request=request)

@view_config(route_name='presentation',renderer='templates/presentation.html')
@is_loggedin(1)
def presentation(request,is_loggedin):
	try:
		p_id=int(request.matchdict['p_id'])
	except Exception as e:
		s_id=[]
		return dict(status=False,s_id=[],is_loggedin=is_loggedin)
	resp = get_all_slides_id(p_id)
	resp.update({'is_loggedin':is_loggedin})
	print(resp)
	return resp

@view_config(route_name='catalog')
@is_loggedin()
def catalog(request):
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT * FROM `Category`"
			cursor.execute(sql)
			result=cursor.fetchall()
			cat1=[]
			for r in result:
				cat={'id':r['idCategory'], 'name':r['CategoryName']}
				cat1.append(cat)

			sql1="SELECT * FROM `ItemType`"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			item1=[]
			for s in result1:
				item={'id':s['idItemType'], 'name':s['ItemTypeName']}
				item1.append(item)

		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/catalog.jinja2',{'cat1':cat1,'item1':item1},request=request)


@view_config(route_name='quotation')
@is_loggedin()
def quotation(request):
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT * FROM `Vendor`"
			cursor.execute(sql)
			result=cursor.fetchall()
			ven1=[]
			for r in result:
				ven={'id':r['idVendor'], 'name':r['Name']}
				ven1.append(ven)

			sql1="SELECT * FROM `Catalog`"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			name1=[]
			for s in result1:
				name={'id':s['idCatalog'], 'name':s['ItemName']}
				name1.append(name)
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/vendorpiece.jinja2',{'ven1':ven1,'name1':name1},request=request)

@view_config(route_name='addquote')
@is_loggedin()
def quotation(request):
	itemid=request.params['id']
	nameitem=request.params['name']
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT * FROM `Vendor`"
			cursor.execute(sql)
			result=cursor.fetchall()
			ven1=[]
			for r in result:
				ven={'id':r['idVendor'], 'name':r['Name']}
				ven1.append(ven)
			sql1="SELECT SKU from `Catalog` where `idCatalog`='%s'" %(itemid)
			cursor.execute(sql1)
			res=cursor.fetchall()
			sku=res[0]['SKU']
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/addquote.jinja2',{'sku':sku,'itemid':itemid,'nameitem':nameitem,'ven1':ven1},request=request)

@view_config(route_name='itemfetch')
@is_loggedin()
def itemfetch(request):
	userid=request.params['id']
	s = conn.connect()
	connection=s["connection"]
	typename=[]
	catname=[]
	try:
		with connection.cursor() as cursor:
			sql="SELECT c.`idCatalog`, i.`ItemTypeName`, c.`ItemDescription`, c.`ItemName`, ca.`CategoryName`, im.`URL` FROM `ItemType` as i, `Catalog` as c, `Category` as ca, `Images` as im WHERE ca.`idCategory`=c.`idCategory` AND i.`idItemType`=c.`idItemType` AND c.`idCatalog`=im.`idCatalog`"
			cursor.execute(sql)
			result=cursor.fetchall()
			item=[]
			for a in result:
				item1={'itemtypename':a['ItemTypeName'],'idcat':a['idCatalog'] ,'url':a['URL'], 'description':a['ItemDescription'], 'itemname':a['ItemName'], 'catname':a['CategoryName']}
				item.append(item1)

			sql1="SELECT * from `ItemType`"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			for b in result1:
				typename.append(b['ItemTypeName'])
			typename1=[str(i) for i in typename]

			sql2="SELECT * from `Category`"
			cursor.execute(sql2)
			res2=cursor.fetchall()
			for c in res2:
				catname.append(c['CategoryName'])
			catname1=[str(i) for i in catname]
		connection.commit()
	except Exception as e:
			print(e)
	finally:
		connection.close()
	return render_to_response('templates/itemfetch.jinja2',{'userid':userid,'item':item,'typename':typename1,'catname':catname1},request=request)

@view_config(route_name='itemdetails')
@is_loggedin()
def itemdetails(request):
	idcat=request.params['id']
	userid=request.params['userid']
	listname=[]
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			details=[]
			sql="SELECT * FROM `VendorPieceQuotation` where `idCatalog`='%s'" %(idcat)
			cursor.execute(sql)
			result=cursor.fetchall()
			detail=[]
			for a in result:
				sql3="SELECT Name FROM Vendor where idVendor='%s'" %(a['idVendor'])
				cursor.execute(sql3)
				result3=cursor.fetchall()
				venname=result3[0]['Name']
				detail1={'venname':venname,'idvenpiece':a['idVendorPieceQuotation'],'costexc':a['Quotation(Exc taxes)'],'excise':a['Excise Duty'],'tax':a['Taxes'],'costinc':a['Quotation(Inc taxes)'],'shipping':a['Shipping Charges'],'totalcost':a['Total Cost Price'],'warranty':a['Warranty'],'delivery':a['Delivery Time'],'payment':a['PaymentTerms'],'comments':a['Comments']}
				detail.append(detail1)

			sql1="SELECT `ItemDescription`,`ItemName`,`Width(inch)`,`Depth(inch)`,`Height(inch)`,`Remarks` FROM `Catalog` where `idCatalog`='%s'" %(idcat)
			cursor.execute(sql1)
			result1=cursor.fetchall()

			sql2="SELECT `URL` FROM `Images` where `idCatalog`='%s'" %(idcat)
			cursor.execute(sql2)
			result2=cursor.fetchall()

			sql4="SELECT ca.`CategoryName`, i.`ItemTypeName` FROM `Category` as ca, `ItemType` as i, `Catalog` as c where ca.`idCategory`=c.`IdCategory` and i.`idItemtype`=c.`idItemType` and `idCatalog`='%s'" %(idcat)
			cursor.execute(sql4)
			result4=cursor.fetchall()

			sql5="SELECT idList,ListName FROM List where idUser='%s' and Flag=0" %(userid)
			cursor.execute(sql5)
			result5=cursor.fetchall()
			for b in result5:
				listname1={'listid':b['idList'],'listname':b['ListName']}
				listname.append(listname1)

			details={'categoryname':result4[0]['CategoryName'],'itemtypename':result4[0]['ItemTypeName'],'idcat':idcat,'itemdesc':result1[0]['ItemDescription'],'itemname':result1[0]['ItemName'],'width':result1[0]['Width(inch)'],'depth':result1[0]['Depth(inch)'],'height':result1[0]['Height(inch)'],'remarks':result1[0]['Remarks'],'url':result2[0]['URL']}		
		connection.commit()	
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/itemdetailsnew.jinja2',{'userid':userid,'details':details,'detail':detail,'listname':listname},request=request)

@view_config(route_name='editdetails')
@is_loggedin()
def editdetails(request):
	details=request.params['det']
	details1 = ast.literal_eval(details)
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql1="SELECT * from `ItemType`"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			typename1=[]
			for b in result1:
				typename={'id':b['idItemType'], 'name':b['ItemTypeName']}
				typename1.append(typename)


			sql2="SELECT * from `Category`"
			cursor.execute(sql2)
			res2=cursor.fetchall()
			catname1=[]
			for c in res2:
				catname={'id':c['idCategory'], 'name':c['CategoryName']}
				catname1.append(catname)
		connection.commit()
	except Exception as e:
			print(e)
	finally:
		connection.close()
	return render_to_response('templates/edititem.jinja2',{'details1':details1,'typename':typename1,'catname':catname1},request=request)

@view_config(route_name='vendoredit')
@is_loggedin()
def vendoredit(request):
	details=request.params['det']
	details1 = ast.literal_eval(details)
	return render_to_response('templates/editvendor.jinja2',{'details1':details1},request=request)

@view_config(route_name='search')
@is_loggedin()
def search(request):
	ids=[]
	item4=[]
	res2=[]
	search=request.params['search']
	words=search.split()
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			ItemStrings=["ItemName like '%"+x+"%' or ItemDescription like '%"+x+"%'" for x in words]
			sql="SELECT idCatalog FROM Catalog WHERE " + " or ".join(ItemStrings)
			cursor.execute(sql)
			res=cursor.fetchall()
			for a in res:
				ids.append(a['idCatalog'])
			for b in ids:
				sql1="SELECT c.`idCatalog`, i.`ItemTypeName`, c.`ItemName`, ca.`CategoryName`, im.`URL` FROM `ItemType` as i, `Catalog` as c, `Category` as ca, `Images` as im WHERE ca.`idCategory`=c.`idCategory` AND i.`idItemType`=c.`idItemType` AND c.`idCatalog`=im.`idCatalog` AND c.`idCatalog`='%s'" %(b)
				cursor.execute(sql1)
				res1=cursor.fetchall()
				res2.extend(res1)
			for c in res2:
				item1={'idcat':c['idCatalog'],'itemtypename':c['ItemTypeName'],'url':c['URL'] , 'itemname':c['ItemName'], 'catname':c['CategoryName']}
				item4.append(item1)
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/itemfetch.jinja2',{'item':item4},request=request)

@view_config(route_name='viewlist')
@is_loggedin()
def viewlist(request):
	userid=request.params['id']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT ListName FROM List where idUser='%s'" %(userid)
			cursor.execute(sql)
			result=cursor.fetchall()
			namelist=[]
			for a in result:
				namelist1=a['ListName']
				namelist.append(namelist1)
			namelist2=[str(i) for i in namelist]
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/viewlist.jinja2',{'namelist':namelist2,'userid':userid},request=request)

@view_config(route_name='viewpresentation')
@is_loggedin()
def viewpresentation(request):
	projectname=[]
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT id,presentation_name from presentation_project"
			cursor.execute(sql)
			result1=cursor.fetchall()
			for b in result1:
				projectname.append(b['presentation_name'])
			projectname1=[str(i) for i in projectname]
			projectname1=[x for x in projectname1 if x!='None']
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	return render_to_response('templates/viewproject.jinja2',{'name':projectname1},request=request)

@view_config(route_name='filter')
@is_loggedin()
def filter(request):
	itemname=request.params['item']
	catname1=request.params['cat']
	typename=[]
	catname=[]
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql1="SELECT * from `ItemType`"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			for b in result1:
				typename.append(b['ItemTypeName'])
			typename1=[str(i) for i in typename]
			
			sql2="SELECT * from `Category`"
			cursor.execute(sql2)
			res2=cursor.fetchall()
			for c in res2:
				catname.append(c['CategoryName'])
			catname2=[str(i) for i in catname]
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()

	if((itemname!="") and (catname1=="")):
		s = conn.connect()
		connection=s["connection"]
		try:
			with connection.cursor() as cursor:
				sql1="SELECT `idItemType` FROM `ItemType` WHERE `ItemTypeName`=%s"
				cursor.execute(sql1,(itemname))
				res1=cursor.fetchall()
				iditem=res1[0]['idItemType']

				sql="SELECT c.`idCatalog`, c.`ItemName`, ca.`CategoryName`, i.`ItemTypeName`, im.`URL` from `ItemType` as i, `Catalog` as c, `Category` as ca, `Images` as im WHERE ca.`idCategory`=c.`idCategory` AND i.`idItemType`=c.`idItemType` AND c.`idCatalog`=im.`idCatalog` AND c.`idItemType`='%s'" %(iditem)
				cursor.execute(sql)
				res=cursor.fetchall()
				item=[]
				for a in res:
					item1={'itemtypename':a['ItemTypeName'], 'idcat':a['idCatalog'] ,'url':a['URL'], 'itemname':a['ItemName'], 'catname':a['CategoryName']}
					item.append(item1)
			connection.commit()
		except Exception as e:
			print(e)
		finally:
			connection.close()
		return render_to_response('templates/itemfetch.jinja2',{'itemname':itemname,'item':item,'typename':typename1,'catname':catname2},request=request)
		
	elif((catname1!="") and (itemname=="")):
		s = conn.connect()
		connection=s["connection"]
		try:
			with connection.cursor() as cursor:
				sql1="SELECT `idCategory` FROM `Category` WHERE `CategoryName`=%s"
				cursor.execute(sql1,(catname1))
				res1=cursor.fetchall()
				idcat=res1[0]['idCategory']

				sql="SELECT c.`idCatalog`, c.`ItemName`, ca.`CategoryName`, i.`ItemTypeName`, im.`URL` from `ItemType` as i, `Catalog` as c, `Category` as ca, `Images` as im WHERE ca.`idCategory`=c.`idCategory` AND i.`idItemType`=c.`idItemType` AND c.`idCatalog`=im.`idCatalog` AND c.`idCategory`='%s'" %(idcat)
				cursor.execute(sql)
				res=cursor.fetchall()
				item=[]
				for a in res:
					item1={'itemtypename':a['ItemTypeName'], 'idcat':a['idCatalog'] ,'url':a['URL'], 'itemname':a['ItemName'], 'catname':a['CategoryName']}
					item.append(item1)
			connection.commit()
		except Exception as e:
			print(e)
		finally:
			connection.close()
		return render_to_response('templates/itemfetch.jinja2',{'catname1':catname1,'item':item,'typename':typename1,'catname':catname2},request=request)

	elif((catname1!="") and (itemname!="")):
		s = conn.connect()
		connection=s["connection"]
		try:
			with connection.cursor() as cursor:
				sql1="SELECT `idItemType` FROM `ItemType` WHERE `ItemTypeName`=%s"
				cursor.execute(sql1,(itemname))
				res1=cursor.fetchall()
				iditem=res1[0]['idItemType']

				sql2="SELECT `idCategory` FROM `Category` WHERE `CategoryName`=%s"
				cursor.execute(sql2,(catname1))
				res2=cursor.fetchall()
				idcat=res2[0]['idCategory']

				sql="SELECT c.`idCatalog`, c.`ItemName`, ca.`CategoryName`, i.`ItemTypeName`, im.`URL` from `ItemType` as i, `Catalog` as c, `Category` as ca, `Images` as im WHERE ca.`idCategory`=c.`idCategory` AND i.`idItemType`=c.`idItemType` AND c.`idCatalog`=im.`idCatalog` AND c.`idItemType`='%s' AND c.`idCategory`='%s'" %(iditem,idcat)
				cursor.execute(sql)
				res=cursor.fetchall()
				item=[]
				for a in res:
					item1={'itemtypename':a['ItemTypeName'], 'idcat':a['idCatalog'] ,'url':a['URL'], 'itemname':a['ItemName'], 'catname':a['CategoryName']}
					item.append(item1)
			connection.commit()
		except Exception as e:
			print(e)
		finally:
			connection.close()
		return render_to_response('templates/itemfetch.jinja2',{'itemname':itemname,'catname1':catname1,'item':item,'typename':typename1,'catname':catname2},request=request)
	else:
		return render_to_response('templates/itemfetch.jinja2',{},request=request)

@view_config(route_name='submit')
@is_loggedin()
def vendorsubmit(request):
	name=request.params['name']
	address=request.params['address']
	contactno=request.params['contactno']
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Vendor` (`Name`, `Address`,`Contact_No`) VALUES (%s, %s, %s)"
			cursor.execute(sql, (name,address,contactno))
		connection.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Vendor is added!')
	return render_to_response('templates/vendorform.jinja2',{},request=request)

@view_config(route_name='submitcat')
@is_loggedin()
def submitcat(request):
	catname=request.params['name']
	desc=request.params['description']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Category` (`CategoryName`,`CategoryDescription`) VALUES (%s,%s)"
			cursor.execute(sql, (catname,desc))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Category is added!')
	return render_to_response('templates/category.jinja2',{},request=request)

@view_config(route_name='submitcatalog')
@is_loggedin()
def submitcatalog(request):
	sku=request.params['SKU']
	idcat=request.params['idcat']
	remarks=request.params['remarks']
	name=request.params['name']
	iditem=request.params['iditem']
	description=request.params['description']
	width=request.params['width']
	depth=request.params['depth']
	height=request.params['height']
	imagename=request.params['image'].filename
	request.storage.save(request.POST['image'])
	urlimage=request.storage.url(imagename)

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Catalog` (`idCategory`,`idItemType`,`SKU`,`ItemName`,`ItemDescription`,`Width(inch)`,`Depth(inch)`,`Height(inch)`,`Remarks`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql, (idcat,iditem,sku,name,description,width,depth,height,remarks))
			catalogid= "SELECT LAST_INSERT_ID()"
			cursor.execute(catalogid)
			catt=cursor.fetchall()
			catid=catt[0]
			catid1=catid['LAST_INSERT_ID()']
			sql2 = "INSERT INTO `Images` (`URL`,`idCatalog`) VALUES (%s,%s)"
			cursor.execute(sql2, (urlimage,catid1))

		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Item is added!')
	return render_to_response('templates/catalog.jinja2',{},request=request)

@view_config(route_name='submitmat')
@is_loggedin()
def submitmat(request):
	name=request.params['name']
	quantity=request.params['quantity']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Material` (`Name`,`Quantity`) VALUES (%s)"
			cursor.execute(sql, (name,quantity))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Material is added!')
	return render_to_response('templates/material.jinja2',{},request=request)

@view_config(route_name='submitfab')
@is_loggedin()
def submitfab(request):
	length=request.params['len']
	fabtype=request.params['type']
	cost=request.params['cost']
	code=request.params['code']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Fabric` (`Length(metre)`,`Type`,`Cost/metre`,`Fabric Code`) VALUES (%s,%s,%s,%s)"
			cursor.execute(sql, (length,fabtype,cost,code))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Fabric is added!')
	return render_to_response('templates/fabric.jinja2',{},request=request)

@view_config(route_name='submititem')
@is_loggedin()
def submititem(request):
	typename=request.params['typename']
	typedesc=request.params['typedesc']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `ItemType` (`ItemTypeName`,`ItemTypeDescription`) VALUES (%s,%s)"
			cursor.execute(sql, (typename,typedesc))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Item Type is added!')
	return render_to_response('templates/itemtype.jinja2',{},request=request)

@view_config(route_name='submitquot')
@is_loggedin()
def submitquot(request):
	idven=request.params['idven']
	idcat2=request.params['iditem']
	quotationex=request.params['quotationex']
	quotationin=request.params['quotationin']
	taxes=request.params['tax']
	shippingcharge=request.params['shipping']
	totalcost=request.params['cost']
	delivery=request.params['delivery']
	payment=request.params['payment']
	comments=request.params['comments']
	warranty=request.params['warranty']
	exciseduty=request.params['exciseduty']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `VendorPieceQuotation` (`idVendor`,`idCatalog`,`Quotation(Exc Taxes)`,`Excise Duty`,`Taxes`,`Quotation(Inc Taxes)`,`Shipping Charges`,`Total Cost Price`,`Warranty`,`Delivery Time`,`PaymentTerms`,`Comments`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql, (idven,idcat2,quotationex,exciseduty,taxes,quotationin,shippingcharge,totalcost,warranty,delivery,payment,comments))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Quotation is added for an Item!')
	return render_to_response('templates/vendorpiece.jinja2',{},request=request)

@view_config(route_name='submitaddquote')
@is_loggedin()
def submitaddquote(request):
	idven=request.params['idven']
	idcat2=request.params['id']
	quotationex=request.params['quotationex']
	quotationin=request.params['quotationin']
	taxes=request.params['tax']
	shippingcharge=request.params['shipping']
	totalcost=request.params['cost']
	delivery=request.params['delivery']
	payment=request.params['payment']
	comments=request.params['comments']
	warranty=request.params['warranty']
	exciseduty=request.params['exciseduty']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `VendorPieceQuotation` (`idVendor`,`idCatalog`,`Quotation(Exc Taxes)`,`Excise Duty`,`Taxes`,`Quotation(Inc Taxes)`,`Shipping Charges`,`Total Cost Price`,`Warranty`,`Delivery Time`,`PaymentTerms`,`Comments`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql, (idven,idcat2,quotationex,exciseduty,taxes,quotationin,shippingcharge,totalcost,warranty,delivery,payment,comments))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Quotation is added for an Item!')
	return render_to_response('templates/addquote.jinja2',{},request=request)

@view_config(route_name='submitedititem')
@is_loggedin()
def submitedititem(request):
	iditemtype=request.params['iditemtype']
	idcategory=request.params['idcategory']
	idcat=request.params['id']
	itemname=request.params['itemname']
	itemdesc=request.params['desc']
	width=request.params['width']
	depth=request.params['depth']
	height=request.params['height']
	remarks=request.params['remarks']
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql1="UPDATE `Catalog` SET `idCategory`=%s, `idItemType`=%s, `ItemName`=%s, `ItemDescription`=%s, `Width(inch)`=%s, `Depth(inch)`=%s, `Height(inch)`=%s, `Remarks`=%s where `idCatalog`=%s" 
			cursor.execute(sql1,(idcategory,iditemtype,itemname,itemdesc,width,depth,height,remarks,idcat))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Item deatils are edited and saved successfully!')
	return render_to_response('templates/edititem.jinja2',{},request=request)

@view_config(route_name='submiteditquote')
@is_loggedin()
def submiteditquote(request):
	idvenpiece=request.params['id']
	quotationex=request.params['quotationex']
	quotationin=request.params['quotationin']
	taxes=request.params['tax']
	shippingcharge=request.params['shipping']
	totalcost=request.params['cost']
	delivery=request.params['delivery']
	payment=request.params['payment']
	comments=request.params['comments']
	warranty=request.params['warranty']
	exciseduty=request.params['exciseduty']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "UPDATE `VendorPieceQuotation` SET `Quotation(Exc Taxes)`=%s, `Excise Duty`=%s,`Taxes`=%s,`Quotation(Inc Taxes)`=%s,`Shipping Charges`=%s,`Total Cost Price`=%s,`Warranty`=%s,`Delivery Time`=%s,`PaymentTerms`=%s,`Comments`=%s where `idVendorPieceQuotation`=%s" 
			cursor.execute(sql,(quotationex,exciseduty,taxes,quotationin,shippingcharge,totalcost,warranty,delivery,payment,comments,idvenpiece))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Quotations for an Item are edited and saved successfully!')
	return render_to_response('templates/editvendor.jinja2',{},request=request)

@view_config(route_name='submitaddlist')
@is_loggedin()
def submitaddlist(request):
	listname=request.params['name']
	listdesc=request.params['description']
	userid=request.params['id']

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `List` (`idUser`,`ListName`,`ListDescription`) VALUES (%s,%s,%s)"
			cursor.execute(sql,(userid,listname,listdesc))
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New List is added!')
	return render_to_response('templates/addlist.jinja2',{'id':userid},request=request)

@view_config(route_name='subviewproject')
@is_loggedin()
def subviewproject(request):
	p_name=request.params['name']
	projectname1=[]
	projectname=[]

	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT id, apartment_name, style_name, client_name from presentation_project where presentation_name=%s"
			cursor.execute(sql,(p_name))
			res=cursor.fetchall()
			p_id=res[0]['id']
			a_name=res[0]['apartment_name']
			s_name=res[0]['style_name']
			c_name=res[0]['client_name']

			sql1="SELECT presentation_name from presentation_project"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			for b in result1:
				projectname.append(b['presentation_name'])
			projectname1=[str(i) for i in projectname]
			projectname1=[x for x in projectname1 if x!='None']
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	return render_to_response('templates/viewproject.jinja2',{'p_id':p_id,'p_name':p_name,'a_name':a_name,'s_name':s_name,'c_name':c_name,'name':projectname1},request=request)

@view_config(route_name='subviewlist')
@is_loggedin()
def subviewlist(request):
	listname=request.params['listname']
	userid=request.params['id']
	ids=[]
	item=[]
	res3=[]
	images=[]
	filename=[]
	newList=[]
	
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql="SELECT idList from List where ListName=%s"
			cursor.execute(sql,(listname))
			res=cursor.fetchall()
			listid=res[0]['idList']

			sql3="SELECT ListName FROM List where idUser='%s'" %(userid)
			cursor.execute(sql3)
			result=cursor.fetchall()
			namelist=[]
			for d in result:
				namelist1=d['ListName']
				namelist.append(namelist1)
			namelist2=[str(i) for i in namelist]

			sql1="SELECT idCatalog from ListItems where idList='%s'" %(listid)
			cursor.execute(sql1)
			res1=cursor.fetchall()
			for a in res1:
				ids1=a['idCatalog']
				ids.append(ids1)
			
			for b in ids:
				sql2="SELECT c.`idCatalog`, i.`ItemTypeName`, c.`ItemName`, ca.`CategoryName`, im.`URL` FROM `ItemType` as i, `Catalog` as c, `Category` as ca, `Images` as im WHERE ca.`idCategory`=c.`idCategory` AND i.`idItemType`=c.`idItemType` AND c.`idCatalog`=im.`idCatalog` AND c.`idCatalog`='%s'" %(b)
				cursor.execute(sql2)
				res2=cursor.fetchall()
				res3.extend(res2)

			for c in res3:
				item1={'idcat':c['idCatalog'],'itemtypename':c['ItemTypeName'],'url':c['URL'] , 'itemname':c['ItemName'], 'catname':c['CategoryName']}
				item.append(item1)
				images1=[c['URL']]
				images.extend(images1)
		connection.commit()
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	return render_to_response('templates/viewlist.jinja2',{'listname':listname,'item':item,'namelist':namelist2,'userid':userid},request=request)

@view_config(route_name='download')
@is_loggedin()
def download(request):
	listname=request.params['listname']
	newList=[]
	images=[]
	listid=[]
	ids=[]
	
	s = conn.connect()
	connection=s["connection"]
	try:
		with connection.cursor() as cursor:
			sql6="SELECT idList from List where ListName=%s"
			cursor.execute(sql6,(listname))
			res=cursor.fetchall()
			listid=res[0]['idList']
	
			sql1="SELECT idCatalog from ListItems where idList='%s'" %(listid)
			cursor.execute(sql1)
			res1=cursor.fetchall()
			for a in res1:
				ids1=a['idCatalog']
				ids.append(ids1)
			for c in ids:
				sql="SELECT URL from Images where idCatalog='%s'" %(c)
				cursor.execute(sql)
				res=cursor.fetchall()
				for b in res:
					images1=[b['URL']]
					images.extend(images1)
			for i in images:
				newList.append(i.split("/")[-1])
			
			r = glob.glob(dst_dir1)
			for i in r:
				os.remove(i)
			for d in newList:
				for file in glob.iglob(os.path.join(src_dir,d)):
					shutil.copy(file,dst_dir)
		connection.commit()
		fp = tempfile.NamedTemporaryFile('w+b', dir=src_dir, delete=True)
		compression=zipfile.ZIP_DEFLATED
		zf = zipfile.ZipFile(fp, mode='w')
		for folder,subfolder,files in os.walk(dst_dir):
			for file in files:
				zf.write(os.path.join(folder, file),file,compress_type=compression)
		zf.close()
		fp.seek(0)
		response = request.response
		response.content_type = 'application/zip'
		response.app_iter = FileIter(fp)
	except Exception as e:
	    print(e)
	finally:
		connection.close()
	return response

@view_config(route_name='uploadimage')
@is_loggedin()
def uploadimage(request):
	#slide_id=request.params['id_slide']
	imagename=request.params['image'].filename
	request.storage.save(request.POST['image'])
	urlimage=request.storage.url(imagename)
	'''
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="INSERT into slide_elements (s_id,temp_url) values(%s,%s)"
			cursor.execute(sql,(slide_id,urlimage))
			sql2="SELECT URL FROM slide_elements where s_id=%s" %(slide_id)
			cursor.execute(sql2)
			result2=cursor.fetchall()
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	'''
	return render_to_response('templates/imgdisplay.html',{'url':urlimage},request=request)

@view_config(route_name='slide', renderer='json')
#@is_loggedin()
def slide(request):
	pid=request.matchdict['p_id']
	sid=request.matchdict['s_id']

	s = conn.connect()
	connection=s["connection"]
	resp_text=list()
	resp_url=list()
	slides=list()
	resp = dict(status=True,data=dict(text=resp_text,url=resp_url,slides=slides))
	try:
		with connection.cursor() as cursor:
			if int(sid):
				sql2="select p.s_id,p.pr_id,a.id,b.URL,a.temp_url,a.position_x,a.position_y,a.object_length,a.object_breadth,a.e_desc,a.e_id from Presentation p left join slide_elements a on p.s_id=a.s_id and p.flag=0 and a.flag=0 left join Images b on a.e_id=b.idCatalog where a.s_id={s_id} and p.pr_id={p_id}  order by p.s_id;".format(s_id=int(sid),p_id=int(pid))
			else:
				sql2="select p.s_id,p.pr_id,a.id,b.URL,a.temp_url,a.position_x,a.position_y,a.object_length,a.object_breadth,a.e_desc,a.e_id from Presentation p left join slide_elements a on p.s_id=a.s_id and p.flag=0 and a.flag=0 left join Images b on a.e_id=b.idCatalog where p.pr_id={p_id}  order by p.s_id;".format(p_id=int(pid))
			cursor.execute(sql2)
			res=cursor.fetchall()

		p_s_id=0
		for i in res:
			c_s_id=int(i["s_id"])
			if i["id"]:
				if (i["URL"] or i["temp_url"]):
					resp_url.append(i)
				else:
					resp_text.append(i)
			if c_s_id!=p_s_id:
				s=c_s_id
				slides.append(s)
				p_s_id=c_s_id

	except Exception as e:
		resp["status"]=False
		print(e)
	finally:
		connection.close()
	return resp