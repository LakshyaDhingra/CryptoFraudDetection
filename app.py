from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Analyze token/contract
@app.route('/analyze', methods=['POST'])
def analyze():
    address = request.form['address']
    # Call function to check contract risks
    result = check_rug_pull_risk(address)
    return render_template('result.html', result=result)

def check_rug_pull_risk(address):
    # Example API call to Etherscan for contract details
    api_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey=YourApiKey"
    response = requests.get(api_url)
    data = response.json()

    # Simple logic to detect risks (expand with better analysis)
    if data['status'] == '1':
        source_code = data['result'][0]['SourceCode']
        if "mint" in source_code.lower():
            return "High Risk: Unlimited token minting detected!"
        else:
            return "Low Risk: No major vulnerabilities found."
    else:
        return "Error: Unable to retrieve contract details."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
