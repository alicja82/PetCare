<template>
  <div class="home-page">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
      <div class="container-fluid px-4">
        <router-link class="navbar-brand fw-bold fs-4" to="/">
          🐾 PetCare
        </router-link>
        <div class="d-flex align-items-center">
          <span class="navbar-text text-white me-3">
            <i class="bi bi-person-circle"></i> {{ authStore.user?.username }}
          </span>
          <button class="btn btn-outline-light btn-sm" @click="handleLogout">
            Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
          <div class="welcome-card card shadow-lg border-0 mb-4">
            <div class="card-body p-5">
              <h1 class="display-4 mb-3">Welcome to PetCare! 🐾</h1>
              <p class="lead text-muted">Manage your pets with ease and keep track of their health and well-being.</p>
            </div>
          </div>

          <div class="row mb-4">
            <div class="col-md-4 mb-3">
              <router-link to="/pets" class="text-decoration-none">
                <div class="feature-card card shadow border-0 h-100">
                  <div class="card-body text-center p-4">
                    <div class="icon-circle mb-3">
                      <i class="bi bi-heart-fill fs-1"></i>
                    </div>
                    <h5 class="card-title">My Pets</h5>
                    <p class="card-text text-muted">View and manage your pets</p>
                  </div>
                </div>
              </router-link>
            </div>
            <div class="col-md-4 mb-3">
              <div class="feature-card card shadow border-0 h-100 opacity-50">
                <div class="card-body text-center p-4">
                  <div class="icon-circle mb-3">
                    <i class="bi bi-calendar-check fs-1"></i>
                  </div>
                  <h5 class="card-title">Feeding Schedule</h5>
                  <p class="card-text text-muted">Coming soon...</p>
                </div>
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="feature-card card shadow border-0 h-100 opacity-50">
                <div class="card-body text-center p-4">
                  <div class="icon-circle mb-3">
                    <i class="bi bi-hospital fs-1"></i>
                  </div>
                  <h5 class="card-title">Vet Visits</h5>
                  <p class="card-text text-muted">Coming soon...</p>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow border-0">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Your Account Information</h5>
            </div>
            <div class="card-body p-4">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="info-item">
                    <strong class="text-muted">Username:</strong>
                    <p class="mb-0 fs-5">{{ authStore.user?.username }}</p>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="info-item">
                    <strong class="text-muted">Email:</strong>
                    <p class="mb-0 fs-5">{{ authStore.user?.email }}</p>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="info-item">
                    <strong class="text-muted">User ID:</strong>
                    <p class="mb-0 fs-5">{{ authStore.user?.id }}</p>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="info-item">
                    <strong class="text-muted">Member Since:</strong>
                    <p class="mb-0 fs-5">{{ formatDate(authStore.user?.created_at) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchUser()
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.info-item {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.card {
  border-radius: 15px;
}

.feature-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.15) !important;
}

.icon-circle {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
}
</style>
