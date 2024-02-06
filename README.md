## SIGDIAL 2023: What’s Hard in English RST Parsing? Predictive Models for Error Analysis
```
@inproceedings{liu-etal-2023-whats,
    title = "What{'}s Hard in {E}nglish {RST} Parsing? Predictive Models for Error Analysis",
    author = "Liu, Yang Janet  and
      Aoyama, Tatsuya  and
      Zeldes, Amir",
    editor = "Stoyanchev, Svetlana  and
      Joty, Shafiq  and
      Schlangen, David  and
      Dusek, Ondrej  and
      Kennington, Casey  and
      Alikhani, Malihe",
    booktitle = "Proceedings of the 24th Annual Meeting of the Special Interest Group on Discourse and Dialogue",
    month = sep,
    year = "2023",
    address = "Prague, Czechia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.sigdial-1.3",
    doi = "10.18653/v1/2023.sigdial-1.3",
    pages = "31--42",
    abstract = "Despite recent advances in Natural Language Processing (NLP), hierarchical discourse parsing in the framework of Rhetorical Structure Theory remains challenging, and our understanding of the reasons for this are as yet limited. In this paper, we examine and model some of the factors associated with parsing difficulties in previous work: the existence of implicit discourse relations, challenges in identifying long-distance relations, out-of-vocabulary items, and more. In order to assess the relative importance of these variables, we also release two annotated English test-sets with explicit correct and distracting discourse markers associated with gold standard RST relations. Our results show that as in shallow discourse parsing, the explicit/implicit distinction plays a role, but that long-distance dependencies are the main challenge, while lack of lexical overlap is less of a problem, at least for in-domain parsing. Our final model is able to predict where errors will occur with an accuracy of 76.3{\%} for the bottom-up parser and 76.6{\%} for the top-down parser.",
}
```


### Directory Structure 
```
NLPErrors4RST/
├── data/
│   ├── GUM9/
│   │   ├── bottomup/
│   │   │   ├── run1/
│   │   │   ├── run2/
│   │   │   ├── run3/
│   │   │   ├── run4/
│   │   │   └── run5/
│   │   ├── human/
│   │   ├── topdown/
│   │   │   ├── run1/
│   │   │   ├── run2/
│   │   │   ├── run3/
│   │   │   ├── run4/
│   │   │   └── run5/
│   │   ├── en-gum-dev-list.txt
│   │   └── GUM_facts.tab
│   └── RSTDT/
│       └── README.md
├── utils/
│   ├── get_dep_info.py
│   ├── get_dep_info_rstdt.py
│   ├── get_distractor_errors.py
│   ├── get_gold_anno.py
│   ├── get_oov_rate.py
│   ├── main_GUM9.py
│   ├── main_RSTDT.py
│   ├── process_facts.py
│   ├── process_preds.py
│   ├── relation2class4rstdt.py
│   ├── sigdial_new_GUM.R
│   ├── sigdial_new_RSTDT.R
│   └── sigdial_pred_GUM.R
└── README.md
```


### Directory & File Descriptions  

- `data` contains all the gold and predicted parses (`.rsd`) used in the analysis
- `data/GUM9/GUM_facts.tab` is the processed file that can be directly used by the R scripts in `utils/`
- `utils/main_GUM9.py` and `utils/main_RSTDT.py` are the scripts to generate the `*_facts.tab` file
- `sigdial_new_GUM.R` and `utils/sigdial_new_RSTDT.R` contains the code used for the analyses described in Section 4.1
- `sigdial_pred_GUM.R` contains the code used for the modeling in Section 4.2 
- Other `.py` scripts were used to generate relevant information and are provided here for reference