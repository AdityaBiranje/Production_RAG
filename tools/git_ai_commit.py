#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from google import genai

console = Console()

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    console.print("[red]GEMINI_API_KEY not found in .env[/red]")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

console.print("[cyan]📦 Staging changes...[/cyan]")
run(["git","add","."])

diff = run(["git","diff","--cached"])
if not diff.stdout.strip():
    console.print("[yellow]Nothing to commit.[/yellow]")
    sys.exit(0)

prompt = f"""
You are an expert software engineer.

Generate ONE conventional commit message.

Rules:
- Output ONLY the commit message.
- Max 72 characters.
- Use feat/fix/refactor/docs/chore/test/style/perf/build/ci.
- No markdown.
- No explanation.

Git diff:
{diff.stdout[:15000]}
"""

console.print("[cyan]🤖 Generating commit message with Gemini...[/cyan]")

resp = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

msg = resp.text.strip().splitlines()[0].strip("` ")

console.print(Panel(msg, title="Suggested Commit"))

choice = input("Commit and push? [Y/e/n]: ").strip().lower()

if choice == "n":
    console.print("[yellow]Cancelled.[/yellow]")
    sys.exit(0)

if choice == "e":
    new = input("Enter commit message: ").strip()
    if new:
        msg = new

commit = subprocess.run(["git","commit","-m",msg])
if commit.returncode != 0:
    sys.exit(commit.returncode)

push = subprocess.run(["git","push"])
if push.returncode == 0:
    console.print("[green]✅ Commit pushed successfully![/green]")
else:
    console.print("[red]Push failed.[/red]")
