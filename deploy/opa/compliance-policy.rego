package compliance

default allow = false

allow {
    input.document_id != ""
    input.amount < 100000
}

deny_reason[msg] {
    input.document_id == ""
    msg := "document_id is empty"
}

deny_reason[msg] {
    input.amount >= 100000
    msg := "amount exceeds threshold"
}
