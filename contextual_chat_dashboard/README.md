# Usage

```bash
python main.py
```

理想的な返答
```
You: 金曜日にレポート提出がある。notesに追加して。

Dashboard Agent: Note added: 金曜日にレポート提出がある。

You: 私のnotesを見せて

Dashboard Agent:
- 金曜日にレポート提出がある
```

now
```
You: 金曜日にレポート提出がある。notesに追加して。
[DEBUG] BEFORE: notes = []
[DEBUG] AFTER: notes = ['金曜日にレポート提出がある。']

 Dashboard Agent: Note added: 金曜日にレポート提出がある。

You: 私のnotesを見せて
[DEBUG] Notes when calling show_notes = []

 Dashboard Agent: No notes yet.
```