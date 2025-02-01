import os
import sys

def list_files(directories, allowed_exts, file_counter=1, prefix=''):
    file_map = {}
    
    if prefix == '':
        print("./")
        prefix = './'
    
    for name in sorted(os.listdir('.')):
        path = os.path.join('.', name)
        rel_path = os.path.join(prefix, name)
        
        if os.path.isdir(path):
            if path not in directories:
                directories[path] = Directory()
            print(f"{'+ ' if not directories[path].expanded else '- '}{rel_path}/")
            if directories[path].expanded:
                try:
                    os.chdir(path)
                    file_counter, new_files = list_files(directories, allowed_exts, file_counter, rel_path + '/')
                    file_map.update(new_files)
                    os.chdir('..')
                except PermissionError:
                    pass
        elif any(name.endswith(ext) for ext in allowed_exts):
            print(f"{file_counter}. {rel_path}")
            file_map[file_counter] = rel_path
            file_counter += 1
            
    return file_counter, file_map

class Directory:
    def __init__(self):
        self.expanded = False

def main():
    if len(sys.argv) < 2:
        print("Error: No file extensions provided")
        print("Usage: python file_selector.py .ext1 .ext2 ...")
        print("Example: python file_selector.py .py .txt")
        sys.exit(1)

    allowed_exts = sys.argv[1:]
    if not all(ext.startswith('.') for ext in allowed_exts):
        print("Error: Extensions must start with '.'")
        sys.exit(1)

    directories = {}
    while True:
        _, file_map = list_files(directories, allowed_exts)
        
        print("\n[e]xpand dir, [c]ollapse dir, [s]elect files, [q]uit")
        cmd = input("> ").strip()
        parts = cmd.split(None, 1)
        
        if not parts:
            continue
            
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None
        
        if command == 'q':
            break
        elif command == 'e':
            if not arg:
                arg = input("Directory to expand: ")
            path = os.path.join('.', arg.strip('./'))
            if path in directories:
                directories[path].expanded = True
        elif command == 'c':
            if not arg:
                arg = input("Directory to collapse: ")
            path = os.path.join('.', arg.strip('./'))
            if path in directories:
                directories[path].expanded = False
        elif command == 's':
            if not arg:
                arg = input("File numbers (space-separated): ")
            nums = arg.split()
            selected = [file_map[int(n)] for n in nums if int(n) in file_map]
            
            with open('output.txt', 'w') as out:
                for rel_path in selected:
                    out.write(f" ===== START OF FILE {rel_path} =====\n")
                    with open(rel_path) as f:
                        out.write(f.read())
                    out.write(f"\n ===== END OF FILE {rel_path} =====\n\n")
            print(f"Created output.txt with {len(selected)} files")

if __name__ == "__main__":
    main()
