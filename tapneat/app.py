import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from collections import namedtuple
from .model.model import *
from sqlalchemy import desc
from datetime import datetime, timedelta
import dateparser
from .model.schema import *
import base64
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/tapneat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)

@socketio.on('connect')
def handleConnect():
	now = datetime.now()
	dow = calendar.day_name[now.weekday()]
	print(dow)
	for mitem in MenuItem.query.order_by(MenuItem.itemName).all():
		
		
		mresult = MenuItemSchema.dump(mitem).data
		#print(mresult['itemImage'])
		emit('get menu', mresult, broadcast=False)
	
	for pd in promo_discount.query.all():
		if pd.promoId > 4:
			if now >= pd.promoStart and now <= pd.promoEnd:
				if pd.promoDuration !=2:
					pdresult = PromoDiscountSchema.dump(pd).data
					emit('promomob', pdresult, broadcast=False)
				else:
					if dow == pd.promoDay:
						pdresult = PromoDiscountSchema.dump(pd).data
						emit('promomob', pdresult, broadcast=False)
			elif now > pd.promoEnd:
				l = Log()
				l.lDesc = pd.promoName + " has expired action reqcuired"
				l.log_date = now

				db.session.add(l)
				db.session.commit()

	for l in Log.query.order_by(desc(Log.log_date)).all():
		mresult =LogSchema.dump(l).data
		# print(str(mresult))
		emit('get logs', mresult, broadcast=False)

	for sr in SalesReport.query.all():
		mresult = SalesReportSchema.dump(sr).data
		#print(mresult['itemImage'])
		emit('get sales', mresult, broadcast=False)
	for sr in StatisticalReport.query.all():
		mresult = StatisticalReportSchema.dump(sr).data
		#print(mresult['itemImage'])
		emit('get stat', mresult, broadcast=False)

	for otype in OrderType.query.all():
		oresult = OrderTypeSchema.dump(otype).data
		#print(mresult['itemImage'])
		emit('get otype', oresult, broadcast=False)

	for ctype in CustomerType.query.all():
		cresult = CustomerTypeSchema.dump(ctype).data
		#print(mresult['itemImage'])
		emit('get ctype', cresult, broadcast=False)

	for trans in OrderTransaction.query.join(OrderTransaction.orderstat).filter_by(osId=1).all():
		result = OrderTransactionSchema.dump(trans).data
		emit('new orders', result, broadcast=False)
		
	for pd in promo_discount.query.all():
	 	pdresult = PromoDiscountSchema.dump(pd).data
	 	emit('get promo', pdresult, broadcast=False)


	for pt in PromoDiscountType.query.all():
	 	ptresult = PromoTypeSchema.dump(pt).data
		#print(str(ptresult))
	 	emit('get promotype', ptresult, broadcast=False)


	for sr in Specreq.query.all():
		sresult = SpecreqSchema.dump(sr).data
		emit('get sr', sresult, broadcast=False)

	for rt in reqtype.query.all():
		rresult = RequestTypeSchema.dump(rt).data
		emit('get rt', rresult, broadcast=False)
		
	for mc in menu_category.query.all():
		menucat = MenuCategorySchema.dump(mc).data
		# print(str(menucat));
		emit('get menucat', menucat, broadcast=False)

	for trans in OrderTransaction.query.join(OrderTransaction.orderstat).filter_by(osId=2).order_by(OrderTransaction.date_time_cleared).all():
		if trans.date_time_cleared != None:
			result = OrderTransactionSchema.dump(trans).data
			emit('report order', result, broadcast=False)

	settings = GeneralSettings.query.first()
	delcost = settings.delivery
	numoftables = settings.numOfTables
	resname = settings.businessName
	sttngs = GeneralSettingsSchema.dump(settings).data
	emit('general settings', sttngs, broadcast=False)
	emit('get tablenum', {"numoftables": numoftables}, broadcast=False)
	emit('get name', {"bname": resname}, broadcast=False)
	emit('deliverycost', {"delCost": delcost}, broadcast=False)

	for trans in OrderTransaction.query.filter_by(date_time_cleared=None).all():
		result = OrderTransactionSchema.dump(trans).data
		emit('all orders', result, broadcast=False)
	for usr in Users.query.all():
		u = UsersSchema.dump(usr).data
		emit('all accounts', u, broadcast=False)
	for lvl in AccessLvl.query.all():
		level = AccessLvlSchema.dump(lvl).data
		emit('get alvl', level, broadcast=False)


