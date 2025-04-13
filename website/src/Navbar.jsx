import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-blue-500 text-white py-4 px-6 shadow-lg w-[100vw]">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Recommendation System</h1>
        <div className="space-x-4">
          <Link to="/" className='hover:text-gray-300 transition'>Home</Link>
          <Link to="/recommend" className='hover:text-gray-300 transition'>Personalized</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
