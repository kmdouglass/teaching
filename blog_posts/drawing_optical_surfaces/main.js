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


let canvas = document.querySelector("canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Create f = 50.1 mm a planoconvex lens comprised of two surfaces, the second one being spherical.
const radius0 = 12.5; // mm
const thickness0 = 5.3;  // mm
const radius1 = 12.5;  // mm
const roc1 = 25.8; // mm
const K1 = 0;  // spherical
const numPoints = 20;
let surface0 = flatSurface(numPoints, radius0, 0);
let surface1 = conicSurface(numPoints, roc1, K1, radius1, thickness0);

console.log(surface0);
console.log(surface1);

// Draw the sag of the spherical surface
let ctx = canvas.getContext("2d");
