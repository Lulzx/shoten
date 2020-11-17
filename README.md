# 📚 Shoten

An e-book platform for a great reading experience with a search interface to find books and audiobooks.


## 💭 Main ideas

### 🤩 Features

- reading session
- search content
- activity data
- community forum
- user statistics
- personal bookshelf
- audiobooks [https://librivox.org]
- convert web articles to ebooks (in pdf, epub formats)

### 🧐 Reading

- position
- dictionary
- annotations
- notes (with folders)

### ⌨️ Keyboard access

- shortcuts 
- navigation

### 📚 Bookshelf

- favorites
- to read -> future
- reading now -> present
- have read -> past
- reviewed
- recently viewed
- recommendations

---

## Built with:

- [Svelte](http://svelte.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)


## Installation

- Make sure to install [Node.js](https://nodejs.org/en/download/), [Yarn](https://yarnpkg.com/getting-started/install) and [Python](https://www.python.org/downloads/)

1. **Clone the project**

   ```sh
    git clone --depth=1 https://github.com/Lulzx/shoten.git
    cd shoten
   ```

2. **Install and run backend (http://localhost:8000)**

    ```sh
    git clone --depth=1 https://github.com/Lulzx/shoten-backend.git
    cd shoten-backend
    pip install -r requirements.txt
    python -m uvicorn server:app --reload
    ```

3. **Install and run frontend (http://localhost:5000)**

    ```sh
    yarn install
    yarn dev:nollup
    ```


| Syntax           | Description                                                                       |
|------------------|-----------------------------------------------------------------------------------|
| `dev`            | Development (port 5000)                                                           |
| `dev:nollup`     | Development with crazy fast rebuilds (port 5000)                                  |
| `build`          | Build a bundled app with SSR + pre-rendering and dynamic imports                   |
| `serve`          | Run after a build to preview. Serves SPA on 5000 and SSR on 5005                  |
| `export`         | Create static pages from content in dist folder (used by `yarn build`)            |

---

## Roadmap

See the [open issues](https://github.com/lulzx/shoten/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is available in Public Domain, you're free to use it without any restrictions.
