'use client'

import { useRouter } from 'next/navigation'



export default function Home() {
  const router = useRouter()

  return (
    <div className="flex items-center justify-center h-screen" >
      <button className="Button" type="button" onClick={() => router.push('/generate-question')}>Let's Get Started !</button>
    </div>
  );
}
