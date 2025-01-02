import random
from typing import Type
import models


def block_id_generator(
    block_type: Type[models.Block],
) -> models.BlockIdentifier:
    """Generate an appropriate identifier for the given block type.

    Args:
        block_type: The Block class to generate an ID for

    Returns:
        A BlockIdentifier appropriate for the block type
    """
    if block_type == models.ToolProvider:
        return models.ToolProviderIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("tp-{texture}-{tool_noun}")
            )
        )
    elif block_type == models.ToolCall:
        return models.ToolCallIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("tc-{prefix}-{texture}-{tool_noun}")
            )
        )
    elif block_type == models.MultiToolCall:
        return models.MultiToolCallIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("mtc-{prefix}-{texture}-{tool_noun}")
            )
        )
    elif block_type == models.ToolCallResult:
        return models.ToolCallResultIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("tcr-{prefix}-{texture}-{tool_noun}")
            )
        )
    elif block_type == models.MultiToolCallResult:
        return models.MultiToolCallResultIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("mtcr-{texture}-{tool_noun}")
            )
        )
    elif block_type == models.UserInput:
        return models.UserInputIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("ui-{prefix}-{adjective}-{nature_noun}")
            )
        )
    elif block_type == models.Branch:
        return models.BranchIdentifier(
            models.BlockIdentifier(
                friendly_name_generator(
                    "branch-{prefix}-{adjective}-{nature_noun}"
                )
            )
        )
    elif block_type == models.Activity:
        return models.ActivityIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("act-{adjective}-{action_noun}")
            )
        )
    elif block_type == models.ModelResponse:
        return models.ModelResponseIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("mr-{adjective}-{abstract_noun}")
            )
        )
    elif block_type == models.TextBlock:
        return models.BlockIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("text-{adjective}-{abstract_noun}")
            )
        )
    elif block_type == models.Block:
        return models.BlockIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("block-{adjective}-{abstract_noun}")
            )
        )
    elif block_type == models.Noop:
        return models.BlockIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("noop-{adjective}-{abstract_noun}")
            )
        )
    elif block_type == models.Root:
        return models.BlockIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("root-{adjective}-{abstract_noun}")
            )
        )
    elif block_type == models.End:
        return models.BlockIdentifier(
            models.BlockIdentifier(
                friendly_name_generator("end-{adjective}-{abstract_noun}")
            )
        )
    else:
        raise ValueError(f"Unsupported block type: {block_type}")


def friendly_name_generator(format: str = "{adjective}-{color}-{noun}") -> str:
    """
    Creates Docker-style friendly names by combining an adjective and a noun.
    Example: 'elegant-red-forest', 'quiet-blue-mountain', 'peaceful-violet-river'
    """
    adjectives = [
        "admirable",
        "balanced",
        "capable",
        "delightful",
        "elegant",
        "friendly",
        "graceful",
        "helpful",
        "innovative",
        "joyful",
        "kind",
        "lively",
        "mindful",
        "noble",
        "optimistic",
        "peaceful",
        "quiet",
        "reliable",
        "sincere",
        "thoughtful",
        "unique",
        "vibrant",
        "wise",
        "zealous",
    ]

    colors = [
        "amber",
        "azure",
        "beige",
        "bronze",
        "coral",
        "crimson",
        "cyan",
        "emerald",
        "fuchsia",
        "golden",
        "indigo",
        "ivory",
        "jade",
        "lavender",
        "magenta",
        "maroon",
        "mauve",
        "navy",
        "olive",
        "onyx",
        "pearl",
        "plum",
        "ruby",
        "russet",
        "sage",
        "sapphire",
        "scarlet",
        "sienna",
        "silver",
        "teal",
        "turquoise",
        "umber",
        "violet",
    ]

    textures = [
        "brushed",
        "bumpy",
        "coarse",
        "crinkled",
        "crystalline",
        "downy",
        "feathery",
        "fluffy",
        "fuzzy",
        "glossy",
        "grainy",
        "grooved",
        "lustrous",
        "matted",
        "metallic",
        "pearly",
        "polished",
        "rippled",
        "rough",
        "rugged",
        "satiny",
        "silky",
        "sleek",
        "smooth",
        "soft",
        "textured",
        "velvety",
        "wavy",
        "woven",
    ]

    # Different categories of nouns for different block types
    tool_nouns = [
        "anvil",
        "chisel",
        "compass",
        "drill",
        "frame",
        "gear",
        "hammer",
        "index",
        "kernel",
        "lens",
        "motor",
        "packet",
        "pulley",
        "query",
        "router",
        "sensor",
        "signal",
        "switch",
        "table",
        "token",
        "tool",
        "wrench",
    ]

    nature_nouns = [
        "aurora",
        "brook",
        "canyon",
        "cliff",
        "cloud",
        "creek",
        "forest",
        "glacier",
        "grove",
        "hill",
        "lake",
        "meadow",
        "mountain",
        "ocean",
        "peak",
        "ridge",
        "river",
        "valley",
        "waterfall",
    ]

    abstract_nouns = [
        "axiom",
        "cipher",
        "delta",
        "echo",
        "enigma",
        "graph",
        "layer",
        "logic",
        "matrix",
        "nexus",
        "node",
        "oracle",
        "prism",
        "schema",
        "syntax",
        "theory",
        "vector",
        "zenith",
    ]

    action_nouns = [
        "beacon",
        "flow",
        "leap",
        "pulse",
        "quest",
        "spark",
        "stride",
        "surge",
        "sweep",
        "swing",
        "twist",
        "wave",
    ]

    # Select random words from each category
    adjective = random.choice(adjectives)
    color = random.choice(colors)
    texture = random.choice(textures)
    tool_noun = random.choice(tool_nouns)
    nature_noun = random.choice(nature_nouns)
    abstract_noun = random.choice(abstract_nouns)
    action_noun = random.choice(action_nouns)
    noun = random.choice([tool_noun, nature_noun, abstract_noun, action_noun])

    # Create a dictionary of available components
    components = {
        "adjective": adjective,
        "color": color,
        "texture": texture,
        "tool_noun": tool_noun,
        "nature_noun": nature_noun,
        "abstract_noun": abstract_noun,
        "action_noun": action_noun,
        "noun": noun,
    }

    # Use the format string with the components dictionary
    return format.format(**components)
