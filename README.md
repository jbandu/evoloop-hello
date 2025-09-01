# EvoLoop Hello
A demo web app built with EvoLoop, an autonomous development process.

## Setup
1. Clone repo: `git clone https://github.com/jbandu/evoloop-hello.git`
2. Open `index.html` in a browser or visit https://jbandu.github.io/evoloop-hello/.

## Running Tests
- Install Selenium: `pip3 install selenium`
- Install ChromeDriver: `brew install --cask chromedriver`
- Run: `python3 test.py`

## Features
- Counter with increment, decrement, and reset (no negative values).
- Dark mode toggle with persistence via localStorage.
- Save counter as text file.

## EvoLoop Process
1. Triage: triage.py analyzes features.
2. Spec: Generates spec.json.
3. Execute: executor.py updates code.
4. Test: test.py validates.
