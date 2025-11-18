import Link from 'next/link';
import Image from 'next/image';

export default function Navbar() {
  return (
    <>
      {/* NAVBAR */}
      <nav className="w-full flex justify-between items-center px-8 py-6 absolute top-0 left-0 z-20">
        {/* Logo + Title */}
        <div className="flex items-center gap-3">
          <Image 
            src="/images/logo.jpg"
            alt="CamForgeX Logo" 
            width={100} 
            height={100}
            className="w-10 h-10 object-contain" // Fixed size with proper image fitting
          />
          <h1 className="text-2xl font-bold leading-none">CamForgeX</h1>
        </div>

        {/* Nav Buttons */}
        <div className="flex items-center gap-4">
          <Link
            href="/login"
            className="px-6 py-2.5 bg-white/10 rounded-full border border-white/20 hover:bg-white/20 transition backdrop-blur-sm"
          >
            Login
          </Link>

          <Link
            href="/register"
            className="px-6 py-2.5 bg-white text-black rounded-full font-semibold hover:bg-gray-200 transition"
          >
            Register
          </Link>
        </div>
      </nav>
    </>
  );
}