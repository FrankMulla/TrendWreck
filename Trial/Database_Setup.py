# **** Configuration Code **** #
"""The sys module provides a number of functions and variables that can be used to manipulate different
parts of the python run time enviornment"""

# import os
# import sys
# Classes for mapper and configuration code
from sqlalchemy import Column, Integer, Boolean, DECIMAL, ForeignKey, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base  # Used in config and class code
from sqlalchemy.orm import relationship  # Helps us create our foreign key relationships

Base = declarative_base()
'''The declarative base lets sqlalchemy know that our classes are special
sqlalchemy classes corresponding to tables in the database'''


# **** Class, Mapper and Table code **** #

class Account(Base):
    # ** Table Information
    __tablename__ = 'account'

    # ** Mapper Code
    accountId = Column(Integer, primary_key=True)
    username = Column(String(15), primary_key=True)
    password = Column(String, nullable=False)
    firstName = Column(String(15), nullable=False)
    middleName = Column(String(15))
    lastName = Column(String(15), nullable=False)
    retailer = Column(Boolean, nullable=False)
    lastLogin = Column(Date)
    accountStatus = Column(String(8), nullable=False)
    email = Column(String(150), nullable=False)
    joinDate = Column(Date)


class Label(Base):
    __tablename__ = 'label'

    labelId = Column(Integer, primary_key=True)
    labelDescription = Column(String(50), nullable=False)


class Media(Base):
    __tablename__ = 'media'

    mediaId = Column(Integer, primary_key=True)
    mediaType = Column(String(10))
    mediaUrl = Column(String(250))
    ad = Column(Boolean)


class Item(Base):
    __tablename__ = 'item'

    itemId = Column(Integer, primary_key=True)
    clothingLine_id = Column(Integer, ForeignKey('clothingLine.clothingLineId'))
    itemDescription = Column(String(250))
    clothingType = Column(String(50))
    media_id = Column(Integer, ForeignKey('media.mediaId'))
    uploadDate = Column(Date)
    price = Column(DECIMAL)
    label_id = Column(Integer, ForeignKey('label.labelId'))
    clicks = Column(Integer)
    likes = Column(Integer)
    media = relationship(Media)
    label = relationship(Label)


class Business(Base):
    # ** Table Info
    __tablename__ = 'business'

    businessId = Column(Integer, primary_key=True)
    account_Id = Column(Integer, ForeignKey('account.accountId'))
    businessName = Column(String(40))
    businessDescription = Column(String(250))
    verifiedStatus = Column(Boolean)
    businessImageID = Column(Integer, ForeignKey('item.itemId'))
    promotionalVidID = Column(Integer, ForeignKey('item.itemId'))
    businessBannerID = Column(Integer, ForeignKey('item.itemId'))
    account = relationship(Account)
    item = relationship(Item)


class Branch(Base):
    __tablename__ = 'branch'

    branchId = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('business.businessId'))
    branchName = Column(String(30))
    branchLocation = Column(String(50))
    branchCity = Column(String(50))
    branchCell = Column(String(15))
    branchEmail = Column(String(25))
    business = relationship(Business)


class ClothingLine(Base):
    __tablename__ = 'clothingLine'

    clothingLineId = Column(Integer, primary_key=True)
    bussiness_id = Column(Integer, ForeignKey('business.businessId'))
    clothingLineName = Column(String(25))
    clothingLineDescription = Column(String(250))
    clothingLineVideoId = Column(Integer, ForeignKey('item.itemId'), nullable=True)
    business = relationship(Business)
    item = relationship(Item)


class PaymentPackage(Base):
    __tablename__ = 'paymentPackage'
    packageId = Column(Integer, primary_key=True)
    packageDescription = Column(String(250))
    packageCost = Column(DECIMAL)


class Ads(Base):
    __tablename__ = 'ads'

    adId = Column(Integer, primary_key=True)
    adDescription = Column(String(250), nullable=False)
    providerEmail = Column(String(50), nullable=False)
    paymentEmail = Column(String(50))
    paymentPackageId = Column(Integer, ForeignKey('paymentPackage.packageId'))
    mediaID = Column(Integer, ForeignKey('media.mediaId'))
    link = Column(String(250))
    number = Column(String(12))
    expiryDate = Column(Date)
    paymentPackage = relationship(PaymentPackage)
    media = relationship(Media)


class Tags(Base):
    __tablename__ = 'tags'

    tagId = Column(Integer, primary_key=True)
    tagDescription = Column(String(20), nullable=False)


class FeedTags(Base):
    __tablename__ = 'feedTags'

    account_id = Column(Integer, ForeignKey('account.accountId'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tagId'), primary_key=True)
    account = relationship(Account)
    tag = relationship(Tags)


class BusinessTags(Base):
    __tablename__ = 'businessTags'

    business_id = Column(Integer, ForeignKey('business.businessId'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tagId'), primary_key=True)
    business = relationship(Business)
    tag = relationship(Tags)


class ItemTags(Base):
    __tablename__ = 'itemTags'

    item_id = Column(Integer, ForeignKey('item.itemId'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tagId'), primary_key=True)
    item = relationship(Item)
    tag = relationship(Tags)


class WishList(Base):
    __tablename__ = 'wishList'

    account_id = Column(Integer, ForeignKey('account.accountId'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.itemId'), primary_key=True)
    account = relationship(Account)
    item = relationship(Item)


class Subscriptions(Base):
    __tablename__ = 'subscriptions'

    account_id = Column(Integer, ForeignKey('account.accountId'), primary_key=True)
    business_id = Column(Integer, ForeignKey('business.businessId'), primary_key=True)
    account = relationship(Account)
    business = relationship(Business)


class Favourites(Base):
    __tablename__ = 'favourites'

    account_id = Column(Integer, ForeignKey('account.accountId'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.itemId'), primary_key=True)
    account = relationship(Account)
    item = relationship(Item)


# **** Insert at end of file **** #
# **** ToDo figure out how to put postgresql in the create engine block and use that
engine = create_engine('sqlite:///trendwreck.db')
# engine = create_engine("postgresql://user:password@localhost:5432/trendwreck")
Base.metadata.create_all(engine)  # Adds the classes as tables to the database
