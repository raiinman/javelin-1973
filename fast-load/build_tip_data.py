"""Generate original tip translations and the matching Lua index. No checks or game execution."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
package = root / 'DeadSignalFastLoad/42/media/lua'
rows = [line.split('|', 1) for line in (root / 'survival-tips.tsv').read_text(encoding='utf-8').splitlines() if line]
translations = {}
index = ['-- Generated from the original tip library. Do not edit independently.', 'return {']
for number, (category, text) in enumerate(rows, 1):
    key = f'UI_quick_tip_FL_{number:03}'
    translations[key] = text
    index.append('    {key=' + json.dumps(key) + ', category=' + json.dumps(category) + '},')
index.append('}')
target = package / 'shared/Translate/EN/UI.json'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(translations, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(package / 'client/DeadSignalFastLoad/TipIndex.lua').write_text('\n'.join(index) + '\n', encoding='utf-8')
(root / 'startup-preview-tips.js').write_text('window.survivalTips = ' + json.dumps([
    {'category': category, 'text': text} for category, text in rows
], ensure_ascii=False) + ';\n', encoding='utf-8')
print(f'Generated {len(rows)} original tips. No tests or game were run.')
