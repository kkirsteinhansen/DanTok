./scripts/0.prep.sh
python3 0.split.py ../../annotation/gold/danish-tiktok-dev.conllu
python3 0.split.py ../../annotation/gold/danish-tiktok-test.conllu
cp ../../annotation/gold/danish-tiktok*conllu* .

python3 scripts/1.train.py > machamp/1.train.sh
cd machamp
chmod +x 1.train.sh
./1.train.sh
cd ..

python3 scripts/1.pred.py > machamp/1.pred.sh
cd machamp
chmod +x 1.pred.sh
./1.pred.sh
cd ..

python3 scripts/3.test.py > machamp/3.test.sh
cd machamp
chmod +x 3.test.sh
./3.test.sh
cd ..

