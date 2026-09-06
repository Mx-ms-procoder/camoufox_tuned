"""Use the actual upstream BudgetType::COUNT in cbindgen array lengths."""
from pathlib import Path
import re
import sys


def fix(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    pattern = r'(\[[^\]\n]*;\s*)BudgetType::COUNT(\])'
    if not re.search(pattern, text):
        return 0
    definition = re.search(r'impl BudgetType\s*\{\s*const COUNT:\s*usize\s*=\s*(\d+);', text)
    if not definition:
        raise ValueError('BudgetType::COUNT changed; review the upstream definition')
    count = definition.group(1)
    updated, replacements = re.subn(pattern, lambda m: m[1] + count + m[2], text)
    path.write_text(updated, encoding='utf-8')
    print(f'Replaced {replacements} array lengths with upstream COUNT={count}')
    return replacements


if __name__ == '__main__':
    fix(Path(sys.argv[1]))
