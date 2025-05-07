## Kranjska-Topics

This repository contains the Python scripts supporting the experiments and analysis presented in our paper:

> **Debating Regional Challenges: Insights into the Carniolan Provincial Assembly in the Austro-Hungarian Empire**  
> *Presented at DH2025 conference in Lisbon, July 2025*  
> DOI: [not available yet]

---

### Overview

This repository provides three Python scripts used to prepare the data, extract the topics, and run topic analysis over the years for the Kranjska 1.0 corpus, as described in the paper. The source corpus has to be downloaded from external repository (see below).

---

### Contents

```
src
  ├── extract_lemmas.py         # Prepares input data for topic postprocessing
  ├── prepare_data_speeches.py  # Prepares input data for topic analysis
  ├── topics_time.py            # Main script to run topic analysis, prints the results and generates visualisations
```

---

### Carniolan Provincial Assembly corpus Kranjska 1.0

The corpus Kranjska 1.0 is publicly available on CLARIN.SI under CC BY 4.0 license.
URL: http://hdl.handle.net/11356/1824

Two zip files have to be downloaded:
- Kranjska corpus in TEI format: Kranjska-xml-text.zip (31.12 MB), needed for topic analysis
- Kranjska corpus in TEI with linguistic annotation: Kranjska-xml.zip (157.91 MB), needed for postprocessing, where the topics' keywords are limited to lemmas to avoid repetition of word forms

Unzip both files in the `./corpus/` directory.

---

### How to Run

1. Download external files and place them in the appropriate folders.
2. Change the names of input and output files and folders in all Python scripts (if needed).
3. Prepare the data for topic analysis (generate ./data/bert_docs_time_stamps.json file):
   ```bash
   python prepare_data_speeches.py
   ```
4. Prepare the data for postprocessing (generate ./data/word_lemmas.json file):
   ```bash
   python extract_lemmas.py
   ```
5. Install the BERTopic library and all dependencies, if needed.
6. Run the main analysis and plot results:
   ```bash
   python topics_time.py
   ```

---

### Contact

For questions or feedback, feel free to reach out:

**Alenka Kavčič**  
[alenka.kavcic@fri.uni-lj.si]

---

### License

This code is released under the GPL 3.0 or later license. See `LICENSE` for details.
