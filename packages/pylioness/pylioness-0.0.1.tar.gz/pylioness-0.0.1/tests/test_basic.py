
import os
import binascii

from pylioness.lioness import AES_SHA256_Lioness, Chacha20_Blake2b_Lioness


def test_AES_SHA256_Lioness_end_to_end():
    plaintext = b"'What do we know,' he had said, 'of the world and the universe about us? Our means of receiving impressions are absurdly few, and our notions of surrounding objects infinitely narrow. We see things only as we are constructed to see them, and can gain no idea of their absolute nature. With five feeble senses we pretend to comprehend the boundlessly complex cosmos, yet other beings with wider, stronger, or different range of senses might not only see very differently the things we see, but might see and st"
    key = os.urandom(96)
    c = AES_SHA256_Lioness(key, len(plaintext))
    ciphertext = c.encrypt(plaintext)
    assert len(plaintext) == len(ciphertext)
    output = c.decrypt(ciphertext)
    assert len(output) == len(ciphertext)
    assert output == plaintext


def test_Chacha20_Blake2_Lioness_end_to_end():
    plaintext = b"'What do we know,' he had said, 'of the world and the universe about us? Our means of receiving impressions are absurdly few, and our notions of surrounding objects infinitely narrow. We see things only as we are constructed to see them, and can gain no idea of their absolute nature. With five feeble senses we pretend to comprehend the boundlessly complex cosmos, yet other beings with wider, stronger, or different range of senses might not only see very differently the things we see, but might see and st"
    key = os.urandom(Chacha20_Blake2b_Lioness.KEY_LEN)
    c = Chacha20_Blake2b_Lioness(key, len(plaintext))
    ciphertext = c.encrypt(plaintext)
    assert len(plaintext) == len(ciphertext)
    output = c.decrypt(ciphertext)
    assert len(output) == len(ciphertext)
    assert output == plaintext


def test_vectors_Chacha20_Blake2_Lioness():
    vectors = [
        (
            binascii.unhexlify("0f2c69732932c99e56fa50fbb2763ad77ee221fc5d9e6c08f89fc577a7467f1ee34" +
                               "003440ee2bfbfaac60912b0e547fbe9a6a9292db70bc718c6f2773ab198ac8f25537" +
                               "8f7ea799e1d4b8596079173b6e443c416f13195f1976acc03d53a4b8581b609df3b7" +
                               "029d5b487051d5ae4189129c045edc8822e1f52e30251e4b322b3f6d6e8bb0ddb057" +
                               "8dcba41603abf5e51848c84d2082d293f30a645faf4df028ee2c40853ea33e40b55f" +
                               "ca902371dc00dc1e0e77161bd097a59e8368bf99174d9"),
            binascii.unhexlify("5ac4cb9674a8908915a2b1aaf2043271612531911a26186bd5c811951330753a0e3259f3fcf52f" +
                               "b86e666ab4d96243e57d73b976611f928d44ad137799016861576ca0a6b8a8a9e2ea02db71e71c" +
                               "9654e476ca845c44456eba62f11f004b222756e485185c446c30b7a05cf9acd53b3131227b428d" +
                               "a5c9601664d45ae5c2387956307961a0680894844190605dce0c86e597105884e151eb8a005eda" +
                               "08ff5891a6b40bae299cddad979063a9a356f3477feabb9cc7bd80a1e2d6a419fcd8af9e98f7b1" +
                               "93c71bd6056d7634b8c2b8f85920f314554104659e52d9266ddbc2ac40c1b875f6b00225f832cf" +
                               "310e139ad8cc2568608f0323534fa15a84280e776e7e1167a001f6e18c49f3cd02c19837da47ac" +
                               "091219ee2fdb4458836db20cbd362bb65add9b40f2817f666caf19787abc2013737eea8c7552d7" +
                               "55a29beba5da31956f75fe7628221fe8d0a75da5bee39af956a2246c5a339560dcf029eb76d191" +
                               "963354b70142df29ec69930977ce2f0e491513664ce83a8fa75f3e698530cf9dafbdb90b19745e" +
                               "9257d03d7320c6d306f529eda242cb3f6f452a943f6e1c04eb02cbb0368d79e49a2b42ac3ff7cd" +
                               "9a5686bfdb90a29322016bbcef5c733f451a9f4ea7c534116158eb611796d47b83ffe7cd6e6c11" +
                               "d56e2d26c7a386853212a2f92efeabc74e8fe69e3d374d7b033d0ec9862221435b14ad534217ad" +
                               "7da50bc236"),
            binascii.unhexlify("9eb45ca2ca4d0b6ff05a749511aad1357aa64caf9ce547c7388fe24fd1300fe856bb5c396869a" +
                               "cd21c45805e6a7c8a1b7f71cc5f0ea9dd0c4ecd4bba9a7a4853bc352bc9f6562e9907973f91fb" +
                               "cf7c710f5a89abc8eb4489b90e8111cbf85ffd595d603268ddceb40e39e747a4e7bd5c965585b" +
                               "6964e180bd6ccb9d0fad210c7f7dd6f90cf6db9bda70d41d3922cedec5ea147ef318de5f34e6f" +
                               "e5bd646859a9d4171b973b6b58c8d7f94bc9eb293c197f3408a51e3626196e3f6bca625cef90f" +
                               "a7a3e3713bdaebdda82f48db1a97c9ed5c48bc419dbc3d1f9ef43d1b17dd83c966bde9d9360b7" +
                               "cdac0871844c27921dcf3bb7edce9fb24661a41a8f92c8502925f062e9cd2f77c561e5825eae2" +
                               "11657652330bc64cd63b18d1014975f167f8b68d6e702dd3d3547971662238216cc5b07517cc9" +
                               "0aaa49a61ee423861cdc49c0e1f64e086007095a00f8adb0314fd85c88158001202edf2ed43c2" +
                               "01176d6141e469dd89430352a927ee22a41c62c8cfdfd5d592e76793e58a9c63b7fe6dad335d7" +
                               "acec90727675854d7708358115794e013bb4fdb504c44e21ce500f764fac211e8de20b81ca55f" +
                               "c778ace024d2a40045241e71b023ceb519c8c28285c333b9f90f5e2cde21ca6744e43f89d0054" +
                               "5dd34df072c7214f6cbd2123c4b0613614609961dd855d6d611c3018e4df3550b4e93f33f7c3e" +
                               "8b2c890ca0405c957aa277d"),
        ),
    ]

    for v in vectors:
        key = v[0]
        plaintext = v[1]
        want = v[2]
        c = Chacha20_Blake2b_Lioness(key, len(plaintext))
        ciphertext = c.encrypt(plaintext)
        assert ciphertext == want
