from web3 import Web3
import logging

from fetch_balance_and_proof import fetch_proof, fetch_balance
from wallet import generalWallet

# 配置日志记录到文件
logging.basicConfig(filename='zkpepe_airdrop.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 连接到以太坊节点
w3 = Web3(
    Web3.HTTPProvider('xxx'))

# 合约地址和ABI
contract_address = '0x95702a335e3349d197036Acb04BECA1b4997A91a'
merkleRoot = '0xe9b832036112edb10e685c24b9341fe66008845bf4888fa21bd4f80ecef46a19'
contract_abi = [
    {
        "constant": False,
        "inputs": [
            {
                "name": "proof",
                "type": "bytes32[]"
            },
            {
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "claim",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# 实例化合约对象
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


# 发送交易
def send_transaction(proof, amount, private_key):
    acct = w3.eth.account.from_key(private_key)

    try:
        transaction = contract.functions.claim(proof, amount).build_transaction({
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address),
        })
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
        transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        print(f'{acct.address} get zkpepe airdrop: {amount/10**18} Transaction Hash: {transaction_hash.hex()}\n')
        logging.info(f'{acct.address} get zkpepe airdrop: {amount/10**18} Transaction Hash: {transaction_hash.hex()}')
        return transaction_hash.hex()
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    # 遍历地址
    for wallet in generalWallet:
        address = wallet["address"]
        index = wallet["index"]
        proof = fetch_proof(address, index)
        amount = fetch_balance(address, index)
        if proof is None or amount is None:
            continue

        send_transaction(proof, amount * 10 ** 18, wallet["privateKey"])