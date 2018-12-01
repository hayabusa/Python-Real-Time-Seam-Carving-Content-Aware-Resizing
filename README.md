### About
This is an implementation of the 
[real time content aware resize](https://link.springer.com/article/10.1007/s11432-009-0041-9)
algorithm with Mask and Face Detection Functions.
Project implemented in  ```Python```, which provide resize services.

### Example
*Befoe Seam Carving*

![alt text](example/vie.jpg)

*Seam Carving with Mask*

![alt text](example/a.jpg)

*Seam Carving without Mask*

![alt text](example/a2.jpg)
### How Seam Carving Works
Seam carving (or liquid rescaling) is an algorithm for content-aware image resizing, developed by Shai Avidan, of Mitsubishi Electric Research Laboratories (MERL), and Ariel Shamir, of the Interdisciplinary Center and MERL. It functions by establishing a number of seams (paths of least importance) in an image and automatically removes seams to reduce image size or inserts seams to extend it. Seam carving also allows manually defining areas in which pixels may not be modified, and features the ability to remove whole objects from photographs.

The purpose of the algorithm is image retargeting, which is the problem of displaying images without distortion on media of various sizes (cell phones, projection screens) using document standards, like HTML, that already support dynamic changes in page layout and text but not images.

### How Mask & Face Detection Works
In the Energy Map, we will give the Masked Parts with High Energy Value.

![alt text](example/ab.jpg)

*Face Detection Generated Mask*

![alt text](example/cao.jpg)
