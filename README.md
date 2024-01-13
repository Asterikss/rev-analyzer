<h1 align="center">
    <img src="https://github.com/Asterikss/rev-analyzer/blob/master/assets/rev_analyzer_logo.png?raw=true" alt="RevAnalyzer">

</h1>

<p align="center">
    <a href="https://github.com/Asterikss/rev-analyzer/pulls" title="Contributing"><img src="https://img.shields.io/badge/contributions-welcome-orange"></a>
    <a href="https://www.youtube.com/watch?v=WpMRV0r08CI&t=120s" title="AdamMalysz"><img src="https://img.shields.io/badge/animals_hurt_during_developments-~0-green"></a>
    <a href="https://github.com/Asterikss/rev-analyzer/issues/new" title="Issues"><img src="https://img.shields.io/badge/open-issue-red"></a>
    <a href="https://github.com/Asterikss/rev-analyzer/subscription" title="Watch"><img src="https://img.shields.io/badge/watch_this-repo-yellow"></a>
</p>

**RevAnalyzer** leverages machine learning for
efficient review analysis. It provides insights into customer feedback
while enabling heavy customization of the process.


## Demo
TODO

## Run Locally

Clone the project

```bash
  git clone https://github.com/Asterikss/rev-analyzer.git
  cd rev-analyzer
```

Create a new environment
*  Venv
    * Linux
    ```bash
    python -m venv rev-analyzer
    source env_name/bin/activate
    ```
    * Windows

    ```bash
    python -m venv rev-analyzer
    env_name\Scripts\activate
    ```

* Conda

    ```bash
    conda create --name rev-analyzer python=3.10
    conda activate rev-analyzer
    ```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run the app

```bash
  streamlit run 1_🔬_Analyzer.py
```

*The app needs to be run from the root of the project  
*Best viewed at 125% browser zoom  
*If this line from `requirements.txt` fails:
`https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz#egg=en_core_web_sm`,
and you want to download it via the command line, be sure to run `python -m
spacy download en_core_web_sm`, otherwise, you will encounter an error.
