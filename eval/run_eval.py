"""
eval/run_eval.py
Day 17 evaluation harness. Turns "it seemed fine when I tried it" into a
number you can improve.
"""
import argparse
import csv
import pathlib
import sys
import time
import requests

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_CASES = HERE / "testcases.csv"


def run_case(base_url: str, question: str) -> str:
    """Send one question and return the assistant's reply text."""
    resp = requests.post(f"{base_url}/chat", json={"message": question}, timeout=60)
    resp.raise_for_status()
    return resp.json()["reply"]


def diagnose(base_url: str, question: str) -> None:
    """Print the chunks retrieve() would inject — retrieval vs instruction bug."""
    try:
        resp = requests.get(
            f"{base_url}/debug/retrieve", params={"q": question}, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        print(f"      retrieved {data['count']} chunk(s):")
        for i, chunk in enumerate(data["chunks"], 1):
            preview = chunk.replace("\n", " ")[:200]
            print(f"        [{i}] {preview}")
    except requests.RequestException as err:
        print(f"      (could not fetch retrieved chunks: {err})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the assistant eval suite.")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--cases", default=str(DEFAULT_CASES), help="testcases.csv path")
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="on failure, print the retrieved chunks to locate the cause",
    )
    args = parser.parse_args()

    with open(args.cases, newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))

    if not cases:
        print("No test cases found.")
        return 1

    passed = 0
    for c in cases:
        question = (c.get("question") or "").strip()
        must_contain = (c.get("must_contain") or "").strip()
        must_not_contain = (c.get("must_not_contain") or "").strip()

        try:
            reply = run_case(args.url, question)
        except requests.RequestException as err:
            print(f"ERROR - {question}\n      request failed: {err}")
            print("      ⏳ Rate limit detected! Cooling down for 15 seconds...")
            time.sleep(15)  # Stop the rapid-fire loop failure
            continue

        reply_lc = reply.lower()
        ok = True
        reasons = []
        if must_contain and must_contain.lower() not in reply_lc:
            ok = False
            reasons.append(f'missing "{must_contain}"')
        if must_not_contain and must_not_contain.lower() in reply_lc:
            ok = False
            reasons.append(f'contains forbidden "{must_not_contain}"')

        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"{status} - {question}")
        if not ok:
            print(f"      reason: {', '.join(reasons)}")
            print(f"      reply : {reply.strip()[:200]}")
            if args.diagnose:
                diagnose(args.url, question)
        
        # Slow the loop further to stay comfortably under provider rate limits
        time.sleep(20)

    print(f"\n{passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())