from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.response import FileIter
from pyramid.response import FileResponse
from pyramid_flash_message import MessageQueue
from pyramid.view import render_view_to_response
from pyramid.request import Request
from catalog.presentationlogic import *
import tempfile
import pymysql.cursors
import ast
import zipfile
import glob
import shutil
import os
import json
src_dir = "catalog/catalog/images"
dst_dir = "catalog/catalog/listimages"
dst_dir1 = "catalog/catalog/listimages/*"

@view_config(route_name='login',renderer='templates/login.jinja2')
def login(request):
	return {}

@view_config(route_name='submitlogin')
def submitlogin(request):
	name=request.params['uname']
	password=request.params['password']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="SELECT * FROM `User`"
			cursor.execute(sql)
			result=cursor.fetchall()
			for res in result:
				user=res['UserName']
				pwd=res['Password']
				if name==user and password==pwd:
					return render_to_response('templates/home.jinja2',{'userid':res['idUser'],'uname':res['Name']},request=request)
			else:
				return render_to_response('templates/login.jinja2',{},request=request)
		connection.commit()
	except NameError:
		print('An exception')
	finally:
		connection.close()
	return {}

@view_config(route_name='addpre')
def addpre(request):
	id1=addproject()
	return render_to_response('templates/presentation1.html',{'id':id1},request=request)

@view_config(route_name='addslide')
def add_slide(request):
	s_id=addslide(request)
	return render_to_response('templates/presentation.html',{'s_id':s_id},request=request)

@view_config(route_name='vendor',renderer='templates/vendorform.jinja2')
def vendor(request):
	return {}

@view_config(route_name='category',renderer='templates/category.jinja2')
def category(request):
	return {}

@view_config(route_name='material',renderer='templates/material.jinja2')
def material(request):
	return {}

@view_config(route_name='fabric',renderer='templates/fabric.jinja2')
def fabric(request):
	return {}

@view_config(route_name='itemtype',renderer='templates/itemtype.jinja2')
def itemtype(request):
	return {}

@view_config(route_name='createlist')
def createlist(request):
	userid=request.params['id']
	return render_to_response('templates/addlist.jinja2',{'id':userid},request=request)

@view_config(route_name='itemadded')
def itemadded(request):
	listid=request.params['idlist']
	catalogid=request.params['id']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql="INSERT INTO `ListItems` (`idList`,`idCatalog`) VALUES (%s,%s)"
			cursor.execute(sql, (listid,catalogid))
		connection.commit()
	except NameError:
		print('An exception')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Item added to List!')
	return render_to_response('templates/submitlist.jinja2',{},request=request)

@view_config(route_name='presentation',renderer='templates/presentation.html')
def itemtype(request):
	return {}

@view_config(route_name='catalog')
def catalog(request):
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
		print('An exception')
	finally:
		connection.close()

	return render_to_response('templates/catalog.jinja2',{'cat1':cat1,'item1':item1},request=request)


@view_config(route_name='quotation')
def quotation(request):
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
		print('An exception')
	finally:
		connection.close()
	return render_to_response('templates/vendorpiece.jinja2',{'ven1':ven1,'name1':name1},request=request)

@view_config(route_name='addquote')
def quotation(request):
	itemid=request.params['id']
	nameitem=request.params['name']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
		print('An exception')
	finally:
		connection.close()
	return render_to_response('templates/addquote.jinja2',{'sku':sku,'itemid':itemid,'nameitem':nameitem,'ven1':ven1},request=request)

@view_config(route_name='itemfetch')
def itemfetch(request):
	userid=request.params['id']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
			typename1.append('Reset')

			sql2="SELECT * from `Category`"
			cursor.execute(sql2)
			res2=cursor.fetchall()
			for c in res2:
				catname.append(c['CategoryName'])
			catname1=[str(i) for i in catname]
			catname1.append('Reset')
		connection.commit()
	except NameError:
			print('An exception')
	finally:
		connection.close()
	return render_to_response('templates/itemfetch.jinja2',{'userid':userid,'item':item,'typename':typename1,'catname':catname1},request=request)

@view_config(route_name='itemdetails')
def itemdetails(request):
	idcat=request.params['id']
	userid=request.params['userid']
	listname=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
		print('An exception')
	finally:
		connection.close()
	return render_to_response('templates/itemdetailsnew.jinja2',{'userid':userid,'details':details,'detail':detail,'listname':listname},request=request)

@view_config(route_name='editdetails')
def editdetails(request):
	details=request.params['det']
	details1 = ast.literal_eval(details)
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
			print('An exception')
	finally:
		connection.close()
	return render_to_response('templates/edititem.jinja2',{'details1':details1,'typename':typename1,'catname':catname1},request=request)

