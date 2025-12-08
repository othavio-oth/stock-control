from typing import List
from pytest import Session
from app.models.tickets import Ticket


def get_allowed_ticket_ids(db: Session, ticket: Ticket) -> List[int]:
        ticket_rows = (
            db.query(Ticket.id)
            .filter(Ticket.cost_center_id == ticket.cost_center_id)
            .order_by(Ticket.id.desc())
            .all()
        )
        ordered_ids = [row.id for row in ticket_rows]
        if not ordered_ids:
            return [ticket.id]

        try:
            current_index = ordered_ids.index(ticket.id)
        except ValueError:
            # fallback: use the newest two tickets if current ticket missing
            return ordered_ids[:2] or [ticket.id]

        allowed = ordered_ids[current_index : current_index + 2]
        return allowed or [ticket.id]