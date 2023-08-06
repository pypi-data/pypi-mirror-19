
import os
import time
import binascii

from pylioness.lioness import AES_SHA256_Lioness, Chacha20_Blake2b_Lioness


def test_timing_Chacha20_Blake2_Lioness():
    key = binascii.unhexlify("6fb8e9fb1899057ed6f5ded81288d9ff75fea899f697fb1aea588d9fa50ab6f2a6154fe7fba935720ecf07495a21761bb864d6931eb853a804a9dee71c37a8cbbc3a55247f5e44fa6f071470f5dbdf30de773da440783caf98ecf8de166e1e5248b3ba40b58bb15ce9274651a0c80cc65310a2f484eb15fe605102749f20c9be438c214a178360b4aa36ade0e8cf53d5d35982a8f6fcc91597deb3eb5a6656218abd1958ac483381e6a145e4f0934bca72cd8ec107b7de22e4600317282b7c6b")
    block = b"'What do we know,' he had said, 'of the world and the universe about us? Our means of receiving impressions are absurdly few, and our notions of surrounding objects infinitely narrow. We see things only as we are constructed to see them, and can gain no idea of their absolute nature. With five feeble senses we pretend to comprehend the boundlessly complex cosmos, yet other beings with wider, stronger, or different range of senses might not only see very differently the things we see, but might see and st"
    t0 = time.time()
    for _ in range(100):
        c = Chacha20_Blake2b_Lioness(key, len(block))
        ciphertext = c.encrypt(block)
    t1 = time.time()
    c = ciphertext
    print("Time per chacha20+blake2 lioness block encrypt: %.2fms" % ((t1 - t0) * 1000.0 / 100))


def test_timing_AES_SHA256_Lioness():
    block = b"'What do we know,' he had said, 'of the world and the universe about us? Our means of receiving impressions are absurdly few, and our notions of surrounding objects infinitely narrow. We see things only as we are constructed to see them, and can gain no idea of their absolute nature. With five feeble senses we pretend to comprehend the boundlessly complex cosmos, yet other beings with wider, stronger, or different range of senses might not only see very differently the things we see, but might see and st"
    key = os.urandom(96)
    t0 = time.time()
    for _ in range(100):
        c = AES_SHA256_Lioness(key, len(block))
        ciphertext = c.encrypt(block)
    t1 = time.time()
    c = ciphertext
    print("Time per aes_ctr+sha256 lioness block encrypt: %.2fms" % ((t1 - t0) * 1000.0 / 100))
