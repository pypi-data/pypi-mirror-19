from distutils.core import setup
setup(
    name="appJar",
    packages=["appJar"],
    version="0.01",
    description="A GUI wrapper for tkinter",
    author="Richard Jarvis",
    author_email="info@appjar.info",
    url="http://appJar.info",
    keywords=["python", "gui", "tkinter"],
    classifiers=[],
    include_package_date = True,
    package_data = {
        "appJar": ["lib/*", "resources/icons/*", "examples/*"]
    }
)
