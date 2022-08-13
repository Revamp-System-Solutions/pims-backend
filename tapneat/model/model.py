from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.dialects.mysql import \
		BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
		DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
		LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
		NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
		TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

db = SQLAlchemy()

class Log(db.Model):
	__tablename__= 'logs'
	lId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	lDesc = db.Column('log_info', db.String(500))
	log_date = db.Column(DateTime(timezone=True), nullable=False)

class menu_category(db.Model):
	__tablename__ = 'menu_category'
	mcId  = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	mcName = db.Column('name', db.String(45))

class menu_item_status(db.Model):
	__tablename__ = 'menu_item_status'
	misId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	misDesc = db.Column('description', db.String(15))

class MenuItem(db.Model):
	__tablename__ = 'menu_items'
	itemId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	itemName = db.Column('name', db.String(45))
	itemImage = db.Column('image', db.LargeBinary(length=(2**32)-1))
	itemDesc = db.Column('description', db.String(500))
	itemPrice = db.Column('price', db.Float)
	itemMenuCatId = db.Column(db.Integer, db.ForeignKey('menu_category.id'))
	itemStatusId = db.Column(db.Integer, db.ForeignKey('menu_item_status.id'))
	itemPromoId = db.Column(db.Integer, db.ForeignKey('promo_discount.id'))
	promo_discount = db.relationship('promo_discount', backref='menu_items')
	item_status = db.relationship('menu_item_status', backref='menu_items')
	item_category = db.relationship('menu_category', backref='menu_items')

class Specreq(db.Model):
	__tablename__ = 'special_request'
	srId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	srDesc = db.Column('description', db.String(45))
	menu_items_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
	menuId = db.relationship('MenuItem', backref='special_request')
	srPrice = db.Column('price', db.Float)


class reqtype(db.Model):
	__tablename__ = 'request_type'
	rtId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	rtDesc = db.Column('definition', db.String(15))

class promo_discount(db.Model):
	__tablename__ = 'promo_discount'
	promoId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	promoName = db.Column('name', db.String(45))
	promoDesc = db.Column('description', db.String(150))
	promoType = db.Column(db.Integer,db.ForeignKey('promo_discount_type.id'))
	promoVal = db.Column('value', db.Float)
	promoDuration = db.Column(db.Integer,db.ForeignKey('duration_type.id'))
	promoDay = db.Column('day_of_the_week', db.String(45))
	promoStart = db.Column('date_started',DateTime(timezone=True), nullable=True)
	promoEnd = db.Column('expiry_date', DateTime(timezone=True), nullable=True)
	pdId = db.relationship('PromoDiscountType', backref='promo_discount')
	dtId = db.relationship('DurationType', backref='promo_discount')
class PromoDiscountType(db.Model):
	__tablename__ = 'promo_discount_type'
	pdId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	pdname = db.Column('name', db.String(45))

class DurationType(db.Model):
	__tablename__ = 'duration_type'
	dtId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	pdName = db.Column('name', db.String(45))


class OrderTransaction(db.Model):
	__tablename__ = "order_transactions"
	otId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	date_time_sent = db.Column(DateTime(timezone=True), nullable=False)
	ordQtId = db.Column('order_queue_type_id', db.Integer, db.ForeignKey('order_queue_type.id'))
	ordtId = db.Column('order_type_id', db.Integer, db.ForeignKey('order_type.id'))
	number_of_guests = db.Column(db.Integer)
	table_number = db.Column(db.Integer)
	ctId = db.Column('customer_type_id', db.Integer, db.ForeignKey('customer_type.id'))
	ordStatId = db.Column('order_status_id', db.Integer, db.ForeignKey('order_status.id'))
	pId = db.Column('promo_discount_id', db.Integer, db.ForeignKey('promo_discount.id'))
	settingsId = db.Column('general_settings_id', db.Integer, db.ForeignKey('general_settings.id'))
	cost = db.Column('total_cost', db.Float)
	uId = db.Column('users_id',db.Integer, db.ForeignKey('users.id'))
	date_time_cleared = db.Column(DateTime(timezone=True), nullable=True)
	order_type = relationship('OrderType', backref='order_type')
	order_queue_type = relationship('OrderQueueType', backref='order_queue_type')
	customer_type = relationship('CustomerType', backref='customer_type')
	orderstat = relationship('OrderStatus', backref='order_status')
	pd = relationship('promo_discount', backref='promo_discount')
	gs = relationship('GeneralSettings', backref='general_settings')

