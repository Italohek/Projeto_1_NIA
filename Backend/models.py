# aqui temos o arquivo models.py que define os modelos de dados para o sistema
# utilizando SQLAlchemy ORM. Cada classe representa uma tabela no banco de dados
# e define suas colunas, tipos de dados e relacionamentos.

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, DateTime, DECIMAL, Float, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ---------------- BRANDS ----------------
class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sub_brands = relationship("SubBrand", back_populates="brand", cascade="all, delete-orphan")
    stores = relationship("Store", back_populates="brand", cascade="all, delete-orphan")
    channels = relationship("Channel", back_populates="brand")
    categories = relationship("Category", back_populates="brand")
    products = relationship("Product", back_populates="brand")
    option_groups = relationship("OptionGroup", back_populates="brand")
    items = relationship("Item", back_populates="brand")
    payment_types = relationship("PaymentType", back_populates="brand")
    coupons = relationship("Coupon", back_populates="brand")

# ---------------- SUB BRANDS ----------------
class SubBrand(Base):
    __tablename__ = "sub_brands"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="sub_brands")
    stores = relationship("Store", back_populates="sub_brand")
    categories = relationship("Category", back_populates="sub_brand")
    products = relationship("Product", back_populates="sub_brand")
    option_groups = relationship("OptionGroup", back_populates="sub_brand")
    items = relationship("Item", back_populates="sub_brand")
    customers = relationship("Customer", back_populates="sub_brand")

# ---------------- STORES ----------------
class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    name = Column(String(255), nullable=False)
    city = Column(String(100))
    state = Column(String(2))
    district = Column(String(100))
    address_street = Column(String(200))
    address_number = Column(Integer)
    zipcode = Column(String(10))
    latitude = Column(DECIMAL(9,6))
    longitude = Column(DECIMAL(9,6))
    is_active = Column(Boolean, default=True)
    is_own = Column(Boolean, default=False)
    is_holding = Column(Boolean, default=False)
    creation_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="stores")
    sub_brand = relationship("SubBrand", back_populates="stores")
    sales = relationship("Sale", back_populates="store")
    customers = relationship("Customer", back_populates="store")

# ---------------- CHANNELS ----------------
class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    type = Column(CHAR(1))
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="channels")
    sales = relationship("Sale", back_populates="channel")

# ---------------- CATEGORIES ----------------
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    name = Column(String(200), nullable=False)
    type = Column(CHAR(1), default="P")
    pos_uuid = Column(String(100))
    deleted_at = Column(DateTime)

    brand = relationship("Brand", back_populates="categories")
    sub_brand = relationship("SubBrand", back_populates="categories")
    products = relationship("Product", back_populates="category")
    option_groups = relationship("OptionGroup", back_populates="category")
    items = relationship("Item", back_populates="category")

# ---------------- PRODUCTS ----------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(500), nullable=False)
    pos_uuid = Column(String(100))
    deleted_at = Column(DateTime)

    brand = relationship("Brand", back_populates="products")
    sub_brand = relationship("SubBrand", back_populates="products")
    category = relationship("Category", back_populates="products")
    product_sales = relationship("ProductSale", back_populates="product")

# ---------------- OPTION GROUPS ----------------
class OptionGroup(Base):
    __tablename__ = "option_groups"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(500), nullable=False)
    pos_uuid = Column(String(100))
    deleted_at = Column(DateTime)

    brand = relationship("Brand", back_populates="option_groups")
    sub_brand = relationship("SubBrand", back_populates="option_groups")
    category = relationship("Category", back_populates="option_groups")

# ---------------- ITEMS ----------------
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(500), nullable=False)
    pos_uuid = Column(String(100))
    deleted_at = Column(DateTime)

    brand = relationship("Brand", back_populates="items")
    sub_brand = relationship("SubBrand", back_populates="items")
    category = relationship("Category", back_populates="items")

# ---------------- CUSTOMERS ----------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(50))
    cpf = Column(String(100))
    birth_date = Column(Date)
    gender = Column(String(10))
    store_id = Column(Integer, ForeignKey("stores.id"))
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    registration_origin = Column(String(20))
    agree_terms = Column(Boolean, default=False)
    receive_promotions_email = Column(Boolean, default=False)
    receive_promotions_sms = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    store = relationship("Store", back_populates="customers")
    sub_brand = relationship("SubBrand", back_populates="customers")
    sales = relationship("Sale", back_populates="customer")

