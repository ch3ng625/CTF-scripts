def decrypt(enc, key):
    keylen = len(key)
    index = 0
    for i in range(len(enc)):
        if enc[i].isalpha():
            # pt = enc - key (mod 26)
            k = index % keylen
            pt = (ord(enc[i].lower()) - ord(key[k]) + 26) % 26
            pt += ord('a')
            if enc[i].isupper():
                print(chr(pt).upper(), end="")
            else:
                print(chr(pt), end="")
            index += 1
        else:
            # ignore non-alphabetic characters
            print(enc[i], end="")
    print()
    print()
    return

def main():
    key = "fuckmybrain"

    messages = [
        "Mya qutf de buj otv rms dy srd vkdof :)\nPieagnm - Jkoijeg nbw zwx mle grwsnn",
        "Xua zxcbje iai c leer nzgpg ii uy...",
        "Ufgoqcbje....\nWejmvse - Fbtkqal zqb rso rnl cwihsf",
        "Ybgbq wpl gw lto udgnju fcpp, C jybc zfu zrryolqp zfuz xjs rkeqxfrl ojwceec J uovg :)\nmnvze://zsrivszwm.rfz/8cr5ai10r915218697i1w658enqc0cs8/ozrxnkc/ub_sja",
        "Si rbazmvm, Q'yq vtefc gfrkr nn ;)\nQbqquzs - Pnhekxs dpi fca fhf zdmgzt"
        ]
    
    for msg in messages:
        decrypt(msg, key)

    return

main()