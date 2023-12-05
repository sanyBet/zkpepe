import requests
import time

proxies = None


def fetch_balance(address, index):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(f"https://www.zksyncpepe.com/resources/amounts/{address.lower()}.json", proxies=proxies)

            if response.status_code == 200:
                if response.text:  # Check if the response content is not empty
                    balance = response.json()[0]
                    print(f"wallet{index} {address} balance: {balance}")
                    return balance
                else:
                    print("Error: Response content is empty.")
            else:
                print(f"Error: {response.status_code}")
                print("Response content:", response.text)

        except requests.exceptions.RequestException:
            retries += 1
            print(f"wallet{index} {address} Retry {retries}/{max_retries}")
            time.sleep(1)

    print(f"Max retries reached for address {address}")
    return None


def fetch_proof(address, index):
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(f"https://www.zksyncpepe.com/resources/proofs/{address.lower()}.json", proxies=proxies)

            if response.status_code == 200:
                if response.text:  # Check if the response content is not empty
                    proof = response.json()
                    print(f"wallet{index} {address} proof: {proof}")
                    return proof
                else:
                    print("Error: Response content is empty.")
            else:
                print(f"Error: {response.status_code}")
                print("Response content:", response.text)

        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"wallet{index} {address} Retry {retries}/{max_retries}")
            time.sleep(1)

    print(f"wallet{index} {address} Max retries reached for address")
    return None
