# -*- coding: utf-8 -*-
from client import OpenClawGenParkFinance

finance = OpenClawGenParkFinance()

# 1. Benford's Law Forensic Audit
txs = [19.5, 142.0, 18.2, 105.0, 24.5, 312.0, 11.0, 48.0, 190.0, 21.0, 52.0, 130.0, 16.0, 71.0, 12.0]
benford = finance.audit_benfords_law(txs)
print(f"Benford's Law Audit: Chi^2 = {benford['chi_square_statistic']} ({benford['forensic_verdict']})")

# 2. WACC Calculation
wacc = finance.compute_wacc(equity_value_usd=80000000.0, debt_value_usd=20000000.0, cost_of_equity=0.12, cost_of_debt=0.06, corporate_tax_rate=0.21)
print(f"\nWACC: {wacc['wacc_percentage']}% (Firm Value: ${wacc['total_firm_value_usd']})")

# 3. DCF NPV
cfs = [150000.0, 220000.0, 310000.0, 420000.0]
dcf = finance.calculate_dcf_npv(cfs, discount_rate=wacc['wacc'], initial_investment=600000.0)
print(f"\nDCF Decision: NPV = ${dcf['net_present_value_npv_usd']} ({dcf['investment_decision']})")
