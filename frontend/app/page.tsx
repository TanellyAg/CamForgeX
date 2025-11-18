"use client";

import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 via-purple-900 to-teal-700 relative overflow-hidden">
      {/* Background */}
      <Image
        src="/images/bg-hero.jpg"
        alt="background"
        fill
        className="object-cover opacity-30"
        priority
      />

      {/* HERO SECTION - properly aligned with navbar consideration */}
      <section className="relative z-10 min-h-screen flex flex-col justify-center items-center px-4 sm:px-8 text-center max-w-6xl mx-auto pt-20">
        {/* Main heading section */}
        <div className="mb-8 w-full">
          <p className="text-lg md:text-xl text-gray-200 mb-6 sm:mb-8">
            The Future of Music Creation & Distribution is Here with CamForgeX&apos;s
          </p>

          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold leading-tight mb-6">
            <span className="bg-gradient-to-r from-[#40F680] via-[#8B5CF6] to-[#01C7A0] bg-clip-text text-transparent block">
              AI MUSIC GENERATOR
            </span>
            <span className="text-gray-200 tracking-wide text-3xl sm:text-4xl md:text-5xl lg:text-6xl block mt-2 sm:mt-4">
              AND DISTRIBUTOR
            </span>
          </h1>
        </div>

        {/* Description */}
        <p className="text-gray-300 text-lg sm:text-xl md:text-2xl max-w-2xl mx-auto mb-10 sm:mb-14 px-4 leading-relaxed">
          Leveraging advanced AI to generate, refine, and distribute your music at the
          click of a button
        </p>

        {/* CTA Button */}
        <div className="flex justify-center">
          <Link
            href="/get-started"
            className="px-10 sm:px-14 py-4 sm:py-5 rounded-full 
              bg-white/10 border border-white/30 
              text-white font-semibold text-lg sm:text-xl
              hover:bg-white/20 transition-all
              flex items-center gap-3 backdrop-blur-sm
              hover:scale-105 transform duration-300"
          >
            GET STARTED
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2.5}
              stroke="currentColor"
              className="w-5 h-5 sm:w-6 sm:h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M17.25 12l-6.5 6.5m6.5-6.5l-6.5-6.5m6.5 6.5H3"
              />
            </svg>
          </Link>
        </div>
      </section>
    </main>
  );
}