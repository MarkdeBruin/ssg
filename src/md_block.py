from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()

    match block:
        case b if b.startswith("```") and b.endswith("```"):
            return BlockType.CODE

        case b if b.startswith("#"):
            prefix = b.split(" ", 1)[0]
            if 1 <= len(prefix) <= 6 and all(ch == "#" for ch in prefix):
                return BlockType.HEADING

        case _ if all(line.strip().startswith(">") for line in lines):
            return BlockType.QUOTE

        case _ if all(line.strip().startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST

        case _ if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH