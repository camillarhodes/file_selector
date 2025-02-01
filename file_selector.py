import os
import sys

def get_all_files(path, allowed_exts):
    files = set()
    for root, _, filenames in os.walk(path):
        for name in filenames:
            if any(name.endswith(ext) for ext in allowed_exts):
                rel_path = os.path.join(os.path.relpath(root, '.'), name)
                files.add(rel_path)
    return files

def list_files(directories, allowed_exts, file_counter=1, dir_counter=1, prefix='', selected_files=None):
    file_map = {}
    dir_map = {}
    
    if prefix == '':
        print("./")
        prefix = './'
    
    for name in sorted(os.listdir('.')):
        path = os.path.join('.', name)
        rel_path = os.path.join(prefix, name)
        
        if os.path.isdir(path):
            if path not in directories:
                directories[path] = Directory()
            print(f"[ ] d{dir_counter}. {'+ ' if not directories[path].expanded else '- '}{rel_path}/")
            dir_map[dir_counter] = path
            dir_counter += 1
            
            if directories[path].expanded:
                try:
                    os.chdir(path)
                    file_counter, dir_counter, new_files, new_dirs = list_files(
                        directories, allowed_exts, file_counter, dir_counter, 
                        rel_path + '/', selected_files
                    )
                    file_map.update(new_files)
                    dir_map.update(new_dirs)
                    os.chdir('..')
                except PermissionError:
                    pass
        elif any(name.endswith(ext) for ext in allowed_exts):
            selected = '*' if selected_files and rel_path in selected_files else ' '
            print(f"[{selected}] f{file_counter}. {rel_path}")
            file_map[file_counter] = rel_path
            file_counter += 1
            
    return file_counter, dir_counter, file_map, dir_map

class Directory:
    def __init__(self):
        self.expanded = False

def write_output(selected_files):
    if not selected_files:
        print("No files selected")
        return
        
    with open('output.txt', 'w') as out:
        for rel_path in selected_files:
            out.write(f" ===== START OF FILE {rel_path} =====\n")
            with open(rel_path) as f:
                out.write(f.read())
            out.write(f"\n ===== END OF FILE {rel_path} =====\n\n")
    print(f"Created output.txt with {len(selected_files)} files")

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
    selected_files = set()
    
    while True:
        _, _, file_map, dir_map = list_files(directories, allowed_exts, selected_files=selected_files)
        
        print("\n[e]xpand dir, [c]ollapse dir, [ca]ollapse all, [s]elect files, [sd]elect dir, [w]rite output, [q]uit")
        cmd = input("> ").strip()
        parts = cmd.split(None, 1)
        
        if not parts:
            continue
            
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None
        
        if command == 'q':
            write_output(selected_files)
            break
        elif command == 'w':
            write_output(selected_files)
        elif command == 'ca':
            for d in directories.values():
                d.expanded = False
        elif command == 'e':
            if not arg:
                arg = input("Directory number: ")
            try:
                dir_num = int(arg.strip('d'))
                if dir_num in dir_map:
                    directories[dir_map[dir_num]].expanded = True
            except ValueError:
                print("Invalid directory number")
        elif command == 'c':
            if not arg:
                arg = input("Directory number: ")
            try:
                dir_num = int(arg.strip('d'))
                if dir_num in dir_map:
                    directories[dir_map[dir_num]].expanded = False
            except ValueError:
                print("Invalid directory number")
        elif command == 'sd':
            if not arg:
                arg = input("Directory number: ")
            try:
                dir_num = int(arg.strip('d'))
                if dir_num in dir_map:
                    path = dir_map[dir_num]
                    files = get_all_files(path, allowed_exts)
                    selected_files.update(files)
            except ValueError:
                print("Invalid directory number")
        elif command == 's':
            if not arg:
                arg = input("File numbers (space-separated): ")
            try:
                nums = [int(n.strip('f')) for n in arg.split()]
                for n in nums:
                    if n in file_map:
                        if file_map[n] in selected_files:
                            selected_files.remove(file_map[n])
                        else:
                            selected_files.add(file_map[n])
            except ValueError:
                print("Invalid file numbers")

if __name__ == "__main__":
    main()
