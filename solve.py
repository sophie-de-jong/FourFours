from fractions import Fraction
from math import factorial, isqrt
from typing import Sequence
import sys
import argparse

MAX_POWER = 8


def safe_pow(a: Fraction, b: Fraction) -> Fraction | None:
    if b.denominator != 1:
        return None

    exp = b.numerator
    if exp < 0 or exp > MAX_POWER:
        return None

    try:
        return a ** exp
    except (OverflowError, ZeroDivisionError):
        return None


def unary_variants(value: Fraction, expr: str) -> list[tuple[Fraction, str]]:
    results = [(value, expr)]

    # Factorial
    if value.denominator == 1:
        n = value.numerator
        if 0 <= n <= 8:
            results.append((Fraction(factorial(n)), f"({expr})!"))

    # Square root
    if value.denominator == 1:
        n = value.numerator
        if n >= 0:
            r = isqrt(n)
            if r * r == n:
                results.append((Fraction(r), f"√({expr})"))

    return results


def binary_variants(a_value: Fraction, a_expr: str, b_value: Fraction, b_expr: str) -> list[tuple[Fraction, str]]:
    results: list[tuple[Fraction, str]] = []

    results.append((a_value + b_value, f"({a_expr}+{b_expr})"))
    results.append((a_value - b_value, f"({a_expr}-{b_expr})"))
    results.append((a_value * b_value, f"({a_expr}*{b_expr})"))

    if b_value != 0:
        results.append((a_value / b_value, f"({a_expr}/{b_expr})"))

    p = safe_pow(a_value, b_value)
    if p is not None:
        results.append((p, f"({a_expr}^{b_expr})"))

    return results


def solve(basis: int, limit: int) -> dict[Fraction, str]:
    expressions: list[dict[Fraction, str]] = [dict() for _ in range(basis)]

    # Add concatenations and decimals
    for count in range(1, basis + 1):
        digits = str(basis) * count
        value = Fraction(int(digits))
        decimal_value = Fraction(int(digits), 10 ** count)

        expressions[count - 1][value] = digits
        expressions[count - 1][decimal_value] = "." + digits

    # Add unary variants to existing expressions
    for idx in range(basis):
        updates = {}

        for value, expr in expressions[idx].items():
            for v, e in unary_variants(value, expr):
                if abs(v) > limit:
                    continue

                if v not in expressions[idx] or len(e) < len(expressions[idx][v]):
                    updates[v] = e

        expressions[idx].update(updates)

    # Dynamic programming
    # Build 2, 3, and 4-four expressions
    for idx in range(1, basis):
        table = expressions[idx]

        for left_idx in range(idx):
            right_idx = idx - left_idx - 1

            for a_value, a_expr in expressions[left_idx].items():
                for b_value, b_expr in expressions[right_idx].items():

                    for value, expr in binary_variants(a_value, a_expr, b_value, b_expr):
                        if abs(value) > limit:
                            continue

                        for v, e in unary_variants(value, expr):
                            if abs(v) > limit:
                                continue

                            if v not in table or len(e) < len(table[v]):
                                table[v] = e

    return expressions[basis - 1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solve the Four Fours puzzle."
    )

    parser.add_argument(
        "-b",
        "--basis",
        type=int,
        default=4,
        help="number used in the puzzle (default: 4)"
    )
    parser.add_argument(
        "-m",
        "--min",
        dest="minimum",
        type=int,
        default=0,
        help="minimum displayed value"
    )
    parser.add_argument(
        "-M",
        "--max",
        dest="maximum",
        type=int,
        default=100,
        help="maximum displayed value"
    )
    parser.add_argument(
        "--score",
        action="store_true",
        help="only show percentage solved"
    )
    parser.add_argument(
        "--missing",
        action="store_true",
        help="show missing values as ?"
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10_000,
        help="limit for intermediary results",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.basis < 1 or args.basis > 9:
        parser.error("basis must be positive and a single digit")

    if args.maximum < args.minimum:
        parser.error("maximum must be greater than or equal to minimum")

    solutions = solve(args.basis, args.limit)

    total = args.maximum - args.minimum + 1
    found = 0

    width = max(len(str(args.minimum)), len(str(args.maximum)))

    for n in range(args.minimum, args.maximum + 1):
        expr = solutions.get(Fraction(n))

        if expr is not None:
            found += 1

        if not args.score:
            if expr is None:
                if args.missing:
                    print(f"{n:{width}d} = ?")
            else:
                print(f"{n:{width}d} = {expr}")
    
    score = found / total
    print(f"Solved {found}/{total} ({score:.1%})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))