import * as THREE from 'three';

export const initialCubeState = () => {
  const cubies = [];
  let id = 0;
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        cubies.push({
          id: id++,
          position: new THREE.Vector3(x, y, z),
          quaternion: new THREE.Quaternion(),
        });
      }
    }
  }
  return cubies;
};

export const cloneCubeState = (state) => {
  return state.map(c => ({
    id: c.id,
    position: c.position.clone(),
    quaternion: c.quaternion.clone(),
  }));
};

export const applyMoveToState = (state, moveStr) => {
  const axisMap = {
    'U': { axis: 'y', val: 1 },
    'D': { axis: 'y', val: -1 },
    'R': { axis: 'x', val: 1 },
    'L': { axis: 'x', val: -1 },
    'F': { axis: 'z', val: 1 },
    'B': { axis: 'z', val: -1 },
  };

  const face = moveStr[0];
  const isPrime = moveStr.includes("'");
  const isDouble = moveStr.includes("2");

  const { axis, val } = axisMap[face];
  let angle = Math.PI / 2;
  if (isPrime) angle = -Math.PI / 2;
  if (isDouble) angle = Math.PI;
  
  if (['R', 'U', 'F'].includes(face)) {
    angle = -angle; 
  }

  const rotAxis = new THREE.Vector3(
    axis === 'x' ? 1 : 0,
    axis === 'y' ? 1 : 0,
    axis === 'z' ? 1 : 0
  );

  const q = new THREE.Quaternion().setFromAxisAngle(rotAxis, angle);
  const newState = cloneCubeState(state);

  newState.forEach((cubie) => {
    if (Math.abs(cubie.position[axis] - val) < 0.1) {
      cubie.position.applyQuaternion(q);
      cubie.position.x = Math.round(cubie.position.x);
      cubie.position.y = Math.round(cubie.position.y);
      cubie.position.z = Math.round(cubie.position.z);
      
      cubie.quaternion.premultiply(q); 
    }
  });

  return newState;
};
