import logging

from app import db, app
from sqlalchemy import Column, Integer, Float, String, ForeignKey, func,DateTime
from sqlalchemy.orm import relationship, backref

sensor_gateway = db.Table("sensor_gateway",
                          Column("sensor_id", Integer, ForeignKey("sensor.id"), primary_key=True),
                          Column("gateway_id", Integer, ForeignKey("gateway.id"), primary_key=True),
                          Column("active", Integer, nullable = True),
                          Column("time", Float, default = 10, nullable = True)
                          )
class GateWay(db.Model):
    __tablename__ = "gateway"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)

class Sensor(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), unique = True, nullable=False)
    active = Column(Integer,default = 1 ,nullable=True)
    time = Column(Float, default=10, nullable=True)
    gateways = relationship("GateWay", secondary = sensor_gateway, lazy = 'subquery', backref = backref('sensors', lazy = False))

class DataSensor(db.Model):
    __tablename__ = "data_sensor"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_sensor = Column(Integer, ForeignKey("sensor.id"), nullable = False)
    value = Column(Float, nullable = False)
    type_sensor = Column(String(255), nullable = True)
    type_device = Column(String(255), nullable = True)
    unit = Column(String(255), nullable =  True)
    battery = Column(Float, nullable = True)
    create_at = Column(String(255), nullable = False)



with app.app_context():
    db.create_all()
    try:
        insert_data = GateWay(name= "123124")
        db.session.add(insert_data)
        db.session.commit()
    except:
        logging.error("Da co du lieu gateway")
