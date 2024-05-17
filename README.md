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
