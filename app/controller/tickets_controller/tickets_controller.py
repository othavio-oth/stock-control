from . import *

def list_tickets(db):
    return TicketService.list_tickets(db)

def create_ticket(ticket_data, db):
    import logging
    logging.info(f"Ticket created by user {ticket_data}")
    return TicketService.create_ticket(db, ticket_data)

def edit_ticket(ticket_id, ticket_data, db):
    return TicketService.edit_ticket(db, ticket_id, ticket_data)

def delete_ticket(ticket_id, db):
    return TicketService.remove_ticket(db, ticket_id)

def add_product_to_ticket_controller(product_data, db):
    return TicketService.add_product(db, product_data)

def get_products_for_ticket_controller(ticket_id, db):
    return TicketService.get_products_for_ticket(db, ticket_id)

def get_ticket_products_controller(db):
    return TicketService.service_get_ticket_products(db)

def remove_product_from_ticket_controller(ticket_product_id, db):
    return TicketService.remove_product(db, ticket_product_id)

def get_tickets_by_cost_center_controller(cost_center_id, db):
    return TicketService.get_tickets_by_cost_center(db, cost_center_id)