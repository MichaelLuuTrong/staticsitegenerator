from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    #markdown is a string reprsenting a full document
    res = []
    markdown_split_by_double_newlines = markdown.split('\n\n')

    split_stripped_item_array = []
    for item in markdown_split_by_double_newlines:
        leading_trailing_stripped = item.strip('\n')
        split_again = leading_trailing_stripped.split('\n')
        split_stripped_item_array.append(split_again)
    for item in split_stripped_item_array:
        # print(repr(item))
        if not item:
            continue
        elif len(item) == 1:
            single_item_stripped = item[0].strip()
            res.append(single_item_stripped)
        else:                
            stripped_subitems = []
            for subitem in item:
                stripped_subitem = subitem.strip()
                if stripped_subitem:
                    stripped_subitems.append(stripped_subitem)
            res.append('\n'.join(stripped_subitems))
    return res

def block_to_block_type(block):
    split_block = block.split('\n')
    if re.fullmatch(r"#{1,6} .+", split_block[0]):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in split_block):
        return BlockType.QUOTE
    if all(re.match(r"^[-*+] ", line) for line in split_block):
        return BlockType.UNORDERED_LIST
    if not split_block:
        raise TypeError("block is not a string")
    
    numbers = []
    for line in split_block:
        match = re.match(r"^(\d+)\.", line)
        if match:
            numbers.append(int(match.group(1)))
        else:
            return BlockType.PARAGRAPH
        
    if not numbers:
        return BlockType.PARAGRAPH
    if numbers[0] != 1:
        return BlockType.PARAGRAPH
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1] + 1:
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST







