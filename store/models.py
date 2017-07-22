# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.six import python_2_unicode_compatible
import json

#用户
@python_2_unicode_compatible
class User(AbstractUser):
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

#广告
@python_2_unicode_compatible
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title

#分类
@python_2_unicode_compatible
class Category(models.Model):
    typ = models.CharField(max_length=20, verbose_name='所属大类')
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=1, verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __str__(self):
        return self.name

#品牌
@python_2_unicode_compatible
class Brand(models.Model):
    name = models.CharField(max_length=30, verbose_name='品牌名称')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name

#尺寸
@python_2_unicode_compatible
class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name='尺寸')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '尺寸'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name

#标签
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#商品包括衣服鞋子等
@python_2_unicode_compatible
class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='分类')
    name = models.CharField(max_length=30, verbose_name='名称')
    brand = models.ForeignKey(Brand, verbose_name='品牌')
    size = models.ManyToManyField(Size, verbose_name='尺寸')
    old_price = models.FloatField(default=0.0, verbose_name='原价')
    new_price = models.FloatField(default=0.0, verbose_name='现价')
    discount = models.FloatField(default=1, verbose_name='折扣')
    desc = models.CharField(max_length=100, verbose_name='简介')
    sales = models.IntegerField(default=0, verbose_name='销量')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    num = models.IntegerField(default=0, verbose_name='库存')
    image_url_i = models.ImageField(upload_to='product/%Y/%m', default= 'product/default.jpg', verbose_name='展示图片路径')
    image_url_l = models.ImageField(upload_to='product/%Y/%m', default= 'product/default.jpg', verbose_name='详情图片路径1')
    image_url_m = models.ImageField(upload_to='product/%Y/%m', default= 'product/default.jpg', verbose_name='详情图片路径2')
    image_url_r = models.ImageField(upload_to='product/%Y/%m', default= 'product/default.jpg', verbose_name='详情图片路径3')
    image_url_c = models.ImageField(upload_to='product/%Y/%m', default= 'product/ce.jpg', verbose_name='购物车展示图片')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.brand.name + u"---" + self.category.name


#购物车条目
@python_2_unicode_compatible
class Caritem(models.Model):
    user_id = models.ForeignKey(User, verbose_name='用户id')
    product = models.ForeignKey(Product, verbose_name='购物车中产品条目')
    quantity = models.IntegerField(default=0, verbose_name='数量')
    sum_price = models.FloatField(default=0.0, verbose_name='小计')

    class Meta:
        verbose_name = '购物车条目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


# 购物车
class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0.0

    def add(self, product):
        self.total_price += product.new_price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
                item.sum_price += product.new_price
                return
        else:
            self.items.append(Caritem(product=product, quantity=1, sum_price=product.new_price))


# 订单
class OrderItem(models.Model):
    orderno = models.CharField(editable=False, max_length=50, primary_key=True, serialize=False, verbose_name='订单号')
    user = models.CharField(blank=True, max_length=50, null=True, verbose_name='用户标识')
    product_desc = models.CharField(max_length=128, verbose_name='商品描述')
    product_detail = models.TextField(max_length=1000, verbose_name='商品详情')
    fee = models.DecimalField(decimal_places=0, max_digits=6, verbose_name='金额(单位:分)')
    attach = models.CharField(blank=True, max_length=127, null=True, verbose_name='附加数据')
    dt_start = models.DateTimeField(editable=False, verbose_name='交易开始时间')
    dt_end = models.DateTimeField(editable=False, verbose_name='交易失效时间')
    dt_pay = models.DateTimeField(blank=True, editable=False, null=True, verbose_name='付款时间')
    paied = models.BooleanField(default=False, editable=False, verbose_name='已收款')
    lapsed = models.BooleanField(default=False, editable=False, verbose_name='已失效')
    payway = models.CharField(choices=[('WEIXIN', '微信支付'), ('ALI', '支付宝支付')], default='WEIXIN', max_length=10, verbose_name='支付方式')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    date_update = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '付款单'
        verbose_name_plural = verbose_name



# 阿里支付订单
class AliPayOrder(models.Model):
    out_trade_no = models.CharField(db_index=True, editable=False, max_length=32, verbose_name='商户订单号')
    subject = models.CharField(editable=False, max_length=128, verbose_name='商品名称')
    body = models.CharField(editable=False, max_length=512, verbose_name='商品详情')
    total_fee = models.DecimalField(decimal_places=2, editable=False, max_digits=6, verbose_name='总金额(单位:元)')
    it_b_pay = models.CharField(editable=False, max_length=19, verbose_name='交易有效期')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '支付宝订单'
        verbose_name_plural = verbose_name


