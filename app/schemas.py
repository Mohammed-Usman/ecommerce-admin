from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, VARCHAR, DECIMAL
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, CheckConstraint(
        'quantity >=0'), nullable=False, default=0)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    updated_at = Column(TIMESTAMP, server_default=text(
        "now()"), onupdate=text("now()"), nullable=False)


class ProductCategory(Base):

    __tablename__ = 'product_category'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(50), nullable=False, unique=True)
    description = Column(String(250), nullable=False)
    created_at = Column(TIMESTAMP,
                        nullable=False, server_default=text("now()"))

    updated_at = Column(TIMESTAMP, server_default=text(
        "now()"), onupdate=text("now()"))


class Products(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(50), nullable=False)
    description = Column(String(250), nullable=False)

    category_id = Column(Integer, ForeignKey(
        'product_category.id', ondelete='RESTRICT'))

    inventory_id = Column(Integer, ForeignKey(
        'inventory.id', ondelete='RESTRICT'))

    price = Column(DECIMAL(5, 2), nullable=False)

    created_at = Column(TIMESTAMP,
                        nullable=False, server_default=text("now()"))

    updated_at = Column(TIMESTAMP, server_default=text(
        "now()"), onupdate=text("now()"))


class Sales(Base):

    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    total = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(TIMESTAMP,
                        nullable=False, server_default=text("now()"))


class SaleItems(Base):

    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True, nullable=False)

    sale_id = Column(Integer, ForeignKey(
        'sales.id', ondelete='RESTRICT'))

    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='RESTRICT'))

    quantity = Column(Integer, CheckConstraint(
        'quantity >=0'), nullable=False, default=0)

    created_at = Column(TIMESTAMP,
                        nullable=False, server_default=text("now()"))
