"""Component 5: manager review and final classroom resolution."""


def resolve_complaint(complaint, eligibility, decision=None,
                      manager_name="", reason=""):
    # Only an eligible case can reach a refund outcome.
    status = eligibility["status"]
    if status == "AUTO_REFUND_PATH":
        outcome = "REFUND_APPROVED_DEMO"
        explanation = "Approved automatically under the classroom policy."
        reviewer = "Demo automatic rule"
    elif status == "MANAGER_APPROVAL_REQUIRED":
        if decision not in ("Approve", "Reject"):
            raise ValueError("Choose Approve or Reject.")
        if not manager_name.strip():
            raise ValueError("Enter the demo manager's name.")
        if decision == "Reject" and not reason.strip():
            raise ValueError("Enter a reason for rejecting the refund.")
        outcome = "REFUND_APPROVED_DEMO" if decision == "Approve" else "REFUND_REJECTED_DEMO"
        explanation = reason.strip() or "Approved after demo manager review."
        reviewer = manager_name.strip()
    else:
        raise ValueError("This case is not ready for a refund decision.")

    # Produce a message for the screen. No payment or email is sent.
    if outcome == "REFUND_APPROVED_DEMO":
        message = (
            f"Hello {complaint['customer_name']}, your refund request for "
            f"order {complaint['order_id']} (₹{complaint['amount']:,.2f}) "
            "was approved in this classroom simulation. No money has been transferred."
        )
    else:
        message = (
            f"Hello {complaint['customer_name']}, your refund request for "
            f"order {complaint['order_id']} was rejected in this classroom simulation. "
            f"Reason: {explanation}"
        )
    return {"status": outcome, "case_status": "CLOSED_DEMO",
            "reviewer": reviewer, "reason": explanation, "customer_message": message}
