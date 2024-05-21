@startuml

package "Data Normalization and Feature Engineering" {
    class NormalizeKeypoints {
        +normalize_keypoints(keypoints: array): array
    }

    class RelativeCoordinates {
        +relative_coordinates(keypoints: array): array
    }

    class ExtractFeatures {
        +extract_features(keypoints: array): array
    }

    class PreprocessKeypoints {
        +preprocess_keypoints(keypoints: array): array
    }
}

package "Dataset and Pair Construction" {
    class HandGestureDataset {
        +__init__(data_dir: str)
        +__len__(): int
        +__getitem__(idx: int): tuple
    }

    class CreatePairs {
        +create_pairs(data: array, labels: array): tuple
    }
}

package "Siamese MLP Network" {
    class SiameseNetwork {
        +__init__()
        +forward_once(x: tensor): tensor
        +forward(input1: tensor, input2: tensor): tuple
    }

    class ContrastiveLossFunction {
        +contrastive_loss_function(output1: tensor, output2: tensor, label: tensor, margin: float): tensor
    }

    class Train {
        +train(model: SiameseNetwork, dataloader: DataLoader, optimizer: Optimizer, num_epochs: int)
    }
}

package "Few-shot Learning and Embedding Storage" {
    class SaveEmbeddings {
        +save_embeddings(model: SiameseNetwork, dataloader: DataLoader, file_path: str)
    }

    class LoadAverageEmbeddings {
        +load_average_embeddings(file_path: str): dict
    }

    class GetEmbedding {
        +get_embedding(model: SiameseNetwork, sample: array): array
    }

    class CalculateSimilarity {
        +calculate_similarity(embedding: array, average_embeddings: array): array
    }

    class ClassifySample {
        +classify_sample(embedding: array, average_embeddings: array, threshold: float): int
    }

    class AddNewClassSupportSet {
        +add_new_class_support_set(model: SiameseNetwork, support_set: list, label: int, file_path: str)
    }
}

NormalizeKeypoints --> PreprocessKeypoints
RelativeCoordinates --> PreprocessKeypoints
ExtractFeatures --> PreprocessKeypoints
PreprocessKeypoints --> HandGestureDataset
HandGestureDataset --> CreatePairs
CreatePairs --> Train
SiameseNetwork --> Train
ContrastiveLossFunction --> Train
Train --> SaveEmbeddings
SaveEmbeddings --> LoadAverageEmbeddings
LoadAverageEmbeddings --> ClassifySample
GetEmbedding --> ClassifySample
CalculateSimilarity --> ClassifySample
ClassifySample --> AddNewClassSupportSet

@enduml