@view_config(route_name='vendoredit')
def vendoredit(request):
	details=request.params['det']
	details1 = ast.literal_eval(details)
	return render_to_response('templates/editvendor.jinja2',{'details1':details1},request=request)

@view_config(route_name='search')
def search(request):
	ids=[]
	item4=[]
	res2=[]
	search=request.params['search']
	words=search.split()
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	finally:
		connection.close()
	return render_to_response('templates/itemfetch.jinja2',{'item':item4},request=request)

@view_config(route_name='viewlist')
def viewlist(request):
	userid=request.params['id']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
		print('An exception')
	finally:
		connection.close()
	return render_to_response('templates/viewlist.jinja2',{'namelist':namelist2,'userid':userid},request=request)

@view_config(route_name='filter')
def filter(request):
	itemname=request.params['iditem']
	catname1=request.params['idcat']
	typename=[]
	catname=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql1="SELECT * from `ItemType`"
			cursor.execute(sql1)
			result1=cursor.fetchall()
			for b in result1:
				typename.append(b['ItemTypeName'])
			typename1=[str(i) for i in typename]
			typename1.append('Reset')

			sql2="SELECT * from `Category`"
			cursor.execute(sql2)
			res2=cursor.fetchall()
			for c in res2:
				catname.append(c['CategoryName'])
			catname2=[str(i) for i in catname]
			catname2.append('Reset')
		connection.commit()
	except NameError:
		print('An exception')
	finally:
		connection.close()

	if((itemname!="") and (itemname!="Reset") and (catname1=="")):
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql1="SELECT `idItemType` FROM `ItemType` WHERE `ItemTypeName`='%s'" %(itemname)
				cursor.execute(sql1)
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
		except NameError:
			print('An exception')
		finally:
			connection.close()
		return render_to_response('templates/itemfetch.jinja2',{'itemname':itemname,'item':item,'typename':typename1,'catname':catname2},request=request)
		
	elif((catname1!="") and (catname1!="Reset") and (itemname=="")):
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql1="SELECT `idCategory` FROM `Category` WHERE `CategoryName`='%s'" %(catname1)
				cursor.execute(sql1)
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
		except NameError:
			print('An exception')
		finally:
			connection.close()
		return render_to_response('templates/itemfetch.jinja2',{'catname1':catname1,'item':item,'typename':typename1,'catname':catname2},request=request)

	elif((catname1!="") and (itemname!="")):
		connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql1="SELECT `idItemType` FROM `ItemType` WHERE `ItemTypeName`='%s'" %(itemname)
				cursor.execute(sql1)
				res1=cursor.fetchall()
				iditem=res1[0]['idItemType']

				sql2="SELECT `idCategory` FROM `Category` WHERE `CategoryName`='%s'" %(catname1)
				cursor.execute(sql2)
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
		except NameError:
			print('An exception')
		finally:
			connection.close()
		return render_to_response('templates/itemfetch.jinja2',{'itemname':itemname,'catname1':catname1,'item':item,'typename':typename1,'catname':catname2},request=request)

	elif((itemname == "Reset") or (catname1 == "Reset")):
		return render_to_response('templates/itemfetch.jinja2',{},request=request)

	else:
		return render_to_response('templates/itemfetch.jinja2',{},request=request)

@view_config(route_name='submit')
def vendorsubmit(request):
	name=request.params['name']
	address=request.params['address']
	contactno=request.params['contactno']
	
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Vendor` (`Name`, `Address`,`Contact_No`) VALUES (%s, %s, %s)"
			cursor.execute(sql, (name,address,contactno))
		connection.commit()
	except NameError:
		print('An exception')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Vendor is added!')
	return render_to_response('templates/vendorform.jinja2',{},request=request)

@view_config(route_name='submitcat')
def submitcat(request):
	catname=request.params['name']
	desc=request.params['description']

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Category` (`CategoryName`,`CategoryDescription`) VALUES (%s,%s)"
			cursor.execute(sql, (catname,desc))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Category is added!')
	return render_to_response('templates/category.jinja2',{},request=request)

@view_config(route_name='submitcatalog')
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

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Item is added!')
	return render_to_response('templates/catalog.jinja2',{},request=request)

