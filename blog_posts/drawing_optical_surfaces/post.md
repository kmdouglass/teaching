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
<script src="main.js"></script>
```

I created the canvas with the the ID `canvas`, then I invoke a Javascript file named `main.js`.

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

There's a classic paper by [Spencer and Murty](https://doi.org/10.1364/JOSA.52.000672) that explains how to intersect rays with surfaces of the form

$$ F \left(x, y, z\right) = 0 $$

Many surfaces that we are interested in in optics have profiles that are conic sections, so it's reasonable to focus our attention on drawing these. To represent a conic as a 2D surface, we have to first do a few things:

1. We assume that the vertex of the conic lies at the origin $(0, 0, 0)$ of the surface's coordinate system.
1. We assume that the principal axis of the conic is the z-axis.
1. We rewrite the above function into two different functions: one a function of $z$ and the other a function of $x$ and $y$: $F \left(x, y, z\right) = z - G \left(x, y \right)$.

The function $G\left(x, y \right)$ above is actually the surface sag, i.e. the distance between the surface and the $z=0$ plane at a given $(x, y)$ point. The expression (in cylindrical coordinates!) for the sag of a conic surface is:

$$ G \left(r \right) = \frac{r^2 / R}{1 + \sqrt{1 - \left( 1 + K \right) \left(\frac{r}{R}\right)^2}} $$

where $r$ is the radial coordinate, $R$ is the radius of curvature, and $K = -e^2$ is called the [conic constant](https://en.wikipedia.org/wiki/Conic_constant), which is the negative of the square of the eccentricity. By convention, convex surfaces have a negative radius of curvature, whereas concave surfaces are positive. Drawing conics essentially comes down to plotting the above equation.

## Sampling the surface

With an equation for the surface sag in hand, we next need a few tools to sample points from the surface. I don't really know Javascript, so I let GitHub Copilot take care of these for me:

```js
// Compute the sag of a conic surface
function conic(r, roc, K, radius) {
    if (r > radius) return NaN;

    return r * r / roc / (1 + Math.sqrt(1 - (1 + K) * r * r / roc / roc));
}

// Take an array of values r and call conic on each one
function conicArray(r, roc, K, radius) {
    return r.map(function (r) {
        return conic(r, roc, K, radius);
    });
}

// Create an array of n values from -a to a
function linspace(a, n) {
    let r = [];
    for (let i = 0; i < n; i++) {
        r.push(-a + 2 * a * i / (n - 1));
    }
    return r;
}
```

The first function, `conic` actually produces the single surface samples. `conicArray` just repeats this for an array of radial coordinates. Finally, `linspace` produces linearly spaced radial coordinates. This is more-or-less the same thing as what my Rust/Webassembly ray-tracer is passing off to the Javascript layer.

## Coordinate transformations

Remember when I said that the conic's vertex was at $\left(0, 0, 0\right)$ and that the principal axis was the z-axis? Well, that puts the vertex at the upper left corner of the screen when it gets drawn to the canvas. Ideally, we'd have the surface centered on the canvas with a nice, visually appealing margin around it.

What's more, we'll almost always have more than one surface in our optical system. Each surface will have a local coordinate system where its vertex is at the origin, and the system will have a global coordinate system that places the surfaces within it.

All this means we'll have to transform from the coordinate system of each surface into the global one of the system, then transform from that into the coordinate system of the canvas to draw everything correctly.

Let's start first by transforming from each surface coordinate system to the global one of the optical system. If we assume sequential surfaces laid out in order along the z-axis, then this is simple:

$$x = x_l$$
$$y = y_l$$
$$z = z_l + t_i$$

In other words, $t_i$ is the axial location of surface $i$. $l$ denotes the local coordinate system of the surface.

Next, let's assume that the 2D representation of the optical system in its coordinate system is in the $\left(y, z\right)$ plane with the z-axis pointing to the right of screen, the y-axis pointing up, and the x-axis pointing into the screen. The canvas coordinate system, on the other hand, has its origin at the upper left corner and its y-axis is pointing down the screen.

The transform from the optical system's coordinate system to the canvas is

$$x_c = a \left( z + \bar{z} \right)$$
$$y_c = -a \left( y + \bar{y} \right)$$

where the subscript $c$ denotes the canvas coordinate system and the overbar denotes the center of mass of all the surface samples points.

$a$ is a scaling factor that we can use to make sure that the entire system fits nicely within the canvas.


## References

- Spencer and Murty, "General Ray-Tracing Procedure", JOSA 6, 672 (1962): https://doi.org/10.1364/JOSA.52.000672
- https://www.youtube.com/playlist?list=PLpPnRKq7eNW3We9VdCfx9fprhqXHwTPXL