"""
eval/run_eval.py

Runs evaluation test cases against the Smart Support Assistant.

Usage:
    python eval/run_eval.py --document-id 405bf47e-a9cd-4b5b-b260-81382a6cf74d
    python eval/run_eval.py --document-id 405bf47e-a9cd-4b5b-b260-81382a6cf74d --diagnose
"""

import argparse
import csv
import pathlib
import sys

import requests

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_CASES = HERE / "testcases.csv"


def run_case(base_url: str, document_id: str, question: str) -> str:
    """Send one question and return assistant reply."""

    response = requests.post(
        f"{base_url}/chat",
        json={
            "message": question,
            "document_id": document_id
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()["reply"]


def diagnose(base_url: str, document_id: str, question: str):

    try:

        response = requests.get(
            f"{base_url}/debug/retrieve",
            params={
                "q": question,
                "document_id": document_id
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        print(f"      retrieved {data['count']} chunk(s):")

        for i, chunk in enumerate(data["chunks"], 1):

            preview = chunk.replace("\n", " ")[:200]

            print(f"        [{i}] {preview}")

    except requests.RequestException as err:

        print(f"      (could not fetch retrieved chunks: {err})")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        default="http://localhost:8000"
    )

    parser.add_argument(
        "--cases",
        default=str(DEFAULT_CASES)
    )

    parser.add_argument(
    "--document-id",
    default="405bf47e-a9cd-4b5b-b260-81382a6cf74d",
    help="Document ID to evaluate against"
)

    parser.add_argument(
        "--diagnose",
        action="store_true"
    )

    args = parser.parse_args()

    with open(args.cases, newline="", encoding="utf-8") as f:

        cases = list(csv.DictReader(f))

    if not cases:

        print("No test cases found.")

        return 1

    passed = 0

    for case in cases:

        question = case["question"].strip()

        must_contain = case["must_contain"].strip()

        must_not_contain = case["must_not_contain"].strip()

        try:

            reply = run_case(
                args.url,
                args.document_id,
                question
            )

        except requests.RequestException as err:

            print(f"ERROR - {question}")

            print(err)

            continue

        reply_lower = reply.lower()

        ok = True

        reasons = []

        if must_contain:

            if must_contain.lower() not in reply_lower:

                ok = False

                reasons.append(
                    f'Missing "{must_contain}"'
                )

        if must_not_contain:

            if must_not_contain.lower() in reply_lower:

                ok = False

                reasons.append(
                    f'Contains "{must_not_contain}"'
                )

        if ok:

            passed += 1

        print(f'{"PASS" if ok else "FAIL"} - {question}')

        if not ok:

            print("      " + ", ".join(reasons))

            print("      Reply:", reply)

            if args.diagnose:

                diagnose(
                    args.url,
                    args.document_id,
                    question
                )

    print()

    print(f"{passed}/{len(cases)} passed")

    return 0 if passed == len(cases) else 1


if __name__ == "__main__":

    sys.exit(main())