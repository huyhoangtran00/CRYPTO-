import fastapi
from pydantic import *
from runner import *
from fastapi.middleware.cors import CORSMiddleware
from algorithms.helper import *

app = fastapi.FastAPI()

frontend_url = "http://localhost:3000"
origins = [frontend_url]


# RSA
class MessageInput(BaseModel):
    message: str


class RSADecryptInput(BaseModel):
    encrypted: str  # khong can tach
    private_key: str  # (d,n)


class RSAVerifyInput(BaseModel):
    message: str
    signature: str
    public_key: str  # (e,n)


class ElGamalDecryptInput(BaseModel):
    encrypted: str  # (c1, c2)
    private_key: str  # (p, a)


class ElGamalVerifyInput(BaseModel):
    message: str
    signature: str  # (sig_1, sig_2)
    alpha: str  # Số nguyên n dạng chuỗi
    beta: str
    p: str


class ECDSADecryptInput(BaseModel):
    c_1: str
    c_2: str
    private_key: str


class ECDSASignatureInput(BaseModel):
    message: str
    private_key: str  # so ngau nhien minh chon


class ECDSAVerifyInput(BaseModel):
    message: str
    signature: str  # (r,s)
    public_key: str  # (x,y)


@app.get("/")
def read_root():
    return {"Status": "Active"}


@app.post("/rsa-encrypt")
async def rsa_encrypt(input_data: MessageInput):
    result = await run_rsa_enc(input_data.message)
    return result


@app.post("/rsa-decrypt")
async def rsa_decrypt(input_data: RSADecryptInput):
    encrypted = int(input_data.encrypted)
    private_key = input_data.private_key
    d, n = split_key(private_key)
    result = await run_rsa_dec(encrypted, d, n)

    return result


@app.post("/rsa-signature")
async def rsa_signature(input_data: MessageInput):
    result = await run_rsa_sig(input_data.message)
    return result


@app.post("/rsa-verify")
async def rsa_verify(input_data: RSAVerifyInput):
    message = str(input_data.message)

    # ElGamal
    signature = int(input_data.signature)
    public_key = input_data.public_key
    e, n = split_key(public_key)
    pubkey = (e, n)
    result = await run_rsa_ver(message, signature, pubkey)
    return result


@app.post("/elgamal-encrypt")
async def elgamal_encrypt(input_data: MessageInput):
    result = await run_elgamal_enc(input_data.message)
    return result


@app.post("/elgamal-signature")
async def elgamal_signature(input_data: MessageInput):
    result = await run_elgamal_sig(input_data.message)
    return result


@app.post("/elgamal-decrypt")
async def elgamal_decrypt(input_data: ElGamalDecryptInput):
    encrypted = input_data.encrypted
    c_1, c_2 = split_key(encrypted)
    private_key = input_data.private_key
    p, a = split_key(private_key)
    result = await run_elgamal_dec(c_1, c_2, a, p)
    return result


@app.post("/elgamal-verify")
async def elgamal_verify(input_data: ElGamalVerifyInput):
    message = str(input_data.message)
    signature = input_data.signature
    sig_1, sig_2 = split_key(signature)
    alpha = int(input_data.alpha)
    beta = int(input_data.beta)
    p = int(input_data.p)
    result = await run_elgamal_ver(message, sig_1, sig_2, alpha, beta, p)
    return result


# EcElgamal - encrypt
@app.post("/ecelgamal-encrypt")
async def ecelgamal_encrypt(input_data: MessageInput):
    result = await run_ecelgamal_enc(input_data.message)
    return result


# ECElGamal (ECDSA) - Signature
@app.post("/ecdsa-signature")
async def ecelgamal_signature(input_data: ECDSASignatureInput):
    result = await run_ecelgamal_sig(input_data.message, int(input_data.private_key))
    return result


# ECElGamal (ECDSA) - Decrypt
@app.post("/ecelgamal-decrypt")
async def ecelgamal_decrypt(input_data: ECDSADecryptInput):
    c_1 = input_data.c_1
    c_2 = input_data.c_2
    C_1 = split_key(c_1)
    C_2 = split_key(c_2)
    private_key = int(input_data.private_key)
    result = await run_ecelgamal_dec((C_1, C_2), private_key)
    return result


# ECElGamal (ECDSA) - Verify
@app.post("/ecdsa-verify")
async def ecelgamal_verify(input_data: ECDSAVerifyInput):
    message = str(input_data.message)
    signature = input_data.signature
    signatures = split_key(signature)
    public_key = input_data.public_key
    publickey = split_key(public_key)
    result = await run_ecelgamal_ver(message, signatures, publickey)
    return result


@app.post("/aks-check-prime")
async def check_prime(data: MessageInput):
    n = int(data.message)
    return {"is_prime": f"{aks_prime_test(n)}"}


# @app.get("")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, modify this as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/messages")
async def read_root():
    # encrypted_message, rsa_obj = runner.rsa_runner(message)
    encrypted_message, rsa_obj = runner.rsa_cryptography("BUIDUCANH")
    return {"message": str(hex(encrypted_message))}


@app.post("/api/rsa/")
async def rsa_cryptography_api(data: MessageInput):
    encrypted_message, rsa_obj = runner.rsa_cryptography(data.message)
    return {"message": str(hex(encrypted_message))}
