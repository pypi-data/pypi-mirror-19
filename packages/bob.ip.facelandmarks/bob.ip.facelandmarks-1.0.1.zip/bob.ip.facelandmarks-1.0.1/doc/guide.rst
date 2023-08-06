.. py:currentmodule:: bob.ip.facelandmarks

.. testsetup:: *

   from __future__ import print_function
   import math
   import bob.io.base
   import bob.io.base.test_utils
   import bob.io.image
   import bob.io.video
   import bob.ip.color
   import bob.ip.facedetect
   import bob.ip.facelandmarks
   import bob.ip.facelandmarks.utils

   import pkg_resources
   #lena_file = '/idiap/user/sbhatta/work/git/bob.ip.facelandmarks/data/lena.jpg'
   #multi_file = '/idiap/user/sbhatta/work/git/bob.ip.facelandmarks/data/multiple-faces.jpg'
   lena_file = bob.io.base.test_utils.datafile('lena.jpg', 'bob.ip.facelandmarks')
   multi_file = bob.io.base.test_utils.datafile('multiple-faces.jpg', 'bob.ip.facelandmarks', 'data')
   face_image = bob.io.base.load(lena_file)
   multi_image = bob.io.base.load(multi_file)

=============
 User Guide
=============

This Bob package allows you to use the [Menpofit_] package to detect facial landmarks.
Given a gray-level image depicting a human face, this package can be used to extract a specific set of 68 landmarks,
as defined in Menpofit. Please refer to the original Menpofit [documentation_] for implementation details. 
Here, we show some examples of how to use the ``bob.ip.facelandmarks`` package. 


Landmark Detection on a Single Face
-----------------------------------

The most simple face detection task is to detect a single face in an image.
This task can be accomplished using the ``detect_landmarks()`` function in this package.
The following code-example shows how to extract facial keypoints for a single face in a gray-level input image:

.. doctest::

   >>> face_image = bob.io.base.load('lena.jpg') # doctest: +SKIP
   >>> gray_image = bob.ip.color.rgb_to_gray(face_image)
   >>> key_points = bob.ip.facelandmarks.utils.detect_landmarks(gray_image, 1)
   >>> print(key_points[0].landmarks.shape)
   (68, 2)

   >>> print(key_points[0].bounding_box.topleft)
   (226, 237)

   >>> print(key_points[0].bounding_box.bottomright)
   (394, 376)

This package also provides a handy function, ``draw_landmarks()``, for plotting the extracted facial-landmarks on an image.

.. doctest::

   >>> bob.ip.facelandmarks.utils.draw_landmarks(gray_image, key_points)

The result is shown in the image below.

.. plot:: plot/single_face_lmks.py
   :include-source: False



The ``detect_landmarks()`` function has the following signature: `detect_landmarks(gray_image, top=0, min_quality=0.0)`.

 * ``gray_image``: a numpy-array containing the gray-level input image, and,
 * ``top``: positive integer (default=0), specifying the number of faces to be detected in this image.
 * ``min_quality``: positive floating-point number (default=0), specifying the minimum acceptable quality for the result of face-detection. 

The first parameter is obligatory, and should be a valid 2D numpy-array representing a gray-level image.
The remaining two parameters are optional.
In the example above, ``top`` is specified as 1, hence, landmarks for only one face are extracted.

The function ``detect_landmarks()`` first detects faces in the input image, using ``bob.ip.facedetect``, and then uses the result of the face-detection-step for detecting facial-landmarks. 


If the ``min_quality`` parameter is specified, then bounding-boxes having a quality-value lower than the specified value are ignored.

The return value of ``detect_landmarks()`` is a list. 
When only one face is expected in the input, this list will contain only one element.
Each element in the list is an object with three members, named as follows:

 * ``bounding_box``: an object with two elements (topright, and bottomleft), each of which is a tuple (row,col) giving the coordinates of the top-left and bottom-right corners of the detected face-bounding-box.
 * ``quality``: a floating-point number between 0 and 100.0, giving a quality-estimate for the result of the face-detection step. 
 * ``landmarks``: a numpy-array of shape (68, 2).

The first two members, ``bounding_box`` and ``quality``, come from ``bob.ip.facedetect``.
The detected bounding-boxes are sorted in order of decreasing quality, and the top-N (where N is the value specified for the parameter ``top``) bounding-boxes are used, one by one, in the landmark-detection step.

For each detected face, each row in ``landmarks`` represents one of the 68 facial-landmarks, and gives the coordinates (row,col) of that landmark.
As described in the Menpofit documentation, The facial-landmarks are listed in a specific order in the array:

.. code-block:: python

   jaw_indices = [0, 17]
   lbrow_indices = [17, 22]
   rbrow_indices = [22, 27]
   upper_nose_indices = [27, 31]
   lower_nose_indices = [31, 36]
   leye_indices = [36, 42]
   reye_indices = [42, 48]
   outer_mouth_indices = [48, 60]
   inner_mouth_indices = [60, 67]


If the bounding-box of the desired face is already available (via a preceding call to the function ``face.ip.facedetect.detect_single_face()``), the function ``detect_landmarks_on_boundingbox(gray_image, bounding_box)`` may be used to determine the facial-landmarks within this bounding-box.
Note that the return-value of ``detect_landmarks_on_boundingbox()`` is a 2D numpy-array representing the coordinates of the 68 landmarks (and not an object as in the case of ``detect_landmarks()``). 

.. doctest::
   
   >>> gray_image = bob.ip.color.rgb_to_gray(face_image)
   >>> my_bounding_box, _ = bob.ip.facedetect.detect_single_face(gray_image)
   >>> my_key_points = bob.ip.facelandmarks.utils.detect_landmarks_on_boundingbox(gray_image, my_bounding_box)
   >>> print(my_key_points.shape)
   (68, 2)



Landmark Detection on Multiple Faces
------------------------------------

To extract landmarks for multiple faces in the same image, use the ``top`` parameter when calling ``detect_landmarks()``.
In the following example, the input image contains several faces, out of which, landmarks are extracted for the 5 faces with the best face-detection-quality.

.. doctest::

   >>> multi_image = bob.io.base.load('multiple-faces.jpg') # doctest: +SKIP
   >>> gray_image = bob.ip.color.rgb_to_gray(multi_image)
   >>> key_points = bob.ip.facelandmarks.utils.detect_landmarks(gray_image, top=5)        
   >>> for i in range(5):
   ...   print(key_points[i].bounding_box.topleft) 
   (136, 2243)
   (1480, 2226)
   (1574, 2959)
   (853, 913)
   (107, 3016)


.. _Menpofit: http://www.menpo.org/menpofit/ 

.. _documentation: https://menpofit.readthedocs.io/en/stable/
