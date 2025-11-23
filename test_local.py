import requests, time, json

TESTS = [
    {"language": "python", "cwe": "CWE-89", "code": "cursor.execute('SELECT * FROM users WHERE id=' + user_input)"},
    {"language": "javascript", "cwe": "CWE-79", "code": "document.body.innerHTML = userInput;"},
    {"language": "java", "cwe": "CWE-22", "code": "File f = new File('/var/www/' + filename);"}
]

def run():
    url = "http://127.0.0.1:8000/local_fix"

    for t in TESTS:
        start = time.time()
        r = requests.post(url, json=t)
        elapsed = int((time.time() - start) * 1000)

        try:
            print(json.dumps(r.json(), indent=2))
        except:
            print("Non-JSON:", r.text[:300])

        print("Latency:", elapsed, "ms\n")

if __name__ == "__main__":
    run()
