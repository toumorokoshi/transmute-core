import os
import shutil
import sys
import subprocess
from uranium import current_build
from uranium.rules import rule, Once

current_build.packages.install("uranium-plus[vscode]")
import uranium_plus

current_build.config.update(
    {
        "uranium-plus": {
            "module": "transmute_core",
            "publish": {"additional_args": ["--release"]},
            "test": {"packages": ["mock", "pytest-benchmark", "flask", "tornado"]},
        }
    }
)

if sys.version_info > (3, 4):
    current_build.packages.install("aiohttp")
    current_build.packages.install("pytest-aiohttp")

if sys.version_info > (3, 6):
    current_build.packages.install("pydantic")

uranium_plus.bootstrap(current_build)
current_build.tasks.prepend("install_swagger_ui", "main")
current_build.tasks.prepend("clean_and_install_swagger_ui", "publish")


def dev_docs(build):
    build.packages.install("Babel")
    build.packages.install("Sphinx")
    build.packages.install("Sphinx-autobuild")
    build.packages.install("sphinx_rtd_theme")
    build.packages.install("sphinxcontrib-programoutput")
    return build.executables.run(
        ["sphinx-autobuild", "docs", os.path.join("docs", "_build")]
        + build.options.args
    )[0]


@rule(Once())
def install_swagger_ui(build):
    clean_and_install_swagger_ui(build)


def clean_and_install_swagger_ui(build):
    import io
    import shutil
    import tarfile

    version = "3.20.9"
    PATH = "https://github.com/swagger-api/swagger-ui/archive/v{0}.tar.gz".format(
        version
    )
    TARGET_PATH = os.path.join(build.root, "transmute_core", "swagger", "static")
    EXTRACTED_TOP_LEVEL_DIRNAME = "swagger-ui-{0}".format(version)
    build.packages.install("requests")
    import requests

    r = requests.get(PATH, stream=True)
    stream = io.BytesIO()
    stream.write(r.content)
    stream.seek(0)
    tf = tarfile.TarFile.open(fileobj=stream)
    if os.path.exists(TARGET_PATH):
        shutil.rmtree(TARGET_PATH)
    tf.extractall(path=TARGET_PATH)
    # move the files under the top level directory.
    for name in os.listdir(
        os.path.join(TARGET_PATH, EXTRACTED_TOP_LEVEL_DIRNAME, "dist")
    ):
        shutil.move(
            os.path.join(TARGET_PATH, EXTRACTED_TOP_LEVEL_DIRNAME, "dist", name),
            TARGET_PATH,
        )
