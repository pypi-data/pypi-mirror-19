#! /usr/bin/env python
from collections import defaultdict

import sys


class Args:
    d = defaultdict(list)
    synonyms = defaultdict(list)
    callbacks = defaultdict(list)

    def register(self, callback, n_args=0, synonyms=None):
        if not synonyms:
            synonyms = []
        word = callback.__name__
        if not self.d[word]:
            self.d[word] = [callback, n_args]
            self.synonyms[word] = synonyms

    def act(self, args):
        l = len(args)
        i = 0
        while i < l:
            a = self.resolve_word(args[i])
            if a in self.d:
                callback = self.d[a][0]
                n = self.d[a][1]
                callargs = []
                for j in range(n):
                    callargs.append(args[i + j + 1])
                i += n + 1
                self.callbacks[callback] = callargs
                callback(*callargs)
            else:
                print 'Unknown argument', a
                i += 1

    def resolve_word(self, word):
        if word in self.d:
            return word
        else:
            for key in self.synonyms:
                if word in self.synonyms[key]:
                    return key
        return None


if __name__ == "__main__":
    class testclass:
        def playfrom(self, n):
            print 'playing from', n

        def shuffle(self):
            print 'shuffling'


    def printversion():
        print 'V1.0.1.4.3.5.0.9'


    tc = testclass()

    args = Args()
    args.register(tc.playfrom, 1, ['from', 'fr'])
    args.register(tc.shuffle, 0, ['shuf', 'shuff', 'shuffle'])
    args.register(printversion, 0)

    print args.synonyms
    print args.d
    args.act(sys.argv[1:])
