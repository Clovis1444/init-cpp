# About

This project template is based on idea of **Library-Application Separation** - separating the _reusable logic_ from the _executable code_.

Some ideas for the template structure were taken from this [article](https://medium.com/heuristics/c-application-development-part-1-project-structure-454b00f9eddc).

# Template architecture

```
├── lib/
│   ├── include/
│   │   └── App/
│   ├── src/
│   └── CMakeLists.txt
├── app/
│   ├── src/
│   └── CMakeLists.txt
└── CMakeLists.txt
```

There are 2 subdirectories in this template:

- **lib** - library that contains application logic.
- **app** - executable that uses **lib** library.

## lib

This subdirectory contains 2 main dirs for _source files_:

- **include** - all **public** library headers that will be included in **app**.

> [!IMPORTANT]
> All public headers should be located in a subdir named the same as your application. So when you include your library include should look like this:
>
> ```cpp
> #include "App/App.h"
> ```

- **src** - all **private** library headers and source files that should not be accessible by the **app**.

## app

The purpose of this subdirectory is to utilize **lib** and produce the executable.

All source files should be placed in **src** dir. Source files in this dir should not contain any program main logic.

# Project setup

Run the following command to setup your project:

```bash
python3 ./setupProject.py
```

After your project successfull setup you may delete `setupProject.py` file.

> [!IMPORTANT] > `setupProject.py` supposed to execute on a clean project. There is no guarantee that it will work on a modified project.

# Usage

To build your project use `build.sh`.

To build and run your project use `run.sh`

> [!NOTE]
> To set things like compiler, build generator, etc - edit `build.sh` file
