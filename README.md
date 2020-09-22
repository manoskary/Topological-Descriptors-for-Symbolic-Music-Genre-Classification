<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/github_username/repo">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Harmonic Analysis and Trajectories</h3>

  <p align="center">
    A Notebook repository for automated harmonic analysis of symbolic music data files with topological tools and graphs. It includes an initiation to genre classification, structure segmentation, key estimation and audio transcription.
    <br />
    <a href="https://github.com/melkisedeath/Topological-Descriptors-for-Symbolic-Music-Genre-Classification"><strong>Explore the docs »</strong></a>
    <br />
    <!-- <br />
    <a href="https://github.com/github_username/repo">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo/issues">Request Feature</a> -->
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [License](#license)
* [Contact](#contact)
* [Future Planning](#future-planning)
* [References](#references)



<!-- ABOUT THE PROJECT -->
## About The Project


This is the work of my internship during the period 25/10/2019 - 24/08/2020. It focuses on the creation of the harmonic fingerprint of musical scores in any symbolic form(mid, xml, mxl, krn, abc, etc.). 

In this project, we present a novel approach for representing music harmony and classifying musical style. Our method is based on the approach of Louis Bigo on Tonnetz trajectories. In this method, we use the Tonnetz to represent the data (i.e. MIDI pieces). A compliance function selects the appropriate Tonnetz for the considered chord material. In this Tonnetz we build a harmonic trajectory of the MIDI piece based on some core principles and different case by case strategies. This trajectory is then reduced to several discrete values which are used for the classification process.

For classification, we use the scikit-learn platform and algorithms. We propose several methods including basic machine learning techniques such as Random Forrests, SVMs, etc but also a method using graph kernels using the GRAKEL algorithms.

This is the update and further developpement of the previous repository. We added graph kernels for classification, connected component labelling for the strong normalisation of the trajectory construction and introduced self-similarity for structure segmetation.

### Built With

* [Python](https://www.python.org/)
* [Grakel](https://github.com/ysig/GraKeL)
* [Music21](http://web.mit.edu/music21/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* The Lakh Dataset
* music21
* networkx
* matplotlib
* scipy
* numpy
* jupyter
* heapq_max
* scikit-learn
* pandas
* grakel

Python related dependencies can be installed using:
```
  $ pip install -r requirements.txt
```
use pip for python 2 & pip3 for python 3

### Installation
 
1. Clone the repo
```sh
git clone https://github.com/melkisedeath/Topological-Descriptors-for-Symbolic-Music-Genre-Classification.git
```
2. Download the Lakh Dataset following the instructions from [The Lakh Dataset](https://colinraffel.com/projects/lmd/) and move the LMD-Matched repository in the results subfolder, i.e. yourPath/Music_Classification/results.
3. Run the notebooks.

<!-- USAGE EXAMPLES -->
## Usage

Each notebook is a usefull demonstration. Run the notebooks and follow the descriptive instructions. You can also read the dissertation for a more complete view. The notebook numbering follows the chapters.

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/melkisedeath/Topological-Descriptors-for-Symbolic-Music-Genre-Classification/issues) for a list of proposed features (and known issues).

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Manos Karistineos - [Linkedin](https://www.linkedin.com/in/manos-karistineos/) - [e-mail](mailto:manoskaristineos@gmail.com)

Project Link: [github.com/melkisedeath/Topological-Descriptors-for-Symbolic-Music-Genre-Classification](https://github.com/melkisedeath/Topological-Descriptors-for-Symbolic-Music-Genre-Classification)

<!-- FUTURE PLANNING -->
## Future Planning

* Using sparse representations for harmonic characteristics. 
* Adapting graph to repeated sections. 
* Better MIDI parsing and filtering. 

<!-- ACKNOWLEDGEMENTS -->
## References
Publication to come!

* [Music Genre Descriptor for Classification based on Tonnetz Trajectories, Emmanouil Karystinaios, Corentin Guichaoua, Moreno Andreatta, Louis Bigo, Isabelle Bloch. *Journée de l'informatique musicale*, 2020.]()

