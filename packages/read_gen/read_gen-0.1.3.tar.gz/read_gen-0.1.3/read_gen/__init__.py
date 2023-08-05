#!/usr/bin/env python

__version__ = '0.1.3'
__description__ = 'Produce error-prone reads from a generated sequence'

import random

class ReadGen:
    def __init__(self, l, n, sl, e,
        nucleotide_error_rate=0.02, with_indels=True, read_length_variation=0.1, alphabet='AGCT',
        with_original=True, note=None, fastafy=True
    ):
        # These probably shouldn't be modified after initialisation.
        self.l = l
        self.n = n
        self.sl = sl
        self.e = e
        self.ne = nucleotide_error_rate
        self.with_indels = with_indels
        self.read_length_variation = read_length_variation
        self.alphabet = set(alphabet)
        self.with_original = with_original
        self.note = note
        self.fastafy = fastafy
    
        self.seq = ''.join([random.sample(self.alphabet, 1)[0] for i in range(self.sl)])
        self.id_prefix = 'readgen-'

        self._do_errs = e > 0 and len(alphabet) > 1
        self._read_id_cursor = 0

    def fudge_read(self, read):
        # `self.e` chance that this read is erroneous.
        if random.random() >= self.e:
            return read

        # Now that the read is a problem there's `self.ne` chance
        # per nucleotide position for an error.
        delta = 0
        for pos_i in range(len(read)):
            # `delta` will maintain correct positioning as characters are inserted or deleted.
            pos = pos_i + delta

            if random.random() < self.ne:
                # Substitute, insert or delete?
                err_mode = random.randint(0, 2) if self.with_indels else 0
                if err_mode == 0: # Substitute!
                    cur = read[pos]

                    new = cur
                    while new == cur: new = random.sample(self.alphabet, 1)[0]

                    read = read[0:pos] + new + read[pos + 1:]
                elif err_mode == 1: # Insert!
                    read = read[0:pos] + random.sample(self.alphabet, 1)[0] + read[pos:]
                    delta += 1
                else: # Delete!
                    read = read[0:pos] + read[pos + 1:]
                    delta -= 1

        return read

    def fastafy_read(self, read, orig):
        self._read_id_cursor += 1

        return '>' + self.id_prefix + str(self._read_id_cursor) + \
            (' ' + orig if self.with_original else '') + \
            (' ' + self.note if self.note else '') + \
            '\n' + read

    def __iter__(self):
        if self.l <= 0 or self.n <= 0 or self.sl <= 0: raise StopIteration()

        var = self.read_length_variation

        for read_i in range(self.n):
            _l = int(round(self.l * (1 - var + random.random() * var * 2))) if var else self.l
            _l = min(_l, self.sl)

            pos = random.randint(0, self.sl - _l)
            read = self.seq[pos:pos + _l]
            orig = read

            if self._do_errs: read = self.fudge_read(read)
            if self.fastafy: read = self.fastafy_read(read, orig)

            yield read