# 阿里支付结果
class AliPayResult(models.Model):
    order = models.OneToOneField(editable=False, on_delete=models.deletion.CASCADE, primary_key=True, related_name='pay_result', serialize=False, to='store.AliPayOrder')
    notify_time = models.CharField(blank=True, editable=False, max_length=19, null=True, verbose_name='通知时间')
    notify_type = models.CharField(blank=True, editable=False, max_length=50, null=True, verbose_name='通知类型')
    notify_id = models.CharField(blank=True, editable=False, max_length=50, null=True, verbose_name='通知校验ID')
    out_trade_no = models.CharField(blank=True, editable=False, max_length=32, null=True, verbose_name='商户订单号')
    subject = models.CharField(blank=True, editable=False, max_length=128, null=True, verbose_name='商品名称')
    trade_no = models.CharField(blank=True, editable=False, max_length=64, null=True, verbose_name='支付宝交易号')
    trade_status = models.CharField(blank=True, editable=False, max_length=16, null=True, verbose_name='交易状态')
    seller_id = models.CharField(blank=True, editable=False, max_length=30, null=True, verbose_name='卖家支付宝用户号')
    seller_email = models.CharField(blank=True, editable=False, max_length=100, null=True, verbose_name='卖家支付宝账号')
    buyer_id = models.CharField(blank=True, editable=False, max_length=30, null=True, verbose_name='买家支付宝用户号')
    buyer_email = models.CharField(blank=True, editable=False, max_length=100, null=True, verbose_name='买家支付宝账号  ')
    total_fee = models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True, verbose_name='总金额(单位:元)')

    class Meta:
        verbose_name = '阿里支付结果'
        verbose_name_plural = verbose_name


# 微信支付订单
class WeiXinOrder(models.Model):
    appid = models.CharField(editable=False, max_length=32, verbose_name='公众账号ID')
    mch_id = models.CharField(editable=False, max_length=32, verbose_name='商户号')
    body = models.CharField(editable=False, max_length=128, verbose_name='商品描述')
    attach = models.CharField(blank=True, editable=False, max_length=127, null=True, verbose_name='附加数据')
    out_trade_no = models.CharField(db_index=True, editable=False, max_length=32, verbose_name='商户订单号')
    fee_type = models.CharField(editable=False, max_length=16, verbose_name='货币类型')
    total_fee = models.SmallIntegerField(editable=False, verbose_name='总金额')
    spbill_create_ip = models.CharField(editable=False, max_length=16, verbose_name='终端IP')
    time_start = models.CharField(editable=False, max_length=14, verbose_name='交易起始时间')
    time_expire = models.CharField(editable=False, max_length=14, verbose_name='交易结束时间')
    notify_url = models.CharField(editable=False, max_length=256, verbose_name='通知地址')
    trade_type = models.CharField(editable=False, max_length=16, verbose_name='交易类型')

    class Meta:
        verbose_name = '微信统一订单'
        verbose_name_plural = verbose_name

# 微信支付结果
class WeiXinPayResult(models.Model):
    order = models.OneToOneField(editable=False, on_delete=models.deletion.CASCADE, primary_key=True, related_name='pay_result', serialize=False, to='store.WeiXinOrder')
    prepayid = models.CharField(blank=True, db_index=True, editable=False, max_length=64, null=True, verbose_name='预支付交易会话标识')
    openid = models.CharField(blank=True, editable=False, max_length=128, null=True, verbose_name='用户标识(openId)')
    bank_type = models.CharField(blank=True, editable=False, max_length=16, null=True, verbose_name='付款银行')
    total_fee = models.SmallIntegerField(blank=True, editable=False, null=True, verbose_name='总金额')
    attach = models.CharField(blank=True, editable=False, max_length=128, null=True, verbose_name='商户附加数据')
    tradestate = models.CharField(blank=True, editable=False, max_length=32, null=True, verbose_name='交易状态')
    tradestatedesc = models.CharField(blank=True, editable=False, max_length=256, null=True, verbose_name='交易状态描述')

    class Meta:
        verbose_name = '微信支付结果'
        verbose_name_plural = verbose_name

