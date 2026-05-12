# Retrieval Eval Report

- Generated at: `2026-05-12T21:41:39.033411+00:00`
- Eval coverage: `55` questions

## Metrics

| Metric | Value | Delta vs baseline |
|---|---:|---:|
| `top1_accuracy` | 0.5200 | +0.0000 |
| `top3_accuracy` | 0.6400 | +0.0000 |
| `top5_accuracy` | 0.7600 | +0.0000 |
| `mrr` | 0.5970 | +0.0000 |
| `citation_accuracy` | 0.7600 | +0.0000 |
| `unknown_answer_accuracy` | 1.0000 | +0.0000 |

## Failed Examples

### k6: What does topic 06 describe?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-06.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.14, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.14, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.14, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.14, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.14, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k7: What does topic 07 describe?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-07.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.14, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.14, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.14, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.14, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.14, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k8: What does topic 08 describe?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-08.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.14, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.14, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.14, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.14, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.14, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k9: What does topic 09 describe?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-09.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.14, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.14, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.14, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.14, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.14, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k26: Summarize concept 06 from the notes.
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-06.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.13, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.13, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.13, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.13, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.13, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k27: Summarize concept 07 from the notes.
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-07.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.13, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.13, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.13, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.13, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.13, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k28: Summarize concept 08 from the notes.
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-08.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.13, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.13, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.13, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.13, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.13, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k29: Summarize concept 09 from the notes.
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-09.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.13, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.13, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.13, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.13, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.13, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k46: Where is practical usage for topic 06 discussed?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-06.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.34, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.34, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.34, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.34, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.34, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k47: Where is practical usage for topic 07 discussed?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-07.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.34, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.34, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.34, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.34, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.34, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k48: Where is practical usage for topic 08 discussed?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-08.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.34, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.34, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.34, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.34, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.34, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`

### k49: Where is practical usage for topic 09 discussed?
- reasons: `retrieval_miss, citation_miss`
- expected_sources: `['kb/topic-09.md']`
- retrieved_sources: `['kb\\topic-01.md', 'kb\\topic-02.md', 'kb\\topic-03.md', 'kb\\topic-04.md', 'kb\\topic-05.md']`
- citations: `['- kb\\topic-01.md :: Topic 1 > Key Point (score=0.34, chunk_id=1)', '- kb\\topic-02.md :: Topic 2 > Key Point (score=0.34, chunk_id=2)', '- kb\\topic-03.md :: Topic 3 > Key Point (score=0.34, chunk_id=3)', '- kb\\topic-04.md :: Topic 4 > Key Point (score=0.34, chunk_id=4)', '- kb\\topic-05.md :: Topic 5 > Key Point (score=0.34, chunk_id=5)']`
- answer_preview: `Topic 1 describes concept 1 and practical usage.`
