# Reflection - draft answers for student review

**Question-source note:** The repository README requests four reflection answers, but the supplied student handout contains no reflection questions. The following four prompts are suggested substitutes, not quotations from the handout. Review these drafts against your own understanding and replace the prompts if your instructor supplies the official questions. These answers describe the observed code and reports, not a claim about personal experiences.

## 1. What did the three tools contribute?

Pylint identified shared mutable defaults, inconsistent returns, unused variables, broad exception handling, naming problems, and missing documentation. Bandit identified SQL construction, non-cryptographic random PIN generation, and silently swallowed exceptions. Flake8 identified long lines, trailing spaces, unused variables, and comparison to None. Their overlap helped confirm some fixes, while their different focus areas made all three useful.

## 2. Which findings deserved priority, and how were they fixed?

The medium-severity SQL finding deserved priority because user-provided names were inserted directly into query text. Parameter binding keeps those values separate from SQL syntax. The two low-severity Bandit findings were also fixed: secrets now generates PINs, and reset failures are allowed to propagate instead of disappearing. Shared mutable logs and inconsistent rental returns were then corrected, followed by documentation and formatting. Severity labels were taken from actual reports rather than assigning a high rating to every issue.

## 3. How were the changes verified, and what were the tools' limits?

All three tools were rerun on the final file. Pylint improved from 3.89/10 to 10.00/10, Bandit went from three findings to zero, and Flake8 went from ten findings to zero. Ten regression tests checked security-sensitive and boundary behavior. Manual inspection also revealed that a missing station could crash hasBikes, which the reports did not directly identify. Clean static reports therefore provide useful evidence but do not prove program correctness or complete security.

## 4. How can static analysis improve future development?

Running these tools before commits or in continuous integration can catch mistakes early and keep style consistent. Reports should be reviewed in context: insecure SQL requires a code change, while naming warnings concern maintainability. Behavioral tests should accompany fixes that change return values or error handling. For this exercise, keeping baseline and final reports makes the improvements measurable, and separate tool-focused commits make each group of changes easier to review and explain.
