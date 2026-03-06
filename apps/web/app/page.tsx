import { redirect } from 'next/navigation';

export default function Home() {
  redirect('/dashboard');
import { Hero } from "../components/blocks/Hero";
import { Benefits } from "../components/blocks/Benefits";
import { SocialProof } from "../components/blocks/SocialProof";
import { Pricing } from "../components/blocks/Pricing";
import { FAQ } from "../components/blocks/FAQ";
import { FinalCTA } from "../components/blocks/FinalCTA";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-8 p-8">
      <Hero />
      <Benefits />
      <SocialProof />
      <Pricing />
      <FAQ />
      <FinalCTA />
    </main>
  );
}
