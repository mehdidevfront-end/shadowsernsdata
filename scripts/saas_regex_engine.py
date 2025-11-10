"""SaaS regex engine: provide compiled patterns and helpers to detect SaaS occurrences in text.

Functions:
 - load_allowed_saas(path): loads allowed_saas JSON (list with domains)
 - build_patterns(allowed_saas=None): returns dict name->compiled regex
 - detect_saas(text, patterns): returns list of matches
"""
import json
import os
import re
from typing import List, Dict


DEFAULT_PATTERNS = {
    'Dropbox': [r"\b(?:https?://)?(?:[a-z0-9-]+\.)?dropbox\.com\b"],
    'Zoom': [r"\b(?:https?://)?(?:[a-z0-9-]+\.)?(?:zoom\.us|zoom\.com)\b"],
    'Slack': [r"\b(?:https?://)?(?:[a-z0-9-]+\.)?slack\.com\b"],
    'GoogleDrive': [r"\b(?:https?://)?(?:drive|docs)\.google\.com\b", r"\b(?:https?://)?(?:[a-z0-9-]+\.)?googleusercontent\.com\b"],
    'OneDrive': [r"\b(?:https?://)?(?:[a-z0-9-]+\.)?onedrive\.live\.com\b"],
    'Salesforce': [r"\b(?:https?://)?(?:[a-z0-9-]+\.)?salesforce\.com\b"],
}


def load_allowed_saas(path: str):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def build_patterns(allowed_saas: List[Dict] = None):
    patterns = {}
    if allowed_saas:
        for item in allowed_saas:
            name = item.get('name') or item.get('id') or 'unknown'
            doms = item.get('domains') or []
            regexes = [fr"\b(?:https?://)?(?:[a-z0-9-]+\.)?{re.escape(d)}\b" for d in doms]
            if regexes:
                patterns[name] = [re.compile(r, re.IGNORECASE) for r in regexes]
    # merge defaults but don't overwrite explicit
    for k, rs in DEFAULT_PATTERNS.items():
        if k not in patterns:
            patterns[k] = [re.compile(r, re.IGNORECASE) for r in rs]

    return patterns


def detect_saas(text: str, patterns: Dict[str, List[re.Pattern]]):
    matches = []
    for name, regs in patterns.items():
        for reg in regs:
            for m in reg.finditer(text or ''):
                matches.append({
                    'provider': name,
                    'match': m.group(0),
                    'span': m.span(),
                    'pattern': reg.pattern,
                })
    return matches


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--text', '-t', help='Text to scan (or use stdin)')
    p.add_argument('--allowed', '-a', help='allowed_saas JSON to load (optional)')
    args = p.parse_args()
    txt = args.text
    if not txt:
        import sys
        txt = sys.stdin.read()
    allowed = None
    if args.allowed:
        allowed = load_allowed_saas(args.allowed)
    pats = build_patterns(allowed)
    res = detect_saas(txt, pats)
    print(json.dumps(res, indent=2, ensure_ascii=False))
