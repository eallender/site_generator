# 📝 Static Site Generator

A lightweight static site generator written in Python, created as part of the [Boot.dev](https://boot.dev) backend curriculum.

This project parses Markdown files and converts them into clean, styled HTML pages.

## About This Project

This project demonstrates a basic static site generator built with Python. It takes Markdown source files, processes them, and outputs a complete HTML website. The site is designed to be easily hosted on platforms like GitHub Pages, handling base paths for subdirectories.

This example site features articles about the works of J.R.R. Tolkien.

## Features

- Converts `.md` Markdown files into `.html`
- Supports:
  - Headings (`#`, `##`, etc.)
  - Paragraphs
  - Blockquotes
  - Ordered and unordered lists
  - Code blocks
- Recursively processes input directories
- Outputs a full static site structure
- Automatically creates necessary directories
- Clean HTML template wrapping

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.x
*   Git

### Installation and Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/eallender/site_generator.git
    cd site_generator
    ```
2.  **Run the local build script:**
    For local testing, the `main.sh` script will build to the `docs` directory
    ```bash
    ./main.sh
    ```
    (Or `python src/main.py` depending on your setup)

3.  **Serve Locally:**
    If you have a simple HTTP server, you can serve the generated `docs` directory. This is already done for you as apart of the `main.sh` script. For example, using Python's built-in server:
    ```bash
    cd docs
    python3 -m http.server 8888
    ```
    Then open your browser to `http://localhost:8888`.

## ⚙️ Deployment

This project is configured for deployment with [GitHub Pages](https://pages.github.com/).

### Build for Production

A dedicated `build.sh` script is used to generate the site with the correct base path for GitHub Pages, outputting to the `docs` directory.

```bash
./build.sh
```

This script typically runs: python3 src/main.py "/site_generator/"
This passes the proper root directory to our site generator so that it can be hosted on GitHub Pages.

### Testing the codebase

A dedicated `test.sh` script is used to run the site_generators suite of unit tests.

```bash
./test.sh
```

### GitHub Pages Configuration
The site is served from the docs directory on the main branch of this repository.
You can configure this in your repository's settings under "Pages".

The live site can be found at: https://eallender.github.io/site_generator/

## 📁 Project Structure
```
├── build.sh                        The build script for build code for production (GitHub Page Hosting).
├── content
│   ├── blog
│   │   ├── glorfindel              
│   │   │   └── index.md            
│   │   ├── majesty
│   │   │   └── index.md            The content directory holds all of the raw markdown files that are
│   │   └── tom                     converted to HTML and then hosted on the site.
│   │       └── index.md
│   ├── contact
│   │   └── index.md
│   └── index.md
├── docs                            
│   ├── blog                        
│   │   ├── glorfindel
│   │   │   └── index.html
│   │   ├── majesty
│   │   │   └── index.html
│   │   └── tom                     The docs directory contains the actual site files that are hosted
│   │       └── index.html          on GitHub Pages. This is where the `./build.sh` script outputs to.
│   ├── contact
│   │   └── index.html
│   ├── images
│   │   ├── glorfindel.png
│   │   ├── rivendell.png
│   │   ├── tolkien.png
│   │   └── tom.png
│   ├── index.css
│   └── index.html
├── main.sh                         The script for running the site generator locally.
├── pyproject.toml
├── README.md
├── src                             The src directory holding all the project code.
│   ├── htmlnode.py
│   ├── main.py
│   ├── textnode.py
│   └── utils
│       ├── convert.py
│       ├── regex.py
│       └── site_gen.py
├── static                          Contains all static assets for the site that are also 
│   ├── images                      copied to the docs folder for hosting.
│   │   ├── glorfindel.png
│   │   ├── rivendell.png
│   │   ├── tolkien.png
│   │   └── tom.png
│   └── index.css
├── template.html
├── test                            This directory contains all of the unit tests for the code.
│   ├── test_htmlnode.py
│   ├── test_textnode.py
│   └── test_utils
│       ├── test_convert.py
│       └── test_regex.py
└── test.sh                         The test script for running unit tests.
```