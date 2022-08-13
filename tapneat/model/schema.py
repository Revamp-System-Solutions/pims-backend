from .model import *
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import base64

class _OrderListSchema(ModelSchema):
	class Meta:
		model = OrderList

class _SpecreqSchema(ModelSchema):
	class Meta:
		model = Specreq
	# order_lists = fields.Nested('_OrderListSchema', many=True, include=['olId', 'qty'])

class _MenuItemSchema(ModelSchema):
	class Meta:
		model = MenuItem
	# order_lists = fields.Nested('_OrderListSchema', many=True, include=['olId', 'qty'])
	itemImage = fields.Method('b64encode_image')

	def b64encode_image(self, menuItem):
		return base64.b64encode(menuItem.itemImage)

class _RequestTypeSchema(ModelSchema):
	class Meta:
		model = reqtype
		order_lists = fields.Nested('_OrderListSchema', many=True, include=['olId', 'qty'])

class _OrderTransactionSchema(ModelSchema):
	class Meta:
		model = OrderTransaction
	order_lists = fields.Nested(_OrderListSchema, many=True, include=['olId','qty'])
class _MenuCategorySchema(ModelSchema):
	class Meta:
		model = menu_category

class _PromoDiscountSchema(ModelSchema):
	class Meta:
		model = promo_discount
	promo_discount_type = fields.Nested('_PromoTypeSchema', many=True, include=['pdId'])

class _PromoTypeSchema(ModelSchema):
	class Meta:
		model = PromoDiscountType

class _OrderTypeSchema(ModelSchema):
	class Meta:
		model = OrderType

class _CustomerTypeSchema(ModelSchema):
	class Meta:
		model = CustomerType

class _GeneralSettingsSchema(ModelSchema):
	class Meta:
		model = GeneralSettings

class _UsersSchema(ModelSchema):
	class Meta:
		model = Users

class _AccessLvlSchema(ModelSchema):
	class Meta:
		model = AccessLvl
class _SalesReportSchema(ModelSchema):
	class Meta:
		model = SalesReport
class _StatisticalReportSchema(ModelSchema):
	class Meta:
		model = StatisticalReport
class _LogSchema(ModelSchema):
	class Meta:
		model = Log

OrderTransactionSchema = _OrderTransactionSchema()
OrderListSchema = _OrderListSchema()
MenuItemSchema = _MenuItemSchema()
SpecreqSchema = _SpecreqSchema()
RequestTypeSchema = _RequestTypeSchema()
MenuCategorySchema = _MenuCategorySchema()
PromoDiscountSchema = _PromoDiscountSchema()
PromoTypeSchema = _PromoTypeSchema()
OrderTypeSchema = _OrderTypeSchema()
CustomerTypeSchema = _CustomerTypeSchema()
GeneralSettingsSchema = _GeneralSettingsSchema()
UsersSchema = _UsersSchema()
AccessLvlSchema = _AccessLvlSchema()
SalesReportSchema = _SalesReportSchema()
StatisticalReportSchema = _StatisticalReportSchema()
LogSchema = _LogSchema()