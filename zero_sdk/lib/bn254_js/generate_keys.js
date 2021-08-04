import bls from 'bls-wasm';
import bip39 from 'bip39'

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

    const output = public_key + ' ' + private_key
    process.stdout.write(output)
}


const args = process.argv.slice(2)
const mnemonic = args[0]

generate_keys(mnemonic)