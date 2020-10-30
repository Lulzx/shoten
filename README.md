# shoten-search
The search interface for the shoten web application

# how to use

- Install NodeJS, Yarn and Python 3.8+

Then,
```
git clone --depth=1 https://github.com/Lulzx/shoten-search.git
cd shoten-search
yarn install
yarn build
yarn dev
```

- To run the API

```
pip install -r requirements.txt
python -m uvicorn scratch:app --reload
```