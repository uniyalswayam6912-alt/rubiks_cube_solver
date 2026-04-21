import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

const faceColors = {
  right: 'red',
  left: 'orange',
  up: 'white',
  down: 'yellow',
  front: 'green',
  back: 'blue',
};

// Create a single geometry with materials for all 6 faces
const boxGeo = new THREE.BoxGeometry(0.95, 0.95, 0.95);
const boxMats = [
  new THREE.MeshStandardMaterial({ color: faceColors.right }),
  new THREE.MeshStandardMaterial({ color: faceColors.left }),
  new THREE.MeshStandardMaterial({ color: faceColors.up }),
  new THREE.MeshStandardMaterial({ color: faceColors.down }),
  new THREE.MeshStandardMaterial({ color: faceColors.front }),
  new THREE.MeshStandardMaterial({ color: faceColors.back }),
];

// Dark grey for inner faces
const darkMat = new THREE.MeshStandardMaterial({ color: '#1f2937' });

const Cubie = ({ id, pos, quat }) => {
  const meshRef = useRef();
  
  // Decide which materials to show based on initial logical position
  // E.g., if x=1, the right face (index 0) gets color, else dark.
  const materials = React.useMemo(() => {
    return [
      pos.x === 1 ? boxMats[0] : darkMat,
      pos.x === -1 ? boxMats[1] : darkMat,
      pos.y === 1 ? boxMats[2] : darkMat,
      pos.y === -1 ? boxMats[3] : darkMat,
      pos.z === 1 ? boxMats[4] : darkMat,
      pos.z === -1 ? boxMats[5] : darkMat,
    ];
  }, [id]);

  useFrame(() => {
    if (meshRef.current) {
      // Smoothly interpolate to the target position and quaternion
      meshRef.current.position.lerp(pos, 0.2);
      meshRef.current.quaternion.slerp(quat, 0.2);
    }
  });

  return (
    <mesh ref={meshRef} geometry={boxGeo} material={materials} />
  );
};

export default function Cube3D({ cubeState }) {
  return (
    <div className="w-full h-[400px] bg-slate-800 rounded-xl overflow-hidden border border-slate-700 shadow-2xl">
      <Canvas camera={{ position: [4, 4, 6] }}>
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 10, 10]} intensity={1.5} />
        
        <group>
          {cubeState.map((cubie) => (
            <Cubie 
              key={cubie.id} 
              id={cubie.id} 
              pos={cubie.position} 
              quat={cubie.quaternion} 
            />
          ))}
        </group>
        
        <OrbitControls enablePan={false} enableZoom={true} />
      </Canvas>
    </div>
  );
}