class CustomerType(db.Model):
	__tablename__ = 'customer_type'
	cId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	ctName = db.Column('name', db.String(45))

class OrderType(db.Model):
	__tablename__ = 'order_type'
	oTypeId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	otName = db.Column('type_name', db.String(45))

class OrderQueueType(db.Model):
	__tablename__ = 'order_queue_type'
	oqId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	oqDesc = db.Column('description', db.String(45))

class OrderStatus(db.Model):
	__tablename__ = 'order_status'
	osId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	osDesc = db.Column('description', db.String(45))

class OrderList(db.Model):
	__tablname__ = "order_lists"
	olId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	qty = db.Column('quantity', db.Integer)
	otId = db.Column('order_transactions_id',db.Integer, db.ForeignKey('order_transactions.id'))
	menu_items_id = db.Column( db.Integer, db.ForeignKey('menu_items.id'))
	special_request_id = db.Column(db.Integer, db.ForeignKey('special_request.id'))
	request_type_id = db.Column(db.Integer, db.ForeignKey('request_type.id'))
	activated = db.Column('activated', db.BOOLEAN)
	clearStatus= db.Column('clear_status', db.String(45))
	menu_item = relationship(MenuItem, backref='order_lists')
	order_transaction = relationship(OrderTransaction, backref='order_lists')
	spec_req = relationship(Specreq, backref='special_request')
	req_type = relationship(reqtype, backref='request_type')

class GeneralSettings(db.Model):
	__tablename__ = 'general_settings'
	gsId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	businessName = db.Column('business_name', db.String(100))
	bHoursStart = db.Column('business_hour_start', db.Time)
	bHoursEnd = db.Column('business_hour_end', db.Time)
	bDayStart = db.Column('business_day_start', db.String(45))
	bDayEnd = db.Column('business_day_end', db.String(45))
	menuUpdate = db.Column('menu_update_time', db.Time)
	delivery = db.Column('delivery_charge', db.Float)
	numOfTables = db.Column('number_of_tables', db.Integer)

class Users(db.Model):
	__tablename__ = 'users'
	uId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	ufname = db.Column('first_name', db.String(100))
	umname = db.Column('middle_name', db.String(100))
	ulname = db.Column('last_name', db.String(100))
	username = db.Column('username', db.String(45))
	userpass = db.Column('password', db.String(100))
	uAccesslvl = db.Column( db.Integer, db.ForeignKey('access_level.id'))
	isLoggedIn = db.Column('isLogin', db.BOOLEAN)
	alId = relationship('AccessLvl', backref="users")

class AccessLvl(db.Model):
	__tablename__ = 'access_level'
	alId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	alDesc = db.Column('description', db.String(45))

class StatisticalReport(db.Model):
	__tablename__ = 'statistical_report'
	statId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	generate_date_start = db.Column(DateTime(timezone=True), nullable=False)
	generate_date_end = db.Column(DateTime(timezone=True), nullable=False)
	date_created = db.Column(DateTime(timezone=True), nullable=False)
	users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	# uId - relationship('Users', backref="users")
class CustomerCount(db.Model):
	__tablename__ = 'customer_count'
	ccId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	value = db.Column('value', db.Integer)
	statistical_report_id = db.Column(db.Integer, db.ForeignKey('statistical_report.id'))
	date = db.Column(DateTime(timezone=True), nullable=False)
	statId = relationship(StatisticalReport, backref='customer_count')

class FrequentOrdered(db.Model):
	__tablename__ = 'frequent_ordered_dish'
	foId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	statistical_report_id = db.Column(db.Integer, db.ForeignKey('statistical_report.id'))
	menu_items_id = db.Column( db.Integer, db.ForeignKey('menu_items.id'))
	value = db.Column('order_count', db.Integer)
	date = db.Column(DateTime(timezone=True), nullable=False)
	menuId = relationship(MenuItem, backref='frequent_ordered_dish')
	statId = relationship(StatisticalReport, backref='frequent_ordered_dish')

class SalesReport(db.Model):
	__tablename__ = 'sales'
	sId = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
	generate_date_start = db.Column(DateTime(timezone=True), nullable=False)
	generate_date_end = db.Column(DateTime(timezone=True), nullable=False)
	date_created = db.Column(DateTime(timezone=True), nullable=False)
	users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	# uid = relationship(reqtype, backref='users')