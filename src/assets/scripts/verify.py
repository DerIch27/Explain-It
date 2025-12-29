from rapidfuzz import fuzz
import json
import csv
import io

prefix = 'src/assets/data/'

with io.open(prefix+'directory.json', encoding='utf8') as file:
    directory: dict[str,dict] = json.load(file)

for languageCode, languageInfo in directory.items():
    variants = languageInfo['variants']
    for name, info in variants.items():
        filename = info.get('raw_filename')
        if filename is None:
            print(f'raw_filename missing on {languageCode}:{name}')
            continue
        if info.get('graph_filename') is None:
            print(f'graph_filename missing on {languageCode}:{name}')
            continue
        existing: set[str] = set()
        graph: dict[str,set[str]] = {}
        def addToGraph(key: str, val: str):
            if graph.get(key) == None:
                graph[key] = set()
            graph[key].add(val)
        with io.open(prefix+filename, encoding='utf8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 0:
                    print(filename, 'empty row')
                    continue
                if '' in row:
                    print(filename, 'empty word', row)
                if row[0] in existing:
                    print(filename, 'duplicate', row[0])
                else:
                    existing.add(row[0])
                for i in row[1:]:
                    addToGraph(row[0], i)
                    addToGraph(i, row[0])
        with io.open(prefix+info['graph_filename'], 'w', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            for key, words in sorted(graph.items()):
                writer.writerow([key]+list(words))

def checkSimilarity(allWords: list[str]):
    allMatches: list[tuple[float, str, str]] = []
    for idx in range(len(allWords)):
        i = allWords[idx]
        for j in allWords[idx+1:]:
            score = fuzz.ratio(i, j)
            if 70 < score < 100:
                allMatches.append((score, i, j))
            if i[:len(j)] == j or j[:len(i)] == i: 
                if abs(len(i)-len(j)) <= 3: print(i, j)
    for s, i, j in sorted(allMatches, key=lambda x:x[0]): print(round(s,2), i, j)
#checkSimilarity([i.lower() for i in graph.keys()])