class SimilarItemsResult:
    def __init__(self, metadata, items=[]):
        self.title     = f'Similars ({metadata.name} Recommender)'
        self.items     = items
        self.metadata  = metadata

    def not_empty(self): len(self.items) > 0