@socketio.on('log')
def handelLog(loginfo):
	print(str(loginfo))
	log = Log()
	log.lDesc = loginfo['lInfo']
	d = dateparser.parse(loginfo['ldate'])
	log.log_date = d
	db.session.add(log)
	db.session.commit()

	lg = LogSchema.dump(log).data
	emit('get logs', lg, broadcast=True)

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send( msg, broadcast=True)

"""
Start of Kitchen functions
"""
@socketio.on('clear')
def handleClear(clr):
	ti = OrderTransaction.query.filter_by(otId=clr['transId']).first()
	ti.ordStatId= 2;
	for ol in OrderList.query.join(OrderList.order_transaction).filter_by(otId=ti.otId).all():
		ol.clearStatus = 'Cleared'
	db.session.commit()



@socketio.on('flag')
def handleFlag(flg):
	print('Flagging dish item unavailable: ' + str(flg))
	for i in flg:
		print(i)
		mi = MenuItem.query.filter_by(itemId=i).first()
		mi.itemStatusId = 2
		db.session.commit()
		mresult = MenuItemSchema.dump(mi).data
		emit('get menu', mresult, broadcast=True)
	emit('get mupdate', flg, broadcast=True)


@socketio.on('unflag')
def handleFlag(unflg):
	print('Flagging dish item available: ' + str(unflg))
	for i in unflg:
		print(i)
		mi = MenuItem.query.filter_by(itemId=i).first()
		mi.itemStatusId = 1
		db.session.commit()
		mresult = MenuItemSchema.dump(mi).data
		emit('get menu', mresult, broadcast=True)
	emit('get mupdate', unflg, broadcast=True)
	

@socketio.on('order')
def handleOrder(ordr):
	print("Recieved"+ str(ordr))
	same = False
	if ordr['otId'] != '':
		for x in OrderTransaction.query.all():
			if x.otId == ordr['otId']:
				print(str(x.otId))
				x.ordStatId = ordr['orderstat']
				x.cost = x.cost + ordr['totalcost']
				for l in ordr['orderlist']:
					ol = OrderList()
					ol.order_transaction = x
					mi = MenuItem.query.filter_by(itemId=l['menu_item']).first()
					#mi = MenuItem.query.get(l['itemid'])
					ol.menu_item = mi
					ol.qty = l['qty']
					#sp = Specreq.query.filter_by(srId=l['specreq']).first()
					ol.special_request_id = l['specreq']
					ol.request_type_id = l['reqtype']
					ol.activated = l['activated']
					ol.clearStatus = 'Pending'
					db.session.add(ol)
					
				db.session.commit()
				same = True
				res = OrderTransactionSchema.dump(x)
				errors = res.errors
				order_json = res.data
				emit('new orders', order_json, broadcast=True)
				emit('all orders', order_json, broadcast=True)
				emit('singleorder', order_json, broadcast=False)
				print('Order sent')
	else:
		#if same == False:
		print('I was here')
		trans = OrderTransaction()
		dt_sent = dateparser.parse(ordr['datesent'])
		trans.date_time_sent = dt_sent
		trans.ordQtId = ordr ['orderqueue']
		trans.ordtId = ordr ['ordertype']
		if int(ordr['ordertype']) >= 2 :
			trans.table_number = None
		else:
			trans.number_of_guests = ordr['numofguest']
			trans.table_number = ordr['tablenum']
		trans.ctId = ordr ['custype']
		trans.ordStatId = ordr ['orderstat']
		trans.pId = ordr ['promo']
		trans.settingsId = ordr ['settings']
		if int(ordr['ordertype']) == 3:
			dc =  GeneralSettings.query.first()
			trans.cost = ordr['totalcost'] + dc.delivery
		else:
			trans.cost = ordr['totalcost']
		trans.uId = ordr['userid']
		for l in ordr['orderlist']:
			#print(int(l['specreq']))
			ol = OrderList()
			ol.order_transaction = trans
			mi = MenuItem.query.filter_by(itemId=l['menu_item']).first()
				#mi = MenuItem.query.get(l['itemid'])
			ol.menu_item = mi
			ol.qty = l['qty']
			#sp = Specreq.query.filter_by(srId=l['specreq']).first()
			ol.special_request_id = l['specreq']
			ol.request_type_id = l['reqtype']
			ol.activated = l['activated']
			ol.clearStatus = 'Pending'
			db.session.add(ol)

		db.session.add(trans)
		db.session.commit()
		res = OrderTransactionSchema.dump(trans)
		errors = res.errors
		order_json = res.data
		emit('new orders', order_json, broadcast=True)
		emit('all orders', order_json, broadcast=True)
		emit('singleorder', order_json, broadcast=False)
		#print(str(order_json['otid']))
	# emit('order accepted', order_json, broadcast=True)

