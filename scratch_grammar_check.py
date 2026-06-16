import re
import sys

def check_latex_grammar(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
        
    issues = []
    
    # regex for double words, ignoring case
    # we need to be careful with LaTeX commands like \ref \ref, but usually double words are plain text
    double_word_re = re.compile(r'\b([a-zA-Z]{2,})\s+\1\b', re.IGNORECASE)
    
    # regex for punctuation spacing like "word ,", "word .", but ignoring e.g., "Eq .", though "Eq." has no space
    bad_punctuation_re = re.compile(r'[a-zA-Z]\s+([\,\.])')
    
    # sentence starting with lowercase (very heuristic, might have many false positives)
    # lowercase_start_re = re.compile(r'(?:^|[.?!]\s+)[a-z]')

    for i, line in enumerate(lines):
        line_num = i + 1
        
        # strip comments
        if '%' in line and not r'\%' in line:
            line = line.split('%', 1)[0]
            
        # check double words
        doubles = double_word_re.findall(line)
        for d in doubles:
            # ignore common LaTeX repeats like "in in" or specific code
            if d.lower() not in ['the', 'a', 'is', 'to', 'that', 'and', 'of', 'in']:
                issues.append(f"Line {line_num}: Possible double word '{d} {d}'")
            elif d.lower() in ['the', 'a', 'is', 'to', 'that', 'and', 'of', 'in']:
                issues.append(f"Line {line_num}: Double word '{d} {d}'")
                
        # check bad punctuation
        bads = bad_punctuation_re.findall(line)
        if bads:
            # check if it's not some math mode thing (very naive)
            if '$' not in line:
                issues.append(f"Line {line_num}: Bad punctuation spacing before {bads}")
                
        # basic check for "an" vs "a"
        # finds " a [aeiou]" or " an [^aeiou]"
        a_an = re.findall(r'\b(a|an)\s+([a-zA-Z]+)', line, re.IGNORECASE)
        for article, next_word in a_an:
            article = article.lower()
            next_word = next_word.lower()
            if article == 'a' and next_word[0] in 'aeiou':
                # exceptions: "a user", "a universe", "a one"
                if not (next_word.startswith('uni') or next_word.startswith('use') or next_word == 'one'):
                    issues.append(f"Line {line_num}: 'a {next_word}' should maybe be 'an {next_word}'?")
            elif article == 'an' and next_word[0] not in 'aeiou':
                # exceptions: "an hour"
                if not (next_word == 'hour'):
                    issues.append(f"Line {line_num}: 'an {next_word}' should maybe be 'a {next_word}'?")

    if issues:
        print("Grammar/Typo Potential Issues:")
        for issue in issues[:100]:  # print up to 100
            print(issue)
    else:
        print("No obvious simple typos found.")

if __name__ == '__main__':
    check_latex_grammar(sys.argv[1])
