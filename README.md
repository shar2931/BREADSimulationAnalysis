# InfraBREAD Blackbody Calibration Studies
## by Shardul Rao, Summer 2024 SULI Intern

## Using FRED
This video was very helpful in getting started with FRED as a complete newcomer: https://www.youtube.com/watch?v=MK6PzxAqCx8&ab_channel=DIY-Optics.

Much of my work this summer was done in the file `blackbody-studies.frd`. The key objects used to conduct the calibration simulations are divided into three categories: Optical Source(s), Geometry, and Analysis Surface(s).

### Optical Sources
As the name implies, this category contains the light source objects. In general, objects in FRED can be added or removed from the simulation by right-clicking on the object's name in the left hand side menu and selecting `Traceable`.

![](READMEImages/image.png)

#### Creating Blackbody Source
In order to create a new optical source, right-click on the `Optical Source(s)` header and hover over `Create New Source Primitive` or `Create New Detailed Optical Source`. When doing these blackbody simulations, I used a Detailed Optical Source.

![](READMEImages/image-1.png)

WIthin the Detailed Optical Source menu, to mimic the blackbody absorber, navigate to the `Positions/Directions` tab. Select `Random Plane` from the `Ray Position` dropdown menu and `Random Directions into an Angular Range` from the `Ray Direction` dropdown menu. In order to make the rays propagate down into the relector setup, scroll down to the bottom of the parameters under `Random Directions into an Angular Range` and change `(X, Y, Z) components of forward direction` to `(0, 0, -1)`. The Positions/Directions tab also lets you change the size of the optical source and the number of rays.

![](READMEImages/image-3.png)