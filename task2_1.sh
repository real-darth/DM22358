#!/bin/bash
read -p "Enter amount of iterations:" iter
echo ""
echo "System specifics:"
lscpu
echo "Working..."
python3.9 -m cProfile -o profile2_1.stats task2_1.py $iter
python3.9 lineProfCode.py profile2_1.stats
python3.9 -m snakeviz profile2_1.stats --server