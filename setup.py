import setuptools
#from setup_qt import build_qt

# Cmd: pyinstaller --name="pntest" --windowed ./src/__main__.py --onedir

setuptools.setup(
  name = "pntest", # Replace with your own username
  version = "0.0.1",
  author = "Evan Rolfe",
  author_email = "author@example.com",
  description = "A small example package",
  long_description = "...",
  long_description_content_type = "text/markdown",
  url = "https://github.com/pypa/sampleproject",
  package_dir = {'': 'src'},
  #packages = ['frontend'], #setuptools.find_packages(where = 'src'),
  classifiers = [
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires = '>=3.6',
  entry_points={
    "gui_scripts": [
      "pntest = __main__:main",
    ]
  },
  install_requires=[
    "PySide2"
  ],
  # options=[
  #   'build_qt': {
  #     'packages': ['pntest'],
  #   }
  # ],
  # cmdclass={
  #   'build_qt': build_qt,
  # },
)
