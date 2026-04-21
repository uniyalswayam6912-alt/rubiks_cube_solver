import json
import urllib.request
import urllib.error

def test_api():
    url = "http://127.0.0.1:8000/solve"
    data = json.dumps({"moves": ["L2", "R2", "B2", "D2", "U2", "F2"]}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as f:
            print(f.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print("URL Error:", e)

if __name__ == "__main__":
    test_api()
