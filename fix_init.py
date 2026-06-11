import os

init_dirs = [
    "app",
    "app/api",
    "app/api/v1",
    "app/api/v1/endpoints",
    "app/core",
    "app/models",
    "app/repositories",
    "app/services",
    "tests",
    "tests/unit",
    "tests/integration"
]

for dir_path in init_dirs:
    init_file = os.path.join(dir_path, "__init__.py")
    with open(init_file, "w", encoding="utf-8") as f:
        f.write("#")
    print(f"Created: {init_file}")