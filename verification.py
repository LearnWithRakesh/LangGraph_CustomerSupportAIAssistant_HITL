"""Teaching component: deterministic verification against demo order data."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


DEMO_ORDERS = {
    "ORD-78452": {"customer_name": "Rahul", "product": "Laptop", "amount": 65000.0},
    "ORD-10001": {"customer_name": "Riya", "product": "Headphones", "amount": 5000.0}
}


class VerificationState(TypedDict, total=False):
    complaint: dict
    invoice_present: bool
    photo_present: bool
    status: str
    missing_documents: list[str]
    message: str
    route: str


def verify_order(state: VerificationState) -> dict:
    complaint = state["complaint"]
    order = DEMO_ORDERS.get(complaint["order_id"].strip().upper())
    if order is None:
        return {"route": "review", "status": "ORDER_REVIEW_REQUIRED",
                "message": "Order not found in the demo records. A support agent must review it.",
                "missing_documents": []}
    matches = (
        complaint["customer_name"].strip().casefold() == order["customer_name"].casefold()
        and complaint["product"] == order["product"]
        and abs(complaint["amount"] - order["amount"]) < 0.01
    )
    if not matches:
        return {"route": "review", "status": "ORDER_REVIEW_REQUIRED",
                "message": "Complaint details do not match the demo order. Review the name, product and amount.",
                "missing_documents": []}
    missing = []
    if not state.get("invoice_present", False):
        missing.append("Invoice")
    if not state.get("photo_present", False):
        missing.append("Damage photo")
    return {"route": "request_info" if missing else "ready",
            "missing_documents": missing}


def request_info(state: VerificationState) -> dict:
    return {"status": "WAITING_FOR_DOCUMENTS",
            "message": "Please attach: " + ", ".join(state["missing_documents"])}


def ready_for_eligibility(state: VerificationState) -> dict:
    return {"status": "READY_FOR_ELIGIBILITY",
            "message": "Demo order matches and both attachments are present. Document contents still need review. Refund eligibility has not been decided."}


builder = StateGraph(VerificationState)
builder.add_node("verify_order", verify_order)
builder.add_node("request_info", request_info)
builder.add_node("ready_for_eligibility", ready_for_eligibility)
builder.add_edge(START, "verify_order")
builder.add_conditional_edges("verify_order", lambda state: state["route"],
                              {"review": END, "request_info": "request_info", "ready": "ready_for_eligibility"})
builder.add_edge("request_info", END)
builder.add_edge("ready_for_eligibility", END)
verification_graph = builder.compile()
