import typer
import httpx
from rich.console import Console
from rich.table import Table
from typing import Optional

app = typer.Typer(help="Lexicon compliance platform CLI")
console = Console()

BASE_URL = "http://localhost:8000"

@app.command()
def upload(file: str, tenant: str = "default"):
"""Upload a document for processing."""
with open(file, "rb") as f:
files = {"file": (file, f, "application/pdf")}
headers = {"X-Tenant-ID": tenant}
resp = httpx.post(f"{BASE_URL}/v2/documents", files=files, headers=headers)
if resp.status_code == 200:
doc = resp.json()
console.print(f"[green]Document uploaded: {doc['document_id']} (status: {doc['status']})[/green]")
else:
console.print(f"[red]Upload failed: {resp.status_code} - {resp.text}[/red]")

@app.command()
def status(doc_id: str):
"""Check processing status of a document."""
resp = httpx.get(f"{BASE_URL}/v2/documents/{doc_id}/status")
if resp.status_code == 200:
data = resp.json()
table = Table(title=f"Document {doc_id}")
table.add_column("Field")
table.add_column("Value")
for k, v in data.items():
table.add_row(k, str(v))
console.print(table)
else:
console.print(f"[red]Status check failed: {resp.status_code}[/red]")

@app.command()
def webhook(action: str, event: Optional[str] = None, url: Optional[str] = None, sub_id: Optional[str] = None):
"""Manage webhook subscriptions."""
base = "http://localhost:8008"
if action == "list":
resp = httpx.get(f"{base}/subscriptions")
for sub in resp.json():
console.print(f" {sub['id']}: {sub['event_type']} -> {sub['url']}")
elif action == "subscribe" and event and url:
resp = httpx.post(f"{base}/subscriptions", json={"event_type": event, "url": url})
if resp.status_code == 200:
console.print("[green]Subscription created[/green]")
else:
console.print(f"[red]Failed: {resp.status_code}[/red]")
elif action == "unsubscribe" and sub_id:
resp = httpx.delete(f"{base}/subscriptions/{sub_id}")
if resp.status_code == 200:
console.print("[green]Subscription deleted[/green]")
else:
console.print(f"[red]Failed: {resp.status_code}[/red]")
else:
console.print("Usage: lexctl webhook [list|subscribe|unsubscribe] ...")

@app.command()
def audit(doc_id: str):
"""Retrieve audit trail for a document."""
resp = httpx.get(f"http://localhost:8001/audit/{doc_id}")
if resp.status_code == 200:
data = resp.json()
for entry in data.get("events", []):
console.print(f"{entry['timestamp']} - {entry['action']}")
else:
console.print(f"[red]Audit not available: {resp.status_code}[/red]")

if name == "main":
app()
