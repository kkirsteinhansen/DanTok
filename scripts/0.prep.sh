git clone https://github.com/machamp-nlp/machamp.git
cd machamp
git reset --hard 086dcbc90199299f8e80a046eec52acaf89d13d5

mkdir -p data
wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4923/ud-treebanks-v2.11.tgz
tar -zxvf ud-treebanks-v2.11.tgz
mv ud-treebanks-v2.11 data/
cp -r data/ud-treebanks-v2.11 data/ud-treebanks-v2.11.singleToken
python3 machamp/scripts/misc/cleanconl.py data/ud-treebanks-v2.11.singleToken/*/*conllu

cd data/
git clone https://github.com/Oneplus/Tweebank.git
mkdir ud-treebanks-v2.11.singleToken/UD_English-Tweebank2
mv Tweebank/converted/* ud-treebanks-v2.11.singleToken/UD_English-Tweebank2/
cd ../

cp ../annotation/gold/danish-tiktok-dev.conllu .
python3 scripts/0.split.py danish-tiktok-dev.conllu
python3 scripts/0.split.py danish-tiktok-test.conllu
