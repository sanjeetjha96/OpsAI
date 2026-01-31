"""Create a small set of synthetic sample docs for prototyping.

Creates simple text files in data/sample_docs/ to exercise the indexer.
"""
import os
import argparse


SAMPLE_TEXT = [
    ("ticket_001.txt", "Payment service failing intermittently for EU users. Error code: PAY-502. Timeouts seen in gateway."),
    ("ticket_002.txt", "Dashboard not loading for user in APAC. Frontend 503 and image assets failing to load."),
    ("runbook_001.txt", "Runbook: How to restart payment gateway. Step 1: check pods. Step 2: restart service."),
    ("incident_001.txt", "Past incident: gateway throttling during peak. Root cause: misconfigured rate limiter."),
    ("faq_001.txt", "FAQ: Common errors and what they mean. PAY-502 indicates upstream timeout."),
]


def main(data_dir: str):
    os.makedirs(data_dir, exist_ok=True)
    for name, text in SAMPLE_TEXT:
        path = os.path.join(data_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    print(f"Wrote {len(SAMPLE_TEXT)} sample files to {data_dir}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", default=os.path.join("data", "sample_docs"))
    args = p.parse_args()
    main(args.data_dir)
