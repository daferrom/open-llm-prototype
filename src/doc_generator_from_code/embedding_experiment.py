from transformers import AutoTokenizer, AutoModel, T5EncoderModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from itertools import combinations




# snippets examples from results.vue #

snippets = [
    """
        const activeEnvironments = await useAsyncData('activeEnvironments',
            async () => await $fetch('/api/environments/active'),
***REMOVED***;
    """,
    """
        const urlAliasMapping = computed(() => {
        if (activeEnvironments?.data?.value?.pathMap) {
            const pathValues = activeEnvironments.data.value.pathMap.map(path => path.alias);
            return [...new Set(pathValues)];
        }
        return [];
        });
    """,
    """
        const "getPathId" = (alias: Nullable<string>, id: Nullable<number>) => {
        if (alias === null || id === null) {
            return null;
        }
        return activeEnvironments.data.value?.pathMap.find(value => value.alias === alias && value.brandId === id)?.id ?? null;
        };
    """,
    """
        type Nullable<T> = T | null;
    """,
    """
        const getLightHouseResult = (aliasId: Nullable<number>, dnsId: Nullable<number>) => {
        if (aliasId === null || dnsId === null) {
            return null;
        }
        return activeEnvironments.data.value?.lightHouseResults.find(
            value => value.pathId === aliasId && value.dnsId === dnsId,
***REMOVED*** ?? null;
        };
    """,
    """
        const runLightHouseTest = async (pathId: Nullable<number>, dnsId: number) => {
        // pathId, dnsId
        if (pathId === null || dnsId === null) {
            console.log('Path ID or DNS ID is null');
            return;
        }
        const result = await $fetch('/api/lighthouse/run', {
            method: 'POST',
            body: {
            pathId,
            dnsId,
            },
        });
        console.log('Lighthouse test result:', result);
        await activeEnvironments.refresh();
        };
    """
]

labels = [
    "activeEnvironments",
    "urlAliasMapping",
    "getPathId",
    "typeNullable",
    "getLightHouseResult",
    "runLightHouseTest"]

# Embeddings Models
model_configs = {
    "CodeBERT": ("microsoft/codebert-base", AutoModel),
    "GraphCodeBERT": ("microsoft/graphcodebert-base", AutoModel),
    "CodeT5": ("Salesforce/codet5-base", T5EncoderModel),
    "CodeBERTa": ("huggingface/CodeBERTa-small-v1", AutoModel),
}

def get_embeddings(model_id, model_class, texts):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = model_class.from_pretrained(model_id)
    model.eval()

    embeddings = []
    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            last_hidden = outputs.last_hidden_state
            pooled = last_hidden.mean(dim=1).squeeze().numpy()
            embeddings.append(pooled)
    return embeddings

# Obtain embeddings for each model
embeddings_by_model = {
    name: get_embeddings(mid, mclass, snippets)
    for name, (mid, mclass) in model_configs.items()
}

# Calculate cosine similarity between 1 - 0
print("🔍 Cosine similarity per model:")
for model_name, embeddings in embeddings_by_model.items():
    print(f"\n{model_name} similarities:")
    print(f"\n{model_name} similarities:")
    for i, j in combinations(range(len(embeddings)), 2):
        sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
        print(f"  sim between embs {i}-{j} : {sim:.4f}")

# Visualize embeddings with  PCA
pca = PCA(n_components=2)
plt.figure(figsize=(18, 6))
for i, (model_name, embeddings) in enumerate(embeddings_by_model.items()):
    reduced = pca.fit_transform(embeddings)
    plt.subplot(2, 3, i + 1)
    for j, point in enumerate(reduced):
        plt.scatter(*point)
        plt.text(point[0] + 0.01, point[1] + 0.01, labels[j])
    plt.title(model_name)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
plt.tight_layout()
plt.show()