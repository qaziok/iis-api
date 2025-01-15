from datasets import load_dataset

if __name__ == "__main__":
    ds = load_dataset("wikimedia/wikipedia", "20231101.pl", split='train')
