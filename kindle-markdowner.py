import re
import os

def parse_clippings(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    # Split the content into individual clippings
    clippings = content.split('==========')
    
    books = {}
    
    for i, clipping in enumerate(clippings):
        clipping = clipping.strip()
        if not clipping:
            continue
        
        # Extract the book title and highlight
        lines = clipping.split('\n')
        
        if len(lines) < 3:
            print(f"Skipping clipping {i+1}: not enough lines")
            continue
        
        title = lines[0].strip()
        highlight = lines[-1].strip()  # The last non-empty line should be the highlight
        
        # Remove potential Byte Order Mark (BOM) from the title
        title = title.lstrip('\ufeff')
        
        print(f"Clipping {i+1}:")
        print(f"Title: {title}")
        print(f"Highlight: {highlight}")
        
        if title and highlight:
            if title not in books:
                books[title] = []
            books[title].append(highlight)
    
    print(f"Parsed {len(books)} books from clippings.")
    return books

def write_to_markdown(books):
    # Create output directory if it does not exist
    output_dir = "Kindle_Highlights"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for title, highlights in books.items():
        # Create a valid filename
        file_name = re.sub(r'[\\/*?:"<>|]', "", title) + ".md"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {title}\n\n")
            for highlight in highlights:
                file.write(f"- {highlight}\n\n")
        print(f"Created file: {file_path}")

def main():
    file_path = 'My Clippings.txt'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    books = parse_clippings(file_path)
    write_to_markdown(books)
    print(f"Markdown files have been created in the 'Kindle_Highlights' directory.")

if __name__ == "__main__":
    main()
