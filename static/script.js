let scene, camera, renderer, cube;

function createFaceTexture(color) {
    const size = 256;
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;

    const ctx = canvas.getContext("2d");

    ctx.fillStyle = color;
    ctx.fillRect(0, 0, size, size);

    ctx.strokeStyle = "black";
    ctx.lineWidth = 8;

    for (let i = 1; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo((size/3)*i, 0);
        ctx.lineTo((size/3)*i, size);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, (size/3)*i);
        ctx.lineTo(size, (size/3)*i);
        ctx.stroke();
    }

    return new THREE.CanvasTexture(canvas);
}

function init3DCube() {
    const container = document.getElementById("cube3d");

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    camera.position.z = 4;

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(300, 300);

    container.innerHTML = "";
    container.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(2, 2, 2);

    const materials = [
        new THREE.MeshBasicMaterial({ map: createFaceTexture("#ff0000") }), // R
        new THREE.MeshBasicMaterial({ map: createFaceTexture("#ffa500") }), // L
        new THREE.MeshBasicMaterial({ map: createFaceTexture("#ffffff") }), // U
        new THREE.MeshBasicMaterial({ map: createFaceTexture("#ffff00") }), // D
        new THREE.MeshBasicMaterial({ map: createFaceTexture("#00ff00") }), // F
        new THREE.MeshBasicMaterial({ map: createFaceTexture("#0000ff") })  // B
    ];

    cube = new THREE.Mesh(geometry, materials);
    scene.add(cube);

    animate();
}

function animate() {
    requestAnimationFrame(animate);

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);
}

async function solveCube() {
    const input = document.getElementById("scramble").value.trim();
    const status = document.getElementById("status");
    const solutionText = document.getElementById("solution");

    if (!validateInput(input)) {
        status.innerText = "❌ Invalid moves!";
        return;
    }

    status.innerText = "Solving...";

    try {
        const res = await fetch("/solve", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ scramble: input })
        });

        const data = await res.json();

        if (data.solution) {
            status.innerText = "✅ Solved!";
            solutionText.innerText = "Solution: " + data.solution.join(" ");
        } else {
            status.innerText = "❌ Not solved";
            solutionText.innerText = "";
        }

    } catch (err) {
        status.innerText = "❌ Server error";
    }
}

function generateScramble() {
    const moves = ["U","R","F","L","D","B"];
    const primes = ["","'"];

    let scramble = [];

    for (let i = 0; i < 5; i++) {
        let m = moves[Math.floor(Math.random()*moves.length)];
        let p = primes[Math.floor(Math.random()*primes.length)];
        scramble.push(m+p);
    }

    document.getElementById("scramble").value = scramble.join(" ");
}

function resetAll() {
    document.getElementById("scramble").value = "";
    document.getElementById("solution").innerText = "";
    document.getElementById("status").innerText = "Status: Waiting...";
}

function validateInput(input) {
    const valid = ["U","R","F","L","D","B","U'","R'","F'","L'","D'","B'"];
    return input.split(" ").every(m => valid.includes(m));
}

window.onload = init3DCube;