# Anne - Face recognition using computer vision in IoT enviroment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- [![Codacy Badge](https://api.codacy.com/project/badge/Grade/d113af0da84b4ab9b17b8ffc29c58ecf?branch=admin-javafx)(https://app.codacy.com/project/leonardomarcao/PFA/dashboard) -->

<!-- ![](https://media.giphy.com/media/9V1vE2tcp0T0BoHaGx/giphy.gif) -->
<p align="center">
  <img src="https://media.giphy.com/media/9V1vE2tcp0T0BoHaGx/giphy.gif" alt="">  
</p>

#### Raspberry Pi 3 and Night Vision Camera
<p align="center">
  <img src="https://i.imgur.com/plUrJV1.png" alt="">  
</p>

#### Face Recognition (Prediction on image)
<p align="center">
  <img src="https://i.imgur.com/WRLBOva.png" alt="">  
</p>

#### Mqtt (MQTTv311) (Publisher and Subscriber)
<p align="center">
  <img src="https://i.imgur.com/sk6Qi4n.png" alt="">  
</p>

## About

Residential security system which uses a night vision camera connected to a raspberry pi 3 to monitor access to an electronic lock. The project was carried out using the mqtt protocol, and the purpose of this project is to show the possibility of creating an application at low cost, even if it is not a recommended protocol for it. Facial recognition is performed through an API which uses a knowledge base previously trained with the histograms and, afterwards, does a search using KNN algorithm.

## Installation 

### Requirements
* Python 3.3+ or Python 2.7
* macOS or Linux (Windows not officially supported, but might work)
* Face Recognition API (https://github.com/ageitgey/face_recognition#installation-options)
* Paho-Mqtt (https://pypi.org/project/paho-mqtt/#installation/)
* PiCamera (https://picamera.readthedocs.io/en/release-1.13/install.html)
* MQTT Dash (IoT, Smart Home) – Apps Google Play

### Setting Up Anne Project

## License 

MIT License

Copyright (c) 2019 Leonardo Marcão and Breno Osvaldo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

