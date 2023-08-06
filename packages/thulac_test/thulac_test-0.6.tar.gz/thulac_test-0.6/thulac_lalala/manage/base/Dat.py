#coding: utf-8
import struct
import os


class Dat:

    def __init__(self, filename=None, datSize=None, oldDat=None):
        if(filename):
            inputfile = open(filename, "rb")
            self.datSize = int(os.path.getsize(filename) / 8)
            s = inputfile.read(8 * self.datSize)
            tmp = "<"+str(self.datSize*2)+"i"
            self.dat = struct.unpack(tmp, s)
            self.dat = tuple(self.dat)
            inputfile.close()
        else:
            self.dat = oldDat
            self.datSize = datSize


    
    def printDat(self, filename):
        f = open(filename, "w")
        for i in range(self.datSize):
            f.write(""+self.dat[2 * i]+" "+self.dat[2 * i + 1]+"\n")
        f.close()
    
    def getIndex(self, base, character):
        ind = self.dat[2 * base] + character
        if((ind >= self.datSize) or self.dat[2 * ind + 1] != base):
            return -1
        return ind
    
    def search(self, sentence, bs, es):
        bs = []
        es = []
        empty = True
        for offset in range(len(sentence)):
            preBase = 0
            preInd = 0
            ind = 0
            for i in range(offset, len(sentence)):
                ind = preBase + sentence[i]
                if(ind < 0 or ind >= self.datSize or self.dat[2 * ind + 1] != preInd):
                    break
                preInd = ind
                preBase = self.dat[2 * ind]
                ind = preBase
                if(not (ind < 0 or ind >= self.datSize or self.dat[2 * ind + 1] != preInd)):
                    bs.append(offset)
                    es.append(i + 1)
                    if(empty):
                        empty = False
        return not empty
    
    def match(self, word):
        ind = 0
        base = 0
        for i in range(len(word)):
            ind = self.dat[2 * ind] + word[i]
            if((ind > self.datSize) or (self.dat[2 * ind + 1] != base)):
                return -1
            base = ind
        ind = self.dat[2 * base]
        if((ind < self.datSize) and (self.dat[2 * ind + 1] == base)):
            return ind
        return -1

    def update(self, word, value):
        base = self.match(word)
        if(base >= 0):
            self.dat[2 * base] = value

    def getInfo(self, prefix):
        # print self.dat[:20]
        ind = 0
        base = 0
        for i in range(len(prefix)):

            # print "prefix",typeof(prefix), self.dat[2 * ind]
            ind = self.dat[2 * ind] + ord(prefix[i])
            # print "base", self.dat[2 * ind + 1], base, i
            datInd = self.dat[2 * ind + 1]
            # print datInd
            if((ind >= self.datSize) or self.dat[2 * ind + 1] != base):

                # print "fifth", self.dat[0], self.dat[2 * ind + 1], base
                # print 2 * ind + 1, len(prefix)
                return i
            base = ind
        return -base

    def getDatSize(self):
        return self.datSize
    
    def getDat(self):
        return self.dat




