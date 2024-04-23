import React from 'react';
import Link from 'next/link';

const OurOfferings = () => {
  return (
    <section className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 justify-items-center">

      <div className = "relative bg-gray-200 rounded-lg overflow-hidden shadow-md">
        <h2 className = "text-2xl font-bold text-white absolute inset-y-1/2 px-4 bottom-0 z-10">
          Our Products
        </h2>
        <Link href = "/products" className = "absolute inset-0 h-full w-full bg-black opacity-50 hover:opacity-75 transition-opacity duration-300"></Link>
        <div className = "px-4 py-8">
          <p className = "text-gray-600 mb-8">Explore our range of products for your health needs.</p>
          {/* Add your product content here */}
        </div>
      </div>

      <div className = "relative bg-gray-200 rounded-lg overflow-hidden shadow-md">
        <h2 className = "text-2xl font-bold text-white absolute inset-y-1/2 px-4 bottom-0 z-10">
          Our Services
        </h2>
        <Link href = "/services" className = "absolute inset-0 h-full w-full bg-black opacity-50 hover:opacity-75 transition-opacity duration-300"></Link>
        <div className = "px-4 py-8">
          <p className = "text-gray-600 mb-8">Discover our services designed to improve your health.</p>
          {/* Add your services content here */}
        </div>
      </div>

      <div className = "relative bg-gray-100 rounded-lg overflow-hidden shadow-md">
        <h2 className = "text-2xl font-bold text-white absolute inset-y-1/2 px-4 bottom-0 z-10">
          Industries We Serve
        </h2>
        <Link href = "/industries" className = "absolute inset-0 h-full w-full bg-black opacity-50 hover:opacity-75 transition-opacity duration-300"></Link>
        <div className = "px-4 py-8">
          <p className = "text-gray-600 mb-8">Learn about the industries we support with our solutions.</p>
          {/* Add your product content here */}
        </div>
      </div>

    </section>
  );
};

export default OurOfferings;