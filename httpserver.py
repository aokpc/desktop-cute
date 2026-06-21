import subprocess

MODE = "python"

if MODE=="sfz":
    def server(path: str, port: int = 9090):
        return subprocess.Popen(["sfz", path, "-p", str(port), "-L"])
elif MODE=="python":
    def server(path: str, port: int):
        return subprocess.Popen(["python3", "-m", "http.server","--directory", path, str(port)])