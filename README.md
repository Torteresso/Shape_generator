PRESENTATION
============

This is an old program when I was doing some Python, the idea is :

Start from a POLYGON --> For each segment, draw a perpendicular bisector of random lenght pointing outside the shape
--> Draw lines perpendicular to these new bisectors --> Their intersections form a new POLYGON --> Repeat

The system will eventually evolve to a final (stable?) POLYGON.

This explanation with word is hard to visualize but the program show great visualisation of the process with adjustable speed.

Current state : 

- Ability to evolve any polygon with customizable bisectors lenghts and graphical visualisation of the evolution process.

HOW TO CONFIG AN EVOLUTION : 
==========================

Change this line is the main.py : 
fig = gd.Figure(parameters...)

The parameters are in order : 

- name of the initial shape : "n-polygon" with n an integer >= 3 -for example "8-polygon"-, or "random" for random polygon
- lenght : lenght of each segment of the polygon (integer)
- a turtle object to draw : the variable is named "t" in the main.py
- OPTIONAL : number of previous evolution shown : integer >= 1 (default = 4)
- OPTIONAL : list with lenghts of each bisectors : must be of the same size of n (default : None -> random bisectors lenghts)
- OPTINAL : boolean for fictive figure : set it to true if you want only the calculation part, no graphics visualisation (default : False)

HOW TO USE IT
=============

If you want to test it, you should install these python librairies :  

* [Turtle](https://docs.python.org/3/library/turtle.html)
  
And then you can clone it in Visual Studio Community 2022. That's it ! :)
