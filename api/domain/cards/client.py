import polars as pl

class CardsClient:
    oracle_tags_path: str
    cards_path: str

    def __init__(self, cards_path: str, oracle_tags_path: str):
        self.oracle_tags_path = oracle_tags_path
        self.cards_path = cards_path

        self.oracle_tags = pl.read_ndjson(self.oracle_tags_path, infer_schema_length=10000)
        self.cards = pl.read_ndjson(self.cards_path, infer_schema_length=10000)
        self.cards = self.cards.join(self.oracle_tags, on="oracle_id", how="inner")

if __name__ == '__main__':
    cards_client = CardsClient("/tmp/default_cards.jsonl", "/tmp/oracle_cards.jsonl")
    print(cards_client.cards.head())