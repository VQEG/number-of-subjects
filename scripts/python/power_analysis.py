#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scipy>=1.11",
# ]
# ///
"""
VQEGNumSubjTool - Power Analysis for Number of Subjects

Calculate the minimum number of subjects required for QoE experiments
using power analysis with Bonferroni correction for multiple comparisons.

Based on: Brunnström, K. and M. Barkowsky, "Statistical quality of experience
analysis: on planning the sample size and statistical significance testing",
Journal of Electronic Imaging, 2018. 27(5): p. 11

Usage:
    uv run power_analysis.py [options]
    uv run power_analysis.py --interactive
"""

import argparse
import math
from scipy import stats


def calculate_power(n: int, d: float, alpha: float, test_type: str = "paired") -> float:
    """
    Calculate statistical power for a t-test.

    Args:
        n: Sample size (per group for two-sample test)
        d: Effect size (Cohen's d)
        alpha: Significance level
        test_type: "paired" or "two.sample"

    Returns:
        Statistical power (probability of detecting a true effect)
    """
    if test_type == "paired":
        df = n - 1
        ncp = d * math.sqrt(n)  # Non-centrality parameter
    else:  # two.sample / independent
        df = 2 * n - 2
        ncp = d * math.sqrt(n / 2)

    # Critical value for two-tailed test
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    # Power using non-central t-distribution
    # P(reject H0 | H1 true) = P(T > t_crit) + P(T < -t_crit)
    power_upper = 1 - stats.nct.cdf(t_crit, df, ncp)
    power_lower = stats.nct.cdf(-t_crit, df, ncp)

    return power_upper + power_lower


def calculate_sample_size(
    d: float,
    alpha: float,
    target_power: float = 0.8,
    test_type: str = "paired",
) -> int:
    """
    Calculate required sample size to achieve target power.

    Args:
        d: Effect size (Cohen's d)
        alpha: Significance level (after any corrections)
        target_power: Desired power (default 0.8)
        test_type: "paired" or "two.sample"

    Returns:
        Minimum sample size required
    """
    # Binary search for required n
    lo, hi = 2, 10000

    while hi - lo > 1:
        mid = (lo + hi) // 2
        power = calculate_power(mid, d, alpha, test_type)
        if power < target_power:
            lo = mid
        else:
            hi = mid

    return hi


def calculate_subjects(
    stdev: float = 0.8,
    mos_diff: float = 1.0,
    num_comparisons: int = 100,
    power: float = 0.8,
    base_alpha: float = 0.05,
    test_type: str = "paired",
) -> dict:
    """
    Calculate number of subjects needed for a QoE experiment.

    Args:
        stdev: Expected standard deviation of ratings
        mos_diff: Minimum MOS difference to detect
        num_comparisons: Number of planned t-test comparisons
        power: Desired statistical power
        base_alpha: Base significance level (before Bonferroni correction)
        test_type: "paired" or "two.sample"

    Returns:
        Dictionary with all computed values
    """
    effect_size = mos_diff / stdev
    adjusted_alpha = base_alpha / num_comparisons  # Bonferroni correction

    n_subjects = calculate_sample_size(effect_size, adjusted_alpha, power, test_type)

    return {
        "n_subjects": n_subjects,
        "effect_size": effect_size,
        "adjusted_alpha": adjusted_alpha,
        "base_alpha": base_alpha,
        "stdev": stdev,
        "mos_diff": mos_diff,
        "num_comparisons": num_comparisons,
        "power": power,
        "test_type": test_type,
    }


def format_alpha(alpha: float) -> str:
    """Format alpha value for display."""
    if alpha >= 0.0001:
        return f"{alpha:.6f}"
    return f"{alpha:.2e}"


def print_results(results: dict) -> None:
    """Print formatted results."""
    print("\n" + "=" * 50)
    print("  VQEGNumSubjTool - Power Analysis Results")
    print("=" * 50)
    print(f"\n  Minimum subjects required: {results['n_subjects']}")
    print("\n  Parameters:")
    print(f"    Standard deviation:    {results['stdev']:.2f}")
    print(f"    MOS difference:        {results['mos_diff']:.2f}")
    print(f"    Number of comparisons: {results['num_comparisons']}")
    print(f"    Target power:          {results['power']:.2f}")
    print(f"    Test type:             {results['test_type']}")
    print("\n  Derived values:")
    print(f"    Effect size (d):       {results['effect_size']:.3f}")
    print(f"    Base alpha:            {results['base_alpha']}")
    print(f"    Adjusted alpha:        {format_alpha(results['adjusted_alpha'])}")
    print("    Correction method:     Bonferroni")
    print("=" * 50 + "\n")