"""
End of kitchen function
"""

"""
cashier
"""
"""
login cashier
"""
@socketio.on('login')
def handleLogin(details):
	access = False
	multisession = False
	usrnm = ""
	print("User" + str(details))
	if details['username'] != "":
		usr = Users.query.filter_by(username = details['username']).first()
		
		if usr != None:
			if usr.userpass == details['password'] and usr.uAccesslvl == 2 and usr.isLoggedIn == 0:
				access = True
				usr.isLoggedIn = 1
				db.session.commit()
				usrnm = usr.username
			elif details['password'] == 'forcelogout':
				usr.isLoggedIn = 0
				db.session.commit()	
			elif usr.userpass == details['password'] and usr.uAccesslvl == 2 and usr.isLoggedIn == 1:
				multisession = True
	emit('grant access', {'grantaccess': access, 'username': usrnm, 'multisession': multisession})
			


@socketio.on('confirm')
def handleClear(cnfrm):
	print(str(cnfrm))
	ti = OrderTransaction.query.filter_by(otId=cnfrm['transId']).first()
	dt_clear = dateparser.parse(cnfrm['dateclear'])
	ti.date_time_cleared = dt_clear
	db.session.commit()
"""
end
"""
@socketio.on('statistical')
def handleRequest(stat):
	print(str(stat))
	
"""
Mobile
"""
@socketio.on('reqbill')
def handleRequest(req):
	print(str(req))
	emit('billrequest', req, broadcast=True)

@socketio.on('cancel')
def handleCancel(cncl):
	print(str(cncl))
	ti = OrderTransaction.query.filter_by(otId=cncl['otid']).first()
	dt_clear = dateparser.parse(cncl['dateclear'])
	ti.date_time_cleared = dt_clear
	ti.ordStatId= 3
	db.session.commit()
	res = OrderTransactionSchema.dump(ti)
	errors = res.errors
	order_json = res.data
	emit('new orders', order_json, broadcast=True)
	emit('all orders', order_json, broadcast=True)
	emit('cancelorders', cncl, broadcast=True)

@socketio.on('cancelone')
def handleCancelOne(cnclone):
	print("hey"+ str(cnclone))
	ol = OrderList.query.filter_by(olId=cnclone['olId']).first()
	
	ti = OrderTransaction.query.filter_by(otId=cnclone['otId']).first()
	ti.cost = cnclone['newcost']
	
	db.session.delete(ol)
	db.session.commit()
	
	res = OrderTransactionSchema.dump(ti)
	errors = res.errors
	order_json = res.data
	emit('new orders', order_json, broadcast=True)
	emit('all orders', order_json, broadcast=True)
	# emit('singleorder', order_json, broadcast=False)
	
