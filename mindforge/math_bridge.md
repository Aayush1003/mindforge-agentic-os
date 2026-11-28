# Math bridge: first step

`mindforge.math_bridge.evaluate_expression` is a small, deterministic Python
kernel for a limited arithmetic language. It turns a familiar written
expression into a reduced exact rational result plus a rounded decimal suitable
for display. Example:

```python
from mindforge.math_bridge import evaluate_expression

print(evaluate_expression("(1 + 2) / 6"))
```

Supported syntax is integer literals, parentheses, unary `+`/`-`, and `+`, `-`,
`*`, `/`, and `**`. Names, function calls, attributes, floating-point literals,
and other Python syntax are rejected. Expression size, syntax-tree size,
exponents, and exact-result size are bounded. The decimal field is only a
human-friendly rendering; use `exact` for the precise rational value.

This is a small foundation for a math interchange layer, not a new language
that understands the universe. Exact arithmetic can verify a calculation under
its stated rules; it does not prove a theorem, validate a model's assumptions,
or establish a physical claim. The next step toward a Python + Rust framework
is to define a versioned, language-neutral expression/result contract and add a
Rust implementation with parity tests before choosing a Python binding.
