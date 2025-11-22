import requests
import time
import json

tests = [
    {
        "language": "python",
        "cwe": "CWE-89",
        "code": "cursor.execute('SELECT * FROM users WHERE id=' + user_input)"
    },
    {
        "language": "javascript",
        "cwe": "CWE-79",
        "code": "document.body.innerHTML = userInput;"
    },
    {
        "language": "java",
        "cwe": "CWE-22",
        "code": "File f = new File('/var/www/' + filename);"
    }
]

def run_tests():
    url = "http://127.0.0.1:8000/local_fix"
    for t in tests:
        start = time.time()
        try:
            r = requests.post(url, json=t, timeout=60)
            latency = int((time.time() - start) * 1000)
            print("\n--- TEST ---")
            print("Request:", json.dumps(t, indent=2))
            try:
                print("Response:", json.dumps(r.json(), indent=2))
            except Exception as e:
                print("Non-JSON response or parsing error:", e, r.text[:500])
            print("Client-measured latency (ms):", latency)
        except Exception as ex:
            print("Request failed:", ex)

if __name__ == '__main__':
    run_tests()
