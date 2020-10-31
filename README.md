# shoten-search

The search interface for the shoten web application

# how to use

- Install NodeJS, Yarn and Python 3.8+

Then,
```
git clone --depth=1 https://github.com/Lulzx/shoten-search.git
cd shoten-search
npm install
```


| Syntax           | Description                                                                       |
|------------------|-----------------------------------------------------------------------------------|
| `dev`            | Development (port 5000)                                                           |
| `dev:nollup`     | Development with crazy fast rebuilds (port 5000)                                  |
| `dev-dynamic`    | Development with dynamic imports                                                  |
| `build`          | Build a bundled app with SSR + prerendering and dynamic imports                   |
| `serve`          | Run after a build to preview. Serves SPA on 5000 and SSR on 5005                  |
| `export`         | Create static pages from content in dist folder (used by `npm run build`)         |


- To run the API

```
pip install -r requirements.txt
python -m uvicorn scratch:app --reload
```