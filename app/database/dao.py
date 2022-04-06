# Python standard library imports
from dateutil import parser
import logging

# Project specific imports
from .table_definitions import locations, customers, suppliers, orders

# Third-party imports
from sqlalchemy.sql.expression import func


def cache(fun):
    cache.cache_ = {}

    def inner(*args, **kwargs):
        call_key = frozenset(dict({"fun_name": fun.__name__}, **kwargs).items())
        if call_key not in cache.cache_:
            cache.cache_[call_key] = fun(*args, **kwargs)
        return cache.cache_[call_key]
    return inner


@cache
def save_location(session, loc_name):
    location = session.query(locations.loc_id).filter_by(loc_name=str(loc_name)).first()
    if location:
        loc_id = location.loc_id
    else:
        loc_rec = locations(**{
            'loc_name': str(loc_name)
        })
        session.add(loc_rec)
        session.commit()
        loc_id = loc_rec.loc_id
    return loc_id


@cache
def save_customer(session, customer_id, cust_loc_id):
    cust = session.query(customers.customer_id).filter_by(customer_id=str(customer_id)).first()
    if cust:
        cust_id = cust.customer_id
    else:
        cust_rec = customers(**{
            'customer_id': str(customer_id),
            'loc_id': cust_loc_id
        })
        session.add(cust_rec)
        session.commit()
        cust_id = cust_rec.customer_id
    return cust_id


@cache
def save_supplier(session, supp_id, supp_loc_id):
    supplier = session.query(suppliers.supp_id).filter_by(supp_id=str(supp_id)).first()
    if supplier:
        supp_id = supplier.supp_id
    else:
        supp_rec = suppliers(**{
            'supp_id': str(supp_id),
            'loc_id': supp_loc_id
        })
        session.add(supp_rec)
        session.commit()
        supp_id = supp_rec.supp_id
    return supp_id


# TODO: Discuss data types. It is reasonable to assume that cost is float, even though only integers are being provided.
def save_order(session, order_id, cust_id, supp_id, date, req_amount, supp_amount, cost):
    order = session.query(orders.order_id).filter_by(order_id=str(order_id)).first()
    if order:
        logging.warning(f"Order with order_id {order_id} has already been recorded.")
    else:
        order_rec = orders(**{
            'order_id': str(order_id),
            'customer_id': cust_id,
            'supp_id': supp_id,
            'date': parser.parse(date),
            'req_amount': float(req_amount),
            'supp_amount': float(supp_amount),
            'cost': float(cost)
        })
        session.add(order_rec)
        session.commit()


def get_order_count(session):
    return session.query(func.count(orders.order_id)).scalar()

