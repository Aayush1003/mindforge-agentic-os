# Human-Solvable Science, AI, and Memory Challenges

This collection contains practical problems that an average person or small team can begin exploring today. They are learning simulations, not complete scientific solutions. Every claim should be supported by observations, repeatable experiments, uncertainty estimates, and independent review.

AI can explain concepts, help write code, organize observations, and suggest counterexamples. Humans must choose safe experiments, verify sources, interpret results, protect privacy, and decide which conclusions are supported.

## 1. Physics: Measure how a ball loses energy

**Problem:** Estimate how the bounce height of a soft ball changes from bounce to bounce on a fixed surface.

**Materials:** Soft ball, ruler, phone camera, spreadsheet or Python, clear floor area.

**Human task:**

1. Drop the ball from a fixed height several times.
2. Record the video from a fixed position.
3. Measure each bounce height and repeat for every trial.
4. Calculate the average height ratio and the variation between trials.
5. Predict the next bounce and compare it with a new observation.

**Simple model:**

```text
height[n + 1] = ratio * height[n]
```

Keep the ball, surface, drop height, and camera position consistent. Use enough trials to expose variation. A result is stronger when a second person obtains a similar ratio using the same written procedure.

**Safety:** Use a small soft ball and an unobstructed area. Never throw objects or use breakable equipment.

## 2. Chemistry: Compare safe household filtration

**Problem:** Compare how visible particles settle or pass through different low-risk filter materials.

**Materials:** Clean soil, water, equal containers, clean coffee filters or cloth, light source, camera.

**Human task:**

1. Prepare equal samples of muddy water.
2. Leave one sample to settle.
3. Filter the remaining samples through selected clean materials.
4. Observe them under consistent lighting for the same time.
5. Repeat each condition and record variations.

**Useful measurements:**

- Time to visible settling.
- Clarity against a printed grid or text.
- Change in visible sediment volume.
- Difference between repeated trials.

This is not a test of drinking-water safety. Clear water may still contain harmful microbes or dissolved chemicals. Do not drink samples, add unknown chemicals, or attempt filtration of toxic waste.

## 3. AI: Measure continual-learning forgetting

**Problem:** When a small AI model learns task A and then task B, how much does its performance on task A decrease?

**Simulation:** Create two small synthetic classification tasks. Measure accuracy on both held-out test sets before and after learning task B.

**Methods to compare:**

- Sequential training on task B only.
- Replay: mix a small sample of task A with task B.
- Separate task-specific parameters or a small fixed memory buffer.

**Required evidence:**

- Reproducible synthetic datasets.
- Training and test sets separated before experiments.
- Multiple random seeds.
- Accuracy with average and variation.
- Retention scores for task A and learning scores for task B.
- Negative results and failed methods.

**Human role:** Inspect the code, verify that test data were not reused during training, question benchmark shortcuts, and check whether performance improvements come at a cost such as higher memory or slower learning.

This exercise demonstrates forgetting in a controlled setting. It does not prove that a method is safe or effective for large, real-world AI systems.

## 4. Memory: Compare review methods

**Problem:** Test whether rereading, self-testing, or spaced review improves recall in a small, low-stakes learning task.

**Human task:**

1. Create comparable facts or vocabulary items.
2. Randomly assign items to different review methods.
3. Keep study time as consistent as possible.
4. Test recall immediately and after a delay without looking at notes.
5. Repeat with new material and report all results.

**Possible factors:**

- Sleep and fatigue.
- Prior knowledge.
- Question difficulty.
- Time between review sessions.
- Memory of the test itself.

Participation should be voluntary. Do not collect personal health or psychological records. This is a learning experiment, not a medical diagnosis or treatment.

## 5. Knowledge memory: Improve retrieval from personal notes

**Problem:** Does adding source, date, summary, tags, uncertainty, and next action to notes improve later retrieval?

**Human task:**

1. Create two small sets of non-sensitive notes: structured and unstructured.
2. Write retrieval questions before testing.
3. Search both sets for answers.
4. Record answer accuracy and search time.
5. Repeat with a second set of fresh notes.

**A useful note format:**

```text
Source:
Date:
Summary:
Evidence or uncertainty:
Tags:
Next action:
Corrections:
```

Keep source links and preserve original context. Do not place passwords, secrets, confidential work, or other sensitive information in an unprotected notebook.

## 6. Reproducibility: Audit a claim

**Problem:** Decide whether a scientific or computational claim contains enough evidence for independent review.

**Checklist:**

- Exact question and assumptions are stated.
- Methods are complete enough to follow.
- Data or a safe substitute are available.
- Code or calculations are accessible.
- Uncertainty is reported.
- Negative results are disclosed.
- Independent reproduction is attempted.
- Unknowns and limitations remain visible.

**Result levels:**

- **Complete:** All checklist items are confirmed.
- **Partially complete:** Most items are present, but important evidence is missing.
- **Insufficient:** Core methods, data, code, uncertainty, or reproduction cannot be established.

Missing evidence does not prove that a claim is false. It means confidence should remain limited until the missing evidence is checked.

## Experiment record template

```text
Project question:
Prediction:
Materials or software:
Model and assumptions:
Procedure:
Code or document version:
Measurements:
Uncertainty:
Repeated trials:
Negative or unexpected results:
What the evidence supports:
What remains unknown:
Independent reviewer:
Next test:
```

## When a problem is solved

A small project is complete when:

- The question is precise.
- Assumptions are explicit.
- Methods are reproducible.
- Predictions are compared with observations or a trusted reference.
- Uncertainty and negative results are reported.
- Another person can inspect the record or repeat the test.
- The result is not overstated.

These projects build practical skills in physics, chemistry, AI continual learning, and human memory. They are learning tools, not medical advice or complete solutions to civilization-scale challenges.
