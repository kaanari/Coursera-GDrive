import setuptools
from coursera_gdrive import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coursera-GDrive",
    version=__version__,
    author="Kaan ARI",
    author_email="kaan.ari.tr@gmail.com",
    description="This small project is helpful for downloading Coursera courses into your Google Drive via Google Colab.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaanaritr/Coursera-GDrive",
    license="LGPLv3",
    packages=setuptools.find_packages(),
    keywords=['coursera-dl', 'coursera','download', 'education', 'MOOCs', 'google-drive'],
    classifiers=[
	"Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Other Environment",
    ],
    python_requires='>=3.0',
    project_urls={
        'Documentation':'https://github.com/kaanaritr/Coursera-GDrive',
        'Say Thanks!':'https://github.com/coursera-dl/coursera-dl',
        'Source':'https://github.com/kaanaritr/Coursera-GDrive',
    },
    install_requires=[
        'coursera-dl>=0.11.0'
    ],
    include_package_data=True,
    package_data={'': ['coursera_gdrive/lib/*.csv']}
)
