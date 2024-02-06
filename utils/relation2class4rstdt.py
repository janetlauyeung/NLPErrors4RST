class2rel = {
    'Attribution': ['attribution', 'attribution-e', 'attribution-n', 'attribution-negative'],
    'Background': ['background', 'background-e', 'circumstance', 'circumstance-e'],
    'Cause': ['cause', 'Cause-Result', 'result', 'result-e',
              'Consequence', 'consequence', 'consequence-n-e', 'consequence-n', 'consequence-s-e', 'consequence-s'],
    'Comparison': ['Comparison', 'comparison', 'comparison-e', 'preference', 'preference-e',
                   'Analogy', 'analogy', 'analogy-e', 'proportion', 'Proportion'],
    'Condition': ['condition', 'condition-e', 'hypothetical', 'contingency', 'otherwise', 'Otherwise'],
    'Contrast': ['Contrast', 'concession', 'concession-e', 'antithesis', 'antithesis-e', 'contrast'],  # lowercase contrast: GUM relation
    'Elaboration': ['elaboration-additional', 'elaboration-additional-e', 'elaboration-general-specific',
                    'elaboration-general-specific-e', 'elaboration-part-whole', 'elaboration-part-whole-e',
                    'elaboration-process-step', 'elaboration-process-step-e', 'elaboration-object-attribute-e',
                    'elaboration-object-attribute', 'elaboration-set-member', 'elaboration-set-member-e', 'example',
                    'example-e', 'definition', 'definition-e', 'elaboration'],  # elaboration: GUM relation
    'Enablement': ['purpose', 'purpose-e', 'enablement', 'enablement-e'],
    'Evaluation': ['evaluation', 'evaluation-n', 'evaluation-s-e', 'evaluation-s', 'Evaluation',
                   'interpretation', 'interpretation-n', 'interpretation-s-e', 'interpretation-s', 'Interpretation',
                   'conclusion', 'Conclusion', 'comment', 'comment-e'],
    'Explanation': ['evidence', 'evidence-e', 'explanation-argumentative', 'explanation-argumentative-e', 'Reason', 'reason',
                    'reason-e', "justify", "motivation"],  # justify & motivation: GUM relations
    'Joint': ['List', 'Disjunction'],
    'Manner-Means': ['manner', 'manner-e', 'means', 'means-e'],
    'Topic-Comment': ['problem-solution', 'problem-solution-n', 'problem-solution-s', 'Problem-Solution',
                      'Question-Answer', 'question-answer', 'question-answer-n', 'question-answer-s',
                      'Statement-Response', 'statement-response-n', 'statement-response-s',
                      'Topic-Comment', 'Comment-Topic', 'rhetorical-question', "question", "solutionhood"],  # question & solutionhood: GUM relations
    'Summary': ['summary', 'summary-n', 'summary-s', 'restatement', 'restatement-e'],
    'Temporal': ['temporal-before', 'temporal-before-e', 'temporal-after', 'temporal-after-e', 'Temporal-Same-Time', 'temporal-same-time',
                 'temporal-same-time-e', 'Sequence', 'Inverted-Sequence', 'sequence'],  # lowercase sequence: GUM
    'Topic-Change': ['topic-shift', 'topic-drift', 'Topic-Shift', 'Topic-Drift', "joint"],  # joint: GUM relation
    'Textual-Organization': ['TextualOrganization', "preparation"],  # preparation: GUM relation
    'span': ['span'],
    'Same-Unit': ['Same-Unit', 'same-unit']  # same-unit - lowercase for GUM
}

rel2class = {}
for cl, rels in class2rel.items():
    rel2class[cl] = cl
    for rel in rels:
        rel2class[rel] = cl
