import flask
from flask import Flask, render_template, request, redirect
from web3 import Web3

app = Flask(__name__)

candidates = {1: "badi mohammad", 2: "hamza saht", 3: "omar hussein"}

# Connect to the Sepolia network
web3 = Web3(
    Web3.HTTPProvider(
        "https://eth-sepolia.g.alchemy.com/v2/ji4q9T9gKbrr9hk41agAd6JvmuvKhDJk"
    )
)

# Load the contract ABI and address
contract_address = "0x9eE6c65458701930770ADE3ACC9dE59437640b83"
contract_abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "inputs": [{"internalType": "uint8", "name": "_candidateId", "type": "uint8"}],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "candidates",
        "outputs": [
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "uint256", "name": "voteCount", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "candidatesCount",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint8", "name": "_candidateId", "type": "uint8"}],
        "name": "getCandidatesVoteCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "voters",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


# Define the home route
@app.route("/")
def home():
    return render_template("index.html")


# Define a route to interact with the smart contract
@app.route("/interact", methods=["GET", "POST"])
def interact():
    if flask.request.method == "GET":
        badi = contract.functions.getCandidatesVoteCount(1).call()
        hamza = contract.functions.getCandidatesVoteCount(2).call()
        omar = contract.functions.getCandidatesVoteCount(3).call()
        return render_template("result.html", Badi=badi, Hamza=hamza, Omar=omar)
    elif flask.request.method == "POST":
        votedCandidate = request.form.get("name")
        for key in candidates:
            if votedCandidate.lower() in candidates[key]:
                votedCandidate = key
                break
        else:
            return render_template("index.html")

        print(contract.functions.vote(votedCandidate).call())
        return redirect("/interact", code=302)


if __name__ == "__main__":
    app.run(debug=True)
