#!/usr/bin/env python3
"""
message.py
Generate a Conventional Commits-style message with the latest OpenAI Python SDK.

Usage:
  python message.py <natural-language description>
  git diff | python message.py
"""

import os
import sys
from openai import OpenAI

SYSTEM_PROMPT = """Write a concise commit message using the following tags where appropriate: fix, feat, build, chore, ci, docs, style, refactor, perf, test.

If the commit is specific to a component or feature (e.g., a Vue component), include a scope using the component or feature name in parentheses after the tag (e.g., feat(FoxiiButton): add rounded corners option).

Base the commit message on what the commit does, as described. Always write commit messages as if the action is occurring in the present time.

# Output Format
Provide a single commit message line following the format: [tag][(scope)]: [brief description of the change]. Keep the message concise and clear, and ensure the description uses the present tense.
"""

def get_description() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return sys.stdin.read().strip()

def main():
    descr = get_description()
    if not descr:
        sys.exit("No description provided via arguments or STDIN.")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": descr},
        ],
    )
    msg = response.choices[0].message.content.strip()
    print(msg)

if __name__ == "__main__":
    main()
