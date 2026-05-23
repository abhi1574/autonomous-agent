import subprocess
import tempfile
import os

class CodeExecutorTool:
    name        = "code_executor"
    description = "Safely execute Python code and return output"

    def run(self, input: dict) -> str:
        code    = input.get("code", "")
        timeout = input.get("timeout", 10)

        if not code.strip():
            return "No code provided"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            output = ""
            if result.stdout:
                output += f"Output:\n{result.stdout}"
            if result.stderr:
                output += f"Errors:\n{result.stderr}"
            if not output:
                output = "Code executed successfully with no output"

            os.unlink(temp_path)
            return output

        except subprocess.TimeoutExpired:
            return f"Execution timed out after {timeout} seconds"
        except Exception as e:
            return f"Execution failed: {e}"