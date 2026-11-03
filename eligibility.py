"""Component 4: simple classroom refund rules, not a real store policy."""


def check_refund_eligibility(amount, days_since_delivery, damage_confirmed,
                             documents_reviewed, verification_status):
    # Rule 1: finish the previous component first.
    if verification_status != "READY_FOR_ELIGIBILITY":
        return {"status": "WAITING_FOR_VERIFICATION", "message": "Complete the order and document check first."}

    # Rule 2: an attachment must be reviewed, not just uploaded.
    if not documents_reviewed:
        return {"status": "WAITING_FOR_DOCUMENT_REVIEW", "message": "A support agent must review the invoice and photo."}

    # Classroom policy: confirmed damage reported within 7 days.
    if not damage_confirmed:
        return {"status": "SUPPORT_REVIEW_REQUIRED", "message": "Damage is not confirmed. Send the case to a support agent."}
    if days_since_delivery < 0 or amount <= 0:
        return {"status": "INVALID_DETAILS", "message": "Check the delivery days and purchase amount."}
    if days_since_delivery > 7:
        return {"status": "NOT_ELIGIBLE_UNDER_DEMO_POLICY", "message": "This classroom policy covers damage reported within 7 days of delivery."}

    # Rule 3: route by amount. This function never issues money.
    if amount <= 10000:
        return {"status": "AUTO_REFUND_PATH", "message": "Eligible under demo rules. Continue to the simulated automatic refund step."}
    else:
        return {"status": "MANAGER_APPROVAL_REQUIRED", "message": "Eligible under demo rules. Amount exceeds ₹10,000, so a manager must review it."}
