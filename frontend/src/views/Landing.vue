<template>
  <div class="min-h-screen bg-white selection:bg-blue-100 selection:text-blue-900 font-sans">

    <!-- Pattern Background -->
    <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-1/2 -right-1/4 w-[1000px] h-[1000px] rounded-full bg-gradient-to-br from-blue-50 to-indigo-50 blur-3xl opacity-50"></div>
      <div class="absolute -bottom-1/2 -left-1/4 w-[800px] h-[800px] rounded-full bg-gradient-to-tr from-purple-50 to-pink-50 blur-3xl opacity-50"></div>
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNlN2U1ZTQiLz48L3N2Zz4=')] opacity-[0.3]"></div>
    </div>

    <!-- Main Content -->
    <main class="relative z-10 pt-32 pb-16">

      <!-- Hero Section -->
      <section class="max-w-7xl mx-auto px-6 pt-16 pb-24 text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 border border-blue-100 text-blue-600 text-sm font-medium mb-8 animate-fade-in-up">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
          </span>
          Next-Gen AI Data Analysis
        </div>

        <h1 class="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight mb-8 leading-tight max-w-4xl mx-auto">
          Turn Raw Data Into <br class="hidden md:block"/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
            Intelligent Insights
          </span>
        </h1>

        <p class="text-lg md:text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
          Upload any dataset. Instantly generate interactive visualizations,
          comprehensive EDA reports, and receive precise AI-driven model architecture recommendations.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button @click="$router.push('/register')" class="w-full sm:w-auto px-8 py-4 bg-gray-900 hover:bg-gray-800 text-white rounded-xl font-semibold text-lg shadow-xl shadow-gray-900/20 transition-all hover:-translate-y-0.5 flex items-center justify-center gap-2">
            Start Building Free
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </button>
          <a href="#features" class="w-full sm:w-auto px-8 py-4 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 rounded-xl font-semibold text-lg shadow-sm transition-all text-center">
            Explore Features
          </a>
        </div>
      </section>

      <!-- Dashboard Preview / Illustration -->
      <section class="max-w-6xl mx-auto px-6 mb-32">
        <div class="rounded-2xl border border-gray-200/60 bg-white/50 backdrop-blur-sm p-2 shadow-2xl relative">
          <div class="absolute -top-4 -right-4 w-24 h-24 bg-blue-500 rounded-full mix-blend-multiply filter blur-2xl opacity-70 animate-blob"></div>
          <div class="absolute -bottom-8 -left-4 w-32 h-32 bg-purple-500 rounded-full mix-blend-multiply filter blur-2xl opacity-70 animate-blob animation-delay-2000"></div>

          <!-- Mockup Window -->
          <div class="rounded-xl overflow-hidden border border-gray-100 bg-gray-50 relative z-10 shadow-inner">
            <div class="h-12 bg-gray-100 border-b border-gray-200 flex items-center px-4 gap-2">
              <div class="w-3 h-3 rounded-full bg-red-400"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
              <div class="w-3 h-3 rounded-full bg-green-400"></div>
            </div>
            <!-- Mock Content -->
            <div class="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 h-[400px]">
              <div class="col-span-1 space-y-4">
                <div class="h-24 bg-white rounded-lg shadow-sm border border-gray-100 animate-pulse"></div>
                <div class="h-48 bg-white rounded-lg shadow-sm border border-gray-100 animate-pulse delay-75"></div>
              </div>
              <div class="col-span-2 space-y-4">
                <div class="h-40 bg-white rounded-lg shadow-sm border border-gray-100 animate-pulse delay-150"></div>
                <div class="grid grid-cols-2 gap-4">
                  <div class="h-32 bg-white rounded-lg shadow-sm border border-gray-100 animate-pulse delay-200"></div>
                  <div class="h-32 bg-white rounded-lg shadow-sm border border-gray-100 animate-pulse delay-300"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section id="features" class="max-w-7xl mx-auto px-6 py-24">
        <div class="text-center mb-20">
          <h2 class="text-3xl md:text-5xl font-bold text-gray-900 mb-6">Designed for Data Engineers, <br class="hidden md:block"/>Built for Everyone</h2>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">Stop writing boilerplate plotting code. AutoML handles the heavy lifting so you can focus on building.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-100 shadow-xl shadow-gray-200/40 hover:shadow-2xl transition-shadow group">
            <div class="w-14 h-14 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Instant Visualizations</h3>
            <p class="text-gray-600 leading-relaxed">
              Upload your dataset and instantly receive distribution plots, correlation heatmaps, and outlier detections without writing a single line of code.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-100 shadow-xl shadow-gray-200/40 hover:shadow-2xl transition-shadow group">
            <div class="w-14 h-14 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Smart AI Engine</h3>
            <p class="text-gray-600 leading-relaxed">
              Our intelligent engine analyzes column types, distinct values, and distributions to automatically recommend optimal machine learning architectures.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-100 shadow-xl shadow-gray-200/40 hover:shadow-2xl transition-shadow group">
            <div class="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">Secure & Native</h3>
            <p class="text-gray-600 leading-relaxed">
              Fully isolated JWT environments. Designed with a robust Flask backend and modern Vue 3 architecture. 100% data detachment on deletion.
            </p>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="max-w-5xl mx-auto px-6 py-24">
        <div class="bg-gray-900 rounded-3xl p-12 text-center text-white relative overflow-hidden shadow-2xl">
          <div class="absolute top-0 right-0 w-64 h-64 bg-blue-600/20 rounded-full blur-3xl"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-purple-600/20 rounded-full blur-3xl"></div>

          <div class="relative z-10">
            <h2 class="text-3xl md:text-5xl font-bold mb-6">Ready to decode your data?</h2>
            <p class="text-gray-300 text-lg mb-10 max-w-2xl mx-auto">Join developers pushing the boundaries of automated intelligence.</p>
            <button @click="$router.push('/register')" class="px-8 py-4 bg-white text-gray-900 rounded-xl font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg">
              Create an account
            </button>
          </div>
        </div>
      </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 py-12 relative z-10">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center text-white font-bold">A</div>
          <span class="font-bold text-gray-900">AutoML Insight</span>
        </div>

        <p class="text-gray-500 text-sm">© {{ new Date().getFullYear() }} AutoML. All rights reserved.</p>

        <div class="flex items-center gap-4">
          <a href="#" class="text-gray-400 hover:text-gray-900 transition-colors">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>
          </a>
          <a href="https://github.com" target="_blank" class="text-gray-400 hover:text-gray-900 transition-colors">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
@keyframes fade-in-up {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out;
}
</style>
<script setup>
// Expose Vue components logic here if necessary
</script>
