import random

__all__ = ['GodNameGenerator', 'generate']


MIDDLE_CHARS = [(1.5, 'll'), (1, 'mn'), (1, 'm'), (2.3, 'z'), (1.2, 'n'),
                (1.2, 'p'), (1, 'd'), (2, 'rh'), (1.1, 'g'), (1.3, 'r')]
CONSONANT_CHARS = [(1, 'th'), (1, 's'), (1, 'r'), (1.5, 'h'), (0.8, 'th'),
                   (0.8, 'sh'), (0.3, 'j'), (1.1, 'n'), (1, 'l')]
VOWEL_CHARS = [(3.2, 'a'), (3.2, 'e'), (2.6, 'u'), (2.9, 'o'), (0.9, 'ae'),
               (0.5, 'ea'), (0.5, 'eu')]
ENDING_CHARS = [(1.2, 'es'), (1.2, 'os'), (1, 'on'), (1.2, '')]


def random_weighted_choice(choices):
    total = sum(weight for weight, value in choices)
    random_val = random.uniform(0, total)
    up_to = 0
    for weight, value in choices:
        if random_val <= up_to + weight:
            return value
        up_to += weight


class GodNameGenerator(object):
    def __init__(self, seed=None, min_len=4, max_len=8):
        if seed is not None:
            random.seed(seed)
        self.min_len = min_len
        self.max_len = max_len

    def generate_one(self):
        self.length = random.randrange(self.min_len, self.max_len)
        self.count = 0
        result = random_weighted_choice(ENDING_CHARS)
        return self._from_vowel(result)

    def generate(self, n=1):
        if n < 1:
            raise ValueError()
        elif n == 1:
            return self.generate_one()
        else:
            return [self.generate_one() for i in range(n)]

    def _from_vowel(self, string):
        self.count += 1
        if ((self.count >= self.length-1) or
            bool(random.getrandbits(1))):
            string = random_weighted_choice(CONSONANT_CHARS) + string
            return self._from_consonant(string)
        else:
            string = random_weighted_choice(MIDDLE_CHARS) + string
            return self._from_middle(string)

    def _from_consonant(self, string):
        self.count += 1
        if self.count < self.length:
            string = random_weighted_choice(VOWEL_CHARS) + string
            return self._from_vowel(string)
        else:
            return string

    def _from_middle(self, string):
        self.count += 1
        string = random_weighted_choice(VOWEL_CHARS) + string
        return self._from_vowel(string)


_gen = GodNameGenerator()
generate = _gen.generate


if __name__ == "__main__":
    print(generate())
