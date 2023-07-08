TOKEN_BRIDGE = "000000000000000000000000000000000000000000546f6b656e427269646765"
CORE_GOVERNANCE = "00000000000000000000000000000000000000000000000000000000436f7265"

SIG_LENGTH = 66


class VAA:
    version: int
    idx: int
    num_sigs: int
    sigs: list[str]
    timestamp: int
    nonce: int
    chain: int
    emitter: str
    sequence: int
    consistency: int

    extra: dict[str, int | str]

    def __str__(self) -> str:
        return f"{self.chain}/{self.emitter}/{self.sequence}: {self.consistency}"

    def segment(self) -> str:
        return f"{self.emitter}|{self.consistency}"

    @staticmethod
    def parse(data: bytes) -> "VAA":
        vaa = VAA()

        off = 0

        vaa.version, off = as_int(data, off, 1)
        vaa.idx, off = as_int(data, off, 4)
        vaa.num_sigs, off = as_int(data, off, 1)

        vaa.sigs = []
        for _ in range(vaa.num_sigs):
            sig, off = as_hex(data, off, SIG_LENGTH)
            vaa.sigs.append(sig)

        vaa.timestamp, off = as_int(data, off, 4)
        vaa.nonce, off = as_int(data, off, 4)
        vaa.chain, off = as_int(data, off, 2)
        vaa.emitter, off = as_hex(data, off, 32)
        vaa.sequence, off = as_int(data, off, 8)
        vaa.consistency, off = as_int(data, off, 1)

        extra: dict[str, int | str] = {"Meta": "Unknown"}

        if data[off : off + 32].hex() == TOKEN_BRIDGE:
            extra["Meta"] = "TokenBridge"

            extra["Module"], off = as_hex(data, off, 32)
            extra["Action"], off = as_int(data, off, 1)

            if extra["Action"] == 1:
                extra["Meta"] = "TokenBridge RegisterChain"
                extra["TargetChain"], off = as_int(data, off, 2)
                extra["EmitterChainID"], off = as_int(data, off, 2)
                extra["TargetEmitter"], off = as_hex(data, off, 32)
            elif extra["Action"] == 2:
                extra["Meta"] = "TokenBridge UpgradeContract"
                extra["TargetChain"], off = as_int(data, off, 2)
                extra["NewContract"], off = as_hex(data, off, 32)

        if data[off : off + 32].hex() == CORE_GOVERNANCE:
            extra["Meta"] = "CoreGovernance"

            extra["Module"], off = as_hex(data, off, 32)
            extra["Action"], off = as_int(data, off, 1)
            extra["TargetChain"], off = as_int(data, off, 2)

            if extra["Action"] == 2:
                extra["NewGuardianSetIndex"], off = as_int(data, off, 4)
            else:
                extra["Contract"], off = as_hex(data, off, 32)

        if len(data[off:]) >= 100:
            payload_type, off = as_int(data, off, 1)
            match payload_type:
                case 1:
                    extra["Meta"] = "TokenBridge Transfer"
                    extra["Type"] = payload_type

                    extra["Amount"], off = as_hex(data, off, 32)
                    extra["TokenContract"], off = as_hex(data, off, 32)
                    extra["TokenChain"], off = as_int(data, off, 2)

                    extra["ToAddress"], off = as_hex(data, off, 32)
                    extra["ToChain"], off = as_int(data, off, 2)
                    extra["Fee"], off = as_hex(data, off, 32)
                case 2:
                    extra["Meta"] = "TokenBridge Attest"
                    extra["Type"] = payload_type

                    extra["TokenContract"], off = as_hex(data, off, 32)
                    extra["TokenChain"], off = as_int(data, off, 2)
                    extra["Decimals"], off = as_int(data, off, 1)
                    extra["Symbol"], off = as_hex(data, off, 32)
                    extra["Name"], off = as_hex(data, off, 32)
                case 3:
                    extra["Meta"] = "TokenBridge Transfer With Payload"
                    extra["Type"] = payload_type

                    extra["Amount"], off = as_hex(data, off, 32)
                    extra["TokenContract"], off = as_hex(data, off, 32)
                    extra["TokenChain"], off = as_int(data, off, 2)
                    extra["ToAddress"], off = as_hex(data, off, 32)
                    extra["ToChain"], off = as_int(data, off, 2)
                    extra["FromAddress"], off = as_hex(data, off, 32)
                    extra["Payload"] = data[off:].hex()

                    extra["Fee"] = bytes(32).hex()

        else:
            extra["Raw"] = data[off:].hex()

        vaa.extra = extra
        return vaa


def as_int(data: bytes, off: int, len: int) -> tuple[int, int]:
    val = int.from_bytes(data[off : off + len], "big")
    return (val, off + len)


def as_hex(data: bytes, off: int, len: int) -> tuple[str, int]:
    return (data[off : off + len].hex(), off + len)
