def compute_letter_frequency(word: str) -> str:
    """
    Return a 26-character string representing the frequency of letters a-z.
    For example, 'stressed' -> '01300100000000000000000000'
    """
    freq = [0] * 26
    for ch in word.lower():
        idx = ord(ch) - ord('a')
        if 0 <= idx < 26:
            freq[idx] += 1
    return ''.join(map(str, freq))
