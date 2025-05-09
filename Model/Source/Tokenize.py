from transformers import DataCollatorWithPadding, AutoTokenizer
from torch.utils.data import DataLoader
from datasets import load_dataset, Dataset

def Tokenize(path_f='', path_l=''):
    # Load dữ liệu từ file
    dataset_feature = load_dataset("text", data_files=path_f, split="train")
    dataset_label = load_dataset("text", data_files=path_l, split="train")

    # Làm sạch label: chuyển từ chuỗi → số nguyên
    def clean_label(example):
        try:
            return {"label": int(str(example["text"]).strip())}
        except:
            return {"label": 0}  # fallback nếu lỗi

    dataset_label = dataset_label.map(clean_label)
    dataset_label = dataset_label.remove_columns("text")

    # Gộp feature và label lại thành 1 dataset
    data_combined = Dataset.from_dict({
        "feature": dataset_feature["text"],
        "label": dataset_label["label"]
    })

    # Tokenize
    checkpoint = "wonrax/phobert-base-vietnamese-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def tokenize_function(examples):
        return tokenizer(examples["feature"], truncation=True)

    tokenized_datasets = data_combined.map(tokenize_function, batched=True)

    # Loại token_type_ids nếu tồn tại (PhoBERT không cần)
    if "token_type_ids" in tokenized_datasets.column_names:
        tokenized_datasets = tokenized_datasets.remove_columns(["feature", "token_type_ids"])
    else:
        tokenized_datasets = tokenized_datasets.remove_columns(["feature"])

    tokenized_datasets.set_format("torch")
    data_collator = DataCollatorWithPadding(tokenizer)

    # DataLoader
    train_dataloader = DataLoader(
        tokenized_datasets, shuffle=True, batch_size=5, collate_fn=data_collator
    )

    return train_dataloader