import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className = "bg-gray-800 p-4 absolute top-0 left-0 w-full">
      <div className = "max-w-4xl mx-auto flex justify-between items-center">
        <div className = "flex space-x-4">
          <Link href = "/products" className = "text-white hover:text-gray-300">
            PRODUCT
          </Link>
          <Link href = "/services" className = "text-white hover:text-gray-300">
            SERVICES
          </Link>
          <Link href = "/industries" className = "text-white hover:text-gray-300">
            INDUSTRIES
          </Link>
          <Link href = "/resources" className = "text-white hover:text-gray-300">
            RESOURCES
          </Link>
          <Link href = "/blog" className = "text-white hover:text-gray-300">
            BLOG
          </Link>
        </div>
        <div>
          <button className = "bg-green-500 hover:bg-yellow-400 text-white font-bold py-2 px-4 rounded">
            Need Data?
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;