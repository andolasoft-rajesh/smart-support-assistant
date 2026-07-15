# Rate Limit Fixes

## Summary
The rate-limit issue was addressed by reducing request pressure on the LLM provider and adding retry/backoff behavior.

## Changes made

### 1. Added retry with exponential backoff in the backend LLM service
Updated [backend/app/services/llm.py](backend/app/services/llm.py) to:
- detect transient provider failures such as 429, 503, quota, and rate-limit style errors;
- retry with exponential backoff instead of failing immediately;
- apply the retry logic to both chat generation and embedding requests.

### 2. Slowed down the evaluation loop
Updated [eval/run_eval.py](eval/run_eval.py) to:
- add a longer pause between requests;
- keep the evaluator from sending requests too quickly to the backend/provider.

### 3. Added a regression test
Created [backend/tests/test_llm_retry.py](backend/tests/test_llm_retry.py) to verify that the new backoff logic retries transient failures correctly.

## Verification
The change was verified by running:

```bash
backend\venv\Scripts\python.exe -m unittest backend.tests.test_llm_retry
```

Result:
- 1 test ran
- OK
