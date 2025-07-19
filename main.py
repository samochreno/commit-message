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

SYSTEM_PROMPT = """
Generate a concise commit message using the following tags where appropriate: fix, feat, build, chore, ci, docs, style, refactor, perf, test.

If the commit is specific to a component or feature and that scope is provided in the description (for example, a Vue component or feature name), include the scope in parentheses after the tag (e.g., feat(FoxiiButton): add rounded corners option). If no scope is explicitly provided or implied in the commit description, do not invent or guess a scope—omit it entirely.

Base the commit message on what the commit does, as described. Always write commit messages as if the action is occurring in the present time.

# Output Format

Provide a single commit message line following the format: [tag][(scope)]: [brief description of the change]. If scope is not provided or implied by the description, use only the [tag]: [description] form. Keep the message concise and clear, and ensure the description uses present tense.

# Examples

Example 1:  
Input description: Add documentation for API endpoints  
Output: docs: add documentation for API endpoints

Example 2:  
Input description: Update input validation in FoxiiButton component  
Output: fix(FoxiiButton): update input validation

Example 3:  
Input description: Refactor code structure  
Output: refactor: refactor code structure

(For longer or more complex descriptions, take care to use the exact tag and scope format, and only include a scope if it is explicit or inferable from the description. Do not create or make up scopes.)

# Notes

- Never make up or invent a scope if it is not directly provided or implied by the description.
- Use present tense for all commit messages.
- Keep output to a single concise line following the specified format.
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
