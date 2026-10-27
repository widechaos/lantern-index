# Lantern Index

An offline, fictional haunted-station archive for Hacktoberfest Week 4: Ghost in the Machine. Ask about the bell, lantern or unsent letter, read original records, and pin three sources to open an authored final page.

I started this new project and repository on October 27, 2026, within the contest entry period. The application, story, examples and tests are new. I reused my installed personal Python environment and cached model weights. No client, employer, family or historical archive material is included. Every name, date and event in the story is invented.

## Walkthrough

[42-second text walkthrough](docs/demo.mp4) (use GitHub **Download raw file**). It renders actual local HTTP output into text cards. It is **not** a browser screen recording. The complete [raw transcript](docs/walkthrough.txt), [retrieval results](docs/evaluation.json) and [HTTP checks](docs/http-checks.json) are included.

The local browser UI has search, source cards, pin/remove, a locked final page and reset. Browser interaction and responsive checks have not yet been run. HTTP and model behavior were tested. The HTML/CSS interface is supplied, but its browser flow remains unverified.

## Run

Python 3.12, CPU. Initial installation and model download need internet access. No API key, hosted inference, paid service or account is required. Running the computer and storing dependencies still have costs.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
export HF_HUB_CACHE="$PWD/.cache/models"
.venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('sentence-transformers/all-MiniLM-L6-v2', revision='1110a243fdf4706b3f48f1d95db1a4f5529b4d41')"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
.venv/bin/python server.py
```

Visit http://127.0.0.1:8804. Only the loopback interface is bound. No network deployment is supplied; don't expose the development HTTP server publicly. PORT can be set before startup.

```sh
.venv/bin/python archive.py 'What did Mara write to her brother?'
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python evaluate.py
```

To finish the story: search for the bell, pin **The bell register**; search for the light, pin **The keeper’s lamp**; search for the letter, pin **The unsent letter**. Then open the final page. The evidence IDs are `bell`, `light`, `letter`. This is a short discovery story, not a security puzzle: source code reveals the ending.

## Where the open model matters

[all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), Apache-2.0, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, produces 384-dimensional normalized embeddings through [Sentence Transformers](https://sbert.net/). Similarity compares questions to record titles plus text. Up to three records with cosine similarity at least 0.28 are returned, unchanged and with stable source IDs. Scores are similarities, not calibrated confidence.

The model retrieves related records even with changed wording. It does not generate dialogue, impersonate a person, prove paranormal events, or decide the ending. That ending is authored text gated by source IDs. The reader interprets the evidence.

## Recorded results and limits

- Seven behavior/integration tests passed: preserved source text, input rejection, deterministic ordering, source-gated ending, invalid IDs, cited ending and no archive writes.
- Fifteen author-written diagnostics: all twelve in-scope targets appeared in the top three, eleven ranked first. A Jaccard word-overlap baseline ranked seven first. All three out-of-scope probes returned no matches.
- The miss matters: “Who found a fresh letter many years later?” ranked the unsent letter above the later visitor. The visitor was second. I retained this result instead of tuning the threshold to the fixture.
- Warm query median 3.35 ms on my machine excludes model loading. This tiny set is not an independent benchmark. I did not measure reader engagement, chills, memory preservation or a real visitor's response.
- Nine local HTTP checks passed: static assets, inaccessible arbitrary files, foreign-origin refusal, extra fields, empty input, sealed and unlocked endings.
- Browser UI, keyboard interaction, mobile layout and cross-browser behavior have not yet been verified. No claims about those checks are made.

The story and queries are English-only. A short single-record retriever cannot reliably answer multi-hop questions, handle arbitrary questions or distinguish all overlapping details. Low similarity sometimes means a poor match, not proof that the archive lacks an answer. Unsupported questions can still match a record. At most 512 characters and 256 model tokens are accepted; overlong questions are rejected, not silently truncated.

The server does not persist questions or log request text; pins exist only in tab memory and reload/reset loses them. The server is serial and the intended use is one local reader. No imports, uploads, arbitrary paths, shell tools, external fonts, analytics or remote page assets are available. The example JSON is read-only during search and ending operations.

## Credits and license

Application and original fictional story: MIT, Renchao Wu. The open model, Sentence Transformers, Transformers, NumPy and other dependencies keep their own licenses; model weights and dependencies are not committed. This repository is not affiliated with a railway, family archive, museum or religious observance. The theme is interpreted as a quiet fictional ghost story.
