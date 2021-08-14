import bls from 'bls-wasm';
import bip39 from 'bip39'
import sha3 from 'js-sha3'
import axios from 'axios'

await bls.init(bls.BN254)

function hexStringToByte(str) {
    if (!str) {
        return new Uint8Array();
    }
    var a = [];
    for (var i = 0, len = str.length; i < len; i += 2) {
        a.push(parseInt(str.substr(i, 2), 16));
    }
    return new Uint8Array(a);
}

const generate_keys = async (mnemonic) => {
    const seed = await bip39.mnemonicToSeed(mnemonic, "0chain-client-split-key");
    const buffer = new Uint8Array(seed)
    const blsSecret = new bls.SecretKey();

    bls.setRandFunc(buffer)
    blsSecret.setLittleEndian(buffer)

    const public_key = blsSecret.getPublicKey().serializeToHexStr();
    const private_key = blsSecret.serializeToHexStr();
    const client_id = sha3.sha3_256(hexStringToByte(public_key));

    const output = public_key + ' ' + private_key + ' ' + client_id
    return {
        public_key: public_key,
        private_key: private_key,
        client_id: client_id
    }
    // process.stdout.write(output)
}


const args = process.argv.slice(2)
const mnemonic = args[0]

const makeRequest = async () => {
    const mnemonic = 'capable gloom call way exact lift include diagram paddle mutual penalty cluster doctor apology slab vapor squirrel answer blanket clinic subway rally topic acid'
    const keys = await generate_keys(mnemonic)
    const data = {}
    console.log(keys)
    data.id = keys.client_id
    data.public_key = keys.public_key
    const url = 'https://beta.0chain.net/miner01/v1/client/put'

    axios({
        method: 'post',
        url: url,
        data: data,
    }).then(res => {
        console.log(res.data)
    })

}

makeRequest()