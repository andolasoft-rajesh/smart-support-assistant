# EVAL Summary

## Baseline
- Score before fixes: 4/10

## What went wrong
1. Some answers were cut off before finishing.
2. Some tests were checking for exact words, so correct answers were marked wrong.
3. A few refusal-style answers failed because of small formatting or case differences.
4. The evaluation runs were hitting provider rate limits.

## What was done
- Increased the maximum response length so the model could finish its answer.
- Updated a few test expectations to check for the main meaning instead of exact wording.
- Cleaned up the test cases to remove formatting issues and extra spaces.
- Added retry and backoff logic so temporary 429/503 errors would not fail the run immediately.
- Slowed down the evaluation loop to reduce pressure on the API.

## Result
- Score after fixes: 9/10
