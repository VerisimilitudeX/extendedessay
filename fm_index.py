class FMIndex:
    def __init__(self, text):
        self.text = text + "$"
        self.build_index()

    def build_index(self):
        # Create suffix array
        self.suffix_array = sorted(range(len(self.text)), key=lambda i: self.text[i:])
        # Create BWT
        self.bwt = ''.join(self.text[i-1] for i in self.suffix_array)
        # Create FM-index
        self.C = {char: self.bwt.count(c) for c in set(self.bwt) for char in self.text if c < char}
        self.Occ = {char: [0] for char in set(self.text)}
        for i, char in enumerate(self.bwt):
            for c in self.Occ:
                self.Occ[c].append(self.Occ[c][-1] + (1 if c == char else 0))

    def count(self, pattern):
        start, end = 0, len(self.text) - 1
        for char in reversed(pattern):
            if char not in self.C:
                return 0
            start = self.C[char] + self.Occ[char][start]
            end = self.C[char] + self.Occ[char][end + 1] - 1
            if start > end:
                return 0
        return end - start + 1

    def locate(self, pattern):
        count = self.count(pattern)
        if count == 0:
            return []
        start = self.C[pattern[-1]] + self.Occ[pattern[-1]][0]
        return [self.suffix_array[start + i] for i in range(count)]