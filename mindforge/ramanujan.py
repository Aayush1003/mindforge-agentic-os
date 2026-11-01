"""A compact numerical demonstration of Ramanujan's series for 1/pi."""

from __future__ import annotations

from decimal import Decimal, localcontext
from math import factorial


_PI_REFERENCE = Decimal(
    "3.14159265358979323846264338327950288419716939937510"
)


def ramanujan_pi_demo(terms: int = 3) -> dict[str, object]:
    """Return successive pi estimates from Ramanujan's rapidly convergent series."""
    if not 1 <= terms <= 10:
        raise ValueError("terms must be between 1 and 10")

    with localcontext() as context:
        context.prec = 70
        series_sum = Decimal(0)
        estimates: list[dict[str, object]] = []
        scale = Decimal(2) * Decimal(2).sqrt() / Decimal(9801)

        for k in range(terms):
            numerator = Decimal(factorial(4 * k)) * Decimal(1103 + 26390 * k)
            denominator = Decimal(factorial(k) ** 4) * Decimal(396) ** (4 * k)
            series_sum += numerator / denominator
            pi_estimate = Decimal(1) / (scale * series_sum)
            estimates.append(
                {
                    "terms_used": k + 1,
                    "pi_estimate": str(+pi_estimate),
                    "absolute_error": str(+(abs(pi_estimate - _PI_REFERENCE))),
                }
            )

        return {
            "name": "Ramanujan's series for 1/pi",
            "equation": (
                "1/pi = (2*sqrt(2)/9801) * sum(k=0..infinity, "
                "(4k)!*(1103+26390k) / ((k!)^4*396^(4k)))"
            ),
            "estimates": estimates,
            "note": "A famous convergent identity, not a new law of nature.",
        }
