# Python standard library imports
import logging
import time

# Project specific imports
from app.database.dao import save_location, save_customer, save_supplier, save_order, get_order_count

# Third-party imports
from sqlalchemy.orm import sessionmaker
import pandas as pd


_IS_SUCCESSFUL_PERSIST = False


def get_is_successful_persist():
    return _IS_SUCCESSFUL_PERSIST


def set_is_successful_persist(start_count, end_count, delta):
    global _IS_SUCCESSFUL_PERSIST
    _IS_SUCCESSFUL_PERSIST = end_count == start_count + delta


def read_csv(filepath):
    column_names = ["order_date",
                    "order_id",
                    "customer_id",
                    "customer_location",
                    "requested_amt",
                    "supplier_id",
                    "supplier_location",
                    "supplied_amt",
                    "cost"]
    orders_df = pd.read_csv(filepath, names=column_names)
    # Drop first row containing original column names.
    orders_df.drop(index=orders_df.index[0], axis=0, inplace=True)
    return orders_df


def persist_orders(engine, filename):
    # TODO: Can be retrieved from S3. Should not specify explicit paths, can introduce security vulnerabilities.
    filepath = f"app/data/{filename}.csv"
    start_time = time.time()
    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    curr_session = session()
    try:
        start_orders_count = get_order_count(curr_session)
        orders_df = read_csv(filepath)
        for row_index in range(1, len(orders_df) + 1):
            cust_loc_id = save_location(curr_session, loc_name=orders_df["customer_location"][row_index])
            cust_id = save_customer(curr_session, customer_id=orders_df["customer_id"][row_index], cust_loc_id=cust_loc_id)
            supp_loc_id = save_location(curr_session, loc_name=orders_df["supplier_location"][row_index])
            supp_id = save_supplier(curr_session, supp_id=orders_df["supplier_id"][row_index], supp_loc_id=supp_loc_id)

            save_order(session=curr_session,
                       order_id=orders_df["order_id"][row_index],
                       cust_id=cust_id,
                       supp_id=supp_id,
                       date=orders_df["order_date"][row_index],
                       req_amount=orders_df["requested_amt"][row_index],
                       supp_amount=orders_df["supplied_amt"][row_index],
                       cost=orders_df["cost"][row_index])
        end_orders_count = get_order_count(curr_session)
        set_is_successful_persist(start_orders_count, end_orders_count, orders_df.shape[0])
    except FileNotFoundError as fnfe:
        logging.error(f"Could not find the specified file {filename} in path {filepath}, exception is: {fnfe}.")
    except Exception as e:
        logging.error(f"Something went wrong while persisting file {filename}, exception is: {e}.")
        curr_session.rollback()
    finally:
        curr_session.close()
        persist_duration = ((time.time() - start_time) / 1000) % 60
        logging.info(f"Persisting entries from file {filename} took {persist_duration} sec.")
