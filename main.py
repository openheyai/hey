import models

from generators import user, claude, tools
from tools.equip import equip

if __name__ == "__main__":
    # we start with the root node
    root = models.Root(id="main", parent=None)

    root = equip(root, "fork")
    root = equip(root, "forks")
    root = equip(root, "activate")

    generators = [user.evaluate, claude.evaluate, tools.evaluate]

    current = root

    while True:
        for generator in generators:
            next_block = generator(current)
            try:
                if next_block != current:
                    break
            finally:
                current = next_block
