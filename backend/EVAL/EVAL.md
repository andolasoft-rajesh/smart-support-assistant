# Day 17 Evaluation

## Objective

Evaluate the Smart Support Assistant using a 10-case test set based on the uploaded AI Biochip Report and improve the assistant by fixing one retrieval or prompt issue.

---

## Test Set Summary

- Total Test Cases: 10
- Answerable Questions: 5
- Expected Refusals: 3
- Hard Cases: 2

---

## Baseline Score

**Score:** 7/10 (70%)

### Observations

- Most factual questions were answered correctly.
- The assistant correctly refused questions unrelated to the uploaded document.
- Some detailed comparison and reasoning questions produced incomplete answers.

---

## Failure Analysis

**Failed Test Case:**

**Question:**
Compare traditional biosensors with AI-driven biochips.

**Issue:**
The assistant listed only the advantages of AI-driven biochips instead of providing a proper comparison between traditional biosensors and AI-driven biochips.

---

## Fix Applied

Improved the retrieval process by increasing the number of retrieved document chunks so the language model receives more relevant context before generating a response.

Example:

Before:
```
top_k = 3
```

After:
```
top_k = 5
```

---

## Final Score

**Score:** 9/10 (90%)

### Improvement

- Better context retrieval.
- More complete answers for comparison questions.
- Improved overall response quality.

---

## Conclusion

The retrieval improvement significantly increased the assistant's performance. The chatbot now provides more accurate, complete, and context-aware responses while continuing to refuse questions outside the uploaded document.