# ---------------- SALES ----------------
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    sub_brand_id = Column(Integer, ForeignKey("sub_brands.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    cod_sale1 = Column(String(100))
    cod_sale2 = Column(String(100))
    created_at = Column(DateTime, nullable=False)
    customer_name = Column(String(100))
    sale_status_desc = Column(String(100), nullable=False)
    total_amount_items = Column(DECIMAL(10,2), nullable=False)
    total_discount = Column(DECIMAL(10,2), default=0)
    total_increase = Column(DECIMAL(10,2), default=0)
    delivery_fee = Column(DECIMAL(10,2), default=0)
    service_tax_fee = Column(DECIMAL(10,2), default=0)
    total_amount = Column(DECIMAL(10,2), nullable=False)
    value_paid = Column(DECIMAL(10,2), default=0)
    production_seconds = Column(Integer)
    delivery_seconds = Column(Integer)
    people_quantity = Column(Integer)
    discount_reason = Column(String(300))
    increase_reason = Column(String(300))
    origin = Column(String(100), default='POS')

    store = relationship("Store", back_populates="sales")
    sub_brand = relationship("SubBrand")
    customer = relationship("Customer", back_populates="sales")
    channel = relationship("Channel", back_populates="sales")
    product_sales = relationship("ProductSale", back_populates="sale")
    delivery_sales = relationship("DeliverySale", back_populates="sale")
    payments = relationship("Payment", back_populates="sale")
    coupon_sales = relationship("CouponSale", back_populates="sale")

# ---------------- PRODUCT SALES ----------------
class ProductSale(Base):
    __tablename__ = "product_sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    observations = Column(String(300))

    sale = relationship("Sale", back_populates="product_sales")
    product = relationship("Product", back_populates="product_sales")
    item_product_sales = relationship("ItemProductSale", back_populates="product_sale")

# ---------------- ITEM PRODUCT SALES ----------------
class ItemProductSale(Base):
    __tablename__ = "item_product_sales"

    id = Column(Integer, primary_key=True, index=True)
    product_sale_id = Column(Integer, ForeignKey("product_sales.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    option_group_id = Column(Integer, ForeignKey("option_groups.id"))
    quantity = Column(Float, nullable=False)
    additional_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, default=1)
    observations = Column(String(300))

    product_sale = relationship("ProductSale", back_populates="item_product_sales")
    item_item_product_sales = relationship("ItemItemProductSale", back_populates="item_product_sale")

# ---------------- ITEM ITEM PRODUCT SALES ----------------
class ItemItemProductSale(Base):
    __tablename__ = "item_item_product_sales"

    id = Column(Integer, primary_key=True, index=True)
    item_product_sale_id = Column(Integer, ForeignKey("item_product_sales.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    option_group_id = Column(Integer, ForeignKey("option_groups.id"))
    quantity = Column(Float, nullable=False)
    additional_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, default=1)

    item_product_sale = relationship("ItemProductSale", back_populates="item_item_product_sales")

# ---------------- DELIVERY SALES ----------------
class DeliverySale(Base):
    __tablename__ = "delivery_sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    courier_id = Column(String(100))
    courier_name = Column(String(100))
    courier_phone = Column(String(100))
    courier_type = Column(String(100))
    delivered_by = Column(String(100))
    delivery_type = Column(String(100))
    status = Column(String(100))
    delivery_fee = Column(Float)
    courier_fee = Column(Float)
    timing = Column(String(100))
    mode = Column(String(100))

    sale = relationship("Sale", back_populates="delivery_sales")
    delivery_addresses = relationship("DeliveryAddress", back_populates="delivery_sale")

# ---------------- DELIVERY ADDRESSES ----------------
class DeliveryAddress(Base):
    __tablename__ = "delivery_addresses"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    delivery_sale_id = Column(Integer, ForeignKey("delivery_sales.id", ondelete="CASCADE"))
    street = Column(String(200))
    number = Column(String(20))
    complement = Column(String(200))
    formatted_address = Column(String(500))
    neighborhood = Column(String(100))
    city = Column(String(100))
    state = Column(String(50))
    country = Column(String(100))
    postal_code = Column(String(20))
    reference = Column(String(300))
    latitude = Column(Float)
    longitude = Column(Float)

    delivery_sale = relationship("DeliverySale", back_populates="delivery_addresses")

# ---------------- PAYMENT TYPES ----------------
class PaymentType(Base):
    __tablename__ = "payment_types"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    description = Column(String(100), nullable=False)

    brand = relationship("Brand", back_populates="payment_types")
    payments = relationship("Payment", back_populates="payment_type")

# ---------------- PAYMENTS ----------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    payment_type_id = Column(Integer, ForeignKey("payment_types.id"))
    value = Column(DECIMAL(10,2), nullable=False)
    is_online = Column(Boolean, default=False)
    description = Column(String(100))
    currency = Column(String(10), default="BRL")

    sale = relationship("Sale", back_populates="payments")
    payment_type = relationship("PaymentType", back_populates="payments")

# ---------------- COUPONS ----------------
class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    code = Column(String(50), nullable=False)
    discount_type = Column(String(1))
    discount_value = Column(DECIMAL(10,2))
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)

    brand = relationship("Brand", back_populates="coupons")
    coupon_sales = relationship("CouponSale", back_populates="coupon")

# ---------------- COUPON SALES ----------------
class CouponSale(Base):
    __tablename__ = "coupon_sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"))
    coupon_id = Column(Integer, ForeignKey("coupons.id"))
    value = Column(Float)
    target = Column(String(100))
    sponsorship = Column(String(100))

    sale = relationship("Sale", back_populates="coupon_sales")
    coupon = relationship("Coupon", back_populates="coupon_sales")