class DATMaker(Dat):
    def __init__(self):
        self.head = 0
        self.tail = 0
        self.datSize = 1
        self.dat = [1, -1]

    def compareWords(self, firstLex, secondLex):
        minSize = min(len(firstLex), len(secondLex))
        for i in range(minSize):
            if(firstLex[0][i] > secondLex[0][i]):
                return 1
            if(firstLex[0][i] < secondLex[0][i]):
                return -1
        return len(firstLex) < len(secondLex)  

    def use(self, ind):
        if(self.dat[2 * ind + 1] >= 0):
            print "cell reused!"
        if(self.dat[2 * ind] == 1):
            self.head = self.dat[2 * ind + 1]
            # print head
        else:
            self.dat[2 * (-self.dat[2 * ind]) +1] = self.dat[2 * ind +1]
        if(self.dat[2 * ind + 1] == -self.datSize):
            self.tail = self.dat[2 * ind]
        else:
            self.dat[2 * (-self.dat[2 * ind + 1])] = self.dat[2 * ind]
        self.dat[2 * ind + 1] = ind

    # array*2
    def extends(self):
        # print "extends"
        oldSize = self.datSize
        self.datSize *= 2
        self.dat = [self.dat[i] if i < 2*oldSize else 0 for i in range(2*self.datSize)]
        # print self.dat
        for i in range(oldSize):
            # print "dat", len(self.dat), 2 * (oldSize + i)
            self.dat[2 * (oldSize + i)] = -(oldSize + i - 1)
            self.dat[2 * (oldSize + i) + 1] = -(oldSize + i + 1)
        self.dat[2 * oldSize] = self.tail
        if(-self.tail >= 0):
            self.dat[2 * (-self.tail) + 1] = -oldSize;
        self.tail = -(oldSize * 2 - 1)

    def shrink(self):
        last = self.datSize - 1
        while(self.dat[2 * last + 1] < 0):
            last -= 1
        self.datSize = last + 1
        self.dat = [self.dat[i] for i in range(self.datSize)]

    def alloc(self, offsets):
        size = len(offsets)
        # print size, offsets
        base = -self.head

        while(1):
            if(base == self.datSize):
                self.extends()
            if(size):
                while(2 * (base + ord(offsets[size - 1])) >= self.datSize):
                    self.extends()
            flag = True
            
            # print self.dat
            if(self.dat[2 * base + 1] >= 0):
                flag = False
                # if(size == 1):

                    # print base, self.dat[2 * base + 1]
            else:
                # print 111
                for i in range(size):
                    # print ord(offsets[i]), len(self.dat)
                    # print self.dat[2 * (base + ord(offsets[i])) + 1], 2 * (base + ord(offsets[i])) + 1, base
                    if(self.dat[2 * (base + ord(offsets[i])) + 1] >= 0):
                        flag = False
                        break
            # print offsets
            if(flag):
                self.use(base)
                for i in range(size):
                    self.use(base + ord(offsets[i]))
                return base
            if(self.dat[2 * base + 1] == -self.datSize):
                self.extends()
            base = -self.dat[2 * base + 1]

    def genChildren(self, lexicon, start, prefix, children):
        del children[:]
        l = len(prefix)
        for ind in range(start, len(lexicon)):
            word = lexicon[ind][0]
            # print word.encode("utf-8")
            if(len(word) < l):
                return
            for i in range(l):
                if(word[i] != prefix[i]):
                    return
            if(len(word) > l):
                a = word[l]
                # b = children[-1]
                if(not children or word[l] != children[-1]):
                    children.append(word[l])


    def assign(self, check, offsets, isWord=False):
        base = self.alloc(offsets)
        # print base, "base"
        self.dat[2 * base] = 0
        if(isWord):
            # print 2*base+1, check
            self.dat[2 * base + 1] = check
        else:
            self.dat[2 * base + 1] = base
        for i in range(len(offsets)):
            # print "offsets", ord(offsets[i]), "base", base 
            self.dat[2 * (base + ord(offsets[i]))] = 0
            # print 2 * (base + ord(offsets[i]))
            self.dat[2 * (base + ord(offsets[i])) + 1] = check
        self.dat[2 * check] = base
        return base           

    def makeDat(self, lexicon, noPrefix=0):
        lexicon = sorted(lexicon, self.compareWords)
        size = len(lexicon)
        children = []
        prefix = ""
        self.genChildren(lexicon, 0, prefix, children)
        base = self.assign(0, children, True)
        print children
        # print "base", base
        self.dat[0] = base
        # print self.dat[:200]
        for i in range(len(lexicon)):
            
            word = lexicon[i][0]
            off = Dat.getInfo(self, word)  #下面那个for循环因为off被跳过了很多
            # print "off", off
            if(off <= 0):   
                off = len(word)
            for offset in range(off, len(word)+1):#??? range(off, off)??
                prefix = ""
                for j in range(offset):
                    prefix += word[j]
                pBase = -Dat.getInfo(self, prefix)
                self.genChildren(lexicon, i, prefix, children)
                base = self.assign(pBase,children,offset == len(word))
            off = -Dat.getInfo(self, word)

            
            self.dat[2 * self.dat[2 * off]] = lexicon[i][1]
            # print "2 * self.dat[2 * off]", 2 * self.dat[2 * off], off
        self.shrink()


if __name__ == '__main__':
    dat = DATMaker()
    lexicon = []
    f = open("userword.txt", "r")  
    for i, line in enumerate(f):  
        # line = line.split()
        lexicon.append([line.decode("utf-8"), i])
        # lexicon.append([line.decode("utf-8"), i])
    f.close()
    dat.makeDat(lexicon)
    dat.shrink
    print dat.dat[:100]
    
##word  
#
