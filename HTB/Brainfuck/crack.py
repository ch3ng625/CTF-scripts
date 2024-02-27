def crack(pt, enc):
    chars = "abcdefg"
    print(f"pt : {pt}")
    print(f"enc: {enc}")
    # enc = pt + key (mod 26)
    # key = enc - pt (mod 26)
    print("key: ", end="")
    for i in range(len(pt)):
        if pt[i].isalpha():
            key = (ord(enc[i]) - ord(pt[i])) % 26
            print(chr(key + ord('a')), end='')
        else:
            print(' ', end='')
    print("")
    return

def main():
    orig = "Orestis - Hacking for fun and profit"

    enc1 = "Pieagnm - Jkoijeg nbw zwx mle grwsnn"
    enc2 = "Wejmvse - Fbtkqal zqb rso rnl cwihsf"
    enc3 = "Qbqquzs - Pnhekxs dpi fca fhf zdmgzt"

    crack(orig, enc1)
    print()

    crack(orig, enc2)
    print()

    crack(orig, enc3)
    return

main()