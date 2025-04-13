import React, { useEffect, useState } from "react";
import Navbar from "./Navbar";
import Card from "./ProductCard";
import axios from 'axios';
import { data } from './data';

const Personalized = () => {
  // State for selected user ID and model type
  const [userId, setUserId] = useState("");
  const [modelType, setModelType] = useState("");
  const [recommendation, setRecommendation] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/');
        console.log("Fetched Users:", response.data); // Log to verify the data
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching data:", error); // Handle error
      }
    }
    fetchData();
  }, []);

  // Extract userIds from fetched users
  const userIds = users;
  const modelTypes = ["collaborative", "content_based", "hybrid"];

  const handleRecommendation = async () => {
    if (userId && modelType) {
      const response = await axios.get("http://localhost:5000/recommend", {
        params: {
          user_id: userId,
          model: modelType,
        }
      });

      console.log("Recommendation Response:", response.data); // Log to verify the response
      setRecommendation(response.data);
    }
  };

  return (
    <div className="min-h-full flex flex-col justify-center items-center bg-gray-50">
      <Navbar />
      <div className="w-[50vw] bg-white p-8 rounded-lg shadow-xl mt-10">
        <h2 className="text-3xl font-semibold text-gray-800 mb-8 text-center">
          Get Personalized Recommendations
        </h2>
        <form className="space-y-6">
          {/* User ID Dropdown */}
          <div className="flex flex-col">
            <label
              htmlFor="userId"
              className="text-lg font-semibold text-gray-700 mb-2"
            >
              Select User ID:
            </label>
            <select
              id="userId"
              value={userId}
              onChange={(e) => {
                console.log("User ID Selected:", e.target.value); // Log to verify the selection
                setUserId(e.target.value);
              }}
              className="p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="" disabled>Select User ID</option>
              {userIds.length > 0 ? (
                userIds.map((id) => (
                  <option key={id} value={id}>
                    {id}
                  </option>
                ))
              ) : (
                <option value="">Loading...</option> // Show loading if no users are fetched
              )}
            </select>
          </div>

          {/* Model Type Dropdown */}
          <div className="flex flex-col">
            <label
              htmlFor="modelType"
              className="text-lg font-semibold text-gray-700 mb-2"
            >
              Select Model Type:
            </label>
            <input
              id="modelType"
              list="modelTypes"
              value={modelType}
              onChange={(e) => setModelType(e.target.value)}
              className="p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Type or select Model Type"
            />
            <datalist id="modelTypes">
              {modelTypes.map((type) => (
                <option key={type} value={type} />
              ))}
            </datalist>
          </div>

          {/* Recommendation Button */}
          <div className="text-center">
            <button
              type="button"
              onClick={handleRecommendation}
              className="w-full py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
            >
              Get Recommendations
            </button>
          </div>
        </form>
      </div>

      {/* Display Recommendations */}
      {recommendation && (
        <div className="text-center mt-4">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Personalized Recommendations
          </h2>
          <div className="mt-12 w-[90%] md:w-[80%] lg:w-[75%] mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 px-4">
            {recommendation.map((product) => (
              <Card
                key={product.product_id}
                title={product.title}
                url={product.image}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Personalized;