@view_config(route_name='submitmat')
def submitmat(request):
	name=request.params['name']
	quantity=request.params['quantity']

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Material` (`Name`,`Quantity`) VALUES (%s)"
			cursor.execute(sql, (name,quantity))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Material is added!')
	return render_to_response('templates/material.jinja2',{},request=request)

@view_config(route_name='submitfab')
def submitfab(request):
	length=request.params['len']
	fabtype=request.params['type']
	cost=request.params['cost']
	code=request.params['code']

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `Fabric` (`Length(metre)`,`Type`,`Cost/metre`,`Fabric Code`) VALUES (%s,%s,%s,%s)"
			cursor.execute(sql, (length,fabtype,cost,code))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New Fabric is added!')
	return render_to_response('templates/fabric.jinja2',{},request=request)

@view_config(route_name='submititem')
def submititem(request):
	typename=request.params['typename']
	typedesc=request.params['typedesc']

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `ItemType` (`ItemTypeName`,`ItemTypeDescription`) VALUES (%s,%s)"
			cursor.execute(sql, (typename,typedesc))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Item Type is added!')
	return render_to_response('templates/itemtype.jinja2',{},request=request)

@view_config(route_name='submitquot')
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

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `VendorPieceQuotation` (`idVendor`,`idCatalog`,`Quotation(Exc Taxes)`,`Excise Duty`,`Taxes`,`Quotation(Inc Taxes)`,`Shipping Charges`,`Total Cost Price`,`Warranty`,`Delivery Time`,`PaymentTerms`,`Comments`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql, (idven,idcat2,quotationex,exciseduty,taxes,quotationin,shippingcharge,totalcost,warranty,delivery,payment,comments))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Quotation is added for an Item!')
	return render_to_response('templates/vendorpiece.jinja2',{},request=request)

@view_config(route_name='submitaddquote')
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

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `VendorPieceQuotation` (`idVendor`,`idCatalog`,`Quotation(Exc Taxes)`,`Excise Duty`,`Taxes`,`Quotation(Inc Taxes)`,`Shipping Charges`,`Total Cost Price`,`Warranty`,`Delivery Time`,`PaymentTerms`,`Comments`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql, (idven,idcat2,quotationex,exciseduty,taxes,quotationin,shippingcharge,totalcost,warranty,delivery,payment,comments))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Quotation is added for an Item!')
	return render_to_response('templates/addquote.jinja2',{},request=request)

@view_config(route_name='submitedititem')
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
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql1="UPDATE `Catalog` SET `idCategory`=%s, `idItemType`=%s, `ItemName`=%s, `ItemDescription`=%s, `Width(inch)`=%s, `Depth(inch)`=%s, `Height(inch)`=%s, `Remarks`=%s where `idCatalog`=%s" 
			cursor.execute(sql1,(idcategory,iditemtype,itemname,itemdesc,width,depth,height,remarks,idcat))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Item deatils are edited and saved successfully!')
	return render_to_response('templates/edititem.jinja2',{},request=request)

@view_config(route_name='submiteditquote')
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

	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

	try:
		with connection.cursor() as cursor:
			sql = "UPDATE `VendorPieceQuotation` SET `Quotation(Exc Taxes)`=%s, `Excise Duty`=%s,`Taxes`=%s,`Quotation(Inc Taxes)`=%s,`Shipping Charges`=%s,`Total Cost Price`=%s,`Warranty`=%s,`Delivery Time`=%s,`PaymentTerms`=%s,`Comments`=%s where `idVendorPieceQuotation`=%s" 
			cursor.execute(sql,(quotationex,exciseduty,taxes,quotationin,shippingcharge,totalcost,warranty,delivery,payment,comments,idvenpiece))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('Quotations for an Item are edited and saved successfully!')
	return render_to_response('templates/editvendor.jinja2',{},request=request)

@view_config(route_name='submitaddlist')
def submitaddlist(request):
	listname=request.params['name']
	listdesc=request.params['description']
	userid=request.params['id']
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `List` (`idUser`,`ListName`,`ListDescription`) VALUES (%s,%s,%s)"
			cursor.execute(sql,(userid,listname,listdesc))
		connection.commit()
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	request.session.pop_flash()
	request.flash_message.add('New List is added!')
	return render_to_response('templates/addlist.jinja2',{'id':userid},request=request)

@view_config(route_name='subviewlist')
def subviewlist(request):
	listname=request.params['listname']
	userid=request.params['id']
	ids=[]
	item=[]
	res3=[]
	images=[]
	filename=[]
	newList=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	return render_to_response('templates/viewlist.jinja2',{'listname':listname,'item':item,'namelist':namelist2,'userid':userid},request=request)

@view_config(route_name='download')
def download(request):
	listname=request.params['listname']
	newList=[]
	images=[]
	listid=[]
	ids=[]
	connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='Pieces',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
			src_dir = "/home/rithik/catalog/catalog/images"
			dst_dir = "/home/rithik/catalog/catalog/listimages"
			dst_dir1 = "/home/rithik/catalog/catalog/listimages/*"
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
		for folder,subfolder,files in os.walk('/home/rithik/catalog/catalog/listimages'):
			for file in files:
				zf.write(os.path.join(folder, file),file,compress_type=compression)
		zf.close()
		fp.seek(0)
		response = request.response
		response.content_type = 'application/zip'
		response.app_iter = FileIter(fp)
	except NameError:
	    print('An exception flew by!')
	finally:
		connection.close()
	return response

@view_config(route_name='uploadimage')
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