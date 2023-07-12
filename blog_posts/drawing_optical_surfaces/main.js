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

/*
    * Create an array of radial and axial points on a flat surface.
    * numPoints: number of points to sample
    * radius: radius of the surface
    * offset: axial offset of the surface vertex from the origin
    * returns: [r, z] where r is an array of radial points and z is an array of axial points
*/
function flatSurface(numPoints, radius, offset) {
    let r = linspace(radius, numPoints);
    let z = r.map(function (r) {
        return offset;
    });
    return [r, z];
}

/*
    * Create an array of radial and axial points on a conic surface.
    * numPoints: number of points to sample
    * roc: radius of curvature
    * K: conic constant
    * radius: radius of the surface
    * offset: axial offset of the surface vertex from the origin
    * returns: [r, z] where r is an array of radial points and z is an array of axial points
*/
function conicSurface(numPoints, roc, K, radius, offset) {
    let r = linspace(radius, numPoints);
    let sag = conicArray(r, roc, K, radius);
    
    // Add offset to every value in sag
    let z = sag.map(function (s) {
        return s + offset;
    });

    return [r, z];
}

/*
    * Computes the center of mass of a system of surfaces by averaging the coordinates.
    * surfaces: an array of surfaces, each of which is an array of [r, z] points
    * returns: com, the 2D coordinates of the center of mass
*/
function centerOfMass(surfaces) {
    let com = [0, 0];
    let nPoints = 0;
    
    for (let surface of surfaces) {
        let r = surface[0];
        let z = surface[1];
        for (let i = 0; i < r.length; i++) {
            com[0] += r[i];
            com[1] += z[i];
            nPoints++;
        }
    }

    com[0] /= nPoints;
    com[1] /= nPoints;

    return com;
}

/*
    * Compute the bounding box of a system of surfaces.
    * surfaces: an array of surfaces, each of which is an array of [r, z] points
    * returns: [rMin, rMax, zMin, zMax]
*/
function boundingBox(surfaces) {
    let rMin = Infinity;
    let rMax = -Infinity;
    let zMin = Infinity;
    let zMax = -Infinity;

    for (let surface of surfaces) {
        let r = surface[0];
        let z = surface[1];
        for (let i = 0; i < r.length; i++) {
            rMin = Math.min(rMin, r[i]);
            rMax = Math.max(rMax, r[i]);
            zMin = Math.min(zMin, z[i]);
            zMax = Math.max(zMax, z[i]);
        }
    }

    return [rMin, rMax, zMin, zMax];
}

/*
    * Determine a scaling factor to fit a system of surfaces into a canvas.
    * surfaces: an array of surfaces, each of which is an array of [r, z] points
    * canvasWidth: the width of the canvas
    * canvasHeight: the height of the canvas
    * fillFactor: the fraction of the canvas to fill in the bigger dimension
    * returns: the scaling factor
*/
function findScaleFactor(surfaces, canvasWidth, canvasHeight, fillFactor = 0.9) {
    let [rMin, rMax, zMin, zMax] = boundingBox(surfaces);
    let rRange = rMax - rMin;
    let zRange = zMax - zMin;
    let scaleFactor = fillFactor * Math.min(canvasHeight / rRange, canvasWidth / zRange);
    return scaleFactor;
}

/*
    * Transforms a system of surfaces into the canvas coordinate system.
    * surfaces: an array of surfaces, each of which is an array of [r, z] points
    * canvasWidth: the width of the canvas
    * canvasHeight: the height of the canvas
    * scaleFactor: the factor by which to scale the surfaces
    * returns: an array of transformed surfaces
*/
function toCanvasCoordinates(surfaces, canvasWidth, canvasHeight, scaleFactor = 6) {
    let comSamples = centerOfMass(surfaces);  // (r, z) coordinates
    let comCanvas = [canvasWidth / 2, canvasHeight / 2];  // (x, y) coordinates
    let transformedSurfaces = [];

    for (let surface of surfaces) {
        let r = surface[0];
        let z = surface[1];
        let transformedSurface = [[], []];

        for (let i = 0; i < r.length; i++) {
            // Flip the r and z coordinates because the canvas y-axis points down.
            // Take the negative of the y-coordinate because it points down the screen.
            // Shift the center of mass of the samples to that of the canvas.
            transformedSurface[0].push(comCanvas[0] - scaleFactor * (z[i] - comSamples[1]));
            transformedSurface[1].push(comCanvas[1] + scaleFactor * (r[i] - comSamples[0]));
        }

        transformedSurfaces.push(transformedSurface);
    }

    return transformedSurfaces;
}


let canvas = document.querySelector("canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Create f = 50.1 mm a planoconvex lens comprised of two surfaces, the first one being spherical.
// This corrseponds to Thorlabs part no. LA1255.
const radius0 = 12.5; // mm
const roc0 = 25.8; // mm
const K0 = 0;  // spherical
const thickness0 = 5.3;  // mm
const radius1 = 12.5; // mm
const backFocalLength= 46.6; // mm
const numPoints = 20;
let surface0 = conicSurface(numPoints, roc0, K0, radius0, 0);
let surface1 = flatSurface(numPoints, radius1, thickness0);
let surfaces = [surface0, surface1];

// Transform the surfaces into the canvas coordinate system
scaleFactor = findScaleFactor(surfaces, canvas.width, canvas.height, fillFactor = 0.5);
surfaces = toCanvasCoordinates(surfaces, canvas.width, canvas.height, scaleFactor);

// Draw the surfaces on the canvas
let ctx = canvas.getContext("2d");
ctx.beginPath();
for (let surface of surfaces) {
    let x = surface[0];
    let y = surface[1];
    ctx.moveTo(x[0], y[0]);
    for (let i = 1; i < x.length; i++) {
        ctx.lineTo(x[i], y[i]);
    }
}
ctx.stroke();

// Put a point in the center of the canvas
ctx.beginPath();
ctx.arc(canvas.width / 2, canvas.height / 2, 5, 0, 2 * Math.PI);
ctx.fill();
