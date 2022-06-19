import math
from base64 import b32decode, b32encode
from secrets import token_bytes

import click
from allmydata.util.hashutil import (
    ssk_pubkey_fingerprint_hash,
    ssk_readkey_hash,
    ssk_writekey_hash,
)
from blake3 import blake3
from Cryptodome.PublicKey import RSA
from mnemonic import Mnemonic


def pad(s: str) -> str:
    """
    Add the missing number of trailing "=" characters necessary to
    produce a valid base32-encoded string.

    Tahoe-LAFS truncates trailing "=" characters from base32-encoded
    cap components; this function adds them back.
    """
    n = len(s)
    return s + "=" * (math.ceil(n / 8) * 8 - n)


def capencode(b: bytes) -> str:
    return b32encode(b).decode().rstrip("=").lower()


def capdecode(s: str) -> bytes:
    return b32decode(pad(s.upper()))


def to_mnemonic(b: bytes) -> list[str]:
    return Mnemonic(language="english").to_mnemonic(b).split(" ")


def to_bytes(mnemonic: list[str]) -> bytes:
    return bytes(Mnemonic(language="english").to_entropy(mnemonic))


def to_words(cap: str) -> list[str]:
    s = cap.split(":")
    return to_mnemonic(capdecode(s[2])) + to_mnemonic(capdecode(s[3]))


def to_cap(words: list[str], cap_type: str = "MDMF") -> str:
    a = capencode(to_bytes(words[0:12]))
    b = capencode(to_bytes(words[12:]))
    return f"URI:{cap_type}:{a}:{b}"


def generate_rsa_keypair(seed: bytes, bits: int = 2048) -> tuple[bytes, bytes]:
    hasher = blake3(seed, derive_key_context="Deterministic RSA PRNG v1")

    def prng_bytes(n: int) -> bytes:
        hasher.update(hasher.digest())
        return hasher.digest(length=n)

    rsa_key = RSA.generate(bits, randfunc=prng_bytes, e=65537)
    return rsa_key.export_key("DER"), rsa_key.public_key().export_key("DER")


def generate_mutable_filecap(seed: bytes) -> str:
    priv_key, pub_key = generate_rsa_keypair(seed)
    writekey = capencode(ssk_writekey_hash(priv_key))
    fingerprint = capencode(ssk_pubkey_fingerprint_hash(pub_key))
    return f"URI:MDMF:{writekey}:{fingerprint}"


def diminish(cap: str) -> str:
    s = cap.split(":")
    cap_type = s[1]
    diminishers = {"MDMF": ssk_readkey_hash}
    diminished = capencode(diminishers[cap_type](capdecode(s[2])))
    return f"URI:{cap_type}-RO:{diminished}:{s[3]}"


@click.group()
def main() -> None:
    pass


@click.command("generate")
@click.argument("words", nargs=-1)
def _generate(words: tuple) -> None:
    if words:
        click.echo(generate_mutable_filecap(to_bytes(list(words))))
    else:
        seed = token_bytes(16)
        cap = generate_mutable_filecap(seed)
        click.echo(" ".join(to_mnemonic(seed)))
        click.echo(cap)
        click.echo(diminish(cap))


@click.command("diminish")
@click.argument("cap", nargs=1)
def _diminish(cap: str) -> None:
    click.echo(diminish(cap))


@click.command("to-words")
@click.argument("cap", nargs=1)
def _to_words(cap: str) -> None:
    click.echo(" ".join(to_words(cap)))


@click.command("to-cap")
@click.argument("words", nargs=-1)
def _to_cap(words: tuple) -> None:
    click.echo(to_cap(list(words)))


main.add_command(_generate)
main.add_command(_diminish)
main.add_command(_to_words)
main.add_command(_to_cap)


if __name__ == "__main__":
    main()
