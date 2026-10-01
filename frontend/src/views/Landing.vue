<template>
  <div class="landing-container">


    <!-- Hero Section -->
    <header class="hero">
      <div class="hero-content">
        <h1>Automated ML Analytics Pipeline</h1>
        <p>
          Upload your datasets, generate interactive graph visualizations, and 
          receive hyperparameter model suggestions powered by advanced AI integrations.
        </p>
        <div class="hero-buttons">
          <button @click="goToRegister" class="btn-primary large">Start Building Models</button>
        </div>
      </div>
    </header>

    <!-- App Information / Features Section -->
    <section class="features">
      <h2>How It Works</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="icon">📊</div>
          <h3>Interactive Visualizations</h3>
          <p>Seamlessly render complex data relationships into interactive, easy-to-read graphs directly in your browser.</p>
        </div>
        <div class="feature-card">
          <div class="icon">🧠</div>
          <h3>Smart Model Suggestions</h3>
          <p>Leverage integrated AI to analyze your dataset and automatically recommend the most efficient model architectures and hyperparameters.</p>
        </div>
        <div class="feature-card">
          <div class="icon">⚡</div>
          <h3>Fast & Reliable</h3>
          <p>Powered by a robust backend architecture designed to handle heavy analytical workflows without freezing the user interface.</p>
        </div>
      </div>
    </section>

    <!-- Footer & Contact Section -->
    <footer class="contact-section">
      <h2>Get in Touch</h2>
      <p>Have questions about the architecture or want to collaborate?</p>
      <div class="contact-buttons">
        <a href="mailto:akashmbytes@gmail.com" class="btn-contact email">
          ✉️ Email Support
        </a>
        <a href="https://github.com" target="_blank" class="btn-contact github">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
          GitHub
        </a>
        <a href="https://linkedin.com" target="_blank" class="btn-contact linkedin">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
          LinkedIn
        </a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  // Assumes you have a '/login' route set up in your Vue Router
  router.push('/login')
}

const goToRegister = () => {
  // Assumes you have a '/register' route set up in your Vue Router
  router.push('/register')
}
</script>

<style scoped>
/* Base Variables & Resets */
.landing-container {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #333;
  line-height: 1.6;
  background-color: #f9fafb;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 5%;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.nav-actions {
  display: flex;
  gap: 1rem;
}

/* Buttons */
button, .btn-contact {
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-outline {
  padding: 0.5rem 1.25rem;
  background-color: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.btn-outline:hover {
  background-color: #eff6ff;
}

.btn-primary {
  padding: 0.5rem 1.25rem;
  background-color: #3b82f6;
  color: #ffffff;
  border: 1px solid transparent;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-primary.large {
  padding: 0.75rem 2rem;
  font-size: 1.125rem;
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 6rem 5%;
  background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
  flex-grow: 1;
}

.hero-content h1 {
  font-size: 3rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-content p {
  font-size: 1.25rem;
  color: #4b5563;
  max-width: 600px;
  margin: 0 auto 2rem auto;
}

/* Features Section */
.features {
  padding: 4rem 5%;
  background-color: #ffffff;
  text-align: center;
}

.features h2 {
  font-size: 2rem;
  margin-bottom: 3rem;
  color: #111827;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 2rem;
  border-radius: 8px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
}

.feature-card .icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #111827;
}

.feature-card p {
  color: #6b7280;
}

/* Footer / Contact */
.contact-section {
  padding: 4rem 5%;
  text-align: center;
  background-color: #111827;
  color: #ffffff;
}

.contact-section h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.contact-section p {
  color: #9ca3af;
  margin-bottom: 2rem;
}

.contact-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.btn-contact {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  background-color: #374151;
  color: #ffffff;
  border: 1px solid #4b5563;
}

.btn-contact:hover {
  background-color: #4b5563;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.5rem;
  }
  .navbar {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>