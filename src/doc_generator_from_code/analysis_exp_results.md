# Analysis of experiment with different types of embeddings

The experiment consists in taking 6 snnipets of the example code an determine thought cosine similarities of the embeddings the most appropiete for the task of generating Docuementation using a RAG architecture ai agent.

## 🔍 Cosine similarity per model:

## CodeBERTs:

  sim between embs 0-1 : 0.9767
  sim between embs 0-2 : 0.9689
  sim between embs 0-3 : 0.9789
  sim between embs 0-4 : 0.9592
  sim between embs 0-5 : 0.9399
  sim between embs 1-2 : 0.9922
  sim between embs 1-3 : 0.9669
  sim between embs 1-4 : 0.9890
  sim between embs 1-5 : 0.9732
  sim between embs 2-3 : 0.9641
  sim between embs 2-4 : 0.9951
  sim between embs 2-5 : 0.9703
  sim between embs 3-4 : 0.9513
  sim between embs 3-5 : 0.9272
  sim between embs 4-5 : 0.9806

### Analysis CodeBERT results

The results appear very close to each other, with the lowest cosine similarity at 0.9272 and the highest at 0.9992. This suggests that the model generates embeddings in a highly homogeneous way. The embeddings are too similar to one another, which is not ideal for the task we are aiming to develop. It seems that the model perceives the functions as highly related, even when they may have low semantic similarity.

## GraphCodeBERT similarities:

  sim between embs 0-1 : 0.9490
  sim between embs 0-2 : 0.9280
  sim between embs 0-3 : 0.8707
  sim between embs 0-4 : 0.9406
  sim between embs 0-5 : 0.9419
  sim between embs 1-2 : 0.9703
  sim between embs 1-3 : 0.8896
  sim between embs 1-4 : 0.9709
  sim between embs 1-5 : 0.9664
  sim between embs 2-3 : 0.9057
  sim between embs 2-4 : 0.9892
  sim between embs 2-5 : 0.9597
  sim between embs 3-4 : 0.8996
  sim between embs 3-5 : 0.8704
  sim between embs 4-5 : 0.9725

### Analysis GraphCodeBERT results

The similarity between results are similar, they have more variablity in comparison wiht CodeBERT. It shows a greater sensibility for the embeeding 3 in comparison with the others what it implies that it has a good capacity capturing the structure and the semantic content of the code. The lowest cosine similarity is between embeedings 3 - 5 (getPathId) and (runLightHouseTest) implying different roles for those.  The high similarity is between 2 - 4 (getPathId) and (getLightHouseResult) showing that its capturing well the similarity between those. This models shows high capacity for capturing the structure of the code

## CodeT5 similarities:

  sim between embs 0-1 : 0.7254
  sim between embs 0-2 : 0.6832
  sim between embs 0-3 : 0.4956
  sim between embs 0-4 : 0.6715
  sim between embs 0-5 : 0.6976
  sim between embs 1-2 : 0.8701
  sim between embs 1-3 : 0.4459
  sim between embs 1-4 : 0.8504
  sim between embs 1-5 : 0.7893
  sim between embs 2-3 : 0.4779
  sim between embs 2-4 : 0.9566
  sim between embs 2-5 : 0.8472
  sim between embs 3-4 : 0.4648
  sim between embs 3-5 : 0.4227
  sim between embs 4-5 : 0.8906

### Analysis CodeT5

The similarities show greater variation. Some are notably low, such as the pair (3–5) with a cosine similarity of 0.42 — which makes sense, as one is typeNullable and the other is the largest function in the snippets, runLightHouseTest. The second lowest similarity is between embeddings 1 and 3 (urlAliasMapping and typeNullable), which also reflects an appropriate semantic distance. Other low scores include 0.46 for embeddings 3–4 (typeNullable and getLightHouseResult), 0.47 for 2–3 (getPathId and typeNullable), and 0.50 for 0–3 (activeEnvironments and typeNullable).

A clear pattern emerges: the model successfully distinguishes between type declarations and other functional roles, which is promising for our purpose. On the other end, the highest similarity is 0.95 between embeddings 2 and 4 (getPathId and getLightHouseResult), followed by 4–5, which we expected to be among the highest. Overall, this model shows strong potential for capturing both subtle and significant differences, as well as meaningful similarities, across code functions.

## CodeBERTa similarities:

  sim between embs 0-1 : 0.7658
  sim between embs 0-2 : 0.6874
  sim between embs 0-3 : 0.4702
  sim between embs 0-4 : 0.6988
  sim between embs 0-5 : 0.7715
  sim between embs 1-2 : 0.8605
  sim between embs 1-3 : 0.5172
  sim between embs 1-4 : 0.8374
  sim between embs 1-5 : 0.7946
  sim between embs 2-3 : 0.5912
  sim between embs 2-4 : 0.9501
  sim between embs 2-5 : 0.8059
  sim between embs 3-4 : 0.5767
  sim between embs 3-5 : 0.4966
  sim between embs 4-5 : 0.8714

### CodeBERTa similarities:

This model also shows a high variability. The lowest similarity is 0.47 for the embedding pair 0-3, "activeEnvironments" and "typeNullable", and the highest for pair 2-4, "getPathId" "getLightHouseResult", These results looks good for capturing meaning in the code however the results of CodeT5 is more fine-grained im comparison with this model, has a more uniform understanding.

## Conclusions

[Emmbedings representation on dimension using PCA](results_pca.png)

It looks like the better embeding modelas are GraphCodeBERT, CodeT5, and CodeBERTa. CodeT5 has a greater coincidence form what we expected on similarities in the results and the PCA graphs looks a good "clustering" for the functions that shouuld be closed. In Cosine similarities number our approach would be trying wiht CodeT5 in autogenration of DOC, and having GraphCodeBERT and CodeBERTa as a backup models.


## Docs related:

[https://huggingface.co/Salesforce/codet5-base](Salesforce/codet5-base)

[https://huggingface.co/huggingface/CodeBERTa-small-v1](CodeBERTa-small-v1)

