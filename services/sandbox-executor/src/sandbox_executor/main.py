from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess, tempfile, os

app = FastAPI(title="Sandbox Executor", version="1.0")

class ScriptRequest(BaseModel):
    script: str
    timeout: int = 5

@app.post("/execute")
async def execute_script(req: ScriptRequest):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(req.script)
        script_path = f.name
    try:
        result = subprocess.run(["python3", script_path], capture_output=True, text=True, timeout=req.timeout)
        return {"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode}
    except subprocess.TimeoutExpired:
        raise HTTPException(408, "Script execution timed out")
    finally:
        os.unlink(script_path)

@app.get("/health")
async def health():
    return {"status": "ok"}
