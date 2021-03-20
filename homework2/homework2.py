# CS 6320 - Natural Language Processing - Spring 2021
# Written by Kamin Bouguyon
# Homework 2: N-Grams
# Goal: Train a Bigram model and evaluate against 2 example sentences.

import sys

outFile = 'out.txt'

testsentence1 = 'but if she continued to play whenever she was asked by mr .'
testsentence2 = 'miss fairfax must have found the evening pleasant , emma .'

vocab = {}

def sumList(list):
    sum = 0
    for i in list:
        sum += i
    return sum

def writeMatrix(title, labels, matrix):
    o = open(outFile, 'a')
    # matrix title
    o.write(f'\t\t{title}\n')
    labels.insert(0, '<s>')

    # matrix top labels
    format_row = '{:>10}|' * (len(labels) + 1)
    o.write(format_row.format("", *labels))
    o.write('\n')

    # matrix side labels and body
    for label, row in zip(labels, matrix):
        mapped = map(lambda c : f'{c: 0.4f}' if type(c) is float else c, row)
        o.write(format_row.format(label, *mapped))
        o.write('\n')

    o.write('\n')
    o.close()

def writeLine(string):
    o = open(outFile, 'a')
    o.write(f'{string}\n\n')
    o.close()

def getVocab(file):
    v = {}
    f = open(file, "r")
    currentIndex = 1
    for line in f:
        for token in line.split():
            if token in v:
                v[token]['count'] += 1
            else:
                v[token] = { 'index': currentIndex , 'count': 1 }
                currentIndex += 1
    f.close()
    return v

def countMatrix(sentence, v):
    matrix = [[0 for i in range(len(v)+1)] for j in range(len(v)+1)]
    for index, token in enumerate(sentence):
        if index == 0:
            matrix[0][v[token]['index']] += 1
        else:
            matrix[v[sentence[index-1]]['index']][v[token]['index']] += 1
    return matrix

def probMatrix(v, counts, b):
    matrix = [[0 for i in range(len(v)+1)] for j in range(len(v)+1)]
    for indexA in range(len(v)+1):
        adjustedTotal = sumList(counts[indexA]) + (len(v) * b)
        for indexB in range(len(v)+1):
            adjustedCount = counts[indexA][indexB] + b
            matrix[indexA][indexB] = adjustedCount / adjustedTotal if adjustedCount != 0 else 0
    return matrix

def train(trainFile, b):
    # find all unique tokens in trianing set
    global vocab
    vocab = getVocab(trainFile)

    # populate count matrix for training data (add b to each cell)
    bCounts = [[0 for i in range(len(vocab)+1)] for j in range(len(vocab)+1)]
    f = open(trainFile, 'r')
    for line in f:
        tokenArr = line.split()
        for index, token in enumerate(tokenArr):
            if index == 0:
                bCounts[0][vocab[token]['index']] += 1
            else:
                bCounts[vocab[tokenArr[index-1]]['index']][vocab[token]['index']] += 1

    f.close()
    # calculate C with sumList(bCounts[index_of_token])
    # populate probabiliy matrix for training data
    bProbs = [[0 for i in range(len(vocab)+1)] for j in range(len(vocab)+1)]
    for indexA in range(len(vocab)+1):
        adjustedTotal = sumList(bCounts[indexA]) + (len(vocab) * b)
        for indexB in range(len(vocab)+1):
            adjustedCount = bCounts[indexA][indexB] + b
            bProbs[indexA][indexB] = adjustedCount / adjustedTotal if adjustedCount != 0 else 0

    return bProbs

def parseVocab(sentence):
    v = {}
    currentIndex = 1
    for token in sentence:
        if token in v:
            v[token]['count'] += 1
        else:
            v[token] = { 'index': currentIndex , 'count': 1 }
            currentIndex += 1
    return v

def sentenceProb(sentence, probs):
    p = probs[0][vocab[sentence[0]]['index']]
    for index in range(1, len(sentence)):
        p *= probs[vocab[sentence[index-1]]['index']][vocab[sentence[index]]['index']]
    return p

def evaluate(sentences, b, model):
    # evaluate each sentence
    for index, s in enumerate(sentences, start=1):
        s = s.split()
        v = parseVocab(s)
        # populate count and prob matrices
        count = countMatrix(s, v)
        prob = probMatrix(v, count, b)

        # calculate probabilities of sentence based on training model
        pSent = sentenceProb(s, model)

        # print matrices and probability
        writeMatrix(f'S{index} Count Matrix', list(v), count)
        writeMatrix(f'S{index} Probability Matrix', list(v), prob)
        writeLine(f'Probability of S{index}: {pSent}')

def main():
    if len(sys.argv) < 3:
        raise ValueError('Please include the appropriate variables.')

    trainingFile = sys.argv[1]
    b = int(sys.argv[2])

    model = train(trainingFile, b)

    evaluate([testsentence1, testsentence2], b, model)

main()
