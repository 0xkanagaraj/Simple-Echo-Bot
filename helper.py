from aiogram import types
from typing import List

# To handle text formatting
def preserve_entities(text: str, entities: List[types.MessageEntity]) -> str:
    if not text:
        return None
    elif text and not entities:
        return text

    # Sort entities by start position and length (longest first)
    sorted_entities = sorted(entities, key=lambda e: (e.offset, -e.length))
    
    # Convert to list for easier manipulation
    chars = list(text)
    tag_stack = []
    
    # Insert tags directly into the character array
    for entity in sorted_entities:
        start = entity.offset
        end = start + entity.length
        
        # Opening tag
        opening_tag = _get_opening_tag(entity)
        chars.insert(start, opening_tag)
        tag_stack.append((end + len(opening_tag), _get_closing_tag(entity)))  # Track position and closing tag
        
        # Adjust positions of subsequent entities
        for i in range(sorted_entities.index(entity) + 1, len(sorted_entities)):
            if sorted_entities[i].offset >= start:
                sorted_entities[i].offset += len(opening_tag)
    
    # Insert closing tags in reverse order
    for pos, closing_tag in sorted(tag_stack, reverse=True):
        chars.insert(pos, closing_tag)
    
    text = ''.join(chars)
    if not text:
        return None
    return text

def _get_opening_tag(entity: types.MessageEntity) -> str:
    """Returns the appropriate opening tag for each entity type"""
    match entity.type:
        case "bold": return "<b>"
        case "italic": return "<i>"
        case "underline": return "<u>"
        case "strikethrough": return "<s>"
        case "spoiler": return "<tg-spoiler>"
        case "code": return "<code>"
        case "pre": return "<pre>"
        case "text_link": return f'<a href="{entity.url}">'
        case _: return ""

def _get_closing_tag(entity: types.MessageEntity) -> str:
    """Returns the appropriate closing tag for each entity type"""
    match entity.type:
        case "bold": return "</b>"
        case "italic": return "</i>"
        case "underline": return "</u>"
        case "strikethrough": return "</s>"
        case "spoiler": return "</tg-spoiler>"
        case "code": return "</code>"
        case "pre": return "</pre>"
        case "text_link": return "</a>"
        case _: return ""
