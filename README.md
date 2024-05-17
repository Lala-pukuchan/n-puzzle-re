# n-puzzle-re

## 初期状態
```
python3 npuzzle-solve.py  0.35s user 0.03s system 94% cpu 0.395 total
```

## OpenリストをListから、Heapqに変更した場合、処理時間が減った。
```
python3 npuzzle-solve.py  0.23s user 0.02s system 94% cpu 0.245 total
```

## パズルのデータ形式をlistをtupleにして、hashで持った場合、処理時間が減った。
```
python3 npuzzle-solve.py  0.05s user 0.01s system 88% cpu 0.066 total
```

## それでも、パズル4*4では、かなり時間がかかる。
```
n-puzzle-re % time python npuzzle-solve.py
Goal!
46
(1, 2, 3, 4)
(12, 13, 14, 5)
(11, 0, 15, 6)
(10, 9, 8, 7)
python3 npuzzle-solve.py  75.29s user 0.67s system 99% cpu 1:15.99 total
```

# 処理時間を短くする工夫他
- ゴールの状態をキー:数値、値:マス目の位置の辞書型で持っておく。
```
n-puzzle-re % time python npuzzle-solve.py
Goal!
18
(1, 2, 3)
(8, 0, 4)
(7, 6, 5)
python3 npuzzle-solve.py  0.03s user 0.00s system 96% cpu 0.034 total
```

- Heapqの比較方法をf値が同じ場合はh値が小さい方を優先するようにした。
```
n-puzzle-re % time python npuzzle-solve.py
Goal!
46
(1, 2, 3, 4)
(12, 13, 14, 5)
(11, 0, 15, 6)
(10, 9, 8, 7)
python3 npuzzle-solve.py  16.30s user 0.17s system 99% cpu 16.486 total
```

- closedリストをsetからdictに変更した。
```
n-puzzle-re % time python npuzzle-solve.py
Goal!
46
(1, 2, 3, 4)
(12, 13, 14, 5)
(11, 0, 15, 6)
(10, 9, 8, 7)
python3 npuzzle-solve.py  14.86s user 0.17s system 99% cpu 15.062 total
```

