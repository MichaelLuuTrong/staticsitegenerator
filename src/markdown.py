from enum import Enum

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

def block_to_block_type



