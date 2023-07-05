# Drawing 2D Optical Surfaces in the Browser

On my most recent vacation, I came up with an idea to try performing optical ray tracing in the browser. I have a few reasons for doing so:

- I sometimes need to predict the degree of aberrations in microscopes of varying degrees of complexity.
- Industrial optical design tools like Zemax, CODE V, etc. are way too expensive for what I need to do.
- I wanted to bring scientific software directly to people who need it and to have that software run on their own hardware.

Rust and Webassembly offer an interesting choice for a toolchain for the main parts of the code, and so far writing my ray tracer in Rust has been relatively straightforward. But this blog post is not about writing a ray tracer. You see, beyond a few GeoCities websites I made as a teenager in the late 90's, I have no idea how to actually draw stuff in a web browser.

So here I'm looking into how to actually make 2D drawings of optical systems in the browser. Specifically, I'll use the HTML5 Canvas and Javascript because a few days of searching indicate that these are probably the best way to put custom, dynamic graphics into a webpage.

## Setup the canvas

This part is pretty straightforward. I created two files: `index.html` and `canvas.js`. The body of the HTML page is just two lines:

```html
<canvas id="canvas"></canvas>
<script src="canvas.js"></script>
```

I created the canvas with the the ID `canvas`, then I invoke a Javascript file named `canvas.js`.

I made the canvas fill the entire browser window in Javascript by setting the canvas width and `height` properties to the document's `innerWidth`/`innerHeight` respectively.

```js
let canvas = document.querySelector("canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
```

Just to verify that the canvas size has been set correctly, I gave it a black border of 1px width and removed the last two lines of Javascript to observe a canvas of default size.

Except for MIDIs of anime theme songs playing in the background, my page is already better than what my teenage self could do.

## Modeling optical surfaces

OK, now we're at one of the good parts. Before we jump into the code, we should probably ask ourselves that age-old question: how do we model optical surfaces?

There's a classic paper by [Spencer and Murty](https://doi.org/10.1364/JOSA.52.000672) that explains how to intersect ways with surfaces of the form

$$ F \left(x, y, z\right) = 0 $$

Many surfaces that we are interested in in optics have profiles that  are conic sections.



## References

- Spencer and Murty, "General Ray-Tracing Procedure", JOSA 6, 672 (1962): https://doi.org/10.1364/JOSA.52.000672
- https://www.youtube.com/playlist?list=PLpPnRKq7eNW3We9VdCfx9fprhqXHwTPXL