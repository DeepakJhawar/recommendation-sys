import React, { useEffect, useState } from 'react';
import Card from './ProductCard';
import axios from 'axios';

const Home = () => {
  const [data, setData] = useState(null);
  useEffect(() => {
    const data = async () => {
      try {
        const response = await axios.get('http://localhost:5000/cold-start');
        const data = await response.data;
        setData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }  
    data();
  }, []);
  return (
    <div className="bg-gray-100 min-h-screen py-10">
      <h1 className="text-center text-3xl font-bold text-blue-600 mb-8">
        Top Products
      </h1>
      <div className="container mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 px-4">
        {data && data.map((product) => (
          <Card key={product.product_id} title={product.title} url={product.image} />
        ))}
      </div>
    </div>
  );
};

export default Home;
