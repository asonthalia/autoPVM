<div id="top"></div>
<!--
*** Thanks for checking out the autoPVM project! If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/asonthalia/autoPVM">
    <img src="Images/autoPVM_logo.png" alt="Logo" width="168" height="262">
  </a>

  <h3 align="center">autoPVM v0.1</h3>

  <p align="center">
    Automatically conduct Price-Volume-Mix analysis on datasets.
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/asonthalia/autoPVM/issues">Report Bug</a>
    ·
    <a href="https://github.com/asonthalia/autoPVM/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<a href="https://github.com/asonthalia/autoPVM">
    <img src="https://github.com/asonthalia/autoPVM/blob/main/Images/autoPVM_Bridge.png" alt="Logo" width="535" height="349">
  </a>

This project aims at conducting the Price Variance Mix analysis automatically. The main purpose of PVM analysis is to provide a high-level overview view into the past, and to break down the change in revenue or margins into some key components or categories. The categories are used to highlight and help explain how much of the overall change in revenue or margins was caused by, e.g. the implemented Price changes, versus changes in total costs, versus the impact from change in Volumes, versus changes other effects, comparing two different time periods.  

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Installation

The autoPVM package can be installed using pip.

1. autoPVM uses Numpy, Pandas & Plotly as dependencies.
2. Install package

   ```
   pip install autoPVM
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Import the PVM class using
```
from autoPVM import PVM
```

Read a Pandas dataframe
```
data = pd.read_csv('Sample Dataset/Supermarket Sales.csv')
```

Create an analysis object and pass the dataframe
```
pvm = PVM.PVMAnalysis(data=data)
```

Set column name markers of required quantities and margins
```
PVM.setMarkers(\
                 quantity_pr='QTY_PM'
               , quantity_ac='QTY_AM'
               , margin_pr='MARGIN_PM'
               , margin_ac='MARGIN_AM'
               , hierarchy=['Customer type', 'Gender', 'Branch', 'Product line'])
```
<ul>
  <li> `quantity_pr` marks previous time period quantity</li>
  <li> quantity_ac marks current/next time period quantity</li>
  <li> margin_pr marks previous time period margin</li>
  <li> margin_ac marks current/next time period margin</li>
  <li> hierarchy marks dimensional heirarchy -> HIGHEST LEVEL to LOWEST LEVEL : LEFT to RIGHT </li>
</ul>

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
