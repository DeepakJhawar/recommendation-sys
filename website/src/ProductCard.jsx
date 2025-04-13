import React from 'react';

const Card = ({ title, url }) => {
  return (
    <div className="bg-white shadow-md rounded-xl overflow-hidden transform transition duration-300 hover:scale-105 hover:shadow-2xl">
      <div className="w-full h-48 bg-gray-100 flex items-center justify-center">
        <img
          src={url}
          alt={title}
          className="max-w-full max-h-full object-contain"
        />
      </div>
      <div className="p-6">
        <h2 className="text-lg font-bold text-gray-700 mb-4 text-center">{title}</h2>
      </div>
    </div>
  );
};

export default Card;
