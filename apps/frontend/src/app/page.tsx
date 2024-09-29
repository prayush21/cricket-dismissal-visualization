import Dashboard from "./dashboard";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start w-full max-w-md">
        <h1 className="text-3xl font-bold mb-4">Cricket Dashboard</h1>
        <Dashboard />
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        Made with Avacado by<a href="https://github.com/prayush21">Prayush</a>
      </footer>
    </div>
  );
}
