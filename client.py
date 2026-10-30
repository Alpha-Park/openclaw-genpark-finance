# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Finance - Benford's Law Chi-Square Audit & WACC Discounted Cash Flow Solver
Standard Library only: math, typing.
Calculates Benford's Law first-digit goodness-of-fit Chi-Square statistics to detect fabricated
expense telemetry, evaluates corporate Weighted Average Cost of Capital (WACC), and computes DCF NPV.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkFinance:
    def __init__(self):
        # Benford theoretical first-digit probabilities: log10(1 + 1/d)
        self.benford_probs = {d: math.log10(1.0 + 1.0 / d) for d in range(1, 10)}

    def audit_benfords_law(self, transactions: List[float],
                           significance_threshold: float = 15.51) -> Dict[str, Any]:
        """
        Calculates Chi-Square test of observed leading digits against Benford's Law.
        Critical value for 8 degrees of freedom at alpha=0.05 is 15.51.
        """
        if not transactions:
            return {"error": "Empty transaction list"}

        leading_digits = []
        for tx in transactions:
            val = abs(float(tx))
            if val > 0:
                # Extract first non-zero digit
                s = f"{val:.8f}".replace(".", "").lstrip("0")
                if s:
                    leading_digits.append(int(s[0]))

        N = len(leading_digits)
        if N < 10:
            return {"error": "Need at least 10 non-zero transactions for valid chi-square test"}

        observed_counts = {d: 0 for d in range(1, 10)}
        for d in leading_digits:
            if d in observed_counts:
                observed_counts[d] += 1

        chi_square_stat = 0.0
        digit_audit = []

        for d in range(1, 10):
            obs = observed_counts[d]
            exp = N * self.benford_probs[d]
            sq_diff = (obs - exp) ** 2
            contrib = sq_diff / max(1e-6, exp)
            chi_square_stat += contrib

            digit_audit.append({
                "digit": d,
                "observed_count": obs,
                "expected_count": round(exp, 2),
                "observed_freq": round(obs / N, 4),
                "expected_freq": round(self.benford_probs[d], 4),
                "chi_square_contribution": round(contrib, 4)
            })

        is_anomalous = chi_square_stat > significance_threshold

        return {
            "transactions_analyzed": N,
            "chi_square_statistic": round(chi_square_stat, 4),
            "critical_threshold_alpha_05": significance_threshold,
            "is_anomaly_detected": is_anomalous,
            "forensic_verdict": "BENFORDS_LAW_DEVIATION_SUSPECTED_FABRICATION" if is_anomalous else "CONFORMS_TO_NATURAL_TRANSACTION_DISTRIBUTION",
            "digit_breakdown": digit_audit
        }

    def compute_wacc(self, equity_value_usd: float,
                     debt_value_usd: float,
                     cost_of_equity: float,
                     cost_of_debt: float,
                     corporate_tax_rate: float = 0.21) -> Dict[str, Any]:
        """
        Calculates Weighted Average Cost of Capital (WACC):
        WACC = (E / V) * Re + (D / V) * Rd * (1 - Tc)
        """
        E = max(0.0, equity_value_usd)
        D = max(0.0, debt_value_usd)
        V = E + D
        if V <= 0:
            return {"error": "Total firm value must be positive"}

        re = cost_of_equity
        rd = cost_of_debt
        tc = max(0.0, min(1.0, corporate_tax_rate))

        wacc = (E / V) * re + (D / V) * rd * (1.0 - tc)

        return {
            "total_firm_value_usd": round(V, 2),
            "equity_weight": round(E / V, 4),
            "debt_weight": round(D / V, 4),
            "cost_of_equity": re,
            "after_tax_cost_of_debt": round(rd * (1.0 - tc), 4),
            "wacc": round(wacc, 4),
            "wacc_percentage": round(wacc * 100.0, 2)
        }

    def calculate_dcf_npv(self, cash_flows: List[float],
                          discount_rate: float,
                          initial_investment: float) -> Dict[str, Any]:
        """
        Calculates Net Present Value:
        NPV = -I_0 + sum_{t=1}^T [ CF_t / (1 + r)^t ]
        """
        r = max(-0.5, discount_rate)
        discounted_flows = []
        total_pv = 0.0

        for t, cf in enumerate(cash_flows, 1):
            pv = cf / ((1.0 + r) ** t)
            discounted_flows.append({"year": t, "cash_flow": cf, "present_value": round(pv, 2)})
            total_pv += pv

        npv = total_pv - initial_investment
        profitability_index = total_pv / max(1.0, initial_investment)

        return {
            "initial_investment_usd": initial_investment,
            "discount_rate": r,
            "total_present_value_usd": round(total_pv, 2),
            "net_present_value_npv_usd": round(npv, 2),
            "profitability_index": round(profitability_index, 3),
            "investment_decision": "ACCEPT_VALUE_ACCRETIVE" if npv > 0 else "REJECT_VALUE_DESTRUCTIVE",
            "cash_flows_schedule": discounted_flows
        }
