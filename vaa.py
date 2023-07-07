
TOKEN_BRIDGE = "000000000000000000000000000000000000000000546f6b656e427269646765"
CORE_GOVERNANCE = "00000000000000000000000000000000000000000000000000000000436f7265"


class TokenBridgeAdmin:
    module: bytes
    action_id: int
    action: str

    targetChain: int
    targetEmitter: bytes

    newContract: bytes

    emitterChain: int

    # @staticmethod
    # def parse(vaa: bytes)->"TokenBridgeAdmin":
    #     tba = TokenBridgeAdmin()


    #     tba.module = vaa[off : (off + 32)].hex()
    #     off += 32

    #     ret["action"] = int.from_bytes(vaa[off : (off + 1)], "big")
    #     off += 1

    #     if ret["action"] == 1:
    #         ret["Meta"] = "TokenBridge RegisterChain"
    #         ret["targetChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
    #         off += 2
    #         ret["EmitterChainID"] = int.from_bytes(vaa[off : (off + 2)], "big")
    #         off += 2
    #         ret["targetEmitter"] = vaa[off : (off + 32)].hex()
    #         off += 32

    #     if ret["action"] == 2:
    #         ret["Meta"] = "TokenBridge UpgradeContract"
    #         ret["targetChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
    #         off += 2
    #         ret["newContract"] = vaa[off : (off + 32)].hex()
    #         off += 32

    # pass

class Governance:
    pass

class VAA:
    version: int
    idx: int
    num_sigs: int

    raw_sigs: bytes
    sigs: list[bytes]

    digest: bytes
    timestamp: int
    nonce: int
    chain: int
    emitter: bytes
    sequence: int
    consistency: int


    def __str__(self)->str:
        return f"{self.chain}/{self.emitter.hex()}/{self.sequence}: {self.consistency}"

    def segment(self)->str:
        return f"{self.emitter.hex()}|{self.consistency}"

    @staticmethod
    def parse(data: bytes) -> "VAA":
        vaa = VAA()
        vaa.version = int.from_bytes(data[0:1], "big")
        vaa.idx = int.from_bytes(data[1:5], "big")
        vaa.num_sigs = int.from_bytes(data[5:6], "big")

        vaa.raw_sigs =  data[6 : (vaa.num_sigs * 66) + 6]
        vaa.sigs = []
        for i in range(vaa.num_sigs):
            vaa.sigs.append(data[(6 + (i * 66)) : (6 + (i * 66)) + 66].hex())
        off = (vaa.num_sigs * 66) + 6

        vaa.digest = data[off:]  # This is what is actually signed...

        vaa.timestamp = int.from_bytes(data[off : (off + 4)], "big")
        off += 4

        vaa.nonce = int.from_bytes(data[off : (off + 4)], "big")
        off += 4

        vaa.chain = int.from_bytes(data[off : (off + 2)], "big")
        off += 2

        vaa.emitter = data[off : (off + 32)]
        off += 32

        vaa.sequence = int.from_bytes(data[off : (off + 8)], "big")
        off += 8

        vaa.consistency = int.from_bytes(data[off : (off + 1)], "big")
        off += 1

        return vaa

        #ret["Meta"] = "Unknown"
        #if vaa[off : (off + 32)].hex() == TOKEN_BRIDGE:

        #    ret["Meta"] = "TokenBridge"

        #    ret["module"] = vaa[off : (off + 32)].hex()
        #    off += 32

        #    ret["action"] = int.from_bytes(vaa[off : (off + 1)], "big")
        #    off += 1

        #    if ret["action"] == 1:
        #        ret["Meta"] = "TokenBridge RegisterChain"
        #        ret["targetChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2
        #        ret["EmitterChainID"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2
        #        ret["targetEmitter"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #    if ret["action"] == 2:
        #        ret["Meta"] = "TokenBridge UpgradeContract"
        #        ret["targetChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2
        #        ret["newContract"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #if vaa[off : (off + 32)].hex() == CORE_GOVERNANCE:
        #    ret["Meta"] = "CoreGovernance"

        #    ret["module"] = vaa[off : (off + 32)].hex()
        #    off += 32

        #    ret["action"] = int.from_bytes(vaa[off : (off + 1)], "big")
        #    off += 1

        #    ret["targetChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #    off += 2

        #    if ret["action"] == 2:
        #        ret["NewGuardianSetIndex"] = int.from_bytes(vaa[off : (off + 4)], "big")
        #    else:
        #        ret["Contract"] = vaa[off : (off + 32)].hex()

        #if len(vaa[off:]) == 100 and int.from_bytes(vaa[off : off + 1], "big") == 2:
        #    ret["Meta"] = "TokenBridge Attest"

        #    ret["Type"] = int.from_bytes((vaa[off : off + 1]), "big")
        #    off += 1

        #    ret["Contract"] = vaa[off : (off + 32)].hex()
        #    off += 32

        #    ret["FromChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #    off += 2

        #    ret["Decimals"] = int.from_bytes((vaa[off : off + 1]), "big")
        #    off += 1

        #    ret["Symbol"] = vaa[off : (off + 32)].hex()
        #    off += 32

        #    ret["Name"] = vaa[off : (off + 32)].hex()

        #if len(vaa[off:]) >= 133:

        #    if int.from_bytes((vaa[off : off + 1]), "big") == 1:
        #        ret["Meta"] = "TokenBridge Transfer"

        #        ret["Type"] = int.from_bytes((vaa[off : off + 1]), "big")
        #        off += 1

        #        ret["Amount"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["Contract"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["FromChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2

        #        ret["ToAddress"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["ToChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2

        #        ret["Fee"] = vaa[off : (off + 32)].hex()

        #    elif int.from_bytes((vaa[off : off + 1]), "big") == 3:
        #        ret["Meta"] = "TokenBridge Transfer With Payload"

        #        ret["Type"] = int.from_bytes((vaa[off : off + 1]), "big")
        #        off += 1

        #        ret["Amount"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["Contract"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["FromChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2

        #        ret["ToAddress"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["ToChain"] = int.from_bytes(vaa[off : (off + 2)], "big")
        #        off += 2

        #        ret["Fee"] = self.zeroPadBytes

        #        ret["FromAddress"] = vaa[off : (off + 32)].hex()
        #        off += 32

        #        ret["Payload"] = vaa[off:].hex()
