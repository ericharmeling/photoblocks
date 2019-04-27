from flask import request


def mine(blockchain):
    # Form data
    image_file = request.files['file']
    image_loc = blockchain.dir + image_file.filename
    label = request.form['label']
    last_label = request.form['last_label']
    n_key = request.form['node_key']

    # Store image file on server
    image_file.save(image_loc)

    # Go through data
    blockchain.last_labels.append(last_label)
    iter_block = blockchain.new_block(image_loc, label, blockchain.transactions)
    proof = blockchain.proof_of_work(iter_block)
    block = blockchain.new_block(image_loc, label, blockchain.transactions, nonce=proof)

    blockchain.add_block(block)
    blockchain.transactions = []
    blockchain.add_transaction_fields(sender="God", recipient=n_key, quantity=1)

    return block, 200