"""
End
"""
"""
Manager Things
"""
"""
Add Accounts
"""
@socketio.on('addaccount')
def handleAddAccount(info):
	print(info['upass'])
	acc = Users()
	acc.ufname = info['fn']
	acc.umname = info['mn']
	acc.ulname = info['ln']
	acc.username = info['username']
	acc.userpass = info['upass']
	acc.uAccesslvl = info['lvl']
	acc.isLoggedIn = 0

	db.session.add(acc)
	db.session.commit()
	
	ac = UsersSchema.dump(acc)
	errors = ac.errors
	newaccount = ac.data
	emit('all accounts', newaccount, broadcast=True)

@socketio.on('additem')
def handleMenuItem(newitem):
	print('xb'+str(newitem))
	item = MenuItem()
	item.itemName = newitem['itemName']
	image = base64.b64decode(newitem['itemImage'])
	item.itemImage = image
	pr = promo_discount.query.filter_by(promoId=newitem['itemPromoId']).first()
	if int(newitem['itemPromoId']) != 1:
		item.itemDesc = newitem['itemDesc']
	else:
		item.itemDesc = newitem['itemDesc']+" plus "+pr.promoDesc

	
	item.itemPrice = newitem['itemPrice']

	item.itemMenuCatId = newitem['itemMenuCatId']
	item.itemStatusId = newitem['itemStatusId']
	item.itemPromoId = newitem['itemPromoId']
	for s in newitem['specreq']:
		spec = Specreq()
		spec.srDesc = s['srDesc']
		spec.menuId  = item
		spec.srPrice = s['srPrice']
		db.session.add(spec)
		print(str(s))

	db.session.add(item)
	db.session.commit()
	
	ac = MenuItemSchema.dump(item)
	errors = ac.errors
	newaccount = ac.data
	emit('get menu', newaccount, broadcast=True)
	for s in Specreq.query.all():
		sr = SpecreqSchema.dump(s).data
		emit('get sr', sr, broadcast=True)

@socketio.on('updateitem')
def handleMenuItem(newitem):
	print(str(newitem))
	item = MenuItem.query.filter_by(itemId=newitem['itemId']).first()
	item.itemName = newitem['itemName']
	pr = promo_discount.query.filter_by(promoId=newitem['itemPromoId']).first()
	if int(newitem['itemPromoId']) == 1:
		item.itemDesc = newitem['itemDesc']
	elif int(newitem['itemPromoId']) == item.itemPromoId:
		item.itemDesc = newitem['itemDesc']
	else:
		item.itemDesc = newitem['itemDesc']+" plus "+pr.promoDesc
	#newprice = (1 -promoval)oldprice

	item.itemPrice = newitem['itemPrice']

	item.itemMenuCatId = newitem['itemMenuCatId']
	item.itemStatusId = newitem['itemStatusId']
	item.itemPromoId = newitem['itemPromoId']
	for s in newitem['specreq']:
		if s['srDesc'] != '':
			spec = Specreq.query.filter_by(srId=s['srId']).first()
			spec.srDesc = s['srDesc']
			spec.menuId  = item
			spec.srPrice = s['srPrice']
		else:
			spec = Specreq.query.filter_by(srId=s['srId']).first()
			db.session.delete(spec)

	#db.session.add(item)
	db.session.commit()
	
	ac = MenuItemSchema.dump(item)
	errors = ac.errors
	newaccount = ac.data
	emit('get menu', newaccount, broadcast=True)
@socketio.on('deleteitem')
def handleDeleteItem(delitem):
	print(str(delitem))
	item = MenuItem.query.filter_by(itemName=delitem['itemId']).first()

	db.session.delete(item)
	db.session.commit()

	for m in MenuItem.query.all():
		mi = MenuItemSchema.dump(m).data
		emit('get menu', mi, broadcast=True)

