import { Nav } from "@/components/ui/Nav";
import { Preloader } from "@/components/ui/Preloader";
import { Hero } from "@/components/sections/Hero";
import { Collection } from "@/components/sections/Collection";
import { Manufacture } from "@/components/sections/Manufacture";
import { Editorial } from "@/components/sections/Editorial";
import { Movement } from "@/components/sections/Movement";
import { Lookbook } from "@/components/sections/Lookbook";
import { Journal } from "@/components/sections/Journal";
import { Footer } from "@/components/sections/Footer";

export default function Home() {
  return (
    <>
      <Preloader />
      <Nav />
      <main>
        <Hero />
        <Collection />
        <Manufacture />
        <Editorial />
        <Movement />
        <Lookbook />
        <Journal />
      </main>
      <Footer />
    </>
  );
}
