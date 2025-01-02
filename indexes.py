"""Block indexing and lookup functionality."""

import models


class Index:
    def add(self, block: models.Block) -> None: ...

    def get(self, id: models.BlockIdentifier) -> models.Block | None: ...


class MemoryIndex(Index):
    """Maintains mappings between block IDs and block instances."""

    def __init__(self) -> None:
        self._blocks: dict[models.BlockIdentifier, models.Block] = {}

    def add(self, block: models.Block) -> None:
        """Index a block and mark it as indexed.

        Args:
            block: The block to index
        """
        self._blocks[block.id] = block
        block.indexed = True

    def get(self, id: models.BlockIdentifier) -> models.Block | None:
        """Retrieve a block by its identifier.

        Args:
            id: The block identifier to look up

        Returns:
            The block if found, None otherwise
        """
        return self._blocks.get(id)
