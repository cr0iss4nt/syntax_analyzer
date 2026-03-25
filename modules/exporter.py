import os

def analysis_to_export_text(analysis):
    content = "token,pos,dependency,parent_parent_pos\n"
    content += '\n'.join(','.join([f"'{i}'" for i in analysis]))
    return content