@socketio.on('deletecat')
def handleDeleteItem(delitem):
	print(str(delitem))
	item = menu_category.query.filter_by(mcId=delitem['itemId']).first()

	db.session.delete(item)
	db.session.commit()

	for m in menu_category.query.all():
		mi = MenuCategorySchema.dump(m).data
		print(str(mi))
		emit('get menucat', mi, broadcast=True)

@socketio.on('addmenucategory')
def handleMenuItem(cat):
	print(str(cat))
	for m in cat['mcNames']: 
	
		c = menu_category()
		c.mcName = m
		db.session.add(c)
	db.session.commit()
	
	for m in menu_category.query.all():
		mi = MenuCategorySchema.dump(m).data
		emit('get menucat', mi, broadcast=True)

@socketio.on('savesales')
def handleSaveSales(sales):
	print(str(sales))

	s = SalesReport()
	ds = dateparser.parse(sales['generate_date_start'])
	s.generate_date_start = ds
	de = dateparser.parse(sales['generate_date_end'])
	s.generate_date_end = de
	dd = dateparser.parse(sales['date_created'])
	s.date_created = dd
	s.users_id = sales['uId']

	db.session.add(s)
	db.session.commit()

	ac = SalesReportSchema.dump(s)
	errors = ac.errors
	sal = ac.data
	emit('get sales', sal, broadcast=True)

@socketio.on('saveStat')
def handleSaveStat(stat):
	print(str(stat))

	sr = StatisticalReport()
	ds = dateparser.parse(stat['generate_date_start'])
	sr.generate_date_start = ds
	de = dateparser.parse(stat['generate_date_end'])
	sr.generate_date_end = de
	dd = dateparser.parse(stat['date_created'])
	sr.date_created = dd
	sr.users_id = stat['uId']
	print(str(stat['customerCount']))
	for c in stat['customerCount']:
		cc = CustomerCount()
		cc.statId = sr
		cc.value = 5
		cc.date = dd
		db.session.add(cc)
	for frqnt in stat['frequent']:
		fd = FrequentOrdered()
		fd.statId = sr
		fd.value = 12
		fd.menu_items_id = 12
		fd.date=dd
		db.session.add(fd)

	db.session.add(sr)
	db.session.commit()

	ac = StatisticalReportSchema.dump(sr)
	errors = ac.errors
	sal = ac.data
	emit('get stat', sal, broadcast=True)

"""
Update Setting
"""
@socketio.on('updatesettings')
def handleUpdateSettings(settings):
	print(str(settings))
	old = GeneralSettings.query.first()
	old.businessName = settings['bname']
	old.bHoursStart = settings['bstarttime']
	old.bHoursEnd = settings['bendtime']
	old.bDayStart = settings['bstartday']
	old.bDayEnd = settings['bendday']
	old.menuUpdate = settings['menutime']
	old.delivery = settings['delivery']
	old.numOfTables = settings['numoftables']

	db.session.commit()

	newsettings = GeneralSettingsSchema.dump(old)
	errors = newsettings.errors
	nsettings = newsettings.data
	emit('general settings', nsettings, broadcast=True)

"""
Update Account
"""
@socketio.on('updateaccount')
def handleUpdateAccount(account):
	print(str(account))
	acc = Users.query.filter_by(uId=account['uId']).first()
	if account['action'] == 'updateinfo':
		acc.ufname = account['fn']
		acc.umname = account['mn']
		acc.ulname = account['ln']
		
	elif account['action'] == 'remove':
		db.session.delete(acc)

	elif account['action'] == 'changepass':
		acc.userpass = account['upass']


	db.session.commit()

	for u in Users.query.all():
		usr = UsersSchema.dump(u).data
		emit('all accounts', usr, broadcast=False)

