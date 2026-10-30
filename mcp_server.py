# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkFinance

client = OpenClawGenParkFinance()

TOOLS = [
    {
        "name": "audit_benfords_law",
        "description": "Calculates Benford's Law Chi-Square test to detect fabricated financial receipts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "transactions": {"type": "array", "items": {"type": "number"}},
                "significance_threshold": {"type": "number"}
            },
            "required": ["transactions"]
        }
    },
    {
        "name": "compute_wacc",
        "description": "Calculates corporate Weighted Average Cost of Capital (WACC).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "equity_value_usd": {"type": "number"},
                "debt_value_usd": {"type": "number"},
                "cost_of_equity": {"type": "number"},
                "cost_of_debt": {"type": "number"},
                "corporate_tax_rate": {"type": "number"}
            },
            "required": ["equity_value_usd", "debt_value_usd", "cost_of_equity", "cost_of_debt"]
        }
    },
    {
        "name": "calculate_dcf_npv",
        "description": "Calculates Net Present Value (NPV) and Profitability Index for future cash flows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cash_flows": {"type": "array", "items": {"type": "number"}},
                "discount_rate": {"type": "number"},
                "initial_investment": {"type": "number"}
            },
            "required": ["cash_flows", "discount_rate", "initial_investment"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "audit_benfords_law":
            res = client.audit_benfords_law(args["transactions"], args.get("significance_threshold", 15.51))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_wacc":
            res = client.compute_wacc(args["equity_value_usd"], args["debt_value_usd"], args["cost_of_equity"], args["cost_of_debt"], args.get("corporate_tax_rate", 0.21))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "calculate_dcf_npv":
            res = client.calculate_dcf_npv(args["cash_flows"], args["discount_rate"], args["initial_investment"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
