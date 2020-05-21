from setuptools import setup


setup(
	name='Byte Pair Encoding',
    version = '0.1',
    url = 'https://github.com/vatsalsaglani/BytePairEncoding',
    description='Build a corpus vocabulary using the Byte Pair Encoding(BPE) methodology and also tokenize sentences using the BPE tokenizer',
	author = 'Vatsal Saglani',
    license = 'MIT',
    install_requires = ['tqdm'],
    packages = ['BPE'],
	zip_safe = False

)