def generate_table(
    d_values: list[float] | None = None,
    alpha_values: list[float] | None = None,
    power: float = 0.8,
    test_type: str = "paired",
) -> None:
    """
    Generate a table of sample sizes (replicates R script output).

    Args:
        d_values: List of effect sizes (Cohen's d)
        alpha_values: List of significance levels
        power: Target power
        test_type: "paired" or "two.sample"
    """
    if d_values is None:
        d_values = [round(x, 1) for x in [i / 10 for i in range(2, 25)]]  # 0.2 to 2.4
    if alpha_values is None:
        alpha_values = [0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001, 0.00005, 0.00001]

    print(f"\nSample sizes for {test_type} t-test (power = {power})")
    print("-" * (12 + 10 * len(alpha_values)))

    # Header
    header = f"{'d':>10} |"
    for alpha in alpha_values:
        header += f" {format_alpha(alpha):>8}"
    print(header)
    print("-" * (12 + 10 * len(alpha_values)))

    # Data rows
    for d in d_values:
        row = f"{d:>10.1f} |"
        for alpha in alpha_values:
            n = calculate_sample_size(d, alpha, power, test_type)
            row += f" {n:>8}"
        print(row)


def interactive_mode() -> None:
    """Run interactive mode with user prompts."""
    print("\n" + "=" * 50)
    print("  VQEGNumSubjTool - Interactive Mode")
    print("=" * 50)
    print("\nEnter parameters (press Enter for defaults):\n")

    def get_float(prompt: str, default: float) -> float:
        val = input(f"  {prompt} [{default}]: ").strip()
        return float(val) if val else default

    def get_int(prompt: str, default: int) -> int:
        val = input(f"  {prompt} [{default}]: ").strip()
        return int(val) if val else default

    stdev = get_float("Expected standard deviation", 0.8)
    mos_diff = get_float("Desired MOS difference", 1.0)
    num_comparisons = get_int("Number of comparisons", 100)
    power = get_float("Desired power", 0.8)

    test_type_input = input("  Test type (paired/independent) [paired]: ").strip().lower()
    test_type = "two.sample" if test_type_input in ("independent", "two.sample", "i") else "paired"

    results = calculate_subjects(stdev, mos_diff, num_comparisons, power, test_type=test_type)
    print_results(results)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate number of subjects for QoE experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Use defaults
  %(prog)s --stdev 1.0 --mos-diff 0.5
  %(prog)s --comparisons 1000 --test-type independent
  %(prog)s --table                   # Generate sample size table
  %(prog)s --interactive             # Interactive mode
        """,
    )

    parser.add_argument("--stdev", type=float, default=0.8, help="Expected standard deviation (default: 0.8)")
    parser.add_argument("--mos-diff", type=float, default=1.0, help="Desired MOS difference to detect (default: 1.0)")
    parser.add_argument("--comparisons", type=int, default=100, help="Number of planned comparisons (default: 100)")
    parser.add_argument("--power", type=float, default=0.8, help="Desired statistical power (default: 0.8)")
    parser.add_argument("--alpha", type=float, default=0.05, help="Base significance level (default: 0.05)")
    parser.add_argument(
        "--test-type",
        choices=["paired", "independent"],
        default="paired",
        help="Type of t-test (default: paired)",
    )
    parser.add_argument("--table", action="store_true", help="Generate sample size table")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    test_type = "two.sample" if args.test_type == "independent" else "paired"

    if args.interactive:
        interactive_mode()
    elif args.table:
        generate_table(power=args.power, test_type=test_type)
        print()
        generate_table(power=args.power, test_type="two.sample" if test_type == "paired" else "paired")
    else:
        results = calculate_subjects(
            stdev=args.stdev,
            mos_diff=args.mos_diff,
            num_comparisons=args.comparisons,
            power=args.power,
            base_alpha=args.alpha,
            test_type=test_type,
        )

        if args.json:
            import json

            print(json.dumps(results, indent=2))
        else:
            print_results(results)


if __name__ == "__main__":
    main()
