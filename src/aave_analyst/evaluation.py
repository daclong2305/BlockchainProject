from decimal import Decimal,InvalidOperation,ROUND_HALF_UP
import math


def numeric_equal(actual,expected,unit="USD",decimals=2):
    try:
        a,b=Decimal(str(actual).replace(",","")),Decimal(str(expected).replace(",",""))
        if not a.is_finite() or not b.is_finite():return False
        if unit=="count":return a==b and a==a.to_integral_value()
        precision=Decimal(1).scaleb(-int(decimals))
        return a.quantize(precision,rounding=ROUND_HALF_UP)==b.quantize(precision,rounding=ROUND_HALF_UP)
    except (InvalidOperation,TypeError,ValueError):return False


def benchmark_numeric_equal(actual, expected, unit='USD', relative_tolerance='0.005'):
    """Proposal scoring policy; runtime cell verification stays stricter."""
    if unit == 'count':
        return numeric_equal(actual, expected, unit='count')
    try:
        a, b = Decimal(str(actual).replace(',', '')), Decimal(str(expected).replace(',', ''))
        tolerance = Decimal(str(relative_tolerance))
        if not all(value.is_finite() for value in (a, b, tolerance)) or tolerance < 0:
            return False
        if b == 0:
            return a == 0
        return abs(a - b) <= abs(b) * tolerance
    except (InvalidOperation, TypeError, ValueError):
        return False


def citation_metrics(claim_checks):
    pairs=[p for c in claim_checks for p in c.get("citations",[])]
    required=[c for c in claim_checks if c.get("needs_evidence",True)]
    return {"precision":sum(bool(p.get("supported")) for p in pairs)/len(pairs) if pairs else None,"completeness":sum(any(p.get("supported") for p in c.get("citations",[])) for c in required)/len(required) if required else None}


def factual_score(record,result):
    expected=record.get("expected_numeric",[])
    if not expected:return None
    if result.get("error") or result.get("draft",{}).get("refused"):return False
    # Score numbers explicitly stated in the answer claims, not latent SQL cells.
    claims=result.get("draft",{}).get("claims",[])
    numeric=[c["numeric"] for c in claims if c.get("numeric")]
    remaining=list(numeric)
    for gold in expected:
        match=next((i for i,n in enumerate(remaining) if n.get("unit")==gold.get("unit") and benchmark_numeric_equal(n.get("value"),gold.get("value"),gold.get("unit","USD"),record.get('numeric_relative_tolerance','0.005'))),None)
        if match is None:return False
        remaining.pop(match)
    return True


def percentile(values,p):
    if not values:return None
    values=sorted(values);idx=(len(values)-1)*p;low=int(idx);high=min(low+1,len(values)-1)
    return values[low]+(values[high]-values[low])*(idx-low)
