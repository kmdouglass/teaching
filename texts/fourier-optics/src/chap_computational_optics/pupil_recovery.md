# Pupil Recovery

Pupil recovery algorithms computationally reconstruct an optical system's pupil from a set of measurements.

## Pupil recovery via gradient descent

The paper entitled [Full-field Fourier ptychography (FFP): Spatially varying pupil modeling and its application for rapid field-dependent aberration metrology](https://pubs.aip.org/aip/app/article/4/5/050802/1024434/Full-field-Fourier-ptychography-FFP-Spatially) by Song, et al. presented an algorithm to recover the pupil of an optical system from a series of images taken under different illumination angles. Though the paper was concerned with field-dependent aberrations, i.e. where the system's pupil varies across the field of view (FOV), the algorithm can easily be applied to a small FOV where the pupil does not vary.
