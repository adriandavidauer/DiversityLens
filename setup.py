from setuptools import setup, find_packages

setup(
    name="diversitylens",
    version="0.1.0",
    description="A Python library for demographic analysis (age, gender, ethnicity) of faces in image datasets.",
    author="Veli Ates",
    author_email="veli58ates@gmail.com",
    url="https://github.com/veliatees/DiversityLens",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "opencv-python>=4.5.5.64",
        "dlib>=19.24.0",
        "deepface>=0.0.79",
        "numpy>=1.21.0",
        "Pillow>=9.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
