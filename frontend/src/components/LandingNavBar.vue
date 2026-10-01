<template>

        <nav class="navbar">
      <div @click="router.push('/')" class="logo" style="cursor: default;">
        <span class="logo-text"> AutoML</span>
      </div>
      <div class="nav-actions">
        <button @click="goToLogin" class="btn-outline">Log In</button>
        <button @click="goToRegister" class="btn-primary">Register</button>
      </div>
    </nav>
</template>


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


<script setup>

import { useRouter } from 'vue-router';

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