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

let canvas = document.querySelector("canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Create points to sample the sag function of a spherical surface of radius 12.5 cm
const radius = 12.5;
const roc = 25.8  // mm
const K = 0;  // sphere
const r = linspace(radius, 20);
let surface = conicArray(r, roc, K, radius);

// Draw the sag of the spherical surface
let ctx = canvas.getContext("2d");
for (let i = 0; i < r.length; i++) {
    ctx.fillRect(surface[i] * 10, r[i] * 10, 3, 3);
}
