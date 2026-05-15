import tiktoken
import os
from pathlib import Path

# Initialize encoder for GPT-4o (o200k_base) and GPT-4/3.5-turbo (cl100k_base)
encoders = {
    "gpt-4o": tiktoken.get_encoding("o200k_base"),
    "gpt-4 / gpt-3.5-turbo": tiktoken.get_encoding("cl100k_base"),
}

repo_path = Path("Day27-Track01-AI-Product-Economics")
markdown_files = sorted(repo_path.rglob("*.md"))

print("=" * 70)
print("TIKTOKEN TOKEN COUNT REPORT")
print("Repository: Day27-Track01-AI-Product-Economics")
print("=" * 70)

for file_path in markdown_files:
    content = file_path.read_text(encoding="utf-8")
    rel_path = file_path.relative_to(repo_path)

    print(f"\n{'-' * 70}")
    print(f"FILE: {rel_path}")
    print(f"{'-' * 70}")

    for model_name, enc in encoders.items():
        tokens = len(enc.encode(content))
        chars = len(content)
        # Rough estimate words
        words = len(content.split())
        print(f"  {model_name:25s}: {tokens:6d} tokens | {chars:6d} chars | {words:5d} words")

# Summary totals
print("\n" + "=" * 70)
print("SUMMARY TOTALS")
print("=" * 70)

for model_name, enc in encoders.items():
    total_tokens = 0
    for file_path in markdown_files:
        content = file_path.read_text(encoding="utf-8")
        total_tokens += len(enc.encode(content))
    print(f"  {model_name:25s}: {total_tokens:6d} tokens")

print("\n" + "=" * 70)
print("REFERENCE: Lab fixed token estimates (from cost-reference-card.md)")
print("=" * 70)
estimates = {
    "System prompt": 500,
    "User message": 80,
    "Assistant response": 180,
    "1 prior turn (history)": 260,
    "RAG top-5 chunks": 1250,
    "Web search results": 800,
    "LLM classifier": 170,
}
for item, tokens in estimates.items():
    print(f"  {item:25s}: {tokens:6d} tokens")

print("\nTIP: To verify your own prompt text, paste it into")
print("   https://www.tiktokenizer.app/tiktoken-online")
print("   or run: python -c \"import tiktoken; enc=tiktoken.get_encoding('o200k_base'); print(len(enc.encode('YOUR TEXT')))\"")