"""
Add Promo
"""
@socketio.on('createpromo')
def handleCreatePromo(newpromo):
	print('new promo', str(newpromo))
	
	promo = promo_discount()
	promo.promoName = newpromo['promoName']
	promo.promoDesc = newpromo['promoDesc']
	promo.promoType = int(newpromo['promoType'])
	val = float(int(newpromo['promoVal'])/100)
	promo.promoVal = val
	promo.promoDuration = newpromo['promoDuration']
	promo.promoDay = newpromo['promoDay']
	if newpromo['promoStart'] != None and newpromo['promoEnd'] != None:
		promo.promoStart = dateparser.parse(newpromo['promoStart'])
		promo.promoEnd = dateparser.parse(newpromo['promoEnd'])
	else:
		promo.promoStart = newpromo['promoStart']
		promo.promoEnd = newpromo['promoEnd']
	db.session.add(promo)
	db.session.commit()

	ac = PromoDiscountSchema.dump(promo)
	errors = ac.errors
	promo = ac.data
	print(str(promo))
	emit('get promo', promo, broadcast=True)

@socketio.on('updatepromo')
def handleUpdatePromo(upromo):
	print('promo', str(upromo))
	
	promo = promo_discount.query.filter_by(promoId=upromo['promoId']).first()
	promo.promoName = upromo['promoName']
	promo.promoDesc = upromo['promoDesc']
	promo.promoType = upromo['promoType']
	val = float(int(upromo['promoVal'])/100)
	promo.promoVal = val
	promo.promoDuration = upromo['promoDuration']
	promo.promoDay = upromo['promoDay']
	if upromo['promoStart'] != None and upromo['promoEnd'] != None:
		promo.promoStart = dateparser.parse(upromo['promoStart'])
		promo.promoEnd = dateparser.parse(upromo['promoEnd'])
	else:
		promo.promoStart = upromo['promoStart']
		promo.promoEnd = upromo['promoEnd']
	
	db.session.commit()

	ac = PromoDiscountSchema.dump(promo)
	errors = ac.errors
	promo = ac.data
	print(str(promo))
	emit('get promo', promo, broadcast=True)

@socketio.on('deletepromo')
def handleDeletePromo(pr):
	promo = promo_discount.query.filter_by(promoId=pr['promoId']).first()

	db.session.delete(promo)
	db.session.commit()

	for p in promo_discount.query.all():
		prom = PromoDiscountSchema.dump(p).data
		emit('get promo', prom, broadcast=True)

"""
login manager
"""
@socketio.on('managerlogin')
def handleLogin(mdetails):
	access = False
	multisession = False
	usrnm = ""
	print("User" + str(mdetails))
	if mdetails['username'] != "":
		usr = Users.query.filter_by(username = mdetails['username']).first()
		
		if usr != None:
			if usr.userpass == mdetails['password'] and usr.uAccesslvl == 1 and usr.isLoggedIn == 0:
				access = True
				usr.isLoggedIn = 1
				db.session.commit()
				usrnm = usr.username
			elif mdetails['password'] == 'forcelogout':
				usr.isLoggedIn = 0
				db.session.commit()
			elif usr.userpass == mdetails['password'] and usr.uAccesslvl == 1 and usr.isLoggedIn == 1:
				multisession = True

						
	emit('grant access', {'grantaccess': access, 'username': usrnm, 'multisession': multisession})
"""
end of login
"""


"""
end of Manager
"""
"""
logout all
"""
@socketio.on('logout')
def handleLogout(usrname):
	# access = False
	print("User" + usrname)
	if usrname != "":
		usr = Users.query.filter_by(username = usrname).first()
		
		if usr != None:
			if usr.isLoggedIn == 1:
				usr.isLoggedIn = 0
				db.session.commit()
				u = UsersSchema.dump(usr).data
				emit('all accounts', u, broadcast=True)

	
				
"""
end of logout
"""
@socketio.on('updateordercost')
def handleUpdateOrderCost(update):
	print(str(update))
	order = OrderTransaction.query.filter_by(otId=update['orderId']).first()
	order.cost = update['newcost']
	db.session.commit()

	ordr = OrderTransactionSchema.dump(order).data
	emit('all orders', ordr, broadcast=True)