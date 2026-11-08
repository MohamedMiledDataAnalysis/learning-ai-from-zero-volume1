# Learning AI from Zero — Volume 1: Understanding AI

Companion repository for *Learning AI from Zero — Build Your Own AI Agent*, Volume 1, by Mohamed Miled.

| Folder | What it holds |
|---|---|
| `python/vol1/chNN/`, `r/vol1/chNN/` | The code of each chapter, the exercise solutions and the `check_chNN` scripts that grade the practical tasks |
| `python/agent_core/`, `r/agentcore/` | The agent loop and the four brains (rules, replay, live, record) used from chapter 28 |
| `python/tar_agent/` | The structured finance tools used in chapters 10, 27 and 32 (Volume 2 builds the full agent) |
| `data/` | The Thames Auto Receivables 2026-1 deal pack, the learning datasets, the Corner Shop and Library data |
| `generator/` | The seeded scripts that rebuild the deal pack and its prospectus |
| `solutions/` | Reference answers for the global assessment and the loan-tape exercises |
| `python/tests/`, `r/tests/`, `tests/` | The tests that check every figure printed in the book |

## Set up

You need Python 3.13 and R 4.3 (Volume 1, chapter 2 walks through the installation on Windows, macOS and Linux).

```bash
pip install -r requirements.txt                    # Python packages, pinned
Rscript r/install_packages.R                       # R packages (the list and tested versions are in the file)
python tests/check_deal_pack.py                    # the deal pack: 188 consistency checks
cd python && python -m pytest -q                   # the Python tests
cd .. && Rscript -e "testthat::test_dir('r/tests')"   # the R tests
```

Some R tests and scripts compare R with Python, so run the R tests with Python and its packages installed.

## Model replies: rules, replay, live, record

Scripts that use a language model take `--mode rules|replay|live|record`. Rules and replay need no model.
Live and record need [Ollama](https://ollama.com) running locally with the pinned model:

```bash
ollama pull qwen2.5:7b
python python/record_all.py      # records every reply the book prints
```

You can also record on GitHub: **Actions > Record model replies > Run workflow**, then download the
`recordings` artifact and copy its files into `python/recordings/` and `r/recordings/`.

All names, loans and figures in the deal data are fictional.
