import os
import re


def validateProjectName() -> str:
    project_name: str
    while True:
        project_name = input("Enter your project name: ")

        # Validate user input:
        # - May contain only letters, digits, underscores, dashes
        # - Must start with a letter
        if not project_name:
            continue
        if re.search(r"[^a-zA-Z0-9_-]", project_name):
            print("Project name may contain only letters, digits, underscores, dashes!")
            continue
        if project_name[0] in {"_", "-"} or project_name[0].isdigit():
            print("Project name must start with a letter!")
            continue

        break

    return project_name


def readFileLines(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines


def changeLine(lines: list[str], pattern: str, new_text: str):
    r_pattern = re.compile(pattern)
    for i, line in enumerate(lines):
        if r_pattern.search(line):
            lines[i] = r_pattern.sub(new_text, line)
            return


def writeFile(file_path: str, file_lines: list[str]):
    with open(file_path, "w") as file:
        file.writelines(file_lines)


def setupProject(name: str):
    # We need to do the following changes:
    # - Change project name in the root CMakeLists.txt
    # - Change [target names, lib name] in the app CMakeLists.txt
    # - Change [lib names, sources paths] in the lib CMakeLists.txt
    # - Change namespace in lib header
    # - Change [include, namespace] in lib cpp
    # - Change [include, namespace] in app cpp
    # - Rename lib source files and lib include subdir
    # - Change $TARGET in run.sh

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # root CMakeLists.txt
    root_cmake_path: str = os.path.join(script_dir, "CMakeLists.txt")
    root_cmake_lines: list[str] = readFileLines(root_cmake_path)
    changeLine(root_cmake_lines, r"project\((\w+)\s+VERSION", f"project({name} VERSION")
    writeFile(root_cmake_path, root_cmake_lines)

    # app CMakeLists.txt
    app_cmake_path: str = os.path.join(script_dir, "app/CMakeLists.txt")
    app_cmake_lines: list[str] = readFileLines(app_cmake_path)
    changeLine(app_cmake_lines, r"add_executable\((\w+)\s", f"add_executable({name} ")
    changeLine(
        app_cmake_lines,
        r"target_link_libraries\((\w+)\s",
        f"target_link_libraries({name} ",
    )
    changeLine(app_cmake_lines, r"PRIVATE\s(\w+)Lib\)", f"PRIVATE {name}Lib)")
    writeFile(app_cmake_path, app_cmake_lines)

    # lib CMakeLists.txt
    lib_cmake_path: str = os.path.join(script_dir, "lib/CMakeLists.txt")
    lib_cmake_lines: list[str] = readFileLines(lib_cmake_path)
    changeLine(lib_cmake_lines, r"add_library\((\w+)Lib\s", f"add_library({name}Lib ")
    changeLine(
        lib_cmake_lines,
        r"target_include_directories\((\w+)Lib\s",
        f"target_include_directories({name}Lib ",
    )
    changeLine(lib_cmake_lines, r"/include/\w+/\w+\.h", f"/include/{name}/{name}.h")
    changeLine(lib_cmake_lines, r"/src/\w+\.cpp", f"/src/{name}.cpp")
    writeFile(lib_cmake_path, lib_cmake_lines)

    # lib header
    lib_include_dir: str = os.path.join(script_dir, "lib/include/")
    lib_include_subdir: str = os.path.join(
        lib_include_dir, os.listdir(lib_include_dir)[0]
    )
    lib_header_path: str = os.path.join(
        lib_include_subdir, os.listdir(lib_include_subdir)[0]
    )

    lib_header_lines: list[str] = readFileLines(lib_header_path)
    changeLine(lib_header_lines, r"namespace\s\w+\s", f"namespace {name} ")
    writeFile(lib_header_path, lib_header_lines)

    # lib cpp
    lib_src_dir: str = os.path.join(script_dir, "lib/src/")
    lib_cpp_path: str = os.path.join(lib_src_dir, os.listdir(lib_src_dir)[0])

    lib_cpp_lines: list[str] = readFileLines(lib_cpp_path)
    changeLine(
        lib_cpp_lines, r"#include\s\"\w+/\w+\.h\"", f'#include "{name}/{name}.h"'
    )
    changeLine(lib_cpp_lines, r"namespace\s\w+\s{", f"namespace {name} {{")
    changeLine(lib_cpp_lines, r"//\snamespace\s\w+", f"// namespace {name}")
    writeFile(lib_cpp_path, lib_cpp_lines)

    # app cpp
    app_src_dir: str = os.path.join(script_dir, "app/src/")
    app_cpp_path: str = os.path.join(app_src_dir, os.listdir(app_src_dir)[0])
    app_cpp_lines: list[str] = readFileLines(app_cpp_path)
    changeLine(
        app_cpp_lines, r"#include\s\"\w+/\w+\.h\"", f'#include "{name}/{name}.h"'
    )
    changeLine(app_cpp_lines, r"\w+::Hello", f"{name}::Hello")
    writeFile(app_cpp_path, app_cpp_lines)

    # lib sources rename
    new_lib_header_path: str = os.path.join(lib_include_subdir, f"{name}.h")
    os.rename(lib_header_path, new_lib_header_path)
    new_lib_cpp_path: str = os.path.join(lib_src_dir, f"{name}.cpp")
    os.rename(lib_cpp_path, new_lib_cpp_path)
    # lib include subdir rename
    new_lib_include_subdir: str = os.path.join(lib_include_dir, name)
    os.rename(lib_include_subdir, new_lib_include_subdir)

    # run script $TARGET
    run_script_path: str = os.path.join(script_dir, "run.sh")
    run_script_lines: list[str] = readFileLines(run_script_path)
    changeLine(run_script_lines, r"TARGET=\"/app/\w+\"", f'TARGET="/app/{name}"')
    writeFile(run_script_path, run_script_lines)


def main():
    project_name = validateProjectName()

    setupProject(project_name)

    print("Your project was successfully setup!")


